# SVG tape G-code

This program takes a line drawing from an SVG file and turns it into G-code for a tape dispenser. G-code is a set of instructions that tells a machine where to move.

## How it works

The SVG must contain one continuous path made from straight lines. The program reads its X and Y coordinates in order and converts them to millimeters. The default scale multiplies each coordinate by 0.264.

The output starts with commands that set the movement modes and home the machine. It moves to the first point without dispensing, then adds a dispensing move for each line segment. `M83` sets relative extrusion, so `E10` asks for 10 units of dispensing on each segment instead of reusing one absolute total. The final command is `M104 S0`.

The path reader accepts M, L, and Z commands along with their lowercase forms. These commands move to a point, draw a line, and close a path. It also accepts repeated coordinate pairs and numbers written in scientific notation.

## What the input needs

Curves, extra paths, and SVG transforms are rejected. SVG units and viewBox scaling are not worked out automatically. Set `--scale` to match the way your drawing was made.

The program keeps the original path order. It does not control a cutter or work out the best way to use the tape. The homing, extrusion, and heater commands also depend on the machine. Read the generated file and adjust those commands for your controller before running it.

## Try it

Use Python 3.11 or newer. Open a terminal in this project's folder and create a virtual environment. This keeps its packages separate from your other Python projects.

```sh
python -m venv .venv
```

On Windows, activate it with this command.

```sh
.venv\Scripts\activate
```

On macOS or Linux, use this command instead.

```sh
source .venv/bin/activate
```

Then install the packages the project needs.

```sh
python -m pip install -r requirements.txt
```

```sh
python tape_gcode.py mount_profile.svg
python tape_gcode.py mount_profile.svg --scale 0.264 --output tape_dispense.gcode
```

The included SVG is a rectangle. The output is saved as `tape_dispense.gcode` unless you choose a different name. Use `--feed` to change the movement feed rate and `--extrusion` to change the dispensing amount per segment.

## Tests

```sh
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

The tests check relative paths, closed shapes, coordinate scaling, dispensing mode, and rejection of unsupported path commands.
