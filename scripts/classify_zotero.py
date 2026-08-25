#!/usr/bin/env python3
"""Propose a primary page and related pages for every item in the Zotero BBT JSON export.

Collection path is the primary signal: 1300 of 1408 items sit in at least one
collection and the tree maps closely onto TAXONOMY.md. Collections that hold
mixed content (listed in MIXED) fall through to keyword rules on title,
abstract and tags, as do the 108 items in no collection at all.

Writes processed/Zotero_library_map.csv for review before any notes are written.
"""
import csv
import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "raw" / "Zotero_library.json"
OUT = ROOT / "processed" / "Zotero_library_map.csv"

# --- collection name -> (primary page, related pages, tags) -------------------
# Keyed on the collection's own name; names are unique in this library.
COLLECTION_RULES = {
    # 0 Articles -- the light research
    "1 Ligh Spectra and Light Intensity": ("Light_Quality_and_Photomorphogenesis", ["Horticultural_Lighting"], []),
    "Light Intensity and gas exchange": ("Photosynthesis_and_Plant_Physiology", ["Light_Quality_and_Photomorphogenesis"], []),
    "DLI": ("Horticultural_Lighting", ["Photosynthesis_and_Plant_Physiology"], []),
    "G.Ex - Light response curves": ("Photosynthesis_and_Plant_Physiology", [], []),
    "Photomorphogenesis": ("Light_Quality_and_Photomorphogenesis", [], []),
    "Light spectra and field trial": ("Light_Quality_and_Photomorphogenesis", ["Forest_Seedling_Production"], []),
    "R:FR": ("Light_Quality_and_Photomorphogenesis", [], []),
    "2 Long night treatment": ("Seedling_Cold_Hardiness_and_Dormancy", ["Light_Quality_and_Photomorphogenesis"], []),
    "3 Light shock": ("Photoinhibition_and_Light_Stress", ["Photosynthesis_and_Plant_Physiology"], []),
    "4 DLI and supplementary light": ("Horticultural_Lighting", [], []),
    "01 DLI": ("Horticultural_Lighting", [], []),
    "Supplementary light control": ("Horticultural_Lighting", ["Greenhouse_Horticulture"], []),
    "02 Dynamic control": ("Horticultural_Lighting", ["Greenhouse_Horticulture"], []),
    "03 LED seedling cultivation": ("Horticultural_Lighting", ["Forest_Seedling_Production"], []),
    "3.1 Importance of LEDs": ("Horticultural_Lighting", [], []),
    "04 Cost": ("Horticultural_Lighting", ["Greenhouse_Horticulture"], []),
    "05 Greenhouse energy": ("Greenhouse_Horticulture", ["Horticultural_Lighting"], []),
    "07 other": ("Horticultural_Lighting", [], []),
    "5 Agrivoltacis": ("Agrivoltaics", ["Photovoltaics"], []),
    "Energy calculation": ("Solar_Radiation_Modelling", ["Agrivoltaics", "Photosynthesis_and_Plant_Physiology"], []),
    "Solar Greenhouse": ("PV_Greenhouses", ["Greenhouse_Horticulture", "Agrivoltaics"], []),
    "6 Image and color analysis": ("Plant_Phenotyping_and_Image_Analysis", [], []),
    "Image analysis and Phenotyping": ("Plant_Phenotyping_and_Image_Analysis", [], []),
    "Photobox": ("Plant_Phenotyping_and_Image_Analysis", [], []),
    # 1 Forestry
    "1.1 Seedling Performance": ("Forest_Seedling_Production", [], []),
    "1.1.1 Photosynthesis": ("Photosynthesis_and_Plant_Physiology", ["Forest_Seedling_Production"], []),
    "1.1.2 Gas Ex. and Ch. F.": ("Photosynthesis_and_Plant_Physiology", ["Forest_Seedling_Production"], []),
    "1.1.3 RGC": ("Forest_Seedling_Production", ["Forest_Regeneration"], []),
    "2 Forest regeneration": ("Forest_Regeneration", [], []),
    "3 Somatic embryos": ("Tree_Breeding_and_Propagation", ["Forest_Seedling_Production"], []),
    # 2 Controlled Environment Agriculture
    "2.1 Greenhouses and Growth chambers": ("Greenhouse_Horticulture", [], []),
    "Growth chambers": ("Greenhouse_Horticulture", [], []),
    "2.2 Vertical Farming": ("Vertical_Farming_and_Urban_Agriculture", [], []),
    "2.3 Entoculture": ("Unsorted", ["Agriculture"], ["#needs-topic"]),
    "2.4 Zephyr Project": ("Forest_Seedling_Production", ["Horticultural_Lighting", "Agrivoltaics"], ["#project/zephyr"]),
    # 3 Photobiology
    "LED for Plants": ("Horticultural_Lighting", ["Light_Quality_and_Photomorphogenesis"], []),
    "Spectra": ("Light_Quality_and_Photomorphogenesis", [], []),
    "UV": ("Light_Quality_and_Photomorphogenesis", [], []),
    # 4 Energy
    "1.4 Wind energy in forest": ("Energy_Transition_and_Scenarios", ["Swedish_Forestry"], []),
    "4.1 Solar Radiation": ("Solar_Radiation_Modelling", [], []),
    "Water and population": ("Unsorted", ["Climate_Change", "Agriculture"], ["#needs-topic"]),
    # 5 Photovoltaics
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
    "5.4 PV reliability": ("PV_System_Performance", [], []),
    "5.5 PV Losses": ("PV_System_Performance", [], []),
    "5.5.1 Angular losses": ("PV_System_Performance", ["Solar_Radiation_Modelling"], []),
    "5.5.2 Shading losses": ("PV_Shading_and_Mismatch", [], []),
    "5.5.3 Degradation": ("PV_System_Performance", [], []),
    "5.5.4 Low light": ("PV_Shading_and_Mismatch", ["PV_Cell_and_Module_Technologies"], []),
    "5.5.5 Thermal effects": ("PV_System_Performance", [], []),
    "5.5.6 Soiling and Snow": ("PV_in_Nordic_Climates", ["PV_System_Performance"], []),
    "5.5.7 Albedo": ("Bifacial_PV_and_Albedo", [], []),
    "5.6 PV software": ("PV_Modelling_Tools", [], []),
    "5.7 PV Repowering": ("PV_Economics_and_LCA", [], ["#needs-review"]),
    "5.8 BOS materials": ("Site_Layout_and_Civil_Design", [], []),
    "5.9 PV forescasting": ("PV_Forecasting_and_Ramp_Control", ["PV_System_Performance"], []),
    "5.10 PV ramp control": ("PV_Forecasting_and_Ramp_Control", ["Energy_Storage"], []),
    "5.11 LCA": ("PV_Economics_and_LCA", [], []),
    "5.12 PV health risks": ("Permitting_and_Environmental_Assessment", [], []),
    "Reflection": ("Permitting_and_Environmental_Assessment", [], []),
    # 7 Statistics
    "7 Statistics": ("Statistics_and_Data_Analysis", [], []),
    # leftovers
    "Medicinal plants": ("Unsorted", ["Agriculture"], ["#needs-topic"]),
}

