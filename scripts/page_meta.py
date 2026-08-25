#!/usr/bin/env python3
"""Header metadata for every topic page: domain, parent MOC, aliases, summary.

Used by dump_page.py and by the page writer so headers stay consistent.
"""

# page -> (domain slug, parent MOC, [aliases], summary)
PAGES = {
    # ---- Photovoltaics ------------------------------------------------------
    "Solar_Radiation_Modelling": (
        "photovoltaics", "Photovoltaics",
        ["solar geometry", "transposition", "sky models"],
        "Solar position and geometry, transposition to tilted planes, diffuse/direct decomposition and sky models, and the radiation databases these are validated against."),
    "PAR_and_Spectral_Radiation": (
        "photovoltaics", "Photovoltaics",
        ["PAR", "photosynthetically active radiation", "PPFD", "spectral irradiance"],
        "Photosynthetically active radiation and the spectral side of solar radiation: quanta versus energy, PPFD and PAR:global ratios, spectral distribution and the instruments that measure it."),
    "PV_System_Performance": (
        "photovoltaics", "Photovoltaics",
        ["PV performance", "performance ratio", "yield"],
        "Performance ratio, energy yield, monitoring and field performance of PV systems under real operating conditions."),
    "PV_Degradation_and_Reliability": (
        "photovoltaics", "Photovoltaics",
        ["degradation", "reliability", "soiling", "faults"],
        "How PV systems lose output and fail over time: degradation rates, faults and failure modes, soiling, PID and hot spots, inspection and service."),
    "PV_Shading_and_Mismatch": (
        "photovoltaics", "Photovoltaics",
        ["partial shading", "mismatch", "bypass diodes"],
        "Partial shading and mismatch losses: bypass diodes, array and string configurations, and behaviour under weak and low light."),
    "PV_Standards_and_Measurement": (
        "photovoltaics", "Photovoltaics",
        ["IEC 60904", "STC", "I-V measurement", "energy rating"],
        "The IEC 60904 series and related standards, STC and I–V characterisation, spectral mismatch, reference devices, calibration and measurement uncertainty."),
    "PV_Cell_and_Module_Technologies": (
        "photovoltaics", "Photovoltaics",
        ["solar cells", "thin film", "module technology", "indoor PV"],
        "Cell and module technologies: crystalline silicon, thin film, organic and semi-transparent PV, and indoor and low-light energy harvesting."),
    "Thin_Film_Solar_Cells": (
        "photovoltaics", "Photovoltaics",
        ["CIGS", "CZTS", "chalcogenide", "thin film"],
        "Thin-film absorber materials and how they are made: CIGS and CZTS chemistry, buffer and back-contact layers, sputtering and evaporation processes, and the device results that follow."),
    "Indoor_PV_and_Energy_Harvesting": (
        "photovoltaics", "Photovoltaics",
        ["indoor PV", "energy harvesting", "low-light PV"],
        "PV under artificial and low light: indoor cell characterisation, the missing standard test conditions for it, and millimetre-scale energy harvesting for sensor nodes."),
    "Bifacial_PV_and_Albedo": (
        "photovoltaics", "Photovoltaics",
        ["bifacial", "albedo", "rear-side irradiance"],
        "Bifacial modules and yield, rear-side irradiance, and the albedo measurements and datasets that drive them."),
    "PV_in_Nordic_Climates": (
        "photovoltaics", "Photovoltaics",
        ["snow losses", "winter performance", "high latitude PV"],
        "PV at high latitude: snow losses and snow models, winter performance, and Swedish, Norwegian and Finnish site conditions."),
    "Building_Integrated_PV": (
        "photovoltaics", "Photovoltaics",
        ["BIPV", "rooftop PV", "self-consumption"],
        "BIPV, rooftop and façade systems, self-consumption and residential PV, and rooftop solar potential mapping."),
    "PV_Economics_and_LCA": (
        "photovoltaics", "Photovoltaics",
        ["LCOE", "life-cycle assessment", "techno-economic analysis", "repowering"],
        "LCOE and techno-economic analysis, life-cycle assessment, repowering economics, incentives and financial metrics."),
    "Energy_Storage": (
        "photovoltaics", "Photovoltaics",
        ["batteries", "off-grid", "microgrids"],
        "Batteries with PV, off-grid and stand-alone systems, microgrids, and storage sizing."),
    "PV_Forecasting_and_Ramp_Control": (
        "photovoltaics", "Photovoltaics",
        ["PV forecasting", "nowcasting", "ramp-rate control"],
        "Deterministic and probabilistic forecasting of PV output, satellite-derived nowcasting, and ramp-rate limitation and power smoothing."),
    # ---- Solar park development --------------------------------------------
    "Permitting_and_Environmental_Assessment": (
        "solar-park-development", "Solar_Park_Development",
        ["samråd", "EIA", "glare", "EMF"],
        "Permitting and environmental assessment for solar parks: 12:6 samråd and agency guidance, EIA content, glare, EMF, stormwater, biodiversity and cultural heritage."),
    "Site_Layout_and_Civil_Design": (
        "solar-park-development", "Solar_Park_Development",
        ["layout", "civil design", "corrosion", "wind loads"],
        "Site layout and civil works: row pitch and layout optimisation, terrain and cut/fill, drainage, wind loads, corrosion classes, roads and fencing."),
    "PV_Electrical_Design_and_Inverters": (
        "solar-park-development", "Solar_Park_Development",
        ["inverters", "string design", "grid connection"],
        "Inverter sizing and oversizing, reactive power, string and multi-MPPT design, cabling, installation codes and grid-connection applications."),
    # ---- Agrivoltaics -------------------------------------------------------
    "Agrivoltaics": (
        "agrivoltaics", "Agrivoltaics_and_Dual_Use",
        ["agri-PV", "APV", "dual-use land"],
        "Dual use of land for PV and agriculture: elevated and vertical bifacial layouts, shading factors, crop and grassland response, Nordic pilots and the economics of dual use."),
    "PV_Greenhouses": (
        "agrivoltaics", "Agrivoltaics_and_Dual_Use",
        ["solar greenhouse", "semi-transparent PV"],
        "PV on and in greenhouses: semi-transparent and organic modules, light distribution inside the house, microclimate simulation and crop yield trade-offs."),
    # ---- Energy systems -----------------------------------------------------
    "Power_Systems_and_Grid_Integration": (
        "energy-systems", "Energy_Systems",
        ["grid integration", "hosting capacity", "curtailment"],
        "Grid integration of variable generation: hosting capacity, curtailment, distribution feeders and grid-connection capacity."),
    "Energy_Transition_and_Scenarios": (
        "energy-systems", "Energy_Systems",
        ["energy scenarios", "wind power", "energy transition"],
        "Energy transition scenarios and the wider renewable mix, including wind power and low-carbon technology trade-offs."),
    # ---- Plant photobiology -------------------------------------------------
    "Horticultural_Lighting": (
        "plant-photobiology", "Plant_Photobiology",
        ["LED lighting", "grow lights", "luminaires", "lamp efficacy"],
        "The lighting hardware itself: LEDs and conventional lamps, luminaire design, photon efficacy and lamp comparisons for plant production."),
    "Lighting_Strategy_and_Control": (
        "plant-photobiology", "Plant_Photobiology",
        ["DLI", "supplemental lighting", "lighting control", "lighting energy"],
        "How the light is applied rather than what produces it: daily light integral targets, supplemental and dynamic lighting control, scheduling, and the energy and cost of lighting."),
    "Light_Quality_and_Photomorphogenesis": (
        "plant-photobiology", "Plant_Photobiology",
        ["light quality", "spectrum", "phytochrome", "R:FR", "shade avoidance"],
        "Spectral quality and the plant's response to it: blue, red, far-red and UV, phytochrome and cryptochrome, shade avoidance and morphology."),
    "Photoperiod_and_Dormancy_Induction": (
        "plant-photobiology", "Plant_Photobiology",
        ["photoperiod", "short-day treatment", "long night", "bud set", "growth cessation"],
        "Photoperiodic control of growth and dormancy: short-day and long-night treatment, growth cessation, bud set and dormancy induction."),
    "Photosynthesis_and_Gas_Exchange": (
        "plant-photobiology", "Plant_Photobiology",
        ["gas exchange", "light response curves", "photosynthesis"],
        "Photosynthetic performance measured as gas exchange: light and CO2 response curves, stomatal conductance, quantum yield, transpiration and respiration."),
    "Chlorophyll_Fluorescence": (
        "plant-photobiology", "Plant_Photobiology",
        ["fluorescence", "Fv/Fm", "PSII efficiency", "vitality testing"],
        "Chlorophyll fluorescence as a measurement technique: Fv/Fm and PSII efficiency, quenching analysis, and its use for vitality and stress testing."),
    "Photoinhibition_and_Light_Stress": (
        "plant-photobiology", "Plant_Photobiology",
        ["photoinhibition", "photoprotection", "light shock", "NPQ"],
        "What happens when there is too much light: photoinhibition and photodamage, photoprotective dissipation and NPQ, sun versus shade acclimation, UV screening and light shock after outdoor exposure."),
    "Plant_Phenotyping_and_Image_Analysis": (
        "plant-photobiology", "Plant_Photobiology",
        ["phenotyping", "image analysis", "machine vision", "PlantCV"],
        "Non-destructive measurement of plants by image: RGB and multispectral imaging, machine vision for growth and morphology, and the software behind it."),
    "Radiometry_and_Photometry": (
        "plant-photobiology", "Plant_Photobiology",
        ["radiometry", "photometry", "units", "CIE", "quantum units"],
        "The measurement foundation under all the light work: SI and photometric units, CIE and IUPAC definitions, quanta versus energy, and the classic papers the definitions rest on."),
    # ---- Controlled environment agriculture ---------------------------------
    "Greenhouse_Horticulture": (
        "controlled-environment-agriculture", "Controlled_Environment_Agriculture",
        ["greenhouse", "växthus", "greenhouse climate", "screens"],
        "Greenhouse climate and energy: covers and screens, heating and waste heat, growth chambers, and greenhouse crop production."),
    "Vertical_Farming_and_Urban_Agriculture": (
        "controlled-environment-agriculture", "Controlled_Environment_Agriculture",
        ["plant factory", "vertical farming", "hydroponics", "urban agriculture"],
        "Plant factories and vertical farms, hydroponics, resource-use efficiency, indoor farming economics and urban food systems."),
    # ---- Forestry -----------------------------------------------------------
    "Forest_Seedling_Production": (
        "forestry", "Forestry",
        ["nursery", "containerised seedlings", "seedling quality", "storability"],
        "Nursery production of forest seedlings: container and stock types, fertilisation, seedling quality and vitality assessment, storage and storability, root growth capacity."),
    "Forest_Regeneration": (
        "forestry", "Forestry",
        ["regeneration", "site preparation", "planting", "föryngring"],
        "Getting the next stand established: planting and outplanting, site preparation and scarification, natural regeneration and shelterwood, survival and early growth."),
    "Frost_Hardiness_and_Freezing_Tests": (
        "forestry", "Forestry",
        ["frost hardiness", "cold hardiness", "acclimation", "freezing tests", "LT50"],
        "Cold acclimation and deacclimation, frost and freezing tolerance, and the tests used to measure them — freezing tests, electrolyte leakage, LT50 — plus cold storage and overwintering."),
    "Forest_Damage_and_Herbivory": (
        "forestry", "Forestry",
        ["pine weevil", "browsing", "damage"],
        "Damage to seedlings and young stands: pine weevil, moose and roe deer browsing, frost and drought damage, and protection measures."),
    "Tree_Breeding_and_Propagation": (
        "forestry", "Forestry",
        ["breeding", "somatic embryogenesis", "provenance", "clonal forestry"],
        "Breeding programmes and genetic gain, provenance and transfer, somatic embryogenesis and clonal propagation."),
    "Swedish_Forestry": (
        "forestry", "Forestry",
        ["skogsbruk", "Swedish forestry", "forest policy"],
        "Swedish and Nordic forest management practice and policy, agency guidance, and European forest reporting."),
    "Norway_Spruce": (
        "forestry", "Forestry", ["Picea abies", "gran"],
        "Species page for *Picea abies*: species-specific facts and links out to the process pages."),
    "Scots_Pine": (
        "forestry", "Forestry", ["Pinus sylvestris", "tall"],
        "Species page for *Pinus sylvestris*: species-specific facts and links out to the process pages."),
    # ---- Geospatial ---------------------------------------------------------
    "QGIS": ("geospatial", "Geospatial", ["QGIS tips", "expressions", "plugins"],
             "QGIS itself: tutorials and tips, expressions and geometry generators, styling, plugins, and project and cloud workflows."),
    "PyQGIS_and_GIS_Automation": ("geospatial", "Geospatial", ["PyQGIS", "qgis_process"],
             "Automating GIS work: PyQGIS, processing algorithms from Python, the qgis_process CLI, QGIS in Jupyter, and plugin development."),
    "Google_Earth_Engine": ("geospatial", "Geospatial", ["GEE", "geemap", "Earth Engine"],
             "Earth Engine JavaScript and Python APIs, geemap, the community catalog, time-series extraction and export strategies."),
    "Geospatial_Python": ("geospatial", "Geospatial", ["geopandas", "GDAL", "GRASS"],
             "The geospatial Python stack: geopandas, GDAL, GRASS with Jupyter, lonboard, spopt and cloud-native formats."),
    "Drones_and_Photogrammetry": ("geospatial", "Geospatial", ["UAV", "WebODM", "orthophoto", "thermal inspection"],
             "Drone survey and photogrammetry: WebODM, Pix4D and Metashape, orthophoto and DSM generation with GCPs, thermal inspection of solar farms, and remote-pilot regulation."),
    "Terrain_and_Lidar": ("geospatial", "Geospatial", ["DEM", "laser data", "point clouds"],
             "Height models and laser scanning: point clouds, DEM void filling, contours, slope and aspect, cut/fill volumes and catchment delineation."),
    "3D_Geovisualization": ("geospatial", "Geospatial", ["Blender GIS", "Cesium", "3D Tiles"],
             "Three-dimensional visualisation of sites and landscapes: Blender GIS, Cesium and 3D Tiles, Qgis2threejs, and solar-park renders for stakeholders."),
    "Cartography_and_Map_Design": ("geospatial", "Geospatial", ["cartography", "ColorBrewer", "map layout"],
             "Map and figure design: terrain cartography, colour schemes, atlas layouts, interactive maps and publication-quality output."),
    # ---- Data sources -------------------------------------------------------
    "Geodata_Portals_Nordic": ("data-sources", "Data_Sources", ["Lantmäteriet", "Norgeskart", "geodata"],
             "Swedish, Norwegian and Finnish geodata portals and their access notes."),
    "Solar_and_Weather_Data": ("data-sources", "Data_Sources", ["PVGIS", "SMHI", "weather data", "TMY"],
             "Solar and meteorological data sources: national observation networks, satellite-derived irradiance services, radiation databases and module databases."),
    "Energy_Market_and_Grid_Data": ("data-sources", "Data_Sources", ["Nord Pool", "ENTSO-E", "grid data"],
             "Market and grid data: price and transparency platforms, TSO data services and APIs."),
    "Global_Datasets_and_Catalogs": ("data-sources", "Data_Sources", ["global datasets", "catalogs"],
             "Global and cross-cutting datasets and the catalogs that index them."),
    "Forestry_and_Agriculture_Statistics": ("data-sources", "Data_Sources", ["seedling statistics", "forest statistics"],
             "Production and area statistics for forestry and agriculture, including Nordic seedling production figures."),
    # ---- Tools and methods --------------------------------------------------
    "R": ("tools-and-methods", "Tools_and_Methods", ["tidyverse", "ggplot2", "nlme"],
          "R and its ecosystem: ggplot2, dplyr, sf, nlme and emmeans."),
    "PV_Modelling_Tools": ("tools-and-methods", "Tools_and_Methods", ["pvlib", "PVsyst", "SAM", "PySAM"],
          "Software for modelling PV: pvlib, PySAM and SAM, PVsyst, Meteonorm and PVGIS tooling. Method papers go to the thematic page; this is about the tools."),
    "Statistics_and_Data_Analysis": ("tools-and-methods", "Tools_and_Methods",
          ["mixed models", "emmeans", "experimental design"],
          "Statistical method and experimental design: mixed-effects models, estimated marginal means, regression, time series, Bayesian and Monte Carlo methods."),
    "Optimization_and_Decision_Making": ("tools-and-methods", "Tools_and_Methods",
          ["optimisation", "linear programming", "spatial optimisation"],
          "Optimisation and decision method: linear programming, spatial optimisation and clustering, and decision-making under uncertainty."),
    "Data_Visualization": ("tools-and-methods", "Tools_and_Methods", ["charts", "plotly", "dashboards"],
          "Chart types and figure craft, plotting libraries and dashboards."),
    "Reporting_and_Publishing": ("tools-and-methods", "Tools_and_Methods", ["LaTeX", "reports", "Overleaf"],
          "Producing documents: templated PDF reports, LaTeX and Overleaf, notebooks as publications, diagrams and reference management."),
    "CAD_and_Drafting": ("tools-and-methods", "Tools_and_Methods", ["AutoCAD", "drafting"],
          "AutoCAD and Map 3D, viewports and annotative objects, and AEC workflows bridging CAD and GIS."),
    "SQL": ("tools-and-methods", "Tools_and_Methods", ["databases", "queries"],
          "SQL and database work."),
    "Agentic_Coding": ("tools-and-methods", "Tools_and_Methods", ["Claude Code", "agents", "prompting"],
          "Coding with LLM agents: Claude Code, agent workflows, prompting, and LLM-maintained wikis."),
    "Knowledge_Management": ("tools-and-methods", "Tools_and_Methods", ["Obsidian", "Zotero", "PKM"],
          "Obsidian, Zotero and the conventions of this vault."),
    "Noise_Modelling": ("solar-park-development", "Solar_Park_Development", ["NoiseModelling", "dBmap"],
          "Noise propagation modelling for inverters and transformers, including NoiseModelling in QGIS and DEM effects."),
}
