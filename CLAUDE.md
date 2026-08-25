# CLAUDE.md — Second Brain (Obsidian vault)

## Overview

A personal knowledge vault maintained by Claude Code. Sources arrive in waves: the Zotero library (~1,400 references), browser bookmarks (~380 links), ebooks, and ad-hoc notes. Everything lands in topic pages under `notes/` that are cross-linked with Obsidian wiki-links.

Two files govern the vault: this one holds the **rules**; `TAXONOMY.md` holds the **current map** (domains, topic pages, tag vocabulary, source mappings, skip list). The map is a living document that the agent extends as new subjects appear — it is a starting point, not a fence. Read `TAXONOMY.md` at the start of every run.

Zotero remains the source of truth for bibliographic metadata. The vault stores, per reference, only: Zotero key, one link, a 1–2 line description, keywords, and wiki-links. Nothing bibliographic is ever edited in the vault — fix it in Zotero and re-sync.

### Owner context (inferred from the sources — edit if wrong)

- Background in solar photovoltaics (system performance, partial shading, IEC standards), then doctoral-level work on light for plants (solar radiation → PAR → LED lighting) and forest seedling production in Swedish nurseries.
- Now works in utility-scale solar park development in the Nordics (Sweden, Norway, Finland): permitting, site and electrical design, environmental assessment, drone inspection, PV yield modelling. Daily toolkit is GIS-heavy: QGIS/PyQGIS, Google Earth Engine, geospatial Python, Blender/AutoCAD for 3D and drafting, pvlib/SAM/PVsyst for modelling.
- Works across English, Swedish, and Spanish sources (some German, Norwegian, Finnish). Uses both R (tidyverse, sf, nlme/emmeans) and Python.
- Write for an expert reader: no need to explain PR, DLI, PPFD, STC, IEC 60904, bud set, samråd, etc.

## Folder structure

```
CLAUDE.md        -- rules (this file)
TAXONOMY.md      -- current map: domains, pages, tags, source mappings, skip list (agent-maintained)
raw/             -- unprocessed inputs (notes, exports, bookmark files, ebook lists)
raw/New_Notes.md -- always present; the drop box for quick notes
scripts/         -- helper scripts the agent writes and maintains (classification, vault_stats.py)
processed/       -- inputs already ingested (moved here untouched, never edited)
processed/zotero_state.json -- sync state: last_sync timestamp + {zotero_key: primary_page}
processed/<export>_map.csv  -- classification proposal for each bulk import
notes/           -- one markdown page per topic; MOC pages for domains
notes/index.md   -- map of content: every page + one-line description, grouped by domain
notes/log.md     -- append-only record of every operation
```

## Workflow

1. Read `TAXONOMY.md` and `notes/index.md`.
2. Read everything in `raw/`, detect the source type (see *Source-specific handling*), and process each item.
3. Move the input file to `processed/` when done. If `raw/New_Notes.md` was processed, recreate it empty.
4. Update `notes/index.md`, append to `notes/log.md`, and edit `TAXONOMY.md` if the structure changed.
5. If a file has more than ~50 items, use **Bulk import mode** instead of the single-note flow.
6. When the user asks to sync Zotero (no file in `raw/`), run **Zotero sync**.
7. Finish with **End-of-run maintenance**.
8. Update the website (see *Update the Website*).

## Processing instructions (single notes)

- If the note has URLs, visit them and write an accurate 1–2 line description.
- Identify the core concept, the primary topic, and related topics using `TAXONOMY.md` and the **Topic decision rules**.
- Add the note as a bullet at the top of the primary topic page.
- Add wiki-links `[[Page_Name]]` to related pages. If a related page does not exist, link the nearest existing parent and register a candidate if warranted (see *Growing the taxonomy*).
- Update `notes/index.md` if pages were added or their summaries changed; append to `notes/log.md`.

## Source-specific handling