# Collections whose contents are mixed: keyword rules run first, and the listed
# page is only the fallback.
MIXED = {
    "0 Thesis": ("Unsorted", ["#project/thesis"]),
    "1 Forestry": ("Forest_Regeneration", []),
    "2 Controlled Environment Agriculture": ("Greenhouse_Horticulture", []),
    "3 Photobiology": ("Light_Quality_and_Photomorphogenesis", []),
    "4 Energy": ("Solar_Radiation_Modelling", []),
    "5 Photovoltaics": ("PV_System_Performance", []),
    "06 Data": ("Solar_and_Weather_Data", []),
    "6 Thesis": ("Unsorted", ["#project/thesis"]),
    "Material and equipment used": ("Unsorted", ["#project/thesis"]),
    "Own publications": ("Unsorted", ["#project/own-publications"]),
    "99 Other": ("Unsorted", ["#needs-topic"]),
    "0 Articles": ("Unsorted", []),
    "5.1 PV general data": ("PV_System_Performance", []),
    "5.2 PV components": ("PV_Cell_and_Module_Technologies", []),
}

# Decision rule 6, "data first": an item that *is* a portal, API, dataset or
# piece of software files under Data_Sources rather than with its subject. Only
# applied to item types that can be one; a journal article *about* a database
# still goes to the thematic page.
DATA_ITEM_TYPES = {"webpage", "computerProgram", "dataset"}
_DATA_RULES = [
    (r"pvgis|solargis|solcast|meteonorm|nasa power|\bsoda\b|satel.light|solar resource|str[aå]ng|smhi|\bfmi\b|copernicus|solar radiation data", "Solar_and_Weather_Data"),
    (r"nord pool|entso|svenska kraftn[aä]t|fingrid|energy.charts|electricitymap|cambium", "Energy_Market_and_Grid_Data"),
    (r"lantm[aä]teriet|norgeskart|h[oø]ydedata|maanmittaus|paikkatieto|skogsstyrelsen|l[aä]nsstyrelsen|fornsök|kulturminnes[oø]k|\bnve\b", "Geodata_Portals_Nordic"),
    (r"natural earth|opentopography|global energy monitor|wiki.solar|land.cover|data catalog|catalogue", "Global_Datasets_and_Catalogs"),
    (r"statistik|statistics|plantstatistik|planteskole", "Forestry_and_Agriculture_Statistics"),
]
DATA_RULES = [(re.compile(p, re.I), page) for p, page in _DATA_RULES]

