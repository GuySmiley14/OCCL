# OCCL Specification v0.1

## Open Component & Connector Library

**Version:** 0.1
**Status:** Draft
**Last Updated:** June 2026

---

# 1. Introduction

The **Open Component & Connector Library (OCCL)** is an open-source repository of automotive (and adjacent) electrical components, connectors, and supporting assets.

OCCL serves two primary purposes:

* A **human-readable reference library**, similar to a wiki.
* A **machine-readable library** for software tools such as wiring harness builders, pinout viewers, documentation generators, and validation software.

The guiding principle of OCCL is that it describes **manufacturer-defined hardware**, while user-created harnesses describe **how that hardware is used**.

---

# 2. Design Philosophy

OCCL intentionally separates immutable manufacturer data from project-specific wiring information.

A component definition should answer:

> **"What did the manufacturer build?"**

A harness project should answer:

> **"How has the user wired this component into their system?"**

This separation allows a single OCCL component definition to be reused across countless independent projects.

---

# 3. Repository Structure

```
OCCL/
│
├── Components/
│   ├── AEM/
│   │   ├── BMS Mini Master.json
│   │   └── PDU-8.json
│   │
│   └── ...
│
├── Connectors/
│   ├── TE/
│   │   ├── DTM15-12PA/
│   │   │   ├── connector.json
│   │   │   └── component-face.svg
│   │   │
│   │   ├── DTM06-12SA/
│   │   │   ├── connector.json
│   │   │   ├── harness-front.svg
│   │   │   └── harness-rear.svg
│   │   │
│   │   └── ...
│   │
│   └── ...
│
├── docs/
│   └── OCCL_Spec_v0.1.md
│
└── README.md
```

---

# 4. Components

A component represents a manufactured device.

Examples include:

* BMS
* VCU
* PDU
* Inverter
* Charger
* Display
* Sensor

Component definitions contain information that is considered effectively immutable.

Typical fields include:

* Manufacturer
* Model
* Connector information
* Pin functions
* Manufacturer notes
* Datasheet references

Component definitions intentionally **do not** contain vehicle-specific wiring information.

---

## Example

```json
{
  "manufacturer": "AEM",
  "name": "BMS Mini Master",

  "connectors": [
    {
      "name": "J1",

      "componentConnector": "TE/DTM15-12PA",

      "harnessConnector": "TE/DTM06-12SA",

      "pins": [
        {
          "pin": 1,
          "function": "12V Battery",
          "notes": "Constant battery supply"
        }
      ]
    }
  ]
}
```

---

# 5. Connectors

Connectors are first-class reusable objects.

Many components may reference the same connector.

Connector definitions include:

* Manufacturer
* Part number
* Position count
* SVG assets
* Basic metadata
* Compatible mating connector(s)

Connector definitions intentionally **do not** define component-specific pin functions.

---

# 6. Connector Views

Different connector views communicate different information.

OCCL stores each view as a discrete SVG.

Typical assets include:

```
component-face.svg

harness-front.svg

harness-rear.svg
```

These assets are considered distinct engineering drawings rather than duplicates.

---

## Component Face

Used for:

* PCB troubleshooting
* Pin identification
* Component documentation

---

## Harness Front

Used for:

* Connector mating
* Front-face cavity identification

---

## Harness Rear

Used for:

* Harness assembly
* Wire insertion
* Pinning

---

# 7. Pins

Each physical cavity is represented by exactly one pin object.

Example:

```json
{
    "pin": 1,
    "function": "High Side Driver 1",
    "notes": "20 Amp Max"
}
```

Even when multiple cavities are electrically common, each cavity is represented independently.

Example:

```
Pin 1
Pin 2

↓

Two pin objects

↓

Same function
```

This preserves the physical topology of the connector while allowing renderers to merge identical rows for presentation if desired.

---

# 8. Function vs Signal

OCCL uses the field name:

```
function
```

rather than:

```
signal
```

Reasoning:

Not every electrical connection carries a signal.

Examples include:

* Power
* Ground
* Shield
* Wake line
* High-side driver
* Configuration strap

The term **function** more accurately describes the purpose of the pin.

---

# 9. Notes

Manufacturer comments are stored in:

```
notes
```

Examples:

* 20 Amp Max
* Ground for Unit IDs 3–8
* Reserved
* Leave Open
* Unterminated

These are informational only.

---

# 10. Harness Projects

Harness projects exist outside OCCL.

They reference OCCL components but never modify them.

Example:

```json
{
    "component": "AEM/BMS Mini Master",

    "instance": "BMS1",

    "connections": [

        {
            "connector": "J1",
            "pin": 1,

            "colour": "red",
            "gauge": "20 AWG",

            "endpoint": "Fuse F1",

            "notes": "Battery supply"
        }

    ]
}
```

---

# 11. Immutable vs Mutable Data

## OCCL (Immutable)

* Connector part numbers
* Pin numbering
* Pin functions
* Connector graphics
* Manufacturer notes
* Recommended mating connectors

---

## Harness Projects (Mutable)

* Wire colour
* Wire gauge
* Endpoints
* Project notes
* Labels
* Routing

---

# 12. Mating Connectors

Component definitions include both:

* The connector physically mounted on the component.
* The recommended mating harness connector.

Example:

```json
{
    "componentConnector": "TE/DTM15-12PA",

    "harnessConnector": "TE/DTM06-12SA"
}
```

