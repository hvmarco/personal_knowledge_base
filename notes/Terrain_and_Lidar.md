---
tags: [domain/geospatial]
aliases: [DEM, DTM, lidar, point clouds, contours, aspect-slope, cut and fill]
updated: 2026-08-25
---
# Terrain and Lidar

**Summary**: Working with elevation — point clouds and height models, contours, slope and aspect, void filling, catchment delineation and cut/fill volumes.
**Parent**: [[Geospatial]] · **Related**: [[QGIS]], [[Geodata_Portals_Nordic]], [[Site_Layout_and_Civil_Design]]

---

## Notes

- [Interpolating voids in a DEM for catchment delineation in QGIS](https://www.youtube.com/watch?v=FwJSBoTn1y4) — Hans van der Kwast on filling sinks and holes so a flow-routing run produces a catchment instead of a puddle. Keywords: void filling, sink fill, catchment delineation, hydrology. Related: [[Site_Layout_and_Civil_Design]] #type/video
- [How to calculate surface and cut volume in QGIS](https://www.pointsnorthgis.ca/blog/how-to-calculate-surfacecut-volume-qgis-advanced/) — cut and fill between two surfaces, done properly with raster algebra and zonal statistics. The earthworks number for a site layout. Keywords: cut and fill, volume, raster algebra, zonal statistics. Related: [[Site_Layout_and_Civil_Design]] #type/tutorial
- [QGIS User 0027 — styling contour lines](https://www.youtube.com/watch?v=-xzoVF7Z7u0) — index contours, labels and the rule-based styling that makes a contour map readable. Keywords: contours, labelling, rule-based styling. Related: [[Cartography_and_Map_Design]] #type/video
- [Styling contours in 3D (QGIS3)](https://www.qgistutorials.com/en/docs/3/contour_3d_styling.html) — draping contours over the terrain in the 3D view. Keywords: contours, 3D view, draping, QGIS. Related: [[3D_Geovisualization]] #type/tutorial
- [Aspect-slope maps in QGIS](https://kingsgeocomputation.org/2016/03/16/aspect-slope-maps-in-qgis/) — the bivariate aspect-and-slope symbology built in QGIS: one map showing both which way the ground faces and how steeply. Directly useful for PV siting. Keywords: aspect-slope, bivariate symbology, terrain analysis. Related: [[Solar_Radiation_Modelling]] #type/tutorial
- [New aspect-slope raster function — ArcGIS blog](https://www.esri.com/arcgis-blog/products/arcgis-pro/imagery/new-aspect-slope-raster-function-now-available/) — the Esri version of the same idea, with the colour scheme it standardised. Keywords: aspect-slope, raster function, colour scheme. Related: [[Cartography_and_Map_Design]] #type/reference
- [How to create contour lines in QGIS](https://www.geodose.com/2018/05/how-to-create-contour-lines-in-qgis.html) — contour generation from a DEM, interval choice and smoothing. Keywords: contours, DEM, interval, smoothing. Related: [[QGIS]] #type/tutorial
- [Viewing point clouds in QGIS](https://www.pointsnorthgis.ca/blog/viewing-point-clouds-qgis/) — loading LAZ directly, classification-based styling and the 2D/3D views. Keywords: point cloud, LAZ, classification, QGIS 3D. Related: [[Drones_and_Photogrammetry]] #type/tutorial
