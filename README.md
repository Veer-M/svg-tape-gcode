# SVG tape G-code

This converts a single continuous SVG polyline path into simple tape dispensing moves. It keeps the path order and writes a G-code file that can be inspected before using it on a machine.

## Run it

Use Python 3.11 or newer. Run these commands from this repository's folder.

```sh
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS / Linux:
# source .venv/bin/activate
python -m pip install -r requirements.txt
```

```sh
python tape_gcode.py mount_profile.svg
python tape_gcode.py mount_profile.svg --scale 0.264 --output tape_dispense.gcode
```

## How it works and current limits

Supports M/L/Z, relative equivalents, repeated coordinate pairs, and scientific notation. Curves, multiple paths, and transforms are rejected. The scale is explicit; SVG physical units and viewBox scaling are not interpreted. Output uses millimeters, absolute XY, and relative extrusion so E10 dispenses on every segment. It does not implement a cutter or optimize tape usage. Homing, extrusion, and heater commands assume a compatible machine profile; inspect and adapt them to your controller before running.

## Tests

```sh
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

Tests cover relative and closed paths, coordinate scaling, extrusion mode, and rejection of unsupported paths.
