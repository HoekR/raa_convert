# RAA Conversion — Operational Notes

Quick reference for running and auditing the merge pipeline. For the full review, see [CONVERSION_REVIEW.md](CONVERSION_REVIEW.md).

## Pipeline

1. `mdb_read.ipynb` — MDB → MySQL `raa_old` + `mdbdump/*.csv`
2. `raa_tabel_consolidate.ipynb` — merge → MySQL `raa_nw` + `extab.pkl` / `targetdb_dump_*.pkl`
3. `python validate_export.py` — post-export checks (after step 2)

Six source periods: `batfra`, `negentiende_eeuw`, `me`, `divperioden`, `republiek`, `republiek_friezen`.

## Derived output fields (not in MDB)

| Field | How it is produced |
|---|---|
| All `id` / `*_id` | New sequential IDs after concat + reference dedup |
| `searchable` | `tussenvoegsel` + `geslachtsnaam` |
| `heerlijkheid` | `Heerlijkheid` + `" en "` + `Heerlijkheid2` |
| `geboortedatum`, `overlijdensdatum`, `van`, `tot` | `makedate_from_givendate()` in `help_functions.py` |
| `*_als_bekend` | Joined day-month-year parts before ISO conversion |
| `me`, `republiek`, `batfra`, `negentiende_eeuw`, `divperioden` | Parsed from prefixed `old_*` IDs via `map_dict()` / `pmap` |
| `toelichting` | HTML from `institutionele_toelichtingen/` + concordance JSON |
| Bataafs-Franse URL | Fallback when `toelichting` empty (`makelink()` + external CSV) |
| `mark_for_delete` | `1` when `divperioden==1` (superseded by Friesland data) |

### Date coercion rules (`makedate_from_givendate`)

Inherited from the legacy web application (Jan Wijbrand):

- Missing month/day on **start** dates → `01-01`; on **end** dates → `12-31`
- `?` in year → `0` (start) or `9` (end)
- Invalid calendar dates are silently corrected (e.g. Feb 29 → 28)
- Partial dates without year default to year `1000`

Audit any person or appointment where only a year was known in the source.

### Period flags

- `republiek_friezen` shares `pmap` value `2` with `republiek` — there is no separate `republiek_friezen` column in export.
- `divperioden==1` rows are flagged `mark_for_delete=1` but not physically removed from export.

## Source tables intentionally excluded

| Table | Reason |
|---|---|
| `Gewest` | Not in `common_tables`; out of scope for current web schema |
| `BronFunctieDetails` | Commented out of `common_tables` |
| `Data`, `RegentOud`, `Temp*`, `BovenLokaalCollegeRegentDetails1` | Staging / legacy |
| `functiebovenlokaal`, `functielokaal` | Merged internally for ID mapping only; not in `exporttabellen` |

## Source columns dropped or lost

- `old_*` columns — stripped from final DB (by design)
- `Functie.Periode`, `Functie.Lokaal` — lost when deduplicating on function name alone
- `College.Periode` — lost when deduplicating on institution name alone
- `Opmerkingen2`, `TempID` — not in `columnmaps`
- Cross-period duplicate **persons** are **not** merged; same individual in two periods → two `persoon_id` values

## Complete source table inventory (`data_definitions.coll`)

Per-period MDB tables tracked in `coll`:

- **All periods:** `AcademischeTitel`, `AdellijkeTitel`, `aliassen`, `Bron`, `BronRegentDetails`, `College`, `Functie`, `lokaal`, `Regent`, `BovenLokaalCollegeRegentDetails`, `stand`, plus period-specific extras.
- **Most periods:** `Gewest`, `Data`, `BronFunctieDetails`, `FunctieLokaal`, `FunctieBovenLokaal`, `provinciaal`, `regionaal`.
- **Republiek / Friezen only:** `RegentOud`.
- **ME only:** `BovenLokaalCollegeRegentDetails1`, `TempTable`.

Merged via `common_tables` (see `data_definitions.py`).

## Configuration

Copy `connection.json.example` → `connection.json` (gitignored) and set:

`raa_old` / `raa_out` — SQLAlchemy MySQL URLs. **Reads** use `raa_old` (staging); **writes** use `raa_out` only. Use a dated output name (e.g. `raa_nw_20260629`) so `raa_nw` is never overwritten. The consolidate notebook refuses to write to `raa_nw` or `raa_old`.
- `batfralokatie` — path to Bataafs-Franse instelling CSV
- `toe_dirs` — directories with institutional HTML toelichtingen

## Verification

```bash
python validate_export.py              # uses extab.pkl if present
python validate_export.py --pickle extab.pkl
```

See checklist in [CONVERSION_REVIEW.md](CONVERSION_REVIEW.md#part-5-recommended-verification-checklist).
