# Agriculture


**Summary**: Notes on agricultural mapping and analysis, including field boundary delineation and crop-related Earth observation tooling.
**Last updated**: 2026-08-24

---

## Notes

- [agribound](https://github.com/montimaj/agribound): Python package for delineating field boundaries. An agricultural field boundary delineation toolkit by Sayak Majumdar (montimaj, Desert Research Institute) that combines seven methods — YOLO-based Delineate-Anything object detection, Fields of The World semantic segmentation, DINOv3 vision transformer segmentation, Prithvi-EO-2.0 foundation model inference, unsupervised embedding clustering, supervised fine-tuning, and multi-engine ensembling. Pulls from 10 sources including Sentinel-2, Landsat, HLS, NAIP, SPOT 6/7, and pre-computed embeddings (Google Satellite Embeddings, TESSERA) via Google Earth Engine, refines boundaries with SAM2, and writes fiboa-compliant GeoPackage/GeoJSON/GeoParquet. Python 3.10+, Apache 2.0, manuscript in preparation for *Remote Sensing of Environment* (DOI 10.5281/zenodo.19229665). `field-boundaries` `crop-mapping` `segmentation` `google-earth-engine` `python-package` `fiboa`

## Related pages

- [[Remote_Sensing]] — the satellite imagery these tools run on.
- [[Deep_Learning]] — YOLO, DINOv3, SAM2, and Prithvi-EO-2.0.
- [[Embeddings]] — Google Satellite Embeddings and TESSERA as inputs.
- [[Python]] — packaging and API/CLI tooling.
