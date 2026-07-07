#!/usr/bin/env python3
"""
Regenerates OCCL-index.json from the contents of Components/ and Connectors/.

Run from the repo root:
    python3 scripts/build_occl_index.py
"""

import json
import os

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def validate_component(data):
    """Lightweight spec check. Returns an error string, or None if valid."""
    if not isinstance(data, dict):
        return "not a JSON object"

    for key in ("manufacturer", "partName", "partNumber", "connectors"):
        if key not in data:
            return f"missing '{key}'"

    if not isinstance(data["connectors"], list) or len(data["connectors"]) == 0:
        return "'connectors' must be a non-empty list"

    for i, connector in enumerate(data["connectors"]):
        for key in ("manufacturer", "partNumber", "pins"):
            if key not in connector:
                return f"connector[{i}] missing '{key}'"
        if not isinstance(connector["pins"], list) or len(connector["pins"]) == 0:
            return f"connector[{i}] 'pins' must be a non-empty list"
        for j, pin in enumerate(connector["pins"]):
            if "pin" not in pin:
                return f"connector[{i}] pin[{j}] missing 'pin'"
            if not isinstance(pin["pin"], str):
                return f"connector[{i}] pin[{j}] 'pin' must be a string, got {type(pin['pin']).__name__}"

    return None


def build_components():
    components = []
    invalid = []
    base = os.path.join(REPO_ROOT, "Components")

    for mfr in sorted(os.listdir(base)):
        mfr_path = os.path.join(base, mfr)
        if not os.path.isdir(mfr_path):
            continue

        for fname in sorted(os.listdir(mfr_path)):
            if not fname.endswith(".json"):
                continue

            part_number = fname[:-5]
            path = f"Components/{mfr}/{fname}"
            full_path = os.path.join(mfr_path, fname)

            try:
                with open(full_path) as f:
                    data = json.load(f)
            except (json.JSONDecodeError, OSError) as e:
                invalid.append({"path": path, "reason": f"invalid JSON: {e}"})
                continue

            error = validate_component(data)
            if error:
                invalid.append({"path": path, "reason": error})
                continue

            components.append({
                "manufacturer": mfr,
                "partNumber": part_number,
                "path": path
            })

    return components, invalid


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
                # Connector metadata is optional enrichment, not required.
                # A malformed one just falls back to svg-only, same as if
                # the json file were never contributed at all.
                full_path = os.path.join(mfr_path, fname)
                try:
                    with open(full_path) as f:
                        json.load(f)
                    entry["json"] = f"Connectors/{mfr}/{fname}"
                except (json.JSONDecodeError, OSError):
                    pass

    return list(connectors.values())


def main():
    components, invalid = build_components()

    index = {
        "format": "OCCL-Index",
        "version": 1,
        "components": components,
        "connectors": build_connectors(),
        "invalid": invalid
    }

    out_path = os.path.join(REPO_ROOT, "OCCL-index.json")
    with open(out_path, "w") as f:
        json.dump(index, f, indent=2)
        f.write("\n")

    print(f"Wrote {out_path}: "
          f"{len(index['components'])} components, "
          f"{len(index['connectors'])} connectors, "
          f"{len(invalid)} invalid (excluded)")

    for entry in invalid:
        print(f"  SKIPPED {entry['path']}: {entry['reason']}")


if __name__ == "__main__":
    main()
