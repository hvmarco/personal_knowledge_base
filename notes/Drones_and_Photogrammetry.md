---
tags: [domain/geospatial]
aliases: [drones, UAV, photogrammetry, WebODM, OpenDroneMap, orthophoto, thermal inspection]
updated: 2026-08-25
---
# Drones and Photogrammetry

**Summary**: Flying a site and turning the images into data — OpenDroneMap and the commercial photogrammetry packages, orthophoto and DSM generation, thermal inspection of PV plants, and the airspace rules that decide where a flight is legal.
**Parent**: [[Geospatial]] · **Related**: [[Terrain_and_Lidar]], [[Remote_Sensing]], [[PV_System_Performance]]

---

## Notes

- [How to inspect a solar farm with a drone — DJI Matrice](https://www.youtube.com/watch?v=AVwUHnZplVI) — a practical inspection flight: flight lines, thermal payload settings and what a defective string looks like from the air. Keywords: thermal inspection, solar farm, DJI Matrice, flight planning. Related: [[PV_Degradation_and_Reliability]] #type/video
- [The best drone solar inspection software for 2023](https://thedronelifenj.com/drone-solar-inspection-software/) — a comparison of the inspection platforms, with what each charges for and what it actually automates. Keywords: inspection software, comparison, thermal analytics, pricing. Related: [[PV_System_Performance]] #type/reference
- [Scopito — solar PV inspection software](http://scopito.com/solar-pv-inspection-software/#pricing) — inspection platform with anomaly detection and reporting; bookmarked at the pricing section. Keywords: Scopito, anomaly detection, inspection reports, pricing. Related: [[PV_Degradation_and_Reliability]] #type/tool
- [Raptor Solar — Raptor Maps](https://raptormaps.com/raptor-solar-software/) — the incumbent in utility-scale thermal inspection analytics: fleet-level anomaly classification tied to as-built layouts. Keywords: Raptor Maps, thermal analytics, utility scale, anomalies. Related: [[PV_System_Performance]] #type/tool
- [LFV GeoServer — layer preview](http://daim.lfv.se/geoserver/web/wicket/bookmarkable/org.geoserver.web.demo.MapPreviewPage?0) — the layer preview behind the Swedish drone chart: the airspace layers as WMS/WFS, usable directly in QGIS. Keywords: LFV, airspace layers, WMS, GeoServer. Related: [[Geodata_Portals_Nordic]] #type/api #region/sweden
- [LFV Drönarkartan (RPAS, UAS, UAV)](https://daim.lfv.se/echarts/dronechart/) — the official Swedish drone map: restricted zones, control zones and the airspace conditions for each. The first check before any flight. Keywords: drone chart, airspace, restricted zones, Sweden. Related: [[Permitting_and_Environmental_Assessment]] #type/portal #region/sweden
- [Agisoft Metashape tutorial — orthophoto and DSM generation](https://www.youtube.com/watch?v=O--J8JrAB7M) — the full Metashape chain from images and GCPs to orthophoto and DSM, with the alignment settings that matter. Keywords: Metashape, orthophoto, DSM, ground control points. Related: [[Terrain_and_Lidar]] #type/video
- [PyODM documentation](https://pyodm.readthedocs.io/en/latest/) — the Python client for a NodeODM server: submit a task, poll it, fetch the results. How drone processing gets into a pipeline. Keywords: PyODM, NodeODM, API client, automation. Related: [[Python]] #type/tool
- [Utbildning för fjärrpiloter — Transportstyrelsen](https://transportstyrelsen.se/dronarkort-och-utbildning/) — the Swedish remote pilot certificate: which category needs which training, and where the exams sit. Keywords: remote pilot, A1/A3, drone licence, Transportstyrelsen. Related: [[Permitting_and_Environmental_Assessment]] #type/regulation #region/sweden
- [Topografía de drone en SketchUp](https://www.youtube.com/watch?v=TCMNeb1B9BQ) — bringing a drone-derived surface into SketchUp for terrain work. Keywords: drone survey, SketchUp, terrain model. Related: [[3D_Geovisualization]] #type/video
- [OpenDroneMap outputs](https://docs.opendronemap.org/outputs/) — what a processing run actually produces: orthophoto, DSM, DTM, point cloud, textured mesh, and the file each lands in. Keywords: ODM outputs, orthophoto, point cloud, DTM. Related: [[Terrain_and_Lidar]] #type/reference
- [WebODM pricing](https://webodm.net/pricing) — what the packaged WebODM costs against running the free stack yourself. Keywords: WebODM, pricing, licensing. Related: [[Drones_and_Photogrammetry]] #type/reference
- [Comparison: same dataset, WebODM versus Agisoft Metashape](https://community.opendronemap.org/t/comparison-same-dataset-webodm-vs-agisoft-metashape/5280) — the same flight through both packages, with the differences in point density, orthophoto quality and processing time. Keywords: WebODM, Metashape, comparison, quality. Related: [[Terrain_and_Lidar]] #type/reference
- [PIX4Dmapper](https://www.pix4d.com/product/pix4dmapper-photogrammetry-software) — the professional photogrammetry package: accuracy reporting and GCP handling are what the money buys. Keywords: Pix4D, photogrammetry, accuracy report, GCP. Related: [[Terrain_and_Lidar]] #type/tool
- [DroneDeploy for agriculture](https://www.dronedeploy.com/solutions/agriculture/) — the cloud-processing platform's agricultural offering: flight app, automatic processing and plant-health indices. Keywords: DroneDeploy, cloud processing, plant health, NDVI. Related: [[Agriculture]] #type/tool
- [Maps Made Easy — pricing](https://www.mapsmadeeasy.com/pricing) — pay-per-megapixel cloud photogrammetry; the cheap option for occasional processing. Keywords: cloud processing, pricing, photogrammetry service. Related: [[Drones_and_Photogrammetry]] #type/reference
- [OpenDroneMap/WebODM](https://github.com/OpenDroneMap/WebODM) — the open-source photogrammetry stack: web interface, task queue and plugin system over the ODM engine. The default when the data should not leave the office. Keywords: WebODM, open source, self-hosted, task queue. Related: [[Terrain_and_Lidar]] #type/tool
