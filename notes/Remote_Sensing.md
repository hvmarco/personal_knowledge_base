---
tags: [domain/geospatial]
aliases: [earth observation, satellite imagery]
updated: 2026-08-25
---
# Remote Sensing

**Summary**: Satellite and airborne imagery and the products built on it — land-cover, MODIS/Sentinel processing, albedo retrieval, and the embeddings, formats and tooling that ride on top.
**Parent**: [[Geospatial]] · **Related**: [[Embeddings]], [[Google_Earth_Engine]], [[Data]]

---

## Notes

- [The Technical Debt of Earth Embedding Products](https://cloudnativegeo.org/blog/2026/02/the-technical-debt-of-earth-embedding-products/) — Isaac Corley (Wherobots, 2026-02-28) argues that geospatial foundation model teams solve the hard part, processing petabytes of imagery, but ship incompatible formats, tile schemes and distribution methods that push integration cost onto downstream users. Compares Clay, Major TOM, Earth Index, Copernicus-Embed, Presto, Tessera and AlphaEarth, argues for GeoParquet/COG/Zarr as standards, notes int8 quantization cuts storage 4× with negligible performance loss, and flags that pixel-level 10 m embeddings for Africa alone need 38–77 TB. Keywords: earth embeddings, geospatial foundation models, cloud-native formats, interoperability, storage cost. Related: [[Embeddings]], [[Data]], [[Machine_Learning]] #type/reference
