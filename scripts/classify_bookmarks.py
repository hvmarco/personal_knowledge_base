#!/usr/bin/env python3
"""Classify the browser bookmarks into vault pages.

Content decides the page: the rule table below is matched against url + title
in order, and the first hit wins.  The bookmark folder is only a fallback for
links no rule recognises (FOLDER_DEFAULT), following the folder -> page table
in TAXONOMY.md.

Reads  processed/bookmarks_raw.csv   (from scripts/parse_bookmarks.py)
Writes processed/bookmarks_map.csv   one row per kept link
"""
import csv
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "processed" / "bookmarks_raw.csv"
OUT = ROOT / "processed" / "bookmarks_map.csv"

# --- links never ingested (CLAUDE.md skip list, TAXONOMY.md) ------------------
SKIP_FOLDERS = ("Bookmarks bar/Helios/00 Admin",
                "Bookmarks bar/Helios/11 CMA -TCMA")

SKIP_URL = [
    (r"mail\.google\.com", "email"),
    (r"drive\.google\.com", "cloud drive"),
    (r"translate\.google\.com", "translation service"),
    (r"web\.whatsapp\.com", "chat"),
    (r"dropbox\.com|box\.com/?$", "cloud drive"),
    (r"twitch\.tv", "personal profile"),
    (r"overleaf\.com/dash", "login page"),
    (r"app\.powerbi\.com", "login page"),
    (r"app\.qfield\.cloud/accounts", "login page"),
    (r"qgiscloud\.com/", "personal cloud project"),
    (r"sharepoint\.com", "workspace login"),
    (r"quickconnect\.to|finds\.synology\.com", "NAS login"),
    (r"localhost", "local address"),
    (r"accounts\.autodesk\.com", "login page"),
    (r"share\.streamlit\.io", "personal profile"),
    (r"webodm\.net/dashboard", "login page"),
    (r"geotorget\.lantmateriet\.se/bestallning/mitt-konto", "account page"),
]

