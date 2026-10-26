import pytest
from tape_gcode import parse_path, convert

def test_relative_and_closed():
    assert parse_path('M0,0 l10,0 0,10 z') == [(0,0),(10,0),(10,10),(0,0)]

@pytest.mark.parametrize('data',['M0 0 C1 2 3 4 5 6','M0 0 L1','M0 0 M2 2','L0 0 L1 1'])
def test_reject_unsupported(data):
    with pytest.raises(ValueError):
        parse_path(data)

def test_gcode(tmp_path):
    source = tmp_path/'shape.svg'
    source.write_text('<svg><path d="M0 0 L100 0 L100 50"/></svg>')
    output = tmp_path/'out.gcode'
    convert(source,output)
    text = output.read_text()
    assert 'M83' in text
    assert 'G1 X26.400 Y13.200 E10 F1500' in text
    assert text.endswith('M104 S0\n')
