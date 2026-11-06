{
  "format": "solidcraft/48",
  "name": "dowel-fit-coupon",
  "units": "mm",
  "params": [
    {
      "name": "dowel_d",
      "expr": "25.4 mm",
      "unit": "mm",
      "comment": "the dowel's nominal diameter: 1 inch",
      "model": false
    },
    {
      "name": "step",
      "expr": "0.2 mm",
      "unit": "mm",
      "comment": "clearance added per hole: hole k is dowel_d + k * step",
      "model": false
    },
    {
      "name": "wall",
      "expr": "4 mm",
      "unit": "mm",
      "comment": "plastic between neighbouring holes",
      "model": false
    },
    {
      "name": "margin",
      "expr": "8 mm",
      "unit": "mm",
      "comment": "the band along the front that carries the marker dots",
      "model": false
    },
    {
      "name": "bar_h",
      "expr": "12 mm",
      "unit": "mm",
      "comment": "the bar's height, so each hole is this deep",
      "model": false
    },
    {
      "name": "dot_d",
      "expr": "2 mm",
      "unit": "mm",
      "comment": "a marker dot's diameter",
      "model": false
    },
    {
      "name": "dot_depth",
      "expr": "0.6 mm",
      "unit": "mm",
      "comment": "a marker dot's depth",
      "model": false
    },
    {
      "name": "pitch",
      "expr": "dowel_d + 4 * step + wall",
      "unit": "mm",
      "comment": "centre to centre between holes",
      "model": false
    },
    {
      "name": "bar_l",
      "expr": "4 * pitch + wall",
      "unit": "mm",
      "comment": "the bar's length",
      "model": false
    },
    {
      "name": "bar_w",
      "expr": "margin + pitch",
      "unit": "mm",
      "comment": "the bar's width",
      "model": false
    }
  ],
  "features": [
    {
      "id": 1,
      "name": "Box1",
      "suppressed": false,
      "body_names": [
        "Coupon"
      ],
      "param_names": [
        "d1",
        "d2",
        "d3"
      ],
      "type": "box",
      "corner": [
        0.0,
        0.0,
        0.0
      ],
      "length": "bar_l",
      "width": "bar_w",
      "height": "bar_h",
      "operation": "new_body"
    },
    {
      "id": 2,
      "name": "Cylinder1",
      "suppressed": false,
      "body_names": [
        "Hole 1"
      ],
      "param_names": [
        "d4",
        "d5"
      ],
      "type": "cylinder",
      "base": [
        "wall / 2 + 0.5 * pitch",
        "margin + pitch / 2",
        0.0
      ],
      "axis": [
        0.0,
        0.0,
        1.0
      ],
      "radius": "(dowel_d + 1 * step) / 2",
      "height": "bar_h",
      "operation": "new_body"
    },
    {
      "id": 3,
      "name": "Cylinder2",
      "suppressed": false,
      "body_names": [
        "Hole 1 dot 1"
      ],
      "param_names": [
        "d6",
        "d7"
      ],
      "type": "cylinder",
      "base": [
        "wall / 2 + 0.5 * pitch",
        "margin / 2",
        "bar_h - dot_depth"
      ],
      "axis": [
        0.0,
        0.0,
        1.0
      ],
      "radius": "(dot_d) / 2",
      "height": "dot_depth",
      "operation": "new_body"
    },
    {
      "id": 4,
      "name": "Cylinder3",
      "suppressed": false,
      "body_names": [
        "Hole 2"
      ],
      "param_names": [
        "d8",
        "d9"
      ],
      "type": "cylinder",
      "base": [
        "wall / 2 + 1.5 * pitch",
        "margin + pitch / 2",
        0.0
      ],
      "axis": [
        0.0,
        0.0,
        1.0
      ],
      "radius": "(dowel_d + 2 * step) / 2",
      "height": "bar_h",
      "operation": "new_body"
    },
    {
      "id": 5,
      "name": "Cylinder4",
      "suppressed": false,
      "body_names": [
        "Hole 2 dot 1"
      ],
      "param_names": [
        "d10",
        "d11"
      ],
      "type": "cylinder",
      "base": [
        "wall / 2 + 1.5 * pitch + -0.5 * 3 mm",
        "margin / 2",
        "bar_h - dot_depth"
      ],
      "axis": [
        0.0,
        0.0,
        1.0
      ],
      "radius": "(dot_d) / 2",
      "height": "dot_depth",
      "operation": "new_body"
    },
    {
      "id": 6,
      "name": "Cylinder5",
      "suppressed": false,
      "body_names": [
        "Hole 2 dot 2"
      ],
      "param_names": [
        "d12",
        "d13"
      ],
      "type": "cylinder",
      "base": [
        "wall / 2 + 1.5 * pitch + 0.5 * 3 mm",
        "margin / 2",
        "bar_h - dot_depth"
      ],
      "axis": [
        0.0,
        0.0,
        1.0
      ],
      "radius": "(dot_d) / 2",
      "height": "dot_depth",
      "operation": "new_body"
    },
    {
      "id": 7,
      "name": "Cylinder6",
      "suppressed": false,
      "body_names": [
        "Hole 3"
      ],
      "param_names": [
        "d14",
        "d15"
      ],
      "type": "cylinder",
      "base": [
        "wall / 2 + 2.5 * pitch",
        "margin + pitch / 2",
        0.0
      ],
      "axis": [
        0.0,
        0.0,
        1.0
      ],
      "radius": "(dowel_d + 3 * step) / 2",
      "height": "bar_h",
      "operation": "new_body"
    },
    {
      "id": 8,
      "name": "Cylinder7",
      "suppressed": false,
      "body_names": [
        "Hole 3 dot 1"
      ],
      "param_names": [
        "d16",
        "d17"
      ],
      "type": "cylinder",
      "base": [
        "wall / 2 + 2.5 * pitch + -1 * 3 mm",
        "margin / 2",
        "bar_h - dot_depth"
      ],
      "axis": [
        0.0,
        0.0,
        1.0
      ],
      "radius": "(dot_d) / 2",
      "height": "dot_depth",
      "operation": "new_body"
    },
    {
      "id": 9,
      "name": "Cylinder8",
      "suppressed": false,
      "body_names": [
        "Hole 3 dot 2"
      ],
      "param_names": [
        "d18",
        "d19"
      ],
      "type": "cylinder",
      "base": [
        "wall / 2 + 2.5 * pitch",
        "margin / 2",
        "bar_h - dot_depth"
      ],
      "axis": [
        0.0,
        0.0,
        1.0
      ],
      "radius": "(dot_d) / 2",
      "height": "dot_depth",
      "operation": "new_body"
    },
    {
      "id": 10,
      "name": "Cylinder9",
      "suppressed": false,
      "body_names": [
        "Hole 3 dot 3"
      ],
      "param_names": [
        "d20",
        "d21"
      ],
      "type": "cylinder",
      "base": [
        "wall / 2 + 2.5 * pitch + 1 * 3 mm",
        "margin / 2",
        "bar_h - dot_depth"
      ],
      "axis": [
        0.0,
        0.0,
        1.0
      ],
      "radius": "(dot_d) / 2",
      "height": "dot_depth",
      "operation": "new_body"
    },
    {
      "id": 11,
      "name": "Cylinder10",
      "suppressed": false,
      "body_names": [
        "Hole 4"
      ],
      "param_names": [
        "d22",
        "d23"
      ],
      "type": "cylinder",
      "base": [
        "wall / 2 + 3.5 * pitch",
        "margin + pitch / 2",
        0.0
      ],
      "axis": [
        0.0,
        0.0,
        1.0
      ],
      "radius": "(dowel_d + 4 * step) / 2",
      "height": "bar_h",
      "operation": "new_body"
    },
    {
      "id": 12,
      "name": "Cylinder11",
      "suppressed": false,
      "body_names": [
        "Hole 4 dot 1"
      ],
      "param_names": [
        "d24",
        "d25"
      ],
      "type": "cylinder",
      "base": [
        "wall / 2 + 3.5 * pitch + -1.5 * 3 mm",
        "margin / 2",
        "bar_h - dot_depth"
      ],
      "axis": [
        0.0,
        0.0,
        1.0
      ],
      "radius": "(dot_d) / 2",
      "height": "dot_depth",
      "operation": "new_body"
    },
    {
      "id": 13,
      "name": "Cylinder12",
      "suppressed": false,
      "body_names": [
        "Hole 4 dot 2"
      ],
      "param_names": [
        "d26",
        "d27"
      ],
      "type": "cylinder",
      "base": [
        "wall / 2 + 3.5 * pitch + -0.5 * 3 mm",
        "margin / 2",
        "bar_h - dot_depth"
      ],
      "axis": [
        0.0,
        0.0,
        1.0
      ],
      "radius": "(dot_d) / 2",
      "height": "dot_depth",
      "operation": "new_body"
    },
    {
      "id": 14,
      "name": "Cylinder13",
      "suppressed": false,
      "body_names": [
        "Hole 4 dot 3"
      ],
      "param_names": [
        "d28",
        "d29"
      ],
      "type": "cylinder",
      "base": [
        "wall / 2 + 3.5 * pitch + 0.5 * 3 mm",
        "margin / 2",
        "bar_h - dot_depth"
      ],
      "axis": [
        0.0,
        0.0,
        1.0
      ],
      "radius": "(dot_d) / 2",
      "height": "dot_depth",
      "operation": "new_body"
    },
    {
      "id": 15,
      "name": "Cylinder14",
      "suppressed": false,
      "body_names": [
        "Hole 4 dot 4"
      ],
      "param_names": [
        "d30",
        "d31"
      ],
      "type": "cylinder",
      "base": [
        "wall / 2 + 3.5 * pitch + 1.5 * 3 mm",
        "margin / 2",
        "bar_h - dot_depth"
      ],
      "axis": [
        0.0,
        0.0,
        1.0
      ],
      "radius": "(dot_d) / 2",
      "height": "dot_depth",
      "operation": "new_body"
    },
    {
      "id": 16,
      "name": "Combine1",
      "suppressed": false,
      "type": "combine",
      "target": "Coupon",
      "tools": [
        "Hole 1",
        "Hole 1 dot 1",
        "Hole 2",
        "Hole 2 dot 1",
        "Hole 2 dot 2",
        "Hole 3",
        "Hole 3 dot 1",
        "Hole 3 dot 2",
        "Hole 3 dot 3",
        "Hole 4",
        "Hole 4 dot 1",
        "Hole 4 dot 2",
        "Hole 4 dot 3",
        "Hole 4 dot 4"
      ],
      "operation": "cut",
      "keep_tools": false
    }
  ],
  "next_id": 17,
  "next_component_color_index": 0
}