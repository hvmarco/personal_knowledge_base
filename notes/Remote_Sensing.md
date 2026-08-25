# Remote Sensing


**Summary**: Notes on Earth observation imagery, satellite data products, and the geospatial embeddings, formats, and tooling built on top of them.
**Last updated**: 2026-08-24

---

## Notes

- [The Technical Debt of Earth Embedding Products](https://cloudnativegeo.org/blog/2026/02/the-technical-debt-of-earth-embedding-products/): Article comparing different earth embeddings. Isaac Corley (Wherobots, 2026-02-28) argues that geospatial foundation model teams solve the hard part — processing petabytes of imagery — but each product ships incompatible formats, tile schemes, and distribution methods, pushing the integration cost onto downstream users. Compares Clay, Major TOM, Earth Index, Copernicus-Embed, Presto, Tessera, and AlphaEarth; argues for cloud-native formats (GeoParquet, COG, Zarr) as standards, notes int8 quantization cuts storage 4x with negligible performance loss, and flags that pixel-level 10m embeddings for Africa alone need 38–77 TB. `earth-embeddings` `geospatial-foundation-models` `cloud-native-formats` `interoperability` `storage-cost` `technical-debt`

## Related pages

- [[Embeddings]] — the embedding products this page's notes compare.
- [[Data]] — storage formats and distribution (GeoParquet, COG, Zarr).
- [[Machine_Learning]] — foundation models that produce these embeddings.
- [[Agriculture]] — field boundary delineation from satellite imagery.
- [[Urban_Planning]] — a critique of using satellite land surface temperature as a heat-hazard proxy.
