#!/usr/bin/env python3
"""Classify the Zotero BBT JSON export by CONTENT first.

The Zotero collection tree is treated as a prior, not a verdict: the owner's
manual sorting may be wrong, and the goal is to file each reference by what it
is actually about. So every item is scored against a weighted keyword rule set
built from title, abstract, publication and tags; a strong content signal
overrides the collection, a weak one defers to it.

Weights: 3 = decisive term, 2 = strong, 1 = weak. Title matches count double.

Writes processed/Zotero_library_map.csv.
"""
import csv
import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "raw" / "Zotero_library.json"
OUT = ROOT / "processed" / "Zotero_library_map.csv"

STRONG = 6      # content score at or above this overrides the collection
WEAK = 3        # below this, content only decides when no collection rule fits

# --- page -> [(pattern, weight)] ---------------------------------------------
PAGE_RULES = {
    # ---- plant photobiology -------------------------------------------------
    "Photoinhibition_and_Light_Stress": [
        (r"photoinhibit", 3), (r"photoprotect", 3), (r"light shock", 3),
        (r"xanthophyll", 3), (r"non.photochemical quench|\bnpq\b", 3),
        (r"photodamage|photo.?oxidative", 3), (r"excess light|high.light stress", 3),
        (r"sun and shade (leaves|plants)", 2), (r"uv screening", 2),
        (r"photobleach", 2), (r"light stress", 2),
    ],
    "Photosynthesis_and_Gas_Exchange": [
        (r"gas exchange", 3), (r"light response curve", 3), (r"co2 assimilation", 3),
        (r"stomatal conduct", 3), (r"a/ci|a-ci curve", 3), (r"net photosynthes", 3),
        (r"photosynthetic (capacity|rate)", 3), (r"quantum yield", 2),
        (r"transpirat", 2), (r"photorespir", 2), (r"photosynthe", 1),
    ],
    "Chlorophyll_Fluorescence": [
        (r"chlorophyll fluorescen", 3), (r"fv/fm|fv.fm ratio", 3),
        (r"psii efficiency|photosystem ii efficiency", 3),
        (r"fluorescence", 2), (r"vitality test", 2),
    ],
    "Plant_Carbon_and_Water_Relations": [
        (r"carbohydrat", 3), (r"dry matter (partition|allocation)", 3),
        (r"water relations", 3), (r"water potential", 3), (r"osmotic adjust", 3),
        (r"starch|soluble sugar", 2), (r"drought stress", 2),
        (r"nutrient uptake|fertilisation|fertilization", 2), (r"biomass allocation", 2),
    ],
    "Light_Quality_and_Photomorphogenesis": [
        (r"light quality", 3), (r"spectral quality", 3), (r"far.red", 3),
        (r"red:far|r:fr", 3), (r"blue light", 3), (r"phytochrome", 3),
        (r"cryptochrome", 3), (r"photomorphogen", 3), (r"shade avoidance", 3),
        (r"\buv-?b\b|\buv-?a\b", 2), (r"stem elongation|hypocotyl", 2),
        (r"light spectr|spectral composition", 2), (r"morpholog", 1),
    ],
    "Photoperiod_and_Dormancy_Induction": [
        (r"photoperiod", 3), (r"short.day treatment|\bsdt\b", 3),
        (r"long night|night interruption", 3), (r"growth cessation", 3),
        (r"bud set|terminal bud format", 3), (r"dormanc", 3),
        (r"daylength|day length", 2), (r"apical growth cessation", 3),
    ],
    "Frost_Hardiness_and_Freezing_Tests": [
        (r"frost hardi|cold hardi", 3), (r"freezing (tolerance|test|stress)", 3),
        (r"acclimat|dehardening|deacclimat", 3), (r"electrolyte leakage", 3),
        (r"\blt50\b", 3), (r"cold storage|freezer storage", 2),
        (r"overwinter", 2), (r"bud burst|budburst|flushing", 2), (r"frost damage", 2),
    ],
    "Horticultural_Lighting": [
        (r"\bleds?\b|light.emitting diode", 3), (r"luminaire|\bfixture", 3),
        (r"\blamps?\b|high pressure sodium|\bhps\b|metal halide|fluorescent", 3),
        (r"photon efficacy|luminous efficacy", 3), (r"grow light", 3),
        (r"horticultural lighting|lighting in horticulture", 3),
        (r"solid.state lighting|\bssl\b", 2), (r"light source", 2),
        (r"valoya|philips greenpower|leoled", 3),
    ],
    "Lighting_Strategy_and_Control": [
        (r"daily light integral|\bdli\b", 3), (r"supplement(al|ary) light", 3),
        (r"lighting (control|strategy|schedul)", 3), (r"dynamic control", 3),
        (r"photoperiod extension", 3), (r"lighting (cost|energy)", 3),
        (r"light integral", 2), (r"assimilation light", 2),
    ],
    "Plant_Phenotyping_and_Image_Analysis": [
        (r"phenotyp", 3), (r"image analysis|image.based analysis", 3),
        (r"machine vision|computer vision", 3), (r"plantcv|fieldimager", 3),
        (r"rgb imag|multispectral imag|hyperspectral imag", 2),
        (r"colou?r analysis", 2), (r"non.destructive.{0,20}(measure|monitor|analys)", 2),
    ],
    "Radiometry_and_Photometry": [
        (r"international system of units|\bsi\b units", 3),
        (r"photochemical equivalence", 3), (r"iupac", 3),
        (r"commission internationale de l.eclairage|\bcie\b", 3),
        (r"radiometr|photometr|actinometr", 3),
        (r"energieverteilung im normalspectrum|verwandlung des lichtes", 3),
        (r"quantification of uv radiation", 3), (r"lux|candela|luminous flux", 2),
    ],
    "Phenology_and_Thermal_Time": [
        (r"growing degree day|degree.days", 3), (r"thermal time", 3),
        (r"heat accumulation", 3), (r"phenolog", 2),
    ],
    # ---- controlled environment agriculture --------------------------------
    "Greenhouse_Horticulture": [
        (r"glasshouse|v[aä]xthus", 3), (r"greenhouse (climate|energy|cover|heating)", 3),
        (r"thermal screen|energy screen", 3), (r"waste heat|restv[aä]rme", 3),
        (r"growth chamber", 2), (r"greenhouse", 2), (r"winter production", 2),
    ],
    "Vertical_Farming_and_Urban_Agriculture": [
        (r"vertical farm", 3), (r"plant factor(y|ies)", 3), (r"hydroponic", 3),
        (r"urban agricultur|urban farm", 3), (r"food mile", 3),
        (r"indoor (farm|cultivation|growing)", 3), (r"aquaponic", 3),
    ],
    # ---- forestry -----------------------------------------------------------
    "Forest_Seedling_Production": [
        (r"container[ie][sz]ed seedling", 3), (r"nursery|plantskol|plante?skole", 3),
        (r"stock type", 3), (r"root growth capacity|\brgc\b", 3),
        (r"seedling quality", 3), (r"mini.?plug", 3), (r"storability|seedling storage", 3),
        (r"transplant seedling|pre.cultivation", 2), (r"lifting|packing", 1),
        (r"quickpot|bew[aä]sserungscontainer|\bhiko\b", 3), (r"seedling", 1),
        (r"root growth potential|\brgp\b|root volume|root fibrosity", 3),
        (r"stock quality|target seedling|outplant", 3), (r"field performance", 2),
    ],
    "Forest_Regeneration": [
        (r"site preparation|scarification", 3), (r"shelterwood", 3),
        (r"natural regeneration", 3), (r"outplanting|planting surviv", 3),
        (r"f[oö]ryngring", 3), (r"mechani[sz]ed .{0,12}planting", 3),
        (r"reforestation|afforestation|forest restoration", 3),
        (r"silvicultur", 2), (r"establishment|early growth", 1), (r"regeneration", 2),
    ],
    "Forest_Damage_and_Herbivory": [
        (r"pine weevil|hylobius", 3), (r"browsing|moose|roe deer|\bvole\b|cervid", 3),
        (r"herbivor", 3), (r"insect damage|pest damage", 2),
    ],
    "Tree_Breeding_and_Propagation": [
        (r"somatic embryo", 3), (r"clonal forestry|clone", 3), (r"genetic gain", 3),
        (r"breeding programme|breeding program", 3), (r"provenance|seed orchard", 3),
        (r"genetically improved", 3), (r"gene express", 2), (r"cutting propagation", 3),
    ],
    "Swedish_Forestry": [
        (r"skogsbruk|skogsstyrelsen|skogskunskap", 3),
        (r"swedish forest|forestry in (sweden|finland|norway)", 3),
        (r"forest management in", 3), (r"state of europe.s forests", 3),
        (r"forest polic|forest ecosystem service", 2), (r"principles of silviculture", 3),
    ],
    "Forestry_and_Agriculture_Statistics": [
        (r"plantstatistik|planteskole statistikk", 3),
        (r"(production|nursery|forest) statistic", 3),
        (r"fr[oö].{0,4} och plantstatistik", 3), (r"forest nurseries in", 3),
    ],
    # ---- photovoltaics ------------------------------------------------------
    "PV_System_Performance": [
        (r"performance ratio", 3), (r"yield assessment|energy yield", 3),
        (r"outdoor performance", 3), (r"pv (plant|system) performance", 3),
        (r"monitoring", 2), (r"real operating condition", 3), (r"performance", 1),
    ],
    "PV_Degradation_and_Reliability": [
        (r"degradation", 3), (r"reliabilit", 3), (r"failure mode|fault detect", 3),
        (r"soiling", 3), (r"potential.induced|\bpid\b", 3), (r"hot.?spot", 3),
        (r"lifetime|service life", 2), (r"inspektion|instandhaltung|fehler erkennen", 3),
    ],
    "PV_Standards_and_Measurement": [
        (r"iec 60904|iec 61215|iec 61853", 3), (r"standard test condition", 3),
        (r"i.v characteristic|current.voltage characteristic", 3),
        (r"spectral mismatch", 3), (r"calibrat", 3), (r"energy rating", 3),
        (r"reference (cell|module)", 3), (r"uncertaint", 2), (r"\bstc\b", 2),
    ],
    "PV_Shading_and_Mismatch": [
        (r"partial shading", 3), (r"bypass diode", 3), (r"mismatch", 3),
        (r"array configuration|string configuration", 3), (r"shading loss", 3),
        (r"weak light|low.light (performance|condition)", 3),
    ],
    "PV_Cell_and_Module_Technologies": [
        (r"thin.film", 3), (r"crystalline silicon|mono.?crystalline|poly.?crystalline", 3),
        (r"perovskite|\bcigs\b|\bcdte\b|\ba-si\b|\bgaas\b", 3),
        (r"organic photovoltaic|\bopv\b|dye.sensiti", 3),
        (r"(module|cell) efficienc", 3), (r"indoor (pv|photovoltaic)|energy harvesting", 3),
        (r"solar cell", 2), (r"module technolog", 3),
    ],
    "Thin_Film_Solar_Cells": [
        (r"czts|cu2znsns|cu2snss|cu2cdsnse|kesterite|stannite", 4),
        (r"cigs|cu\(in|chalcopyrite|chalcogenide|cgs", 4),
        (r"buffer layer|back contact|absorber layer|cds", 4),
        (r"sputter|vapou?r deposition|vacuum evaporation|electroplat", 3),
        (r"quantum dot|nanocrystal|colloidal synthesis", 3),
        (r"thin.film solar cell|thin film solar cell", 3),
        (r"molybdenum|mo thin film", 2),
        (r"cuinse2|cuin\(|cu\(in|cu2snс|cis cell|cd.free buffer", 4),
        (r"chemical bath deposition|cbd|co.?evaporat|multisource|sublimation", 3),
        (r"thin.films?", 2), (r"cdte|perovskite|cigs|a-si|amorphous silicon", 3),
        (r"band structure|absorption coefficient|refractive index|doping (limit|pinning)", 2),
    ],
    "Indoor_PV_and_Energy_Harvesting": [
        (r"indoor (photovoltaic|pv|energy|illumination|light|applicat)", 4),
        (r"energy harvest", 4),
        (r"mm.scale|millimet(er|re).scale|wireless sensor node|body sensor", 4),
        (r"artificial light source", 3), (r"low.power (system|electronic|circuit)", 2),
    ],
    "Bifacial_PV_and_Albedo": [
        (r"bifacial", 3), (r"albedo", 3), (r"rear.side|backside irradiance", 3),
        (r"ground reflect", 3),
    ],
    "PV_in_Nordic_Climates": [
        (r"snow (loss|cover|shedding|soiling)", 3), (r"winter performance", 3),
        (r"high.latitude", 3), (r"nordic (climate|condition)", 3),
    ],
    "PV_Economics_and_LCA": [
        (r"\blcoe\b|levelis(ed|ing) cost|leveliz(ed|ing) cost", 3),
        (r"life.?cycle (assessment|impact|cost)", 3), (r"techno.economic", 3),
        (r"repowering", 3), (r"payback", 3), (r"feed.in tariff|incentive scheme", 3),
        (r"wirtschaftlichkeit|cost of photovoltaic", 3), (r"economic analysis", 2),
    ],
    "Energy_Storage": [
        (r"batter", 3), (r"energy storage", 3), (r"off.grid|stand.alone", 3),
        (r"microgrid", 3), (r"storage sizing|storage requirement", 3),
    ],
    "PV_Electrical_Design_and_Inverters": [
        (r"inverter", 3), (r"\bmppt\b|maximum power point track", 3),
        (r"reactive power", 3), (r"cabling|cable sizing", 3),
        (r"electrical installation|elinstallation", 3), (r"grid connection", 3),
        (r"dc.ac ratio|oversizing", 3), (r"transformer", 2),
    ],
    "PV_Forecasting_and_Ramp_Control": [
        (r"forecast", 3), (r"nowcast", 3), (r"ramp.?rate", 5),
        (r"power smoothing", 5),
    ],
    "PV_Modelling_Tools": [
        (r"pvsyst|pvlib|pysam|system advisor model|bifacial_radiance", 3),
        (r"simulation (software|tool)", 2),
    ],
    "Agrivoltaics": [
        (r"agri.?voltaic|agri.?pv", 3), (r"dual.use land|land equivalent ratio", 3),
    ],
    "PV_Greenhouses": [
        (r"semi.?transparent (pv|photovoltaic|module)", 3),
        (r"(pv|photovoltaic|solar).{0,12}greenhouse", 3),
        (r"greenhouse.{0,12}(pv|photovoltaic|solar panel)", 3),
    ],
    "Solar_Radiation_Modelling": [
        (r"transposition|tilted (plane|surface)", 3), (r"diffuse fraction|diffuse horizontal", 3),
        (r"decomposition model", 3), (r"clearness index", 3), (r"sky model|anisotropic sky", 3),
        (r"\bperez\b|hay.davies|reindl", 3), (r"solar position|sun.earth|solar geometr", 3),
        (r"global horizontal|\bghi\b|\bdni\b|\bdhi\b", 3), (r"insolation", 2),
        (r"solar radiation|irradiance", 2),
    ],
    "PAR_and_Spectral_Radiation": [
        (r"photosynthetically active radiation|\bpar\b", 3),
        (r"\bppfd\b|photon flux density", 3), (r"quanta|quantum sensor", 3),
        (r"spectral (distribution|irradiance|resolution)", 3),
        (r"spectroradiomet", 3), (r"par.{0,6}(ratio|fraction)", 3),
    ],
    "Solar_and_Weather_Data": [
        (r"pvgis|meteonorm|solcast|solargis|nasa power|\bsoda\b|satel.light", 3),
        (r"\bsmhi\b|str[aå]ng|\bfmi\b|copernicus", 3),
        (r"radiation database|solar resource map", 3), (r"\btmy\b|typical meteorological", 3),
        (r"weather (data|station|observation)", 2),
    ],
    "Permitting_and_Environmental_Assessment": [
        (r"\bglare\b|reflection hazard", 3), (r"electromagnetic field|\bemf\b", 3),
        (r"stormwater", 3), (r"environmental impact|\beia\b", 3),
        (r"permitting|samr[aå]d|milj[oö]balken", 3), (r"natura 2000", 3),
        (r"biodiversit", 2), (r"health risk", 2),
    ],
    "Site_Layout_and_Civil_Design": [
        (r"corrosion", 3), (r"wind load|eurocode", 3), (r"cut.and.fill", 3),
        (r"row (pitch|spacing)", 3), (r"layout optimi", 3), (r"mounting structure", 3),
        (r"drainage", 2),
    ],
    "Building_Integrated_PV": [
        (r"\bbipv\b|building.integrated", 3), (r"rooftop|roof.mounted", 3),
        (r"fa[cç]ade", 3), (r"self.consumption", 3), (r"residential (solar|pv)", 3),
    ],
    "Power_Systems_and_Grid_Integration": [
        (r"hosting capacity", 3), (r"curtailment", 3), (r"distribution feeder", 3),
        (r"grid integration", 3), (r"penetration level", 3), (r"power system", 2),
    ],
    "Electricity_Markets_and_Prices": [
        (r"nord pool|entso", 3), (r"electricity price|day.ahead market", 3),
        (r"balancing market|reserve product", 3), (r"power purchase agreement|\bppa\b", 3),
    ],
    "Energy_Transition_and_Scenarios": [
        (r"wind (power|energy|turbine)", 3), (r"energy (scenario|transition)", 3),
        (r"renewable energy data|energy outlook", 2),
    ],
    # ---- tools and themes ---------------------------------------------------
    "Statistics_and_Data_Analysis": [
        (r"mixed.effects|emmeans|estimated marginal", 3),
        (r"experimental design|split.plot|randomi[sz]ed block|repeated measures", 3),
        (r"pseudoreplication", 3), (r"\banova\b|analysis of variance", 3),
        (r"bayesian|monte carlo", 3), (r"time series|\barima\b|sarimax", 3),
        (r"regression", 2), (r"statistic", 1),
    ],
    "R": [
        (r"\bggplot2\b|tidyverse|\bdplyr\b|\bnlme\b", 3),
        (r"simple features for r|r: a language", 3), (r"pirate.s guide to r", 3),
    ],
    "Cartography_and_Map_Design": [
        (r"colorbrewer|colour advice for maps", 3), (r"map design|atlas layout", 3),
    ],
    "Reporting_and_Publishing": [
        (r"thesis format|writing the .{0,3}kappa", 3), (r"overleaf|pylatex|jupyter book", 3),
    ],
    "Remote_Sensing": [
        (r"remote sensing", 3), (r"sentinel-\d|landsat|\bmodis\b", 3),
        (r"land surface temperature|land.cover map", 3), (r"satellite imagery", 3),
    ],
    "Geospatial_Python": [
        (r"\bqgis\b|geopandas|\bgdal\b|grass gis|geemap", 3),
    ],
    "Geodata_Portals_Nordic": [
        (r"lantm[aä]teriet|norgeskart|h[oø]ydedata|maanmittaus|paikkatieto", 3),
        (r"l[aä]nsstyrelsen|fornsök|kulturminnes[oø]k", 3),
    ],
    "Global_Datasets_and_Catalogs": [
        (r"natural earth|opentopography|global energy monitor|wiki.solar", 3),
    ],
    "Climate_Change": [
        (r"climate change|climate projection|global warming", 3),
        (r"\bipcc\b|\bafolu\b", 3), (r"climate scenario", 3),
    ],
    "Urban_Planning": [
        (r"urban heat|urban microclimate|urban planning", 3), (r"urban water tariff", 3),
    ],
    "Agriculture": [
        (r"irrigation|water footprint|water withdrawal", 3), (r"agronom", 2),
        (r"soil fertil", 2), (r"\bcrop\b", 1),
    ],
}
COMPILED = {page: [(re.compile(p, re.I), w) for p, w in rules]
            for page, rules in PAGE_RULES.items()}

