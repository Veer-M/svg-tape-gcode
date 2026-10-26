import argparse
import math
from pathlib import Path
import re
import xml.etree.ElementTree as ET

TOKEN = re.compile(r'[MLZmlz]|[-+]?(?:\d*\.\d+|\d+\.?\d*)(?:[eE][-+]?\d+)?')

def parse_path(data):
    tokens = TOKEN.findall(data)
    if re.sub(TOKEN, '', data).replace(',', '').strip():
        raise ValueError('Only M, L, and Z path commands are supported')
    points = []
    i = 0
    command = None
    closed = False
    while i < len(tokens):
        if tokens[i].isalpha():
            command = tokens[i]
            i += 1
            if command.upper() == 'Z':
                if not points or i != len(tokens):
                    raise ValueError('Z must close one nonempty path')
                points.append(points[0])
                closed = True
                break
            if command.upper() == 'M' and points:
                raise ValueError('Multiple subpaths are not supported')
            if i == len(tokens):
                raise ValueError('Missing coordinates')
        if command is None or not points and command.upper() != 'M':
            raise ValueError('Path must begin with M')
        if i + 1 >= len(tokens) or tokens[i].isalpha() or tokens[i+1].isalpha():
            raise ValueError('Coordinates must come in X,Y pairs')
        x, y = float(tokens[i]), float(tokens[i+1])
        if not math.isfinite(x) or not math.isfinite(y):
            raise ValueError('Coordinates must be finite')
        if command.islower() and points:
            x, y = x + points[-1][0], y + points[-1][1]
        points.append((x,y))
        i += 2
        if command.upper() == 'M':
            command = 'l' if command.islower() else 'L'
    if len(points) < 2 or (closed and len(points) < 4):
        raise ValueError('Path needs at least two points, or three before closing')
    return points

def convert(svg, output='tape_dispense.gcode', scale=0.264, feed=1500, extrusion=10):
    if not all(math.isfinite(v) and v > 0 for v in (scale,feed,extrusion)):
        raise ValueError('Scale, feed, and extrusion must be positive and finite')
    root = ET.parse(svg).getroot()
    paths = [e for e in root.iter() if e.tag.split('}')[-1] == 'path']
    if len(paths) != 1:
        raise ValueError('SVG must contain exactly one path')
    if any('transform' in e.attrib for e in root.iter()):
        raise ValueError('Flatten SVG transforms before converting')
    points = [(x*scale,y*scale) for x,y in parse_path(paths[0].get('d',''))]
    lines = ['G21','G90','M83','G28',f'G0 X{points[0][0]:.3f} Y{points[0][1]:.3f} F{feed:g}']
    for x,y in points[1:]:
        lines.append(f'G1 X{x:.3f} Y{y:.3f} E{extrusion:g} F{feed:g}')
    lines.append('M104 S0')
    Path(output).write_text('\n'.join(lines)+'\n', encoding='utf-8')
    return points

def main():
    parser = argparse.ArgumentParser(description='Convert one SVG line path to tape G-code')
    parser.add_argument('svg', nargs='?', default='mount_profile.svg')
    parser.add_argument('--output', default='tape_dispense.gcode')
    parser.add_argument('--scale', type=float, default=0.264)
    parser.add_argument('--feed', type=float, default=1500)
    parser.add_argument('--extrusion', type=float, default=10)
    args = parser.parse_args()
    points = convert(args.svg,args.output,args.scale,args.feed,args.extrusion)
    print(f'Wrote {len(points)-1} dispensing segments to {args.output}')

if __name__ == '__main__':
    main()
