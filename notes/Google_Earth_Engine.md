---
tags: [domain/geospatial]
aliases: [GEE, Earth Engine, geemap, earthengine-api]
updated: 2026-08-25
---
# Google Earth Engine

**Summary**: Earth Engine as a working tool — the JavaScript and Python APIs, the QGIS plugin, time-series extraction, tiled exports and the coding practices that keep a script from timing out.
**Parent**: [[Geospatial]] · **Related**: [[Remote_Sensing]], [[Geospatial_Python]], [[Global_Datasets_and_Catalogs]]

---

## Notes

- [Google Earth Engine plugin for QGIS](https://gee-community.github.io/qgis-earthengine-plugin/) — the community plugin that exposes the Earth Engine API inside QGIS, so an EE layer can be styled and combined with local data. Keywords: QGIS plugin, Earth Engine, community, layers. Related: [[QGIS]] #type/tool
- [From cloud to desktop: working with Earth Engine data in QGIS (workshop, Dec 2025)](https://spatialthoughts.com/training/qgis_gee_workshop_20251217/) — the workshop on moving between Earth Engine and the desktop: export strategies, the plugin, and when to leave the data in the cloud. Keywords: Earth Engine, QGIS, export, workshop. Related: [[QGIS]] #type/course #status/todo
- [GEE courses (geemap)](https://courses.geemap.org/) — Qiusheng Wu's Earth Engine course material built around geemap, the Python package that puts EE in a notebook with an interactive map. Keywords: geemap, Python API, notebooks, course. Related: [[Geospatial_Python]] #type/course
- [csaybar/EEwPython](https://github.com/csaybar/EEwPython) — a notebook series teaching Earth Engine through the Python API, from first image to classification. Keywords: EEwPython, Python API, notebooks, classification. Related: [[Geospatial_Python]] #type/tool
- [Creating maps with Google Earth Engine and PyQGIS](https://spatialthoughts.com/2020/04/04/ndvi-time-series-gee-qgis/) — an NDVI time series computed in Earth Engine and rendered as a map series in QGIS through PyQGIS. Keywords: NDVI time series, PyQGIS, map series, automation. Related: [[PyQGIS_and_GIS_Automation]] #type/tutorial
- [End-to-End Google Earth Engine (full course)](https://courses.spatialthoughts.com/end-to-end-gee.html) — the complete course: image collections, reducers, charts, classification and exports, with the JavaScript idioms that matter. The best single Earth Engine resource here. Keywords: image collections, reducers, classification, exports. Related: [[Remote_Sensing]] #type/course
- [Histogram matching in Google Earth Engine](https://spatialthoughts.com/2020/07/14/histogram-matching-gee/) — matching one image's histogram to another's, for mosaics that do not show their seams. Keywords: histogram matching, mosaic, radiometric consistency. Related: [[Remote_Sensing]] #type/tutorial
- [Extracting time series using Google Earth Engine](https://spatialthoughts.com/2020/04/13/extracting-time-series-ee/) — pulling a per-point or per-polygon time series out of an image collection and getting it into a table. The most-used Earth Engine operation in practice. Keywords: time series, reduceRegion, export table, image collection. Related: [[Statistics_and_Data_Analysis]] #type/tutorial
- [Tiling large exports in Google Earth Engine](https://spatialthoughts.com/2024/10/23/large-image-exports-gee/) — splitting an export into tiles so it completes instead of failing at the request limit. Keywords: export, tiling, limits, large rasters. Related: [[Remote_Sensing]] #type/tutorial
- [Coding best practices — Google Earth Engine](https://developers.google.com/earth-engine/guides/best_practices#if_you_dont_need_to_clip_dont_use_clip) — the official performance guidance: avoid `clip`, avoid client-side loops, use `updateMask`. Reading it once removes most timeouts. Keywords: best practices, performance, clip, client versus server. Related: [[Geospatial_Python]] #type/reference
- [Install the Google Earth Engine Python API](https://courses.spatialthoughts.com/install-gee-python-api.html) — the authentication and install steps for the Python API, including the service-account path. Keywords: Python API, authentication, install, service account. Related: [[Geospatial_Python]] #type/tutorial
- [Cloud-Based Remote Sensing with Google Earth Engine (EEFA book)](https://www.eefabook.org/) — the open textbook: forty-plus chapters from fundamentals to applications, each with runnable scripts. Keywords: EEFA, textbook, applications, open access. Related: [[Remote_Sensing]] #type/course
- [Functional programming concepts — Google Earth Engine](https://developers.google.com/earth-engine/tutorials/tutorial_js_03) — why Earth Engine wants `map` and `reduce` instead of loops, and how to think in collections. Keywords: functional programming, map, reduce, collections. Related: [[Geospatial_Python]] #type/tutorial
- [Creating publication quality charts with GEE (full course)](https://courses.spatialthoughts.com/gee-charts.html) — the charting API worked through properly: time series, box plots with outliers, and charts at multiple locations. Keywords: charts, ui.Chart, time series, publication quality. Related: [[Data_Visualization]] #type/course
- [Earth Engine code editor](https://code.earthengine.google.com/) — the JavaScript IDE itself: script repository, asset manager, task queue and the inspector. Keywords: code editor, assets, tasks, inspector. Related: [[Remote_Sensing]] #type/tool
- [End-to-End Google Earth Engine, January 2025](https://spatialthoughts.com/training/end_to_end_gee_20250120/) — the delivered session page for the course, with schedule and script links. Keywords: training session, Earth Engine, schedule. Related: [[Remote_Sensing]] #type/course
