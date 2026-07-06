#!/usr/bin/env python3
"""
Regenerates OCCL-index.json from the contents of Components/ and Connectors/.

Run from the repo root:
    python3 scripts/build_occl_index.py
"""

import json
import os

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def build_components():
    components = []
    base = os.path.join(REPO_ROOT, "Components")
    for mfr in sorted(os.listdir(base)):
        mfr_path = os.path.join(base, mfr)
        if not os.path.isdir(mfr_path):
            continue
        for fname in sorted(os.listdir(mfr_path)):
            if fname.endswith(".json"):
                part_number = fname[:-5]
                components.append({
                    "manufacturer": mfr,
                    "partNumber": part_number,
                    "path": f"Components/{mfr}/{fname}"
                })
    return components


def build_connectors():
    connectors = {}
    base = os.path.join(REPO_ROOT, "Connectors")
    for mfr in sorted(os.listdir(base)):
        mfr_path = os.path.join(base, mfr)
        if not os.path.isdir(mfr_path):
            continue
        for fname in sorted(os.listdir(mfr_path)):
            part_number, ext = os.path.splitext(fname)
            key = (mfr, part_number)
            entry = connectors.setdefault(key, {
                "manufacturer": mfr,
                "partNumber": part_number,
                "svg": None,
                "json": None
            })
            if ext == ".svg":
                entry["svg"] = f"Connectors/{mfr}/{fname}"
            elif ext == ".json":
                entry["json"] = f"Connectors/{mfr}/{fname}"
    return list(connectors.values())


def main():
    index = {
        "format": "OCCL-Index",
        "version": 1,
        "components": build_components(),
        "connectors": build_connectors()
    }

    out_path = os.path.join(REPO_ROOT, "OCCL-index.json")
    with open(out_path, "w") as f:
        json.dump(index, f, indent=2)
        f.write("\n")

    print(f"Wrote {out_path}: "
          f"{len(index['components'])} components, "
          f"{len(index['connectors'])} connectors")


if __name__ == "__main__":
    main()