# --- keyword rules, first match wins ------------------------------------------
_RULES = [
    # radiometry and photometry fundamentals collected for the light model
    (r"international system of units|\bsi units\b|photochemical equivalence|iupac|commission internationale de l.eclairage|\bcie\b proceedings|energieverteilung im normalspectrum|erzeugung und verwandlung des lichtes|quantification of uv radiation|radiometr|photometr|actinometr", "Radiometry_and_Photometry"),
    (r"growing degree day|heat accumulation from maximum|thermal time|degree.days", "Phenology_and_Thermal_Time"),
    (r"somatic embryo|clonal forestry|genetic gain|breeding programme|provenance|seed orchard", "Tree_Breeding_and_Propagation"),
    (r"pine weevil|hylobius|browsing|moose|roe deer|vole damage", "Forest_Damage_and_Herbivory"),
    (r"frost hard|cold hard|dehardening|acclimat|bud set|bud burst|dormanc|growth cessation|short.day treatment|long night|freezing test|electrolyte leakage", "Seedling_Cold_Hardiness_and_Dormancy"),
    (r"site preparation|scarification|shelterwood|natural regeneration|planting surviv|f[oö]ryngring|mechani[sz]ed .{0,10}planting|reforestation|forest restoration|silvicultur", "Forest_Regeneration"),
    (r"plantstatistik|planteskole statistikk|fr[oö].? och plantstatistik|forest nurseries in|nursery directory|seedling production statistic", "Forestry_and_Agriculture_Statistics"),
    (r"container[ie][sz]ed seedling|nursery|plantskol|skogsplant|quickpot|bew[aä]sserungscontainer|\bhiko\b|stock type|root growth capacity|seedling quality|mini.plug|transplant seedling|storability", "Forest_Seedling_Production"),
    (r"skogsstyrelsen|swedish forest|state of europe|forests? and forestry|forest management in|forestry in (finland|norway|sweden)|skogsbruk|forest ecosystem service|silvatic|principles of silviculture", "Swedish_Forestry"),
    (r"photoinhibit|photoprotect|light shock|xanthophyll|non.photochemical quench|sun and shade leaves|uv screening", "Photoinhibition_and_Light_Stress"),
    (r"chlorophyll fluorescen|gas exchange|photosynthe|light response curve|stomatal conduct|carbohydrat|photorespir", "Photosynthesis_and_Plant_Physiology"),
    (r"far.red|red:far|phytochrome|cryptochrome|photoperiod|blue light|spectral quality|light quality|shade avoidance|photomorphogen|circadian", "Light_Quality_and_Photomorphogenesis"),
    (r"\bled\b|leds\b|light.emitting diode|luminaire|grow light|light source|horticultur|solid.state lighting|\bssl\b|photon efficacy|supplementary light|supplemental light|daily light integral|\bdli\b|valoya|\blamp", "Horticultural_Lighting"),
    (r"plantcv|phenotyp|image analysis|machine vision|rgb imaging|multispectral imaging", "Plant_Phenotyping_and_Image_Analysis"),
    (r"vertical farm|plant factor|hydroponic|urban agricultur|food mile", "Vertical_Farming_and_Urban_Agriculture"),
    (r"semi.transparent .{0,4}(pv|photovoltaic)|pv greenhouse|greenhouse .{0,4}(pv|photovoltaic)|roof.mounted flexible solar", "PV_Greenhouses"),
    (r"greenhouse|glasshouse|growth chamber|thermal screen|climate control|v[aä]xthus|waste heat|restv[aä]rme|winter production|odlingsmilj", "Greenhouse_Horticulture"),
    (r"agrivoltaic|agri.?pv|dual.use land", "Agrivoltaics"),
    (r"bifacial|albedo|rear.side irradiance", "Bifacial_PV_and_Albedo"),
    (r"iec 60904|standard test condition|i-v characteristic|current.voltage characteristic|spectral mismatch|energy rating|calibrat", "PV_Standards_and_Measurement"),
    (r"partial shading|bypass diode|mismatch|array configuration|weak light|low.light performance", "PV_Shading_and_Mismatch"),
    (r"snow loss|snow cover|winter performance|high.latitude|nordic climate", "PV_in_Nordic_Climates"),
    (r"\blcoe\b|life.cycle assessment|life cycle assessment|techno.economic|levelis|leveliz|repowering|payback|feed.in tariff", "PV_Economics_and_LCA"),
    (r"batter|energy storage|off.grid|stand.alone|microgrid", "Energy_Storage"),
    (r"inverter|reactive power|cabling|electrical installation|grid connection|\bmppt\b|elinstallation", "PV_Electrical_Design_and_Inverters"),
    (r"performance ratio|degradation|soiling|monitoring|yield assessment|outdoor performance|reliability|inspektion|instandhaltung|fehler erkennen", "PV_System_Performance"),
    (r"solar cell|thin film|crystalline silicon|module technolog|module efficienc|champion photovoltaic|perovskite|organic photovoltaic|\bgaas\b|energy harvesting", "PV_Cell_and_Module_Technologies"),
    (r"rooftop|building.integrated|\bbipv\b|fa[cç]ade|self.consumption|residential solar|roof.mounted", "Building_Integrated_PV"),
    (r"forecast|nowcast|ramp.rate|ramp rate", "PV_Forecasting_and_Ramp_Control"),
    (r"solar radiation|irradiance|transposition|tilted plane|diffuse fraction|clearness index|sky model|perez|photosynthetically active radiation|solar position|daylength|twilight|sun.earth|insolation|practical navigator|spectral daily", "Solar_Radiation_Modelling"),
    (r"pvgis|meteonorm|solcast|solargis|nasa power|smhi|str[aå]ng|radiation database|\bsoda\b|satel.light|solar resource map", "Solar_and_Weather_Data"),
    (r"dimensions of light|light in regulating plant|light and plant growth", "Light_Quality_and_Photomorphogenesis"),
    (r"pvsyst|pvlib|pysam|system advisor model|bifacial_radiance", "PV_Modelling_Tools"),
    (r"nord pool|entso|electricity price|day.ahead|balancing market|power purchase agreement", "Electricity_Markets_and_Prices"),
    (r"hosting capacity|curtailment|distribution feeder|grid integration|penetration level|power system", "Power_Systems_and_Grid_Integration"),
    (r"wind (power|energy|turbine)|energy scenario|energy transition|renewable energy data", "Energy_Transition_and_Scenarios"),
    (r"mixed.effects|emmeans|estimated marginal|regression|experimental design|split.plot|randomi[sz]ed block|repeated measures|anova|bayesian|monte carlo|time series|arima|statistic", "Statistics_and_Data_Analysis"),
    (r"\bggplot2\b|simple features for r|r: a language|tidyverse|\bdplyr\b|\bnlme\b", "R"),
    (r"natural earth|opentopography|land.cover product|global dataset|data catalog", "Global_Datasets_and_Catalogs"),
    (r"lantm[aä]teriet|norgeskart|h[oø]ydedata|maanmittaus|paikkatieto|geodata", "Geodata_Portals_Nordic"),
    (r"qgis|geopandas|\bgdal\b|grass gis|earth engine|geemap", "Geospatial_Python"),
    (r"remote sensing|satellite imagery|sentinel-|landsat|modis|land surface temperature", "Remote_Sensing"),
    (r"glare|electromagnetic field|\bemf\b|stormwater|environmental impact|permitting|samr[aå]d|milj[oö]balken|natura 2000|biodiversity", "Permitting_and_Environmental_Assessment"),
    (r"corrosion|wind load|eurocode|cut.and.fill|drainage|row pitch|layout optimi", "Site_Layout_and_Civil_Design"),
    (r"noise|sound propagation", "Noise_Modelling"),
    (r"colorbrewer|color advice for maps|map design|atlas layout", "Cartography_and_Map_Design"),
    (r"thesis format|writing the .?kappa|overleaf|latex|jupyter book", "Reporting_and_Publishing"),
    (r"climate change|climate projection|global warming|\bipcc\b|afolu", "Climate_Change"),
    (r"urban heat|urban planning|urban microclimate", "Urban_Planning"),
    (r"edible insect|insects as food|entomophag", "Unsorted"),
    (r"\bcrop\b|agronom|irrigation|water footprint|soil fertil", "Agriculture"),
]
CONTENT_RULES = [(re.compile(p, re.I), page) for p, page in _RULES]