# Clusters that score as their own topic but stay under the 5-note page
# threshold: park them under a "## Candidate: <name>" heading on the host page.
CANDIDATE_OF = {
    "Plant_Carbon_and_Water_Relations": ("Photosynthesis_and_Gas_Exchange",
                                         "Carbon and Water Relations"),
    "Phenology_and_Thermal_Time": ("Frost_Hardiness_and_Freezing_Tests",
                                   "Phenology and Thermal Time"),
}

# --- collection name -> (prior page, related, tags) ---------------------------
# Only a prior: a strong content signal overrides it.
COLLECTION_RULES = {
    "1 Ligh Spectra and Light Intensity": ("Light_Quality_and_Photomorphogenesis", ["Horticultural_Lighting"], []),
    "Light Intensity and gas exchange": ("Photosynthesis_and_Gas_Exchange", ["Light_Quality_and_Photomorphogenesis"], []),
    "DLI": ("Lighting_Strategy_and_Control", [], []),
    "G.Ex - Light response curves": ("Photosynthesis_and_Gas_Exchange", [], []),
    "Photomorphogenesis": ("Light_Quality_and_Photomorphogenesis", [], []),
    "Light spectra and field trial": ("Light_Quality_and_Photomorphogenesis", ["Forest_Seedling_Production"], []),
    "R:FR": ("Light_Quality_and_Photomorphogenesis", [], []),
    "2 Long night treatment": ("Photoperiod_and_Dormancy_Induction", ["Frost_Hardiness_and_Freezing_Tests"], []),
    "3 Light shock": ("Photoinhibition_and_Light_Stress", ["Photosynthesis_and_Gas_Exchange"], []),
    "4 DLI and supplementary light": ("Lighting_Strategy_and_Control", [], []),
    "01 DLI": ("Lighting_Strategy_and_Control", [], []),
    "Supplementary light control": ("Lighting_Strategy_and_Control", ["Greenhouse_Horticulture"], []),
    "02 Dynamic control": ("Lighting_Strategy_and_Control", ["Greenhouse_Horticulture"], []),
    "03 LED seedling cultivation": ("Horticultural_Lighting", ["Forest_Seedling_Production"], []),
    "3.1 Importance of LEDs": ("Horticultural_Lighting", [], []),
    "04 Cost": ("Lighting_Strategy_and_Control", ["Greenhouse_Horticulture"], []),
    "05 Greenhouse energy": ("Greenhouse_Horticulture", ["Lighting_Strategy_and_Control"], []),
    "07 other": ("Lighting_Strategy_and_Control", [], []),
    "5 Agrivoltacis": ("Agrivoltaics", [], []),
    "Energy calculation": ("PAR_and_Spectral_Radiation", ["Solar_Radiation_Modelling"], []),
    "Solar Greenhouse": ("PV_Greenhouses", ["Greenhouse_Horticulture", "Agrivoltaics"], []),
    "6 Image and color analysis": ("Plant_Phenotyping_and_Image_Analysis", [], []),
    "Image analysis and Phenotyping": ("Plant_Phenotyping_and_Image_Analysis", [], []),
    "Photobox": ("Plant_Phenotyping_and_Image_Analysis", [], []),
    "1.1 Seedling Performance": ("Forest_Seedling_Production", [], []),
    "1.1.1 Photosynthesis": ("Photosynthesis_and_Gas_Exchange", ["Forest_Seedling_Production"], []),
    "1.1.2 Gas Ex. and Ch. F.": ("Photosynthesis_and_Gas_Exchange", ["Chlorophyll_Fluorescence"], []),
    "1.1.3 RGC": ("Forest_Seedling_Production", ["Forest_Regeneration"], []),
    "2 Forest regeneration": ("Forest_Regeneration", [], []),
    "3 Somatic embryos": ("Tree_Breeding_and_Propagation", ["Forest_Seedling_Production"], []),
    "2.1 Greenhouses and Growth chambers": ("Greenhouse_Horticulture", [], []),
    "Growth chambers": ("Greenhouse_Horticulture", [], []),
    "2.2 Vertical Farming": ("Vertical_Farming_and_Urban_Agriculture", [], []),
    "2.3 Entoculture": ("Unsorted", ["Agriculture"], ["#needs-topic"]),
    "2.4 Zephyr Project": ("Forest_Seedling_Production", ["Horticultural_Lighting"], ["#project/zephyr"]),
    "LED for Plants": ("Horticultural_Lighting", ["Light_Quality_and_Photomorphogenesis"], []),
    "Spectra": ("Light_Quality_and_Photomorphogenesis", [], []),
    "UV": ("Light_Quality_and_Photomorphogenesis", [], []),
    "1.4 Wind energy in forest": ("Energy_Transition_and_Scenarios", ["Swedish_Forestry"], []),
    "4.1 Solar Radiation": ("Solar_Radiation_Modelling", [], []),
    "Water and population": ("Unsorted", ["Climate_Change", "Agriculture"], ["#needs-topic"]),
    "5 - PV modules": ("PV_Cell_and_Module_Technologies", [], []),
    "5.0 TÜV Mustergutachten": ("Solar_Radiation_Modelling", ["PV_System_Performance"], []),
    "5.1.1 PV-Mexico": ("PV_System_Performance", [], ["#region/mexico", "#project/msc-thesis/4-13"]),
    "5.1.2 PV-Sweden": ("PV_in_Nordic_Climates", [], ["#region/sweden", "#project/msc-thesis/4-14"]),
    "5.2.1 PV cells and modules": ("PV_Cell_and_Module_Technologies", [], []),
    "5.2.2 Inverters and batteries": ("PV_Electrical_Design_and_Inverters", ["Energy_Storage"], []),
    "5.2.3 Bifacial": ("Bifacial_PV_and_Albedo", [], []),
    "5.2.4 Cables": ("PV_Electrical_Design_and_Inverters", [], []),
    "5.3 PV systems design": ("PV_Electrical_Design_and_Inverters", ["PV_System_Performance"], []),
    "5.3.1 PV Standards": ("PV_Standards_and_Measurement", [], ["#project/msc-thesis/4-1"]),
    "5.3.2 mini-PV for indoors": ("PV_Cell_and_Module_Technologies", [], []),
    "5.3.3 Agrivoltaics": ("Agrivoltaics", [], []),
    "5.4 PV Performance and Monitoring": ("PV_System_Performance", [], ["#project/msc-thesis/4-2"]),
    "5.4 PV reliability": ("PV_Degradation_and_Reliability", [], []),
    "5.5 PV Losses": ("PV_System_Performance", [], []),
    "5.5.1 Angular losses": ("PV_System_Performance", ["Solar_Radiation_Modelling"], []),
    "5.5.2 Shading losses": ("PV_Shading_and_Mismatch", [], []),
    "5.5.3 Degradation": ("PV_Degradation_and_Reliability", [], []),
    "5.5.4 Low light": ("PV_Shading_and_Mismatch", ["PV_Cell_and_Module_Technologies"], []),
    "5.5.5 Thermal effects": ("PV_System_Performance", [], []),
    "5.5.6 Soiling and Snow": ("PV_in_Nordic_Climates", ["PV_Degradation_and_Reliability"], []),
    "5.5.7 Albedo": ("Bifacial_PV_and_Albedo", [], []),
    "5.6 PV software": ("PV_Modelling_Tools", [], []),
    "5.7 PV Repowering": ("PV_Economics_and_LCA", [], []),
    "5.8 BOS materials": ("Site_Layout_and_Civil_Design", [], []),
    "5.9 PV forescasting": ("PV_Forecasting_and_Ramp_Control", ["PV_System_Performance"], []),
    "5.10 PV ramp control": ("PV_Forecasting_and_Ramp_Control", ["Energy_Storage"], []),
    "5.11 LCA": ("PV_Economics_and_LCA", [], []),
    "5.12 PV health risks": ("Permitting_and_Environmental_Assessment", [], []),
    "Reflection": ("Permitting_and_Environmental_Assessment", [], []),
    "7 Statistics": ("Statistics_and_Data_Analysis", [], []),
    "Medicinal plants": ("Unsorted", ["Agriculture"], ["#needs-topic"]),
}