# --- content rules: (pattern, page, type tag, related pages) ------------------
# Matched in order against "url title" lowercased; first hit wins.
RULES = [
    # --- permitting, environment, safety ---
    (r"forgesolar", "Permitting_and_Environmental_Assessment", "tool", ["Site_Layout_and_Civil_Design"]),
    (r"naturvardsverket\.se|e-tjanster\.lansstyrelsen\.se|solcellsparker",
     "Permitting_and_Environmental_Assessment", "regulation", ["Solar_Park_Development"]),
    (r"stormwater\.pca\.state\.mn\.us", "Permitting_and_Environmental_Assessment", "reference",
     ["Site_Layout_and_Civil_Design"]),
    # --- civil and layout ---
    (r"dlubal\.com|load-zones", "Site_Layout_and_Civil_Design", "reference", ["Permitting_and_Environmental_Assessment"]),
    (r"iso9223|iso 9223", "Site_Layout_and_Civil_Design", "reference", ["PV_Degradation_and_Reliability"]),
    (r"pvsyst\.com/help.*collada|collada-file-format", "Site_Layout_and_Civil_Design", "reference",
     ["PV_Modelling_Tools", "3D_Geovisualization"]),
    (r"equal.area|equal.sized|kmeans|k-means", "Site_Layout_and_Civil_Design", "tutorial", ["QGIS"]),
    # --- electrical ---
    (r"sma-sunny|sma\.de|multi-mppt|string inverter", "PV_Electrical_Design_and_Inverters", "reference",
     ["PV_System_Performance"]),
    (r"explorist\.life|solarwiringdiagrams", "Energy_Storage", "reference", ["PV_Electrical_Design_and_Inverters"]),
    # --- noise ---
    (r"noisemodelling|noisetools\.net|dbmap", "Noise_Modelling", "tool", ["Permitting_and_Environmental_Assessment"]),
    # --- drones ---
    (r"opendronemap|webodm|pyodm|pix4d|metashape|dronedeploy|mapsmadeeasy|thedronelifenj|scopito|raptormaps|"
     r"dronarkort|drone|dronechart|daim\.lfv\.se|fieldimager|sketchup",
     "Drones_and_Photogrammetry", "tool", ["Remote_Sensing"]),
    # --- 3D and Blender ---
    (r"agrar-photovoltaik|3d-models\.shop", "Agrivoltaics", "reference", ["3D_Geovisualization"]),
    (r"blender|cesium|qgis2threejs|unrealengine|modlearth|digital-landscapes|3d tiles|geospatial_studio",
     "3D_Geovisualization", "tutorial", ["QGIS"]),
    # --- terrain and lidar ---
    (r"aspect-slope|contour lines|cut.volume|surfacecut|catchment|point clouds|laserinnsyn|hoydedata|"
     r"laserskanning|opentopography\.org/?$",
     "Terrain_and_Lidar", "tutorial", ["QGIS"]),
    # --- earth engine ---
    (r"earthengine|earth-engine|geemap|eefabook|end-to-end-gee|gee-charts|histogram-matching|"
     r"extracting-time-series-ee|large-image-exports|eewpython|ndvi-time-series",
     "Google_Earth_Engine", "course", ["Remote_Sensing"]),
    (r"gee-community-catalog|awesome-gee", "Global_Datasets_and_Catalogs", "dataset", ["Google_Earth_Engine"]),
    (r"building-density-gee|glcfcs30d|land cover change dataset|open building",
     "Global_Datasets_and_Catalogs", "dataset", ["Google_Earth_Engine", "Remote_Sensing"]),
    (r"python-remote-sensing|cloud.based remote sensing|cloud native remote sensing",
     "Remote_Sensing", "course", ["Google_Earth_Engine", "Geospatial_Python"]),
    # --- albedo ---
    (r"albedo|mcd43|mod43|bifacial", "Bifacial_PV_and_Albedo", "dataset", ["Solar_and_Weather_Data"]),
    # --- PyQGIS and automation ---
    (r"pyqgis|qgis_process|qgis-actions|qgis_actions|processing_algorithms|automating-gis-workflows|"
     r"qgis in google colab|qgis-in-google-colab|qgis from conda|qgis-enhancement|plugin",
     "PyQGIS_and_GIS_Automation", "tutorial", ["QGIS", "Geospatial_Python"]),
    # --- data visualisation ---
    (r"dataplotly|waterfall chart|charts and diagrams|python-dataviz|pythondatavizchallenge|"
     r"data visualisations with graphs",
     "Data_Visualization", "tutorial", ["QGIS", "Python"]),
    (r"cartogis|terrain cartography|qgis-shadows|atlasgrid|colorbrewer",
     "Cartography_and_Map_Design", "tutorial", ["QGIS"]),
    # --- QGIS proper ---
    (r"qgistutorials|docs\.qgis\.org|qgis\.org|northrivergeographic|giscrack|featuregridcreator|"
     r"geosupportsystem|geodose\.com|qgis user|qgis expressions|geometry generator|value relation|"
     r"converting-tif-to-xyz|qgis-training|geo-trainings|spatialthoughts\.com/(?!training/python|2024/10/13)|"
     r"courses\.spatialthoughts\.com/(introduction-to-qgis|advanced-qgis|qgis-|gdal-tools)|"
     r"gisopencourseware|umep",
     "QGIS", "tutorial", ["PyQGIS_and_GIS_Automation"]),
    # --- geospatial python ---
    (r"geo-python|autogis|pythongis|geopythontutorials|geopandas|gdal\.org|mastering_gdal|grass|"
     r"lonboard|geog-312|geog-510|gispro\.gishub|gis programming|python-foundation|spatial data analysis",
     "Geospatial_Python", "course", ["Python", "QGIS"]),
    # --- optimisation ---
    (r"spopt|linear-programming|algorithmsbook|optimization|decision-making under uncertainty",
     "Optimization_and_Decision_Making", "course", ["Python"]),
    # --- statistics ---
    (r"pymc|monte-carlo|monte carlo|arima|sarimax|mstl|taylor diagram|time-series\b|time series",
     "Statistics_and_Data_Analysis", "tutorial", ["Python"]),
    # --- reporting ---
    (r"pylatex|weasyprint|jupyterbook|jupyter book|py\.cafe|pycafe|diagrams\.net|zbib\.org|zoterobib|invoice",
     "Reporting_and_Publishing", "tool", ["Python"]),
    # --- agentic coding / knowledge ---
    (r"llm-wiki|karpathy", "Agentic_Coding", "reference", ["Knowledge_Management"]),
    # --- CAD ---
    (r"autocad|autodesk|thecadgeek|aec-with-python|qgis-and-python-for-aec|autocad map",
     "CAD_and_Drafting", "course", ["QGIS"]),
    # --- PV modelling tools ---
    (r"rdtools|pvanalytics|pvcaptest|solar-data-tools|pvdeg|pvdegradationtools|pvel|scorecard\.pvel|"
     r"pv_bundt_cake",
     "PV_System_Performance", "tool", ["PV_Modelling_Tools"]),
    (r"pvlib.*snow|townsendsnowdustmodel|quantify-snow|snow loss", "PV_in_Nordic_Climates", "tool",
     ["PV_Modelling_Tools"]),
    (r"pvlib.*storage|battery", "Energy_Storage", "tool", ["PV_Modelling_Tools"]),
    (r"numpy-financial|incer-acv|modeling incentives", "PV_Economics_and_LCA", "tool", ["PV_Modelling_Tools"]),
    (r"cambium|merchant plant", "Electricity_Markets_and_Prices", "video", ["PV_Modelling_Tools"]),
    (r"pvlib|pv-tutorials|pvcollada|pysam|sam\.nrel\.gov|energytransitionacademy|openpvtools|pvradar|"
     r"assessingsolar|hydesign|pvsyst|open-source tools|oss webinar|pv-feasibility|pvpmc",
     "PV_Modelling_Tools", "tool", ["Python"]),
    # --- solar radiation ---
    (r"r\.sun|pcsrt|neteler\.org|earthsun|earthsorbit|transposition",
     "Solar_Radiation_Modelling", "tool", ["PV_Modelling_Tools"]),
    # --- weather and solar data ---
    (r"strang|smhi\.se|opendata\.smhi|skyfall|hypeweb|ilmatieteenlaitos|power\.larc\.nasa\.gov|"
     r"solcast|era-explorer|pvfree|cec.modules|pvgis|photovoltaic-geographical-information-system-pvgis/(?!.*pvmaps)",
     "Solar_and_Weather_Data", "api", ["Solar_Radiation_Modelling"]),
    # --- global datasets ---
    (r"pvmaps|wiki-solar|globalenergymonitor|naturalearthdata|opentopography",
     "Global_Datasets_and_Catalogs", "dataset", ["Remote_Sensing"]),
    # --- nordic geodata portals ---
    (r"lantmateriet|minkarta|geotorget|webgisportal|skogsstyrelsen|geodpags|lansstyrelsen|vbk\.lansstyrelsen|"
     r"nvdb|trafikverket|boverket|raa\.se|fornsok|gis-slu|geodata\.se|norgeskart|kulturminnesok|atlas\.nve\.no|"
     r"maanmittauslaitos|kapsi\.fi|paikkatietoikkuna|karttakuva|epsg\.io|gis\.lu\.se",
     "Geodata_Portals_Nordic", "portal", ["Geospatial"]),
    # --- energy markets and grid ---
    (r"transparency\.entsoe|nordpoolgroup|nordpoolspot", "Energy_Market_and_Grid_Data", "api",
     ["Electricity_Markets_and_Prices"]),
    (r"svk\.se|handel-prissattning", "Electricity_Markets_and_Prices", "regulation",
     ["Energy_Market_and_Grid_Data"]),
    (r"mimer\.svk|fingrid\.fi/en/grid|karttapalaute\.fingrid|pandapower|grid2op",
     "Power_Systems_and_Grid_Integration", "tool", ["Energy_Market_and_Grid_Data"]),
    (r"data\.fingrid\.fi", "Energy_Market_and_Grid_Data", "api", ["Power_Systems_and_Grid_Integration"]),
    (r"energy-charts|electricitymap|scenarioviewer|iea-pvps|dtu\.dk/english/education|kazempour",
     "Energy_Transition_and_Scenarios", "portal", ["Electricity_Markets_and_Prices"]),
    # --- buildings, urban ---
    (r"rooftop solar po|sp_technical_guide", "Building_Integrated_PV", "course", ["Urban_Planning"]),
    (r"urban and regional planning|gis-in-urban", "Urban_Planning", "tutorial", ["QGIS"]),
    # --- reliability ---
    (r"solarpowerworldonline|getting-reliability", "PV_Degradation_and_Reliability", "reference",
     ["PV_System_Performance"]),
    # --- agrivoltaics ---
    (r"agrivolta|agri-pv|one-axis, vertical, and elevated", "Agrivoltaics", "reference", ["PV_Economics_and_LCA"]),
    # --- python general ---
    (r"pythondatasciencehandbook|colab\.research\.google\.com|realpython", "Python", "tutorial",
     ["Statistics_and_Data_Analysis"]),
    # --- hobby ---
    (r"mate-tee|gmb\.io|initialstate", "Unsorted", "reference", []),
]

