---
tags: [domain/themes]
aliases: [agronomy, agricultural mapping]
updated: 2026-08-25
---
# Agriculture

**Summary**: General agronomy and agricultural mapping that fits no more specific page — field boundary delineation, crop-related Earth observation, and cropping practice.
**Parent**: [[Themes]] · **Related**: [[Remote_Sensing]], [[Machine_Learning]], [[Deep_Learning]]

---

## Notes

- [agribound](https://github.com/montimaj/agribound) — Python package for delineating agricultural field boundaries, by Sayak Majumdar (Desert Research Institute). Combines seven methods — YOLO-based Delineate-Anything detection, Fields of The World semantic segmentation, DINOv3 segmentation, Prithvi-EO-2.0 inference, unsupervised embedding clustering, supervised fine-tuning, and multi-engine ensembling — pulling from 10 sources (Sentinel-2, Landsat, HLS, NAIP, SPOT 6/7, Google Satellite Embeddings, TESSERA) through Earth Engine, refining with SAM2 and writing fiboa-compliant GeoPackage/GeoJSON/GeoParquet. Python 3.10+, Apache 2.0, manuscript in preparation for *Remote Sensing of Environment* (DOI 10.5281/zenodo.19229665). Keywords: field boundaries, crop mapping, segmentation, Google Earth Engine, fiboa. Related: [[Deep_Learning]], [[Embeddings]], [[Python]], [[Remote_Sensing]] #type/tool