# Collections with no usable prior at all: content decides, else Unsorted.
NO_PRIOR = {
    "0 Articles": [], "0 Thesis": ["#project/thesis"], "6 Thesis": ["#project/thesis"],
    "1 Forestry": [], "2 Controlled Environment Agriculture": [], "3 Photobiology": [],
    "4 Energy": [], "5 Photovoltaics": [], "5.1 PV general data": [],
    "5.2 PV components": [], "06 Data": [], "99 Other": ["#needs-topic"],
    "Material and equipment used": ["#project/thesis"],
    "Own publications": ["#project/own-publications"],
}

# Hand corrections made while writing the pages: the classifier's answer was
# defensible but wrong on reading the item. Key -> (page, note).
MANUAL_OVERRIDES = {
    "XT2TK2UC": ("Solar_Radiation_Modelling", "sky radiance and luminance distribution models"),
    "JP3EUWDI": ("Solar_Radiation_Modelling", "sky type determination from illuminance"),
    "QKSR9LY7": ("Forest_Seedling_Production", "history of Swedish plant production"),

    "BDC5V23W": ("Photosynthesis_and_Gas_Exchange", "the leaf as a photosynthetic system"),
    "CZXTGX65": ("Greenhouse_Horticulture", "greenhouse engineering textbook"),
    "TLDEN5CW": ("Greenhouse_Horticulture", "greenhouse crop photosynthesis and dry matter"),
    "BVYHSWF9": ("Greenhouse_Horticulture", "light transmission in greenhouses"),
    "NZVDY55V": ("Solar_Radiation_Modelling", "all-weather sky luminance model"),
    "Y3EHQ9AI": ("Solar_Radiation_Modelling", "Tregenza sky subdivision"),
    "S7FMSIQK": ("Solar_Radiation_Modelling", "radiation versus cloud amount and type"),

    "XQDQS8L8": ("Photoperiod_and_Dormancy_Induction", "long-night treatment of spruce"),
    "CDMKG2S3": ("Radiometry_and_Photometry", "ISO 80000-2 quantities and units"),
    "9479NZIZ": ("Radiometry_and_Photometry", "daylight coefficient model"),
    "SYNRUYW6": ("Swedish_Forestry", "soil organic carbon in Swedish forests"),
    "45EWEYW9": ("Swedish_Forestry", "potential Norway spruce production in Sweden"),
    "ZR3LZS5H": ("Building_Integrated_PV", "residential energy certificates and conservation"),
    "S5KZKT95": ("Building_Integrated_PV", "fenestration and daylight optimisation"),
    "FYQTRT7E": ("Greenhouse_Horticulture", "greenhouse shapes review"),
    "QDNJBQA3": ("Greenhouse_Horticulture", "greenhouse technology textbook"),
    "94M4KJ97": ("Greenhouse_Horticulture", "diffuse-light cover materials"),
    "52TCA7AZ": ("Greenhouse_Horticulture", "light transmission in vegetable greenhouses"),
    "H5VWUKVL": ("Greenhouse_Horticulture", "solar fraction by greenhouse orientation"),
    "89MKL8PY": ("Greenhouse_Horticulture", "transmission in plastic greenhouses"),
    "J7RI8899": ("PV_Standards_and_Measurement", "IEC 60904-3 reference spectrum change"),
    "6E36Z9E5": ("PV_Standards_and_Measurement", "IEC 60904-3 measurement principles"),
    "QTAQWCVT": ("PV_System_Performance", "regional PV module performance"),
    "AAEMBZCT": ("Solar_Radiation_Modelling", "SunCalculator angular and spectral distribution"),

    "EUTDJ4BW": ("Thin_Film_Solar_Cells", "thin-film solar cell overview"),
    "IU4R9487": ("Thin_Film_Solar_Cells", "materials science of thin films"),
    "JIVVY3FA": ("Thin_Film_Solar_Cells", "CZTS thin films monograph"),
    "VY6L9TVD": ("Thin_Film_Solar_Cells", "CZTS technology trends"),
    "BESHFTAB": ("Thin_Film_Solar_Cells", "all-sputtering CIGS process"),
    "KMK89DIF": ("Thin_Film_Solar_Cells", "CIGS on enamelled steel"),
    "LHHC65TF": ("Thin_Film_Solar_Cells", "flexible CIGS on stainless steel"),
    "TDCRP6YX": ("Thin_Film_Solar_Cells", "chalcopyrite deposition apparatus patent"),
    "8HQQ4T2G": ("Thin_Film_Solar_Cells", "evaporation processes chapter"),
    "34TSWHA8": ("Thin_Film_Solar_Cells", "deposition technologies handbook"),
    "M9LLWMEC": ("Thin_Film_Solar_Cells", "doping limits in II-VI and I-III-VI2"),
    "2Z7MV44C": ("Thin_Film_Solar_Cells", "CdTe technology page"),
    "U6KZXEKX": ("Thin_Film_Solar_Cells", "CIGS manufacturer product page"),
    "NUC5RRJP": ("Thin_Film_Solar_Cells", "thin-film module measurement artefacts"),

    # The msc-thesis Mexico section is electricity-market and policy material,
    # not PV performance
    "TQ5BXRGR": ("Electricity_Markets_and_Prices", "Mexican interconnection contract statistics"),
    "WRL2AAHP": ("Electricity_Markets_and_Prices", "Mexican electricity market rules"),
    "8A88G588": ("Electricity_Markets_and_Prices", "Mexican energy reform, wholesale market"),
    "3ZSQM3CB": ("Electricity_Markets_and_Prices", "Mexican electricity sector law"),
    "JP4DJCHJ": ("Electricity_Markets_and_Prices", "grid parity monitor"),
    "XISJB62T": ("Electricity_Markets_and_Prices", "IRENA REmap scenario for Mexico"),
    "RD2JE35S": ("PV_Economics_and_LCA", "regional solar potential and its economics"),
    # not PV
    "X6T59667": ("Light_Quality_and_Photomorphogenesis", "light spectra in seedling pre-cultivation"),
    "TBGLIQ5W": ("Building_Integrated_PV", "office plug loads; building energy candidate"),
    "NS6MHKS7": ("Building_Integrated_PV", "EnergyPlus; building energy candidate"),
    "VHXU4E9L": ("Building_Integrated_PV", "EnergyPlus; building energy candidate"),
    # duplicate of RMBFUMGJ
    "P26435V2": ("Site_Layout_and_Civil_Design", "duplicate IFC developer guide"),
    # The MSc-thesis book shelf landed together on the electrical page; split it
    # by what each book is actually about.
    "UTF9EDHH": ("PV_Cell_and_Module_Technologies", "physics of solar energy textbook"),
    "58WST3UE": ("PV_Cell_and_Module_Technologies", "introduction to photovoltaics"),
    "7EGAHEDE": ("PV_Cell_and_Module_Technologies", "fundamentals of PV modules"),
    "W5GF2CCN": ("PV_Cell_and_Module_Technologies", "PV solar energy generation textbook"),
    "JJGCZ487": ("PV_Cell_and_Module_Technologies", "Applied Photovoltaics, cell-to-system"),
    "AW9UZSDW": ("PV_Cell_and_Module_Technologies", "solar energy and environment textbook"),
    "HEIIHR5J": ("PV_Cell_and_Module_Technologies", "Solar Electricity textbook"),
    "2U8DJQ8B": ("PV_Cell_and_Module_Technologies", "solar energy engineering, device-led"),
    "559RS28D": ("PV_Cell_and_Module_Technologies", "hybrid PV/thermal collector design"),
    "UJL3MQAB": ("Building_Integrated_PV", "solar technologies for buildings"),
    "M2ZFA8EL": ("PV_Standards_and_Measurement", "PV power measurement guidelines"),
    "BAPNEDLE": ("PV_System_Performance", "SolarPro performance-modelling articles"),
    # O&M and project development are practice, not electrical design
    "GQZCGPHC": ("PV_Degradation_and_Reliability", "utility-scale O&M overview"),
    "RV769VEY": ("PV_Degradation_and_Reliability", "NREL O&M best practices"),
    "UGWHMKCA": ("PV_Degradation_and_Reliability", "SolarPower Europe O&M guidelines"),
    "RMBFUMGJ": ("Site_Layout_and_Civil_Design", "IFC utility-scale developer guide"),
    "9XTZ5U4B": ("Site_Layout_and_Civil_Design", "PV system installation best practices"),
    "RJ9T5YV4": ("Site_Layout_and_Civil_Design", "ground-based layout optimisation tool"),
    # not PV at all
    "Z9Z3PNP6": ("Optimization_and_Decision_Making", "Lloyd's method variant; kept for equal-area parcelling"),
    # "reliability" / "degradation" pulled non-PV items onto the PV pages
    "V28MQKKX": ("Photosynthesis_and_Gas_Exchange", "quality of gas exchange measurements"),
    "83WKV2WU": ("Statistics_and_Data_Analysis", "measurement error in continuous variables"),
    "53GYUM7P": ("Forest_Regeneration", "silvology; eco-unit development, not PV degradation"),
    "M8GK7W8Z": ("Unsorted", "UV exposure and vitamin D; sits with that candidate"),
    # Swedish agency material belongs with the practice pages
    "U24TU3QG": ("Permitting_and_Environmental_Assessment", "Energimyndigheten, the solcellsparker guidance source"),
    "U9YZMK5X": ("PV_Electrical_Design_and_Inverters", "Elsäkerhetsverket rooftop installation rules"),
    "8MDPCKGK": ("PV_Electrical_Design_and_Inverters", "electrical safety requirements for PV plants"),
    "5TA8F6L9": ("Site_Layout_and_Civil_Design", "steel corrosion; kept for mounting structures, not BIPV"),
    # "calibration" pulled image-calibration papers onto PV standards
    "BFV2B9YG": ("Plant_Phenotyping_and_Image_Analysis", "camera colour calibration for agriculture imaging"),
    "9MQ246BB": ("Plant_Phenotyping_and_Image_Analysis", "image calibration toolbox, not PV measurement"),
    "3X8ZFLRH": ("Radiometry_and_Photometry", "CIE colorimetric standards; belongs with the units papers"),
    # "mismatch" pulled the spectral-mismatch standard onto the shading page
    "IKTHRMYD": ("PV_Standards_and_Measurement", "IEC 60904-7 is a measurement standard"),
    "YZ64XQ5M": ("PV_Standards_and_Measurement", "ASTM G173 reference spectra underpin STC rating"),
    # data services and portals file under Data_Sources first
    "PYGHKWUF": ("Solar_and_Weather_Data", "Meteocontrol is a weather data service"),
    "U4LHCSWI": ("Solar_and_Weather_Data", "validation of the Solcast dataset itself"),
    "YFYWCWCB": ("Solar_and_Weather_Data", "NREL MIDC measurement station data"),
    "QSBBXN9R": ("Solar_and_Weather_Data", "NASA SSE data portal"),
    "SWYFMIAC": ("Solar_and_Weather_Data", "NSRDB data viewer"),
    # subject is elsewhere
    "EPW9ISZR": ("PV_Cell_and_Module_Technologies", "spectral response of cells"),
    "DWUB2EEL": ("PV_Greenhouses", "light distribution inside a PV greenhouse"),
    "DUYGXM47": ("PV_System_Performance", "annual yields of different PV technologies"),
    "TFRZJ9Q6": ("Unsorted", "vitamin D and UV exposure; sits with that candidate"),
    # General PV textbooks caught by an incidental battery/stand-alone mention
    "QM2DVERT": ("PV_Cell_and_Module_Technologies", "general PV textbook, cell-to-system emphasis"),
    "SKMY7GX9": ("PV_Electrical_Design_and_Inverters", "installation and design handbook"),
    "9AD5SEPG": ("PV_Electrical_Design_and_Inverters", "systems engineering textbook"),
    # keep the ramp-control cluster together
    "756KLULT": ("PV_Forecasting_and_Ramp_Control", "ramp-rate control; sits with Marcos and Makibar"),
    # not PV, not LCA
    "B4BKRANY": ("Energy_Transition_and_Scenarios", "low-carbon technology trade-offs, not PV economics"),
    "4WVBVWDV": ("Unsorted", "edible insects; belongs with the entoculture candidate"),
    "4JURZID6": ("Lighting_Strategy_and_Control", "lighting economics, not PV economics"),
    "B72IY295": ("Vertical_Farming_and_Urban_Agriculture",
                 "subject is powering indoor cultivation, not grid penetration"),
    "328P62TM": ("Solar_and_Weather_Data",
                 "review of resource data sets themselves; data-first rule"),
}