This makes each component page self-contained as a reference while still allowing connector definitions to remain independent reusable objects.

Future versions may support multiple compatible mating connectors.

---

# 13. Scope

## Included

* Components
* Connectors
* Connector SVGs
* Pin functions
* Pin notes
* Mating connector information
* Datasheet references

---

## Future Expansion

Possible future additions include:

* Alternate compatible connectors
* Connector dimensions
* STEP models
* Photos
* Terminal information
* Wedge locks
* Seals
* Crimp tooling
* Service documentation

These are considered optional enhancements rather than required metadata.

---

# 14. Guiding Principles

* One physical cavity equals one pin object.
* Components describe manufacturer intent.
* Harnesses describe user implementation.
* Connectors are reusable library objects.
* SVG assets represent distinct engineering views.
* Connector graphics remain independent of component definitions.
* OCCL prioritizes clarity, completeness, and contributor friendliness over aggressive normalization.
* Contributors should be able to create useful entries with only the essential information; richer metadata can be added over time.

---

# 15. Long-Term Vision

OCCL aims to become a community-maintained reference library for electrical components and connectors.

The library should be useful both to humans seeking documentation and to software consuming structured data.

By maintaining a clear separation between manufacturer-defined hardware and user-defined wiring, OCCL enables reliable reuse across projects while remaining approachable for contributors.

The long-term goal is not simply to document parts, but to provide an open foundation upon which wiring harness design, documentation, visualization, and validation tools can be built.

# Appendix A — Design Decisions

This appendix records significant architectural decisions made during the design of OCCL.

The purpose is to preserve the reasoning behind the library's structure so that future contributors understand not only *what* decisions were made, but *why*.

---

## DD-001 — Components are immutable

Component definitions describe the hardware as manufactured.

They intentionally do not contain vehicle- or project-specific information such as wire colours, wire gauges, routing, endpoints, or user notes.

### Rationale

A single component should be reusable across many independent projects without modification.

Vehicle-specific information belongs in a harness project rather than the component library.

---

## DD-002 — Components reference both connector halves

Each component references:

* the connector fitted to the component
* the recommended mating harness connector

### Rationale

Although the mating connector is technically a separate part, users frequently consult OCCL as a reference library to determine which connector mates with a particular component.

Including both part numbers makes component pages self-contained while preserving connector definitions as reusable library objects.

---

## DD-003 — Connectors are first-class library objects

Connectors exist independently of components.

A single connector may be referenced by many different devices.

### Rationale

This avoids duplication of connector graphics and metadata while allowing connectors to evolve independently of component definitions.

---

## DD-004 — SVG views are discrete assets

Different viewpoints of a connector are stored as separate SVGs.

Typical examples include:

* Component face
* Harness front
* Harness rear

### Rationale

These drawings communicate different information and are considered distinct engineering views rather than alternate renderings of the same asset.

Although this increases authoring effort, it produces a more complete and useful reference library.

---

## DD-005 — One physical cavity equals one pin object

Each physical cavity is represented individually within component definitions.

Even if multiple cavities are electrically common, each receives its own pin object.

### Rationale

The library models the physical connector rather than the schematic representation.

This enables accurate highlighting, validation, and harness generation while allowing renderers to merge identical rows when presenting pin tables.

---

## DD-006 — Pin "function" is preferred over "signal"

Pin definitions use the field name:

```
function
```

rather than:

```
signal
```

### Rationale

Not all pins carry signals.

Examples include:

* Power
* Ground
* Shield
* High-side outputs
* Configuration straps

The term *function* more accurately represents the purpose of a connector cavity.

---

## DD-007 — OCCL is a reference library, not an ECAD database

The scope of OCCL is intentionally limited.

The library focuses on documenting:

* Components
* Connectors
* Pin functions
* Connector graphics

Detailed connector ecosystem data such as:

* Terminals
* Seals
* Wedges
* Crimp tooling
* Wire insulation compatibility

is considered optional future metadata.

### Rationale

Keeping the required metadata lightweight lowers the barrier to contribution while allowing the library to grow organically.

---

## DD-008 — Components describe hardware, harnesses describe implementation

OCCL stores manufacturer intent.

Harness projects store implementation details.

### Rationale

Separating these responsibilities prevents duplication while allowing a single component definition to be reused across many independent harness projects.

---

## DD-009 — Connector graphics are independent assets

SVG files are not embedded within component definitions.

Components reference connector part numbers rather than owning connector graphics.

### Rationale

Many different components share identical connectors.

Keeping connector graphics independent minimizes maintenance and ensures consistency across the library.

---

## DD-010 — Human readability is a primary design goal

OCCL is intended to function as both:

* a machine-readable component library
* a human-readable technical reference

Where appropriate, component definitions may include convenience information (such as recommended mating connector part numbers) even when that information can be inferred elsewhere.

### Rationale

A contributor or user browsing the library should be able to answer common engineering questions from a single component page without excessive cross-referencing.

---

## DD-011 — Contributor effort should scale with available information

The minimum useful OCCL contribution should require only:

* Component identification
* Connector identification
* Pin functions
* Connector graphics

Additional metadata should be additive rather than mandatory.

### Rationale

Lowering the barrier to entry encourages contributions while allowing future contributors to enrich existing entries over time.