### Zotero (export file or live sync)
Fields to use, whatever the transport: item key, item type, year, authors, title, publication title, DOI, URL, abstract, manual tags, automatic tags, language, date added, date modified, and **collections** when available (Zotero's CSV export has neither collections nor child notes; a Better BibTeX JSON export or the MCP/API path has both). Collection names are strong hints for `#project/` tags and for the primary topic.

- **Link priority:** `https://doi.org/<DOI>` → `Url` → none. Always append `[zotero](zotero://select/library/items/<Key>)`.
- **Do not fetch URLs** for items that have an abstract. Fetch only for `webpage`/`blogPost` items with no abstract, capped at ~20 fetches per run.
- **Description:** 1–2 lines in your own words. Never paste the abstract.
- **Authors:** `Surname (Year)`, `Surname & Surname (Year)`, `Surname et al. (Year)` for 1, 2, 3+.
- **Non-English titles:** keep the original, add an English gloss in parentheses.
- **Tags:** project-style manual tags map to vault tags per `TAXONOMY.md`; the rest feed the keywords.
- **Dedup:** look the key up in `processed/zotero_state.json` (fallback: `grep -r` on `notes/` for key or DOI). If found, update the existing bullet.
- **Item types:** `computerProgram` → the relevant tools page; agency reports and web pages that are data portals → the `Data_Sources` domain plus a link to the thematic page.

### Browser bookmarks (HTML export)
- Parse folder path, title, URL, and add-date. The folder → page defaults are in `TAXONOMY.md`; a link may deviate from its folder's default when the title clearly belongs elsewhere.
- **Skip** everything on the skip list in `TAXONOMY.md`: admin/accounting, email, chat, cloud-drive, login and portal pages, personal profile pages, duplicates. Log the count skipped, not the links.
- Add a `#type/` tag to every bookmark (tool, course, tutorial, dataset, portal, api, regulation, reference, video).
- Fetch the page for a description only when the title is uninformative (e.g. "Dashboard", "PowerPoint Presentation", a bare domain); otherwise describe from title, domain, and folder. Cap fetches at ~30 per run.
- Data portals, APIs and datasets go to the `Data_Sources` domain first (see decision rule 6).

### Ebooks (list or calibre export)
One bullet per book: `**Title** — Author (Year)`, 1–2 lines on scope, keywords, `#status/unread` or `#status/read`. `Reading_List` is not a page.

### Plain text notes
Add verbatim. Do not summarize the user's own words.

## Bulk import mode (files with >50 items)

- **Script first, judgment second.** Write a classification script (pandas) that proposes a primary page and related pages per item from title, abstract, tags, journal, folder, and collections, with a confidence score. Write it to `processed/<export>_map.csv`; review only low-confidence rows by hand. Do not read 1,400 items one at a time.
- Apply the taxonomy thresholds to the proposed mapping: create every qualifying topic page up front, and **show proposed new domains to the user before writing any notes**.
- Work in batches of 50–100 items. After each batch: update affected pages, `index.md`, `log.md`, `zotero_state.json`, and commit if the vault is a git repo. The state file is the checkpoint for resuming.
- Within a page, bulk-imported references are sorted by publication year (newest first); bookmarks by add-date. Later single additions go on top regardless.
- If a page would receive more than ~80 bullets, list a proposed split under **Proposed splits / merges** in `index.md` and continue; do not split unilaterally.

## Zotero sync (incremental, after the bulk import)

Transport is whichever is configured — a Zotero MCP server, Zotero's local HTTP API, or a Better BibTeX auto-export file. The procedure is the same:

1. Read `last_sync` from `processed/zotero_state.json`.
2. Fetch items added or modified since then. Skip child items (notes, attachments) except when reading them for a description.
3. **New items:** classify and add with the single-note flow. If there is no abstract but a PDF, read its first page only.
4. **Modified items:** compare title, year, DOI/URL, tags with the existing bullet; update only those fields. Never rewrite the description or keywords on a metadata-only change.
5. **Trashed/deleted items:** tag the bullet `#removed-from-zotero`; do not delete it.
6. Update `zotero_state.json`, `index.md`, `log.md`.
7. Keep the sync read-only towards Zotero unless the user explicitly asks to write tags back.

## Update the Website

This vault is published as a MkDocs site (Material theme) on GitHub Pages, built from `mkdocs.yml`, `hooks.py`, `requirements.txt`, and `.github/workflows/deploy.yml`. `hooks.py` appends a live bullet count to each topic page's nav label at build time — no manual upkeep needed there. After every ingest or sync:

- Refresh the **Latest Finds** section at the top of `notes/index.md` with the 3 most recently added notes, picking one from each of three different topic pages, in the vault's usual bullet format: `- **[[Page_Name]]** — [Title](url) — one-line description.`
- If a new topic page or domain was created, add it to `mkdocs.yml`'s `nav:` list under the right domain group (mirroring the grouping in `notes/index.md`).
- Stage, commit, and push (`git add`, `git commit`, `git push`) so the `deploy.yml` GitHub Actions workflow rebuilds and redeploys the site automatically. `processed/` stays gitignored and is never pushed — never `git add` it.

## Topic structure

Three levels, all defined in `TAXONOMY.md`:

- **Domain** = a MOC page (`Photovoltaics`, `Geospatial`, …) holding a short overview and links to its topic pages. Notes never go on a MOC page.
- **Topic page** = where notes live. Each has a `Parent:` line pointing at its MOC.
- **Candidate** = a `## Candidate: <Name>` subheading on the closest topic page (or a group on `Unsorted`) collecting notes for a page that does not exist yet.

## Topic decision rules

1. **Theme over technology.** A paper that uses Python to model PV yield goes to the PV page; the tools page gets a link only if the note says something about the tool itself. A bookmark that *is* a tool (docs, tutorial, package) goes to the tools page, with a link to the thematic page it serves.
2. **Most specific page wins.** If two topic pages fit, pick the one the content spends most words on; link the other.
3. **Research vs practice.** Modelling and physics of PV → `Photovoltaics` domain; permitting, site/electrical design, construction practice → `Solar_Park_Development`. Environmental-impact research (EMF, glare, noise) lives with the practice page that uses it.
4. **Bridge rule.** Anything combining PV with crops, greenhouses, or land use goes to `Agrivoltaics` or `PV_Greenhouses`, linking both parent domains.
5. **Process over species.** A paper on frost hardiness of Norway spruce goes to the cold-hardiness page; the species page gets a backlink.
6. **Data first.** A portal, API, or dataset files under `Data_Sources` with a link to the thematic page that uses it, never the other way round.
7. **Geography, species, crops, projects, and content type are tags, not pages.**
8. **Nothing fits?** Do not force a note into the nearest catch-all. Park it under a `## Candidate: <Name>` subheading on the closest topic page, or on `Unsorted`, and register the candidate in `index.md` and `TAXONOMY.md`.
9. **When unsure between two existing pages,** file under the more general one and add `#needs-review`.
10. **Keep the map current.** Every new page, MOC, rename, merge, or promoted candidate is reflected in `TAXONOMY.md` in the same run, with a changelog line.

## Growing the taxonomy

New topics and domains will keep appearing. The agent is expected to grow the structure, not just fill it.

| Level | Trigger | Autonomy |
|---|---|---|
| Candidate | any note that fits no existing page | always, silently |
| Topic page | a candidate reaches **5 notes**, or the user asks | create it, then report in the run summary |
| Domain (MOC) | **3 topic pages** share a theme no MOC covers, or one page passes ~25 notes with clear sub-themes | **propose first**, create after the user says yes (the user can switch this to autonomous) |
| Rename / merge / split | scope drift, a page over ~80 bullets, two pages with heavy overlap | propose only; wait for approval |

**Before creating any page:** search `TAXONOMY.md`, `index.md`, and frontmatter `aliases` for the same concept under another name (`LED_Lighting` would duplicate `Horticultural_Lighting`); add an alias instead if found. Name it the way the literature does, Title_Case_With_Underscores, noun phrase; no names that are only a place, species, crop, or content type. Decide the parent MOC; if none fits, `Other_Topics`.

**Promotion procedure (candidate → page):** create the page (frontmatter, Summary, `Parent:`); **move** the bullets (never copy) and drop `#needs-topic`; repoint any `[[Parent#Candidate: Name]]` or `[[Unsorted]]` links; update `zotero_state.json` for moved keys; add the page to `index.md`, `TAXONOMY.md` (row + changelog), and `log.md`.

**Domain proposal format** (under **Proposed domains** in `index.md`, then shown to the user):
`- Proposed MOC: [[Home_Energy]] — scope: heat pumps, insulation, household electricity — members: [[Heat_Pumps]], [[Building_Energy_Efficiency]], [[Electricity_Tariffs]] — 31 notes — reason: three pages under Other_Topics share a theme.`
On approval: create the MOC, set `Parent:` on members, regroup `index.md`, add a domain section to `TAXONOMY.md`, log it.

**End-of-run maintenance (after every ingest or sync):**
1. Run `scripts/vault_stats.py` (the agent writes and maintains it): bullets per page, notes per candidate, pages over 80 bullets, pages with no inbound links.
2. Promote every candidate at or above 5 notes.
3. Add new domain, split, or merge proposals to `index.md`.
4. Report in one short block: pages created, proposals waiting, items tagged `#needs-review` / `#needs-topic`, items skipped.

## Tag conventions (Obsidian nested tags; vocabulary in `TAXONOMY.md`)

- `#region/…`, `#species/…`, `#crop/…` — facets that would otherwise tempt page creation.
- `#type/…` — what a bookmark is (tool, course, dataset, portal, …).
- `#project/…` — thesis, research, and solar-park site material.
- `#status/…` — unread, read, todo.
- `#needs-review` (unsure between pages), `#needs-topic` (parked as candidate), `#removed-from-zotero`.
- Everything else is a plain keyword in the bullet, not a tag. New tag values are added to the vocabulary in `TAXONOMY.md` when first used.

## Topic page format

```markdown
---
tags: [domain/photovoltaics]
aliases: [PV performance, performance ratio]
updated: 2026-08-25
---
# PV System Performance

**Summary**: One to two sentences describing this page.
**Parent**: [[Photovoltaics]] · **Related**: [[PV_Shading_and_Mismatch]], [[PV_in_Nordic_Climates]]

---

## Notes

- (newest first)
```

MOC pages use the same header, a 3–5 line overview of the domain, and a bulleted list of child pages with one-line descriptions.

## Note formatting

- Markdown, one bullet per note, newest at top (see bulk-import ordering).
- **Reference (Zotero, ebook):**
  `- **[Title](https://doi.org/…)** — Author et al. (Year), *Journal or Publisher*. One–two line description. Keywords: kw1, kw2, kw3. Related: [[Page_A]], [[Page_B]]. [zotero](zotero://select/library/items/KEY) #project/light-model`
- **Bookmark / web link:**
  `- [Title](url) — text the user wrote alongside the link, verbatim if any. One–two line description. Keywords: … Related: [[…]] #type/tool`
- **Text-only note:**
  `- Title: note text verbatim. Keywords: … Related: [[…]]`
- 3–6 keywords per note, chosen for later recall (method names, species, crop, instrument, dataset, location).
- Wiki-links use `[[Page_Name]]`; `[[Page_Name|display text]]` for readable inline links.
- Descriptions in English regardless of source language.

## Index format (`notes/index.md`)

Grouped by domain in the same order as `TAXONOMY.md`: MOC page first, then its child pages, one line each: `- [[Page_Name]] — one-line description`. End with four bookkeeping sections:

- **Candidate topics** — `- Heat pumps (under [[Energy_Transition_and_Scenarios]]) — 3 notes`
- **Proposed domains** — in the format given above
- **Proposed splits / merges** — pages over ~80 bullets or with heavy overlap
- **Needs attention** — counts of `#needs-review` and `#needs-topic` notes

## Log format (`notes/log.md`)

One line per operation, append-only:

`- 2026-08-25 · My_Library.csv (batch 3/15, keys 101–150) · +48 notes: [[PV_System_Performance]] ×21, [[Solar_Radiation_Modelling]] ×9, … · new pages: [[Energy_Storage]] · taxonomy updated · 2 items #needs-review · 0 skipped`

## Rules

- Page names Title_Case_With_Underscores; use frontmatter `aliases` for readable names and species names.
- Clear, plain language; expert reader.
- Never edit or delete files in `processed/`. Never delete notes from topic pages unless the user asks — mark `#needs-review` instead.
- Never paste abstracts or long passages verbatim; user-written text is the only content copied verbatim.
- Always update `notes/log.md` after changes, `notes/index.md` whenever pages are added or renamed, and `TAXONOMY.md` whenever the structure changes.
- Update the `updated:` frontmatter field on every page touched.