TAG_MAP = {
    "main model": "#project/light-model", "supporting info": "#project/light-model",
    "master thesis": "#project/msc-thesis", "thesis": "#project/msc-thesis",
    "4 pv systems": "#project/msc-thesis",
    "4.1 pv standards": "#project/msc-thesis/4-1",
    "4.2 pv performance and monitoring": "#project/msc-thesis/4-2",
    "4.13 pv-mexico": "#project/msc-thesis/4-13",
    "4.14 pv-sweden": "#project/msc-thesis/4-14",
    "read for course": "#project/course-reading",
    "norway spruce": "#species/picea-abies", "picea abies": "#species/picea-abies",
    "scots pine": "#species/pinus-sylvestris", "pinus sylvestris": "#species/pinus-sylvestris",
    "lettuce": "#crop/lettuce", "tomato": "#crop/tomato",
    "cucumber": "#crop/cucumber", "basil": "#crop/basil",
}

SPECIES_HINTS = [
    (r"picea abies|norway spruce|\bgran\b(?!t)", "#species/picea-abies"),
    (r"pinus sylvestris|scots pine|\btall(?:en|ar)?\b(?= och gran| och tall)", "#species/pinus-sylvestris"),
    (r"pinus contorta|lodgepole", "#species/pinus-contorta"),
    (r"betula|birch", "#species/betula"),
]
REGION_HINTS = [
    (r"\bsweden|swedish|sverige|svensk", "#region/sweden"),
    (r"\bnorway|norwegian|norge", "#region/norway"),
    (r"\bfinland|finnish|suomi", "#region/finland"),
    (r"\bnordic|scandinavia", "#region/nordic"),
    (r"\bmexico|mexican", "#region/mexico"),
    (r"netherlands|dutch", "#region/netherlands"),
]
SPECIES_HINTS = [(re.compile(p, re.I), t) for p, t in SPECIES_HINTS]
REGION_HINTS = [(re.compile(p, re.I), t) for p, t in REGION_HINTS]


