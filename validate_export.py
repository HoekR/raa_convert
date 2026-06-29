#!/usr/bin/env python3
"""Post-export validation for the RAA consolidation pipeline."""

from __future__ import annotations

import argparse
import pickle
import sys
from pathlib import Path

import pandas as pd

PERIOD_COLUMNS = ("me", "republiek", "batfra", "negentiende_eeuw", "divperioden")

EXPECTED_TABLES = {
    "persoon",
    "aanstelling",
    "instelling",
    "functie",
    "alias",
    "bron_details",
    "bron",
    "academische_titel",
    "adellijke_titel",
    "lokaal",
    "provincie",
    "gewest",
    "regio",
    "stand",
}


def load_extab(path: Path) -> dict[str, pd.DataFrame]:
    with path.open("rb") as handle:
        data = pickle.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"{path} does not contain an extab dict")
    return data


def check_required_tables(extab: dict[str, pd.DataFrame]) -> list[str]:
    errors = []
    if "" in extab:
        errors.append("extab contains empty table name (internal table not in exporttabellen)")
    missing = EXPECTED_TABLES - set(extab)
    if missing:
        errors.append(f"Missing tables in extab: {sorted(missing)}")
    return errors


SKIP_DUPLICATE_ID_TABLES = frozenset({"aanstelling"})


def check_duplicate_ids(extab: dict[str, pd.DataFrame]) -> list[str]:
    errors = []
    for name, frame in extab.items():
        if name in SKIP_DUPLICATE_ID_TABLES:
            continue
        if "id" not in frame.columns:
            continue
        id_col = frame["id"]
        if isinstance(id_col, pd.DataFrame):
            errors.append(f"{name}: duplicate 'id' column in export")
            continue
        dupes = id_col.duplicated(keep=False) & id_col.notna()
        if dupes.any():
            errors.append(f"{name}: {int(dupes.sum())} duplicate id values")
    return errors


def check_fk_null_rate(
    extab: dict[str, pd.DataFrame],
    table: str,
    column: str,
    *,
    max_null_fraction: float,
) -> list[str]:
    errors = []
    if table not in extab or column not in extab[table].columns:
        errors.append(f"{table}.{column} column missing")
        return errors
    series = extab[table][column]
    null_frac = series.isna().mean()
    if null_frac > max_null_fraction:
        errors.append(
            f"{table}.{column}: {null_frac:.1%} null (max allowed {max_null_fraction:.1%})"
        )
    return errors


def check_toelichting(extab: dict[str, pd.DataFrame]) -> list[str]:
    errors = []
    if "instelling" not in extab or "toelichting" not in extab["instelling"].columns:
        return errors
    bad = extab["instelling"]["toelichting"].astype("string").str.contains(
        "dtype: object", na=False
    )
    if bad.any():
        errors.append(
            f"instelling.toelichting: {bad.sum()} rows contain pandas Series repr (corrupt URLs)"
        )
    return errors


def check_period_columns(extab: dict[str, pd.DataFrame]) -> list[str]:
    errors = []
    for name, frame in extab.items():
        for col in PERIOD_COLUMNS:
            if col not in frame.columns:
                errors.append(f"{name}: missing period column {col}")
    return errors


def validate(extab: dict[str, pd.DataFrame]) -> list[str]:
    errors: list[str] = []
    errors.extend(check_required_tables(extab))
    errors.extend(check_duplicate_ids(extab))
    errors.extend(check_fk_null_rate(extab, "aanstelling", "persoon_id", max_null_fraction=0.01))
    errors.extend(check_fk_null_rate(extab, "alias", "persoon_id", max_null_fraction=0.10))
    errors.extend(check_fk_null_rate(extab, "bron_details", "persoon_id", max_null_fraction=0.05))
    errors.extend(check_toelichting(extab))
    errors.extend(check_period_columns(extab))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate RAA extab export")
    parser.add_argument(
        "--pickle",
        type=Path,
        default=Path("extab.pkl"),
        help="Path to extab pickle (default: extab.pkl)",
    )
    args = parser.parse_args()

    if not args.pickle.exists():
        print(f"error: {args.pickle} not found — run raa_tabel_consolidate.ipynb first", file=sys.stderr)
        return 1

    extab = load_extab(args.pickle)
    errors = validate(extab)

    print(f"Loaded {len(extab)} tables from {args.pickle}")
    for name, frame in sorted(extab.items()):
        print(f"  {name}: {len(frame)} rows, {len(frame.columns)} columns")

    if errors:
        print("\nFAILED:")
        for err in errors:
            print(f"  - {err}")
        return 1

    print("\nOK: all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