COMPILED = [(re.compile(p, re.I), page, tag, rel) for p, page, tag, rel in RULES]

FOLDER_DEFAULT = {
    "Bookmarks bar/Helios/01 Legal": "Permitting_and_Environmental_Assessment",
    "Bookmarks bar/Helios/02 Drone": "Drones_and_Photogrammetry",
    "Bookmarks bar/Helios/08 Safety design": "Site_Layout_and_Civil_Design",
    "Bookmarks bar/Helios/09 Norways HMS": "Geodata_Portals_Nordic",
    "Bookmarks bar/Helios/10 Finland Helios": "Geodata_Portals_Nordic",
    "Bookmarks bar/Helios": "Geodata_Portals_Nordic",
    "Bookmarks bar/PVmodelling": "PV_Modelling_Tools",
    "Bookmarks bar/PVmodelling/AutoCAD": "CAD_and_Drafting",
    "Bookmarks bar/PVmodelling/Blender": "3D_Geovisualization",
    "Bookmarks bar/PVmodelling/Grass": "Geospatial_Python",
    "Bookmarks bar/PVmodelling/Grid": "Power_Systems_and_Grid_Integration",
    "Bookmarks bar/QGIS": "QGIS",
    "Bookmarks bar/QGIS/Courses": "QGIS",
    "Bookmarks bar/QGIS/Laserdata": "Terrain_and_Lidar",
    "Bookmarks bar/GEE": "Google_Earth_Engine",
    "Bookmarks bar/python": "Geospatial_Python",
    "Bookmarks bar": "Unsorted",
}

