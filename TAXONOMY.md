# TAXONOMY.md — the vault's map (living document)

This file is the current shape of the vault, not a fence. It was seeded from the Zotero library (~1,400 references) and a bookmarks export (~380 links) and is expected to grow. The agent reads it at the start of every run and edits it whenever the structure changes: new page → add a row; new domain → add a section; rename or merge → update rows and append to the changelog. Thresholds and autonomy rules for growing it live in `CLAUDE.md` (*Growing the taxonomy*).

Conventions: page names are `Title_Case_With_Underscores`; every domain has a map-of-content (MOC) page that holds only an overview and links; topic pages carry the notes. The *Seeded from* column says where the first notes will come from (Z = Zotero, B = bookmarks, O = the owner's original topic list) so the agent can predict page sizes.

## Domains at a glance

| MOC page | Covers |
|---|---|
| `Photovoltaics` | PV technology, performance, modelling, economics |
| `Solar_Park_Development` | the practice of building solar parks: permitting, site and electrical design, environmental assessment |
| `Agrivoltaics_and_Dual_Use` | PV combined with crops, greenhouses, land use |
| `Energy_Systems` | grid, electricity markets, storage, energy transition |
| `Plant_Photobiology` | light, photosynthesis, plant physiology, phenotyping |
| `Controlled_Environment_Agriculture` | greenhouses, vertical farming, urban agriculture |
| `Forestry` | seedlings, regeneration, cold hardiness, Nordic forestry |
| `Geospatial` | QGIS, Earth Engine, geospatial Python, remote sensing, drones, terrain, 3D, cartography |
| `Data_Sources` | portals, APIs and datasets, by kind |
| `Tools_and_Methods` | programming, statistics, optimisation, modelling software, reporting |
| `Themes` | cross-cutting themes: climate change, urban planning, general agriculture |
| `Other_Topics` | anything that fits no domain yet, incl. `Unsorted` |

---

## Domain: Photovoltaics — MOC `Photovoltaics`

| Page | Scope | Seeded from |
|---|---|---|
| `Solar_Radiation_Modelling` | solar position, tilted-plane transposition, diffuse/direct decomposition, sky models (CIE, Perez), clearness index, PAR-to-global ratios, radiation databases and their models (PVGIS, STRÅNG, Meteonorm), high-resolution irradiance synthesis, GRASS `r.sun` | Z, B |
| `PV_System_Performance` | performance ratio, yield, monitoring, degradation, reliability and faults, field performance, soiling and optical losses, anti-reflective coatings, reliability scorecards; analysis tools RdTools, PVAnalytics, pvcaptest, Solar Data Tools, pvdeg | Z, B |
| `PV_Shading_and_Mismatch` | partial shading, weak/low-light operation, bypass diodes, array configurations, string design, module-level electronics | Z |
| `PV_Standards_and_Measurement` | IEC 60904 series, STC, I–V characterisation, spectral mismatch, temperature/irradiance corrections, energy rating, calibration labs | Z |
| `PV_Cell_and_Module_Technologies` | crystalline Si, thin film, GaAs, organic and semi-transparent PV, half-cell modules, indoor/low-light PV and energy harvesting | Z |
| `Bifacial_PV_and_Albedo` | bifacial modules and yield, rear-side irradiance, albedo measurement and datasets (MODIS MCD43, Copernicus), bifacial_radiance | Z, B |
| `PV_in_Nordic_Climates` | snow losses and snow models (Marion, Townsend), winter performance, high-latitude yield, Swedish and Finnish site conditions | Z, B |
| `Building_Integrated_PV` | BIPV, rooftop and façade systems, self-consumption, residential PV, rooftop solar potential mapping | Z, B |
| `PV_Economics_and_LCA` | LCOE, techno-economic analysis, life-cycle assessment (incl. INCER ACV), bankability, incentives and policy, financial metrics (IRR, NPV), SAM financial models | Z, B |
| `Energy_Storage` | batteries with PV, off-grid and stand-alone systems, microgrids, storage sizing (SAM, pvlib storage) | Z, B |

## Domain: Solar park development — MOC `Solar_Park_Development`

Practice-oriented counterpart to the PV domain: what it takes to get a utility-scale plant permitted, designed and built in the Nordics. Research on the same phenomena (e.g. EMF papers) also lives here; modelling of PV output does not.

| Page | Scope | Seeded from |
|---|---|---|
| `Permitting_and_Environmental_Assessment` | Swedish 12:6 samråd (miljöbalken), Länsstyrelsen / Naturvårdsverket / Energimyndigheten guidance on solcellsparker, EIA content, glare (ForgeSolar), EMF, stormwater, biodiversity, cultural heritage checks (Fornsök, Kulturminnesøk), Norwegian and Finnish equivalents | Z, B |
| `Site_Layout_and_Civil_Design` | layout optimisation, row pitch, tracking vs fixed, equal-area/equal-count parcelling, terrain and cut/fill, drainage design (IDF, skyfall statistics), wind loads (Eurocode), corrosion classes (ISO 9223), roads and fencing, site-specific cases (airports), PVsyst/PVCollada shading scenes | Z, B |
| `PV_Electrical_Design_and_Inverters` | inverter sizing and oversizing, reactive power, string and multi-MPPT design, central vs string architectures, cabling, electrical installation codes, grid-connection applications | Z, B |
| `Noise_Modelling` | NoiseModelling (QGIS), dBmap, inverter and transformer noise, DEM in noise propagation, health-risk mapping | B |

## Domain: Agrivoltaics — MOC `Agrivoltaics_and_Dual_Use` (the bridge between PV and plants)

| Page | Scope | Seeded from |
|---|---|---|
| `Agrivoltaics` | dual-use land, vertical bifacial and elevated layouts, one-axis systems, shading factors, crop and grassland response under PV, Nordic pilots, economics of dual use, 3D models of agri-PV | Z, B |
| `PV_Greenhouses` | PV on or in greenhouses, semi-transparent and organic PV, light distribution inside PV greenhouses, microclimate simulation, crop yield trade-offs | Z |

## Domain: Energy systems — MOC `Energy_Systems`

| Page | Scope | Seeded from |
|---|---|---|
| `Power_Systems_and_Grid_Integration` | pandapower, Grid2Op, grid-connection capacity maps (Fingrid, Svenska kraftnät Mimer), hosting capacity, curtailment | B |
| `Electricity_Markets_and_Prices` | Nord Pool and ENTSO-E data, Svenska kraftnät trading rules, day-ahead and intraday prices, PPAs, merchant plant modelling (SAM + Cambium), renewables-in-markets coursework | Z, B |
| `Energy_Transition_and_Scenarios` | NREL scenario viewer, Energy-Charts, electricityMap, IEA PVPS, low-carbon technology trade-offs, wind power, decision-making under uncertainty | Z, B |

## Domain: Plant photobiology — MOC `Plant_Photobiology`

| Page | Scope | Seeded from |
|---|---|---|
| `Horticultural_Lighting` | LEDs, supplemental lighting, daily light integral, fixture efficacy and photon efficiency, lighting control strategies, lighting energy use, lamp comparisons | Z |
| `Light_Quality_and_Photomorphogenesis` | spectrum effects (blue, red, far-red, UV), phytochrome and cryptochrome, photoperiod and circadian responses, shade avoidance, morphology | Z |
| `Photosynthesis_and_Plant_Physiology` | gas exchange, chlorophyll fluorescence, PPFD/PAR use, photoinhibition and photoprotection, carbohydrates and dry matter, temperature and water relations | Z |
| `Plant_Phenotyping_and_Image_Analysis` | PlantCV, RGB and multispectral imaging, computer vision for growth measurement, non-destructive plant monitoring, FIELDimageR | Z, B |

## Domain: Controlled environment agriculture — MOC `Controlled_Environment_Agriculture`

| Page | Scope | Seeded from |
|---|---|---|
| `Greenhouse_Horticulture` | greenhouse climate and energy, screens and light transmission, heating and waste heat, closed greenhouses, crop production (lettuce, tomato, cucumber, ornamentals), Dutch and Nordic practice | Z |
| `Vertical_Farming_and_Urban_Agriculture` | plant factories, indoor farming economics, hydroponics, urban food systems, food miles, small-scale/IoT growing | Z, B |

## Domain: Forestry — MOC `Forestry`

| Page | Scope | Seeded from |
|---|---|---|
| `Forest_Seedling_Production` | nursery culture, containerised seedlings, stock types, fertilisation, seedling quality, storage and storability, vitality tests, root growth | Z |
| `Seedling_Cold_Hardiness_and_Dormancy` | frost and cold hardiness, cold acclimation, short-day treatment, growth cessation, bud set, bud burst, freezing tests, electrolyte leakage, dormancy physiology | Z |
| `Forest_Regeneration` | planting, site preparation and scarification, natural regeneration, shelterwood, survival and establishment, early growth, choice of regeneration method | Z |
| `Forest_Damage_and_Herbivory` | pine weevil, moose and roe deer browsing, frost damage, drought, fire, protection measures | Z |
| `Tree_Breeding_and_Propagation` | breeding programmes, genetic gain, somatic embryogenesis, clonal forestry, provenance and transfer, gene expression studies | Z |
| `Swedish_Forestry` | Swedish and Nordic forest management practice and policy, Skogsstyrelsen/Skogskunskap guidance, European forest reports | Z |
| `Norway_Spruce` (alias *Picea abies*), `Scots_Pine` (alias *Pinus sylvestris*) | species pages: species-specific facts and links out; never the primary page for a process paper | Z |

## Domain: Geospatial — MOC `Geospatial`

| Page | Scope | Seeded from |
|---|---|---|
| `QGIS` | tutorials and tips, expressions and geometry generators, styling, plugins (DataPlotly, FeatureGridCreator, Earth Engine plugin), project and cloud workflows (QGIS Cloud, QField), courses | B |
| `PyQGIS_and_GIS_Automation` | PyQGIS, processing algorithms from Python, `qgis_process` CLI, QGIS actions, QGIS in Jupyter/conda, plugin development | B |
| `Google_Earth_Engine` | Earth Engine JS and Python APIs, geemap, community catalog, time-series extraction, tiled exports, histogram matching, coding best practices, courses | B |
| `Geospatial_Python` | geopandas, GDAL, GRASS GIS with Jupyter, lonboard, spopt, Geo-Python/AutoGIS courses, cloud-native formats | B |
| `Remote_Sensing` | satellite and airborne imagery, land-cover products, MODIS/Sentinel processing, albedo from imagery, cloud-based remote sensing courses | Z, B |
| `Drones_and_Photogrammetry` | WebODM/OpenDroneMap, Pix4D, Metashape, DroneDeploy, orthophoto and DSM generation with GCPs, solar-farm thermal inspection (Raptor Maps, Scopito), remote-pilot regulations, drone airspace maps | B |
| `Terrain_and_Lidar` | national height models and laser scanning, point clouds, DEM void filling, contours, aspect-slope, cut/fill volumes, catchment delineation, OpenTopography | B |
| `3D_Geovisualization` | Blender GIS and landscape/energy renders, Cesium and 3D Tiles, Qgis2threejs, Unreal Engine, solar-park visualisation for stakeholders | B |
| `Cartography_and_Map_Design` | terrain cartography, colour schemes (ColorBrewer), atlas layouts, interactive and animated maps, publication-quality charts and maps | Z, B |

## Domain: Data sources — MOC `Data_Sources`

Rule: a bookmark that *is* a portal, API or dataset files here first, with a link to the thematic page that uses it. One bullet per source with access notes (login, API key, licence, CRS, update frequency).

| Page | Scope | Seeded from |
|---|---|---|
| `Geodata_Portals_Nordic` | Sweden: Lantmäteriet (Min karta, Geotorget, ortofoto, laser data), Skogsstyrelsen geodata feeds and Skogens kartor, Länsstyrelsen WebGIS, Trafikverket NVDB, Boverket, Riksantikvarieämbetet Fornsök, SLU soil maps; Norway: Norgeskart, Høydedata, NVE atlas, Kulturminnesøk; Finland: Maanmittauslaitos, Paikkatietoikkuna; EPSG.io | B |
| `Solar_and_Weather_Data` | SMHI open data (observations, STRÅNG, skyfall/IDF statistics), FMI observations, NASA POWER, PVGIS API, Solcast, Copernicus ERA explorer and albedo products, MODIS, module databases (SAM CEC, PV Free) | Z, B |
| `Energy_Market_and_Grid_Data` | Nord Pool API, ENTSO-E Transparency, Svenska kraftnät and Fingrid data/APIs, Energy-Charts, electricityMap, NREL Cambium | B |
| `Global_Datasets_and_Catalogs` | Earth Engine community catalog, global land-cover and building datasets, Global Energy Monitor, Wiki-Solar, PVMAPS, Natural Earth, OpenTopography | B |
| `Forestry_and_Agriculture_Statistics` | seedling production statistics (SE/FI/NO), Skogsstyrelsen statistics, nursery directories, State of Europe's Forests | Z |

## Domain: Tools and methods — MOC `Tools_and_Methods`

| Page | Scope | Seeded from |
|---|---|---|
| `Python` | general Python, pandas, xarray, Colab, Python Data Science Handbook | O, B |
| `R` | ggplot2, dplyr, sf, nlme, emmeans, metR, general R notes | Z |
| `PV_Modelling_Tools` | pvlib (docs, tutorials, snow, storage, PVCollada), PySAM/SAM and Energy Transition Academy material, PVsyst, Meteonorm, PVGIS tooling, PVRADAR, openpvtools, AssessingSolar, hydesign; method papers go to the thematic page | Z, B |
| `Statistics_and_Data_Analysis` | mixed-effects models, estimated marginal means, regression, experimental design, time series (ARIMA/SARIMAX, MSTL), Monte Carlo and Bayesian methods (PyMC), model evaluation (Taylor diagrams) | Z, B |
| `Optimization_and_Decision_Making` | linear programming in Python, spatial optimisation (spopt), equal-size clustering, capacity-constrained point distributions, decision-making under uncertainty, optimisation textbooks | Z, B |
| `Data_Visualization` | chart types (waterfall), plotly/DataPlotly, publication-quality figures, dashboards (Streamlit, Power BI) | B |
| `Reporting_and_Publishing` | WeasyPrint/Jinja2 PDF reports, PyLaTeX, Jupyter Book, Overleaf, Diagrams.net, ZoteroBib, PyCafe | B |
| `CAD_and_Drafting` | AutoCAD and AutoCAD Map 3D, viewports and annotative objects, customisation, AEC workflows with Python and QGIS | B |
| `Machine_Learning`, `Deep_Learning`, `Embeddings` | from the original list; `Deep_Learning` and `Embeddings` link up to `Machine_Learning` | O |
| `SQL`, `Data` | from the original list (`Data` = data engineering, formats, pipelines) | O |
| `Agentic_Coding` | Claude Code, agent workflows, prompting, LLM-maintained wikis | O, B |
| `Knowledge_Management` | Obsidian, Zotero, this vault's own conventions | O |

## Domain: Themes — MOC `Themes`

| Page | Scope | Seeded from |
|---|---|---|
| `Climate_Change` | impacts on forests, crops and energy systems; vegetation-period length; climate projections and extreme-rain statistics used in design | Z, B |
| `Urban_Planning` | urban solar potential, urban microclimate (UMEP), building density, GIS in urban and regional planning | O, B |
| `Agriculture` | general agronomy that fits no specific page | O |

## Other topics — MOC `Other_Topics`

| Page | Scope | Seeded from |
|---|---|---|
| `Unsorted` | notes with no fitting page anywhere; every bullet carries `#needs-topic` and sits under a `## Candidate: <Name>` subheading | — |

---

## Candidate topics (below the 5-note threshold)

Already visible in the sources; promote when they reach 5 notes, per `CLAUDE.md`.

- Hybrid plants and power-to-X (hydesign) — under `Energy_Transition_and_Scenarios`
- pvlib as its own page — under `PV_Modelling_Tools`, if pvlib notes pass ~15
- Off-grid and DIY solar (camper/van wiring) — under `Energy_Storage`
- Hobby projects (Raspberry Pi grow monitoring, fitness, tea) — under `Unsorted`
- Courses to take (Spatial Thoughts, DTU programmes) — handled by `#type/course` + `#status/todo`, not a page, unless the owner wants a learning-plan page

Expected pressure points after the Zotero import (likely to pass ~80 bullets and need a split proposal): `Horticultural_Lighting`, `PV_System_Performance`, `Solar_Radiation_Modelling`, `Forest_Seedling_Production`, `Photosynthesis_and_Plant_Physiology`. Natural split lines are already visible in their scope descriptions (e.g. lighting hardware/efficacy vs lighting strategies; soiling/optical losses as its own page).

## Tag vocabulary (conventions in `CLAUDE.md`; values here)

- `#region/`: sweden, nordic, norway, finland, mexico, netherlands, europe, global
- `#species/`: picea-abies, pinus-sylvestris, (add as met)
- `#crop/`: lettuce, tomato, cucumber, basil, ornamentals, (add as met)
- `#type/` (mainly bookmarks): tool, course, tutorial, dataset, portal, api, regulation, reference, video
- `#status/`: unread, read, todo
- `#project/`: light-model, msc-thesis (+ `/4-1`, `/4-2`, `/4-13`, `/4-14`), thesis, own-publications, zephyr, course-reading, `<site-slug>` for solar-park site folders
- `#needs-review`, `#needs-topic`, `#removed-from-zotero`
- Frontmatter `tags:` on every page carries its domain as `domain/<slug>`: photovoltaics, solar-park-development, agrivoltaics, energy-systems, plant-photobiology, controlled-environment-agriculture, forestry, geospatial, data-sources, tools-and-methods, themes, other-topics. MOC pages add `moc`.

## Source mappings

### Zotero transport

The library is exported as Better BibTeX JSON (`raw/Zotero_library.json`), not CSV: the JSON carries the 87-collection tree and child notes, and 1300 of 1408 items sit in at least one collection. Collection path is therefore the primary classification signal; only the 13 mixed collections listed below and the 108 uncollected items fall through to keyword rules. The CSV export is superseded and archived in `processed/`.

### Zotero collections → pages

The full mapping lives in `scripts/classify_zotero.py` (`COLLECTION_RULES`). Shape of it:

| Zotero collection | Primary page |
|---|---|
| `1 Ligh Spectra and Light Intensity`, `Light spectra and field trial`, `R:FR`, `Spectra`, `UV`, `Photomorphogenesis` | `Light_Quality_and_Photomorphogenesis` |
| `Light Intensity and gas exchange`, `G.Ex - Light response curves`, `1.1.1 Photosynthesis`, `1.1.2 Gas Ex. and Ch. F.` | `Photosynthesis_and_Plant_Physiology` |
| `2 Long night treatment` | `Seedling_Cold_Hardiness_and_Dormancy` |
| `3 Light shock` | `Photoinhibition_and_Light_Stress` (proposed) |
| `4 DLI and supplementary light` + subfolders, `LED for Plants`, `DLI` | `Horticultural_Lighting` |
| `05 Greenhouse energy`, `2.1 Greenhouses and Growth chambers`, `Growth chambers` | `Greenhouse_Horticulture` |
| `5 Agrivoltacis`, `5.3.3 Agrivoltaics` | `Agrivoltaics` |
| `Energy calculation`, `4.1 Solar Radiation`, `5.0 TÜV Mustergutachten` | `Solar_Radiation_Modelling` |
| `Solar Greenhouse` | `PV_Greenhouses` |
| `6 Image and color analysis`, `Image analysis and Phenotyping`, `Photobox` | `Plant_Phenotyping_and_Image_Analysis` |
| `1.1 Seedling Performance`, `1.1.3 RGC`, `2.4 Zephyr Project` | `Forest_Seedling_Production` |
| `2 Forest regeneration` | `Forest_Regeneration` |
| `3 Somatic embryos` | `Tree_Breeding_and_Propagation` |
| `2.2 Vertical Farming` | `Vertical_Farming_and_Urban_Agriculture` |
| `5.2.1 PV cells and modules`, `5 - PV modules`, `5.3.2 mini-PV for indoors` | `PV_Cell_and_Module_Technologies` |
| `5.4 PV Performance and Monitoring`, `5.5 PV Losses` (+ angular, degradation, thermal), `5.1.1 PV-Mexico` | `PV_System_Performance` |
| `5.3.1 PV Standards` | `PV_Standards_and_Measurement` |
| `5.5.2 Shading losses`, `5.5.4 Low light` | `PV_Shading_and_Mismatch` |
| `5.5.6 Soiling and Snow`, `5.1.2 PV-Sweden` | `PV_in_Nordic_Climates` |
| `5.2.3 Bifacial`, `5.5.7 Albedo` | `Bifacial_PV_and_Albedo` |
| `5.2.2 Inverters and batteries`, `5.2.4 Cables`, `5.3 PV systems design` | `PV_Electrical_Design_and_Inverters` |
| `5.6 PV software` | `PV_Modelling_Tools` |
| `5.7 PV Repowering`, `5.11 LCA` | `PV_Economics_and_LCA` |
| `5.8 BOS materials` | `Site_Layout_and_Civil_Design` |
| `5.9 PV forescasting`, `5.10 PV ramp control` | `PV_Forecasting_and_Ramp_Control` (proposed) |
| `5.12 PV health risks`, `Reflection` | `Permitting_and_Environmental_Assessment` |
| `1.4 Wind energy in forest` | `Energy_Transition_and_Scenarios` |
| `7 Statistics` | `Statistics_and_Data_Analysis` |
| `2.3 Entoculture`, `Water and population`, `Medicinal plants` | `Unsorted` (candidates) |

Mixed collections, where keyword rules run first and the collection only supplies a fallback: `0 Articles`, `0 Thesis`, `6 Thesis`, `1 Forestry`, `2 Controlled Environment Agriculture`, `3 Photobiology`, `4 Energy`, `5 Photovoltaics`, `5.1 PV general data`, `5.2 PV components`, `06 Data`, `99 Other`, `Material and equipment used`, `Own publications`.

### Zotero manual tags → vault tags
- `main model`, `supporting info` → `#project/light-model` (+ `#supporting-info`)
- `Master Thesis`, `thesis`, `4 PV systems`, `4.1 PV Standards`, `4.2 PV Performance and Monitoring`, `4.13 PV-Mexico`, `4.14 PV-Sweden` → `#project/msc-thesis` (keep section numbers as `#project/msc-thesis/4-1` etc.)
- `Read for course` → `#project/course-reading`
- species/crop tags → `#species/…`, `#crop/…`; everything else → keywords

### Bookmark folders → pages (default primary page; individual links may deviate)
| Folder | Default page | Notes |
|---|---|---|
| `Helios/01 Legal` | `Permitting_and_Environmental_Assessment` | |
| `Helios/02 Drone` | `Drones_and_Photogrammetry` | QGIS API link → `PyQGIS_and_GIS_Automation` |
| `Helios/08 Safety design` | `Site_Layout_and_Civil_Design` | glare → `Permitting_and_Environmental_Assessment` |
| `Helios/09 Norways HMS`, `Helios/10 Finland Helios` | `Geodata_Portals_Nordic` | grid-connection and weather links → `Energy_Market_and_Grid_Data` / `Solar_and_Weather_Data` |
| `Helios` (root) | `Geodata_Portals_Nordic` / `Solar_and_Weather_Data` / `Energy_Market_and_Grid_Data` | reliability scorecard → `PV_System_Performance`; LCA viewer → `PV_Economics_and_LCA`; Cesium → `3D_Geovisualization` |
| `PVmodelling` | `PV_Modelling_Tools` | data APIs → `Solar_and_Weather_Data`; albedo products → `Bifacial_PV_and_Albedo`; PyMC/Monte Carlo → `Statistics_and_Data_Analysis`; `r.sun` → `Solar_Radiation_Modelling` |
| `PVmodelling/AutoCAD` | `CAD_and_Drafting` | |
| `PVmodelling/Blender` | `3D_Geovisualization` | QGIS/terrain items → `QGIS` / `Terrain_and_Lidar`; snow-loss items → `PV_in_Nordic_Climates` |
| `PVmodelling/Grass` | `Geospatial_Python` | PyQGIS-in-Jupyter → `PyQGIS_and_GIS_Automation`; PV notebooks → `PV_Modelling_Tools` |
| `PVmodelling/Grid` | `Power_Systems_and_Grid_Integration` | |
| `QGIS`, `QGIS/Courses` | `QGIS` | automation → `PyQGIS_and_GIS_Automation`; terrain → `Terrain_and_Lidar`; data portals → `Geodata_Portals_Nordic`; equal-area/K-means → `Site_Layout_and_Civil_Design` |
| `QGIS/Laserdata` | `Terrain_and_Lidar` | portals → `Geodata_Portals_Nordic` |
| `GEE` | `Google_Earth_Engine` | |
| `python` | `Geospatial_Python` | pvlib → `PV_Modelling_Tools`; LaTeX/PyCafe → `Reporting_and_Publishing` |
| `Bookmarks bar` (loose links) | classify by title | roughly half are QGIS/geospatial; the rest energy markets, SAM, optimisation, reporting |

### Skip list (never ingested)
- Folders `Helios/00 Admin` and `Helios/11 CMA -TCMA/*` (accounting, time reporting, SharePoint workspaces, NAS, monitoring-portal logins). If a non-admin link appears in a site folder, tag it `#project/<site-slug>`.
- Login and account pages: Gmail, Drive, Dropbox, Box, WhatsApp, Google Translate, Autodesk account, Power BI app, QFieldCloud sign-in, QGIS Cloud project, Streamlit/Twitch profile pages, Overleaf home, SharePoint and Synology links, Google Maps pins, spreadsheet links.
- Duplicates within the export (same URL after ignoring `www`, trailing slash, `index.html`, and tracking parameters): keep one. If the copies sit in different folders, the surviving note links to the default page of *every* folder it appeared in, since being saved from two contexts means it serves both.

## Changelog
- 2026-08-25 — Seeded from Zotero export (`My_Library.csv`) and bookmarks export (`bookmarks_8_25_26.html`). 12 domains (incl. Other_Topics), 66 topic pages.
- 2026-08-25 — Zotero transport switched to Better BibTeX JSON; added the *Zotero transport* and *Zotero collections → pages* sections. Created the 12 MOC pages and `Unsorted`. Migrated the 10 pre-taxonomy pages to the new format; renamed `Energy_Markets` → `Electricity_Markets_and_Prices` (old name kept as an alias). Added `domain/` frontmatter tags and the `#project/` values thesis, own-publications, zephyr. Four new pages proposed in `index.md` (`Photoinhibition_and_Light_Stress`, `Radiometry_and_Photometry`, `PV_Forecasting_and_Ramp_Control`, `Phenology_and_Thermal_Time`), plus six split proposals — none created yet.
