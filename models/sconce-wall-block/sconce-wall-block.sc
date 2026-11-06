{
  "format": "solidcraft/48",
  "name": "sconce-wall-block",
  "units": "mm",
  "params": [
    {
      "name": "dowel_d",
      "expr": "25.4 mm",
      "unit": "mm",
      "comment": "the arm's dowel: 1 inch as saved; the page offers 3/4 in and 25 mm",
      "model": false
    },
    {
      "name": "clearance",
      "expr": "0.4 mm",
      "unit": "mm",
      "comment": "added to the dowel for the socket: the coupon's hole that fit",
      "model": false
    },
    {
      "name": "socket_depth",
      "expr": "54 mm",
      "unit": "mm",
      "comment": "at least 51 mm (2 inches), so the joint carries the arm's moment",
      "model": false
    },
    {
      "name": "boss_wall",
      "expr": "6 mm",
      "unit": "mm",
      "comment": "plastic around the socket",
      "model": false
    },
    {
      "name": "plate_t",
      "expr": "10 mm",
      "unit": "mm",
      "comment": "the wall plate's thickness, behind the socket",
      "model": false
    },
    {
      "name": "plate_w",
      "expr": "50 mm",
      "unit": "mm",
      "comment": "the wall plate's width",
      "model": false
    },
    {
      "name": "screw_spacing",
      "expr": "110 mm",
      "unit": "mm",
      "comment": "at least 100 mm between the screws, so the top one pulls under 54 N",
      "model": false
    },
    {
      "name": "plate_h",
      "expr": "screw_spacing + 30 mm",
      "unit": "mm",
      "comment": "the wall plate's height",
      "model": false
    },
    {
      "name": "screw_d",
      "expr": "5 mm",
      "unit": "mm",
      "comment": "fits #8 and #10 wood screws and 3/16 in toggle bolts; 6.6 mm for 1/4 in",
      "model": false
    },
    {
      "name": "head_d",
      "expr": "10.5 mm",
      "unit": "mm",
      "comment": "the counterbore that sinks each screw's head below the face",
      "model": false
    },
    {
      "name": "head_depth",
      "expr": "5 mm",
      "unit": "mm",
      "comment": "the counterbore's depth: a screw head, then a cap",
      "model": false
    },
    {
      "name": "cap_h",
      "expr": "2 mm",
      "unit": "mm",
      "comment": "a printed cap's height, pressed in over the screw head",
      "model": false
    },
    {
      "name": "bolt_d",
      "expr": "6.6 mm",
      "unit": "mm",
      "comment": "clearance for an M6 bolt through the boss and the dowel",
      "model": false
    },
    {
      "name": "socket_d",
      "expr": "dowel_d + clearance",
      "unit": "mm",
      "comment": "the socket's diameter",
      "model": false
    },
    {
      "name": "boss_d",
      "expr": "socket_d + 2 * boss_wall",
      "unit": "mm",
      "comment": "the boss around the socket",
      "model": false
    }
  ],
  "features": [
    {
      "id": 1,
      "name": "Box1",
      "suppressed": false,
      "body_names": [
        "Wall block"
      ],
      "param_names": [
        "d1",
        "d2",
        "d3"
      ],
      "type": "box",
      "corner": [
        0.0,
        "-plate_w / 2",
        "-plate_h / 2"
      ],
      "length": "plate_t",
      "width": "plate_w",
      "height": "plate_h",
      "operation": "new_body"
    },
    {
      "id": 2,
      "name": "Cylinder1",
      "suppressed": false,
      "body_names": [
        "Boss"
      ],
      "param_names": [
        "d4",
        "d5"
      ],
      "type": "cylinder",
      "base": [
        0.0,
        0.0,
        0.0
      ],
      "axis": [
        1.0,
        0.0,
        0.0
      ],
      "radius": "(boss_d) / 2",
      "height": "plate_t + socket_depth",
      "operation": "new_body"
    },
    {
      "id": 3,
      "name": "Combine1",
      "suppressed": false,
      "type": "combine",
      "target": "Wall block",
      "tools": [
        "Boss"
      ],
      "operation": "join",
      "keep_tools": false
    },
    {
      "id": 4,
      "name": "Cylinder2",
      "suppressed": false,
      "body_names": [
        "Socket"
      ],
      "param_names": [
        "d6",
        "d7"
      ],
      "type": "cylinder",
      "base": [
        "plate_t",
        0.0,
        0.0
      ],
      "axis": [
        1.0,
        0.0,
        0.0
      ],
      "radius": "(socket_d) / 2",
      "height": "socket_depth",
      "operation": "new_body"
    },
    {
      "id": 5,
      "name": "Cylinder3",
      "suppressed": false,
      "body_names": [
        "Bolt hole"
      ],
      "param_names": [
        "d8",
        "d9"
      ],
      "type": "cylinder",
      "base": [
        "plate_t + socket_depth / 2",
        0.0,
        "-boss_d / 2 - 1 mm"
      ],
      "axis": [
        0.0,
        0.0,
        1.0
      ],
      "radius": "(bolt_d) / 2",
      "height": "boss_d + 2 mm",
      "operation": "new_body"
    },
    {
      "id": 6,
      "name": "Cylinder4",
      "suppressed": false,
      "body_names": [
        "Top screw"
      ],
      "param_names": [
        "d10",
        "d11"
      ],
      "type": "cylinder",
      "base": [
        0.0,
        0.0,
        "screw_spacing / 2"
      ],
      "axis": [
        1.0,
        0.0,
        0.0
      ],
      "radius": "(screw_d) / 2",
      "height": "plate_t",
      "operation": "new_body"
    },
    {
      "id": 7,
      "name": "Cylinder5",
      "suppressed": false,
      "body_names": [
        "Top counterbore"
      ],
      "param_names": [
        "d12",
        "d13"
      ],
      "type": "cylinder",
      "base": [
        "plate_t - head_depth",
        0.0,
        "screw_spacing / 2"
      ],
      "axis": [
        1.0,
        0.0,
        0.0
      ],
      "radius": "(head_d) / 2",
      "height": "head_depth",
      "operation": "new_body"
    },
    {
      "id": 8,
      "name": "Cylinder6",
      "suppressed": false,
      "body_names": [
        "Bottom screw"
      ],
      "param_names": [
        "d14",
        "d15"
      ],
      "type": "cylinder",
      "base": [
        0.0,
        0.0,
        "-screw_spacing / 2"
      ],
      "axis": [
        1.0,
        0.0,
        0.0
      ],
      "radius": "(screw_d) / 2",
      "height": "plate_t",
      "operation": "new_body"
    },
    {
      "id": 9,
      "name": "Cylinder7",
      "suppressed": false,
      "body_names": [
        "Bottom counterbore"
      ],
      "param_names": [
        "d16",
        "d17"
      ],
      "type": "cylinder",
      "base": [
        "plate_t - head_depth",
        0.0,
        "-screw_spacing / 2"
      ],
      "axis": [
        1.0,
        0.0,
        0.0
      ],
      "radius": "(head_d) / 2",
      "height": "head_depth",
      "operation": "new_body"
    },
    {
      "id": 10,
      "name": "Combine2",
      "suppressed": false,
      "type": "combine",
      "target": "Wall block",
      "tools": [
        "Socket",
        "Bolt hole",
        "Top screw",
        "Top counterbore",
        "Bottom screw",
        "Bottom counterbore"
      ],
      "operation": "cut",
      "keep_tools": false
    },
    {
      "id": 11,
      "name": "Cylinder8",
      "suppressed": false,
      "body_names": [
        "Cap 1"
      ],
      "param_names": [
        "d18",
        "d19"
      ],
      "type": "cylinder",
      "base": [
        0.0,
        "plate_w / 2 + 10 mm",
        "-plate_h / 2"
      ],
      "axis": [
        0.0,
        0.0,
        1.0
      ],
      "radius": "(head_d - 0.2 mm) / 2",
      "height": "cap_h",
      "operation": "new_body"
    },
    {
      "id": 12,
      "name": "Cylinder9",
      "suppressed": false,
      "body_names": [
        "Cap 2"
      ],
      "param_names": [
        "d20",
        "d21"
      ],
      "type": "cylinder",
      "base": [
        0.0,
        "plate_w / 2 + 25 mm",
        "-plate_h / 2"
      ],
      "axis": [
        0.0,
        0.0,
        1.0
      ],
      "radius": "(head_d - 0.2 mm) / 2",
      "height": "cap_h",
      "operation": "new_body"
    }
  ],
  "next_id": 13,
  "next_component_color_index": 0
}