# hand corrections, matched against the url after the rules have run (kept
# here so the map stays reproducible instead of drifting into the pages)
OVERRIDES = [
    (r"courses\.spatialthoughts\.com/python-foundation|training/python_foundation",
     "Geospatial_Python", "Python for spatial analysis course"),
    (r"gdal.tools|mastering_gdal", "Geospatial_Python", "GDAL course"),
    (r"python.dataviz|pythondatavizchallenge", "Data_Visualization", "data visualisation course"),
    (r"umep-docs", "Urban_Planning", "urban microclimate toolbox"),
    (r"end.to.end.gee|qgis_gee_workshop|install-gee-python-api",
     "Google_Earth_Engine", "Earth Engine course"),
    (r"gis-in-urban-and-regional-planning", "Urban_Planning", "GIS in planning"),
    (r"contour_3d_styling", "Terrain_and_Lidar", "contours from a DEM"),
    (r"featuregridcreator/blob", "PyQGIS_and_GIS_Automation", "plugin source"),
    (r"interactive_reveal_maps|interactive_canvas_maps",
     "Cartography_and_Map_Design", "interactive map output"),
    (r"anvanda-var-data-i-qgis", "QGIS", "using Lantmateriet data in QGIS"),
    (r"r\.sun", "Solar_Radiation_Modelling", "GRASS solar irradiance module"),
    (r"renewable-analytics\.netlify\.app", "Solar_Radiation_Modelling", "transposition worked example"),
    (r"hydesign", "Hybrid_Plants_and_P2X", "hybrid plant sizing"),
    (r"fieldimager", "Plant_Phenotyping_and_Image_Analysis", "field image phenotyping"),
    (r"pvmaps", "Global_Datasets_and_Catalogs", "JRC PVMAPS dataset"),
    (r"github\.com/spatialthoughts/python-tutorials", "Geospatial_Python", "python tutorial repo"),
    (r"hoydedata|webgisportal\.lantmateriet", "Geodata_Portals_Nordic", "national laser data portal"),
    (r"bibproxy\.du\.se|S0306261925005562", "Agrivoltaics", "economics of agrivoltaic layouts"),
    (r"iea-pvps\.org", "PV_in_Nordic_Climates", "dust and snow losses, Intersolar 2025"),
    (r"mate-tee|gmb\.io|initialstate", "Unsorted_hobby", "hobby project"),
]
COMPILED_OVERRIDES = [(re.compile(p, re.I), page, why) for p, page, why in OVERRIDES]

