---
tags: [domain/geospatial]
aliases: [PyQGIS, QGIS automation, qgis_process, QGIS actions, plugins]
updated: 2026-08-25
---
# PyQGIS and GIS Automation

**Summary**: Driving QGIS from code — the PyQGIS API, processing algorithms from Python, `qgis_process` on the command line, QGIS actions, plugins, and getting a QGIS Python environment to exist in the first place.
**Parent**: [[Geospatial]] · **Related**: [[QGIS]], [[Geospatial_Python]], [[Python]]

---

## Notes

- [Automating GIS Workflows with QGIS (full workshop)](https://courses.spatialthoughts.com/automating-gis-workflows.html) — the graphical modeller, batch processing and the model-to-script step, before any code is written. Where automation should start. Keywords: model designer, batch processing, workflow automation. Related: [[QGIS]] #type/course
- [PyQGIS in a Jupyter notebook](https://lerryws.xyz/python/qgis/2019/08/01/PyQGIS-in-Jupyter-Notebook.html) — how to get the QGIS Python bindings importable inside Jupyter, environment variables and all. Keywords: PyQGIS, Jupyter, environment setup, bindings. Related: [[Geospatial_Python]] #type/tutorial
- [PyQGIS Masterclass — customizing QGIS with Python (full course)](https://courses.spatialthoughts.com/pyqgis-masterclass.html) — the standalone-script, plugin and processing-provider paths, with the QGIS object model explained rather than assumed. Keywords: PyQGIS, plugins, processing provider, object model. Related: [[QGIS]] #type/course
- [Setup QGIS in Google Colab](https://lerryws.xyz/python/qgis/2020/06/12/qgis-in-google-colab.html) — installing QGIS in a Colab runtime so a notebook can call processing algorithms without a local install. Keywords: Colab, QGIS install, headless, notebook. Related: [[Geospatial_Python]] #type/tutorial
- [Running processing algorithms via Python (QGIS3)](https://www.qgistutorials.com/en/docs/3/processing_algorithms_pyqgis.html) — calling `processing.run()` properly: parameter dictionaries, temporary outputs and reading the algorithm help. Keywords: processing.run, algorithms, parameters, PyQGIS. Related: [[QGIS]] #type/tutorial
- [QGIS Automation using Actions (workshop material)](https://courses.spatialthoughts.com/qgis-actions.html) — layer actions that run Python or open a URL from the attribute table; the cheapest way to attach a workflow to a feature. Keywords: QGIS actions, attribute table, Python action, workflow. Related: [[QGIS]] #type/course
- [PyQGIS Developer Cookbook](https://docs.qgis.org/3.34/en/docs/pyqgis_developer_cookbook/index.html) — the official cookbook: the canonical reference for layers, geometry, symbology and the processing framework from Python. Keywords: cookbook, PyQGIS API, official documentation. Related: [[QGIS]] #type/reference
- [Using QGIS from Conda](https://gisunchained.wordpress.com/2019/05/29/using-qgis-from-conda/) — installing QGIS through conda so its Python environment is one you control rather than one the installer chose. Keywords: conda, environment, QGIS install, dependencies. Related: [[Python]] #type/tutorial
- [PIP dependencies for Python plugins (QGIS enhancement proposal 202)](https://github.com/qgis/QGIS-Enhancement-Proposals/issues/202) — the long-running discussion of how a plugin should declare third-party Python dependencies, and why there is still no good answer. Keywords: plugin dependencies, pip, QEP, packaging. Related: [[Python]] #type/reference
- [Run PyQGIS in a Jupyter notebook (gist)](https://gist.github.com/ThomasG77/223064813d8aefda5b3cdb05c2588fa1) — a short working recipe for the same problem, in gist form. Keywords: PyQGIS, Jupyter, gist, setup. Related: [[Geospatial_Python]] #type/tool
- [Running QGIS processing tools on the command line with qgis_process](https://spatialthoughts.com/2022/07/30/qgis_process_command_line/) — `qgis_process` for scripted and scheduled runs, including model execution from a shell. The route to running a QGIS workflow on a server. Keywords: qgis_process, command line, headless, scheduling. Related: [[QGIS]] #type/tutorial
- [PyQGIS Masterclass, April 2024](https://spatialthoughts.com/pyqgis_masterclass_20240425/) — the session page for the delivered masterclass, with the exercise material. Keywords: masterclass, exercises, PyQGIS. Related: [[QGIS]] #type/course
- [FeatureGridCreator — grid_creator.py](https://github.com/rduivenvoorde/featuregridcreator/blob/master/FeatureGridCreator/grid_creator.py) — the plugin's source: how the grid geometries are built, worth reading before adapting it for a module-table layout. Keywords: grid creation, plugin source, geometry, PyQGIS. Related: [[Site_Layout_and_Civil_Design]] #type/tool
- [PyQGIS 101: introduction to QGIS Python programming for non-programmers](https://anitagraser.com/pyqgis-101-introduction-to-qgis-python-programming-for-non-programmers/) — Anita Graser's course for people who know QGIS but not Python, built around small exercises. Keywords: PyQGIS 101, beginners, exercises, Python. Related: [[Python]] #type/course
- [QGIS Plugins planet](https://plugins.qgis.org/planet/user/21/) — the plugin repository feed: what has been published and updated recently. Keywords: plugin repository, updates, QGIS plugins. Related: [[QGIS]] #type/portal
- [FeatureGridCreator plugin documentation](https://rduivenvoorde.github.io/featuregridcreator/FeatureGridCreator/help/html/en/) — the plugin that generates regular feature grids over an area: the fastest way to lay out module tables or sample points on a site. Keywords: feature grid, plugin, layout, sampling. Related: [[Site_Layout_and_Civil_Design]] #type/tool
- [QGIS Python API documentation](https://qgis.org/pyqgis/master/index.html) — the generated API reference for the QGIS classes; the place to check a signature. Keywords: API reference, PyQGIS, classes, signatures. Related: [[QGIS]] #type/reference
- [QGIS Python programming tutorial — PyQGIS](https://www.geodose.com/p/pyqgis.html) — a tutorial series covering scripting from the Python console upwards. Keywords: PyQGIS tutorial, console, scripting. Related: [[Python]] #type/tutorial