TAG_MAP = {
    "main model": "#project/light-model",
    "supporting info": "#project/light-model",
    "master thesis": "#project/msc-thesis",
    "thesis": "#project/msc-thesis",
    "4 pv systems": "#project/msc-thesis",
    "4.1 pv standards": "#project/msc-thesis/4-1",
    "4.2 pv performance and monitoring": "#project/msc-thesis/4-2",
    "4.13 pv-mexico": "#project/msc-thesis/4-13",
    "4.14 pv-sweden": "#project/msc-thesis/4-14",
    "read for course": "#project/course-reading",
    "norway spruce": "#species/picea-abies",
    "picea abies": "#species/picea-abies",
    "scots pine": "#species/pinus-sylvestris",
    "pinus sylvestris": "#species/pinus-sylvestris",
    "lettuce": "#crop/lettuce",
    "tomato": "#crop/tomato",
    "cucumber": "#crop/cucumber",
    "basil": "#crop/basil",
}


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

        haystack = " ".join(filter(None, [
            it.get("title", ""), it.get("abstractNote", ""),
            it.get("publicationTitle", ""), it.get("bookTitle", ""),
            " ".join(t["tag"] for t in it.get("tags", [])),
        ]))
        haystack = re.sub(r"<[^>]+>", " ", haystack)

        primary, related, tags, rule, conf = None, [], [], "", "low"
        mixed_hit = None

        # 1. deepest collection carrying an explicit rule
        for k in mine:
            name = cols[k]["name"]
            if name in COLLECTION_RULES:
                primary, rel, tg = COLLECTION_RULES[name]
                related, tags = list(rel), list(tg)
                rule = "collection:" + name
                conf = "high" if depth[k] >= 1 else "medium"
                break

        # 2. mixed collection -> keyword rules, then the mixed default
        if primary is None:
            mixed_hit = next((cols[k]["name"] for k in mine
                              if cols[k]["name"] in MIXED), None)
            if it.get("itemType") in DATA_ITEM_TYPES:
                for rx, page in DATA_RULES:
                    if rx.search(haystack):
                        primary = page
                        rule = "data-source:" + rx.pattern[:28]
                        conf = "medium"
                        break
        if primary is None:
            for rx, page in CONTENT_RULES:
                if rx.search(haystack):
                    primary = page
                    rule = "keyword:" + rx.pattern[:32]
                    conf = "medium" if mixed_hit else "low"
                    break
            if primary is None and mixed_hit:
                primary, tg = MIXED[mixed_hit]
                tags = list(tg)
                rule, conf = "mixed-default:" + mixed_hit, "low"
            if mixed_hit:
                tags += [t for t in MIXED[mixed_hit][1] if t not in tags]
            if primary == "Unsorted" and "#needs-topic" not in tags:
                tags.append("#needs-topic")

        # 3. nothing matched at all
        if primary is None:
            primary, rule, conf = "Unsorted", "none", "low"
            tags.append("#needs-topic")

        # related pages from the other collections this item sits in
        for k in mine:
            name = cols[k]["name"]
            if name in COLLECTION_RULES:
                p, rel, _ = COLLECTION_RULES[name]
                for cand in [p] + list(rel):
                    if cand != primary and cand != "Unsorted" and cand not in related:
                        related.append(cand)
        related = related[:3]

        for t in it.get("tags", []):
            if t.get("type") == 1:
                continue
            v = TAG_MAP.get(t["tag"].strip().lower())
            if v and v not in tags:
                tags.append(v)
        if it.get("itemType") == "computerProgram":
            tags.append("#type/tool")

        doi = (it.get("DOI") or "").strip()
        link = "https://doi.org/" + doi if doi else (it.get("url") or "")

        rows.append({
            "key": it.get("key", ""),
            "item_type": it.get("itemType", ""),
            "year": year_of(it),
            "authors": authors_short(it.get("creators", [])),
            "title": re.sub(r"<[^>]+>", "", it.get("title", ""))[:160],
            "publication": (it.get("publicationTitle") or it.get("bookTitle")
                            or it.get("publisher") or ""),
            "has_abstract": "y" if it.get("abstractNote") else "",
            "collections": " | ".join(path_of[k] for k in mine),
            "primary_page": primary,
            "related_pages": ", ".join(related),
            "tags": " ".join(dict.fromkeys(tags)),
            "confidence": conf,
            "rule": rule,
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