def authors_short(creators):
    names = [c.get("lastName") or c.get("name") or "" for c in creators
             if c.get("creatorType") == "author"]
    names = [n for n in names if n]
    if not names:
        return ""
    if len(names) == 1:
        return names[0]
    if len(names) == 2:
        return names[0] + " & " + names[1]
    return names[0] + " et al."


def year_of(item):
    m = re.search(r"(1[89]\d\d|20\d\d)", item.get("date") or "")
    return m.group(1) if m else ""


def strip_tags(s):
    return re.sub(r"<[^>]+>", " ", s or "")


def score_pages(title, rest):
    """Return {page: (total, title_only)}; title matches count double.

    title_only breaks ties: a page matched in the title beats one matched only
    in the abstract, where the term is far more often incidental.
    """
    scores = defaultdict(lambda: [0, 0])
    for page, rules in COMPILED.items():
        for rx, w in rules:
            if rx.search(title):
                scores[page][0] += w * 2
                scores[page][1] += w
            elif rx.search(rest):
                scores[page][0] += w
    return {p: tuple(v) for p, v in scores.items()}


def main():
    data = json.loads(SRC.read_text(encoding="utf-8"))
    cols = data["collections"]
    items = [it for it in data["items"] if it.get("itemType") != "attachment"]

    parent_of = {k: (c.get("parent") or None) for k, c in cols.items()}

    def full_path(k):
        parts, seen = [], set()
        while k and k in cols and k not in seen:
            seen.add(k)
            parts.append(cols[k]["name"])
            k = parent_of.get(k)
        return " / ".join(reversed(parts))

    path_of = {k: full_path(k) for k in cols}
    depth = {k: path_of[k].count(" / ") for k in cols}

    item_cols = defaultdict(list)
    for k, c in cols.items():
        for iid in c["items"]:
            item_cols[iid].append(k)

    rows = []
    for it in items:
        mine = sorted(item_cols.get(it.get("itemID"), []),
                      key=lambda k: depth[k], reverse=True)

        title = strip_tags(it.get("title", ""))
        rest = strip_tags(" ".join(filter(None, [
            it.get("abstractNote", ""), it.get("publicationTitle", ""),
            it.get("bookTitle", ""),
            " ".join(t["tag"] for t in it.get("tags", [])),
        ])))

        scores = score_pages(title, rest)
        ranked = sorted(scores.items(), key=lambda kv: (-kv[1][0], -kv[1][1], kv[0]))
        best_page = ranked[0][0] if ranked else None
        best_score = ranked[0][1][0] if ranked else 0
        second = ranked[1][0] if len(ranked) > 1 else None

        prior, prior_rel, tags = None, [], []
        for k in mine:
            name = cols[k]["name"]
            if name in COLLECTION_RULES:
                prior, rel, tg = COLLECTION_RULES[name]
                prior_rel, tags = list(rel), list(tg)
                break
        for k in mine:
            name = cols[k]["name"]
            if name in NO_PRIOR:
                tags += [t for t in NO_PRIOR[name] if t not in tags]

        # decide
        if best_score >= STRONG:
            primary = best_page
            if prior and prior != best_page:
                rule = "content-over-collection({} -> {}, {})".format(prior, best_page, best_score)
                conf = "high" if best_score >= STRONG + 3 else "medium"
            else:
                rule = "content({})".format(best_score)
                conf = "high"
        elif prior:
            primary = prior
            rule = "collection-prior"
            conf = "high" if best_score == 0 or best_page == prior else "medium"
        elif best_score >= WEAK:
            primary, rule, conf = best_page, "content-weak({})".format(best_score), "medium"
        elif best_score > 0:
            primary, rule, conf = best_page, "content-faint({})".format(best_score), "low"
        else:
            primary, rule, conf = "Unsorted", "no-signal", "low"
            if "#needs-topic" not in tags:
                tags.append("#needs-topic")

        if it.get("key") in MANUAL_OVERRIDES:
            primary, why = MANUAL_OVERRIDES[it["key"]]
            rule, conf = "manual:" + why, "high"

        candidate = ""
        if primary in CANDIDATE_OF:
            primary, candidate = CANDIDATE_OF[primary]
            if "#needs-topic" not in tags:
                tags.append("#needs-topic")

        if primary == "Unsorted" and "#needs-topic" not in tags:
            tags.append("#needs-topic")

        related = []
        for cand in ([second] if second and scores.get(second, (0, 0))[0] >= WEAK else []) \
                + prior_rel + ([prior] if prior else []):
            if cand and cand != primary and cand != "Unsorted" and cand not in related:
                related.append(cand)
        for k in mine:
            name = cols[k]["name"]
            if name in COLLECTION_RULES:
                p = COLLECTION_RULES[name][0]
                if p != primary and p != "Unsorted" and p not in related:
                    related.append(p)
        related = related[:3]

        hay = title + " " + rest
        for t in it.get("tags", []):
            if t.get("type") == 1:
                continue
            v = TAG_MAP.get(t["tag"].strip().lower())
            if v and v not in tags:
                tags.append(v)
        for rx, t in SPECIES_HINTS + REGION_HINTS:
            if rx.search(hay) and t not in tags:
                tags.append(t)
        if it.get("itemType") == "computerProgram":
            tags.append("#type/tool")

        doi = (it.get("DOI") or "").strip()
        link = "https://doi.org/" + doi if doi else (it.get("url") or "")

        rows.append({
            "key": it.get("key", ""),
            "item_type": it.get("itemType", ""),
            "year": year_of(it),
            "authors": authors_short(it.get("creators", [])),
            "title": title[:160],
            "publication": (it.get("publicationTitle") or it.get("bookTitle")
                            or it.get("publisher") or ""),
            "has_abstract": "y" if it.get("abstractNote") else "",
            "collections": " | ".join(path_of[k] for k in mine),
            "primary_page": primary,
            "candidate": candidate,
            "related_pages": ", ".join(related),
            "tags": " ".join(dict.fromkeys(tags)),
            "confidence": conf,
            "rule": rule,
            "score": best_score,
            "runner_up": second or "",
            "link": link,
        })

    OUT.parent.mkdir(exist_ok=True)
    with OUT.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print("wrote {} ({} rows)".format(OUT, len(rows)))


if __name__ == "__main__":
    main()
