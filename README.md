# New RAA

This is a conversion of the Repertory of Officeholders from the original MSAccess (mdb) databases. I kept everything in Jupyter notebooks in order to be able to follow and influence the process if necessary.

N.B. This conversion procedure is a result of *much* trial and error. I have tried to comment on all important steps for better understanding.
The technical conversion procedure is vulnerable due to the arcane nature of MSAccess databases, but these have been in use since the 2000s.

## Documentation

- [docs/CONVERSION_REVIEW.md](docs/CONVERSION_REVIEW.md) — full audit report (derived fields, gaps, bugs)
- [docs/CONVERSION_NOTES.md](docs/CONVERSION_NOTES.md) — operational reference for running the pipeline

## Setup

### Python environment

The pipeline runs as **Jupyter notebooks** with local **Python 3**. Create a venv and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m ipykernel install --user --name=raa-convert --display-name="RAA Convert"
```

Select the **RAA Convert** kernel in Jupyter/Cursor when opening the notebooks.

`requirements2.txt` is an older full `pip freeze` from a previous machine; use `requirements.txt` for new setups.

### System dependencies (not pip)

- **[mdbtools](https://github.com/mdbtools/mdbtools)** — `mdb-export`, `mdb-tables`, `mdb-schema` (used by `mdb_read.ipynb`)  
  macOS: `brew install mdbtools`
- **MySQL** — local server for staging (`raa_old`) and output (`raa_nw`)

An older experimental path in `mdb_read.ipynb` mentions `unixodbc` + `pandas_access`; the active path uses mdbtools.

### Connection config

Copy the connection template and edit local paths and credentials:

```bash
cp connection.json.example connection.json
```

`connection.json` is gitignored. Use SQLAlchemy URLs like `mysql+pymysql://<user>:<password>@localhost/raa_old`.

## Steps

The conversion procedure (should) follow these steps:

1. Update MSAccess databases from their HuC repository (only if source data changed)
2. Convert the original databases using [mdb_read.ipynb](mdb_read.ipynb) — **skip if `raa_old` is already up to date**
3. Set `raa_out` in `connection.json` to a **new dated database** (e.g. `raa_nw_20260629`); never point it at `raa_nw` if you want to keep the previous export
4. Merge to new database using [raa_tabel_consolidate.ipynb](raa_tabel_consolidate.ipynb) — reads `raa_old`, writes only to `raa_out`
5. Validate export: `python validate_export.py`

`raa_old` is the MySQL database name for staged per-period tables; `raa_nw` is the merged output.

## Remarks and additions

- Old references and ids are omitted from the final database
- All tables have period indications for the web interface (`me`, `republiek`, `batfra`, `negentiende_eeuw`, `divperioden`); `1` means included in search for that period
- The instelling table is supplemented with html descriptions and (for the Bataafs-Franse period) links to the external guide database
- Reference table updates are overhauled and more complete