# the url as written in the vault: viewer state, session ids and saved extents
# are noise, and the note should point at the service, not at one map view
STRIP_AFTER = [
    "https://www.norgeskart.no/",
    "https://www.kulturminnesok.no/kart/",
    "https://www.geodata.se/geodataportalen/",
    "https://transparency.entsoe.eu/",
    "https://era-explorer.climate.copernicus.eu/",
    "https://www.wiki-solar.org/map/",
    "https://www.energy-charts.info/charts/price_spot_market/chart.htm",
    "https://www.smhi.se/data/meteorologi/ladda-ner-meteorologiska-observationer",
    "https://app.electricitymap.org/zone/ES",
    "https://www.dlubal.com/en/load-zones-for-snow-wind-earthquake/wind-bfs-201310-eks-9.html",
]


JUNK_PARAM = re.compile(r"^(utm_[a-z]+|ab_channel|feature|app|si|fbclid|gclid|tab|"
                        r"redirectedfrom[a-z]*|rmedium|rsource)$", re.I)
# browser text fragments and notebook scroll state say nothing about the resource
JUNK_FRAGMENT = re.compile(r"#(:~:text=|scrollTo=|mw-jump-to-license).*$", re.I)


def clean_url(url):
    """The url as written in the vault: a session id, a tracking parameter or a
    saved map extent is noise, and the note should point at the service rather
    than at one map view."""
    url = re.sub(r";jsessionid=[^?#]*", "", url)
    url = JUNK_FRAGMENT.sub("", url)
    for prefix in STRIP_AFTER:
        if url.startswith(prefix):
            return prefix

    vid = re.search(r"youtube\.com/watch\?(?:.*&)?v=([\w-]+)", url)
    if vid:
        return "https://www.youtube.com/watch?v=" + vid.group(1)
    lst = re.search(r"youtube\.com/playlist\?(?:.*&)?list=([\w-]+)", url)
    if lst:
        return "https://www.youtube.com/playlist?list=" + lst.group(1)

    if "?" in url:
        base, query = url.split("?", 1)
        query, _, frag = query.partition("#")
        kept = [p for p in query.split("&") if p and not JUNK_PARAM.match(p.split("=", 1)[0])]
        url = base + ("?" + "&".join(kept) if kept else "") + ("#" + frag if frag else "")
    return url.rstrip("#")



CANDIDATE_OF = {
    "Unsorted_hobby": ("Unsorted", "Hobby Projects"),
    "Hybrid_Plants_and_P2X": ("Energy_Transition_and_Scenarios", "Hybrid Plants and Power-to-X"),
}

