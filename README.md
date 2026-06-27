# Open Component & Connector Library (OCCL)

The **Open Component & Connector Library (OCCL)** is an open-source collection of electrical components, connectors, pinouts, and SVG assets for automotive and embedded systems.

OCCL is designed to be both:

* 📖 A human-readable reference library for engineers, hobbyists, and vehicle builders.
* 🤖 A machine-readable data source for software such as wiring harness builders, pinout viewers, documentation generators, and validation tools.

## Goals

* Create an open, reusable library of electrical components and connectors.
* Provide consistent, machine-readable pinout data.
* Standardize connector artwork using SVG.
* Enable automation while remaining easy for humans to browse and contribute.

OCCL intentionally separates **manufacturer-defined hardware** from **project-specific wiring**. Component definitions describe *what the manufacturer built*; harness projects describe *how those components are connected within a particular system*.

## Repository Structure

```text
Components/
    Manufacturer/
        Component.json

Connectors/
    Manufacturer/
        Connector.svg
        Connector.json

Docs/
```

## Contributing

Contributions are welcome!

Whether you're adding a new connector, documenting a component, improving an SVG, or correcting metadata, every contribution helps expand the library for the community.

Please read the documentation before submitting a pull request:

* `Docs/OCCL_Spec.md`
* `Docs/JSON_Schema.md` *(coming soon)*
* `Docs/SVG_Style_Guide.md` *(coming soon)*
* `CONTRIBUTING.md` *(coming soon)*

## Status

OCCL is an early-stage project and the file formats, schemas, and documentation are still evolving. Backwards compatibility is not yet guaranteed while the project architecture is being established.

Feedback, discussion, and contributions are encouraged as the library grows.