# what a link *is*, decided by the host first and the rule's default last
TYPE_RULES = [
    (r"youtube\.com|youtu\.be|linkedin\.com/learning|vimeo", "video"),
    (r"courses?\.|/training/|\.edu/|coursera|30daysof|autogis|geo-python|geog-\d|pythongis|"
     r"energytransitionacademy|bookdown|algorithmsbook|eefabook|realpython", "course"),
    (r"github\.com|gitlab\.com|readthedocs|\.github\.io|gdal\.org|geopandas\.org|manpages|"
     r"pysal\.org|pvlib|pandapower|grid2op|noisemodelling|pymc\.io|statsmodels", "tool"),
    (r"tutorials?|/tips|how-to|stackexchange|medium\.com|towardsdatascience|hashnode|"
     r"blog|wiki", "tutorial"),
]


def classify(row):
    hay = (row["url"] + " " + row["title"]).lower()
    for rx, page, tag, rel in COMPILED:
        if rx.search(hay):
            return page, tag, rel, "content:" + rx.pattern[:34]
    folder = row["folder"]
    page = FOLDER_DEFAULT.get(folder)
    while page is None and "/" in folder:
        folder = folder.rsplit("/", 1)[0]
        page = FOLDER_DEFAULT.get(folder)
    return page or "Unsorted", "reference", [], "folder-default"


def type_tag(row, tag):
    """A portal, api, dataset or regulation is decided by the rule; anything
    else takes its type from what the host actually serves."""
    if tag in ("portal", "api", "dataset", "regulation"):
        return tag
    hay = (row["url"] + " " + row["title"]).lower()
    for rx, t in TYPE_RULES:
        if re.search(rx, hay):
            return t
    return tag


def main():
    rows = list(csv.DictReader(SRC.open(encoding="utf-8")))
    seen = {}
    out = []
    skipped = Counter()

    for row in rows:
        if row["folder"].startswith(SKIP_FOLDERS):
            skipped["site admin folder"] += 1
            continue
        hit = next((why for rx, why in
                    ((re.compile(p, re.I), why) for p, why in SKIP_URL)
                    if rx.search(row["url"])), None)
        if hit:
            skipped[hit] += 1
            continue

        if row["norm"] in seen:
            first = seen[row["norm"]]
            if row["folder"] not in first["folders"]:
                first["folders"].append(row["folder"])
            skipped["duplicate url"] += 1
            continue

        page, tag, rel, rule = classify(row)
        for rx, forced, why in COMPILED_OVERRIDES:
            if rx.search(row["url"]):
                page, rule = forced, "manual:" + why
                # a link moved onto a data-source page is a source, whatever
                # the content rule called it
                if forced in ("Geodata_Portals_Nordic", "Global_Datasets_and_Catalogs",
                              "Solar_and_Weather_Data", "Energy_Market_and_Grid_Data")                         and tag not in ("api", "dataset", "portal"):
                    tag = "portal"
                break
        candidate = ""
        if page in CANDIDATE_OF:
            page, candidate = CANDIDATE_OF[page]

        item = {
            "url": clean_url(row["url"]),
            "norm": row["norm"],
            "title": row["title"],
            "added": row["added"],
            "folders": [row["folder"]],
            "primary_page": page,
            "candidate": candidate,
            "related_pages": ";".join(rel),
            "type": type_tag(row, tag),
            "rule": rule,
        }
        seen[row["norm"]] = item
        out.append(item)

    with OUT.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["url", "norm", "title", "added", "folders",
                                           "primary_page", "candidate", "related_pages",
                                           "type", "rule"])
        w.writeheader()
        for item in out:
            item = dict(item)
            item["folders"] = " | ".join(item["folders"])
            w.writerow(item)

    print("wrote {} ({} links kept)".format(OUT, len(out)))
    print("skipped: " + ", ".join("{} {}".format(n, k) for k, n in skipped.most_common()))
    by_page = Counter(i["primary_page"] for i in out)
    for page, n in by_page.most_common():
        print("{:4d}  {}".format(n, page))
    folder_default = sum(1 for i in out if i["rule"] == "folder-default")
    print("decided by content: {}   by folder: {}".format(len(out) - folder_default, folder_default))


if __name__ == "__main__":
    main()
