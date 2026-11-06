{
  "format": "solidcraft/48",
  "name": "rail-shade",
  "units": "mm",
  "params": [
    {
      "name": "socket_d",
      "expr": "45 mm",
      "unit": "mm",
      "comment": "the socket's body: a guess until it's measured",
      "model": false
    },
    {
      "name": "socket_l",
      "expr": "60 mm",
      "unit": "mm",
      "comment": "the socket's length, its top to where the bulb starts",
      "model": false
    },
    {
      "name": "bulb_d",
      "expr": "121 mm",
      "unit": "mm",
      "comment": "the bulb's widest: a guess until it's measured",
      "model": false
    },
    {
      "name": "bulb_l",
      "expr": "100 mm",
      "unit": "mm",
      "comment": "the bulb's length, from the socket to its face",
      "model": false
    },
    {
      "name": "gap",
      "expr": "12 mm",
      "unit": "mm",
      "comment": "air round the lamp: at least 10 mm",
      "model": false
    },
    {
      "name": "shade_t",
      "expr": "2.4 mm",
      "unit": "mm",
      "comment": "the shade's wall",
      "model": false
    },
    {
      "name": "top_t",
      "expr": "3 mm",
      "unit": "mm",
      "comment": "the shade's top, which rests on the stem's lugs",
      "model": false
    },
    {
      "name": "drop",
      "expr": "8 mm",
      "unit": "mm",
      "comment": "the socket's top below the shade's top: the lugs, then air",
      "model": false
    },
    {
      "name": "rim",
      "expr": "5 mm",
      "unit": "mm",
      "comment": "the shade's rim below the bulb's face",
      "model": false
    },
    {
      "name": "vent_d",
      "expr": "8 mm",
      "unit": "mm",
      "comment": "each vent through the shade's top",
      "model": false
    },
    {
      "name": "stem_d",
      "expr": "22 mm",
      "unit": "mm",
      "comment": "the tip's stem (rail-arm-tip)",
      "model": false
    },
    {
      "name": "lug_w",
      "expr": "5 mm",
      "unit": "mm",
      "comment": "each lug on the stem (rail-arm-tip)",
      "model": false
    },
    {
      "name": "lug_h",
      "expr": "3 mm",
      "unit": "mm",
      "comment": "how far each lug stands out (rail-arm-tip)",
      "model": false
    },
    {
      "name": "fit",
      "expr": "0.4 mm",
      "unit": "mm",
      "comment": "round the stem and through the notches",
      "model": false
    },
    {
      "name": "r_top",
      "expr": "socket_d / 2 + gap",
      "unit": "mm",
      "comment": "the shade's inside at its top",
      "model": false
    },
    {
      "name": "r_bulb",
      "expr": "bulb_d / 2 + gap",
      "unit": "mm",
      "comment": "the shade's inside round the bulb",
      "model": false
    },
    {
      "name": "vent_r",
      "expr": "r_top - vent_d / 2 - 3 mm",
      "unit": "mm",
      "comment": "the vents' ring in the shade's top, between the stem's notches and the wall",
      "model": false
    },
    {
      "name": "shoulder_z",
      "expr": "top_t + drop + socket_l",
      "unit": "mm",
      "comment": "where the cone meets the cylinder: the bulb's start",
      "model": false
    },
    {
      "name": "height",
      "expr": "shoulder_z + bulb_l + rim",
      "unit": "mm",
      "comment": "the shade's height",
      "model": false
    }
  ],
  "features": [
    {
      "id": 1,
      "name": "Cylinder1",
      "suppressed": false,
      "body_names": [
        "Shade"
      ],
      "param_names": [
        "d1",
        "d2"
      ],
      "type": "cylinder",
      "base": [
        0.0,
        0.0,
        0.0
      ],
      "axis": [
        0.0,
        0.0,
        1.0
      ],
      "radius": "(2 * (r_top + shade_t)) / 2",
      "height": "top_t",
      "operation": "new_body"
    },
    {
      "id": 2,
      "name": "Cone1",
      "suppressed": false,
      "param_names": [
        "d3",
        "d4",
        "d5"
      ],
      "participants": [
        "Shade"
      ],
      "type": "cone",
      "base": [
        0.0,
        0.0,
        "top_t"
      ],
      "axis": [
        0.0,
        0.0,
        1.0
      ],
      "radius": "(2 * (r_top + shade_t)) / 2",
      "top_radius": "(2 * (r_bulb + shade_t)) / 2",
      "height": "shoulder_z - top_t",
      "operation": "join"
    },
    {
      "id": 3,
      "name": "Cylinder2",
      "suppressed": false,
      "param_names": [
        "d6",
        "d7"
      ],
      "participants": [
        "Shade"
      ],
      "type": "cylinder",
      "base": [
        0.0,
        0.0,
        "shoulder_z"
      ],
      "axis": [
        0.0,
        0.0,
        1.0
      ],
      "radius": "(2 * (r_bulb + shade_t)) / 2",
      "height": "height - shoulder_z",
      "operation": "join"
    },
    {
      "id": 4,
      "name": "Cone2",
      "suppressed": false,
      "param_names": [
        "d8",
        "d9",
        "d10"
      ],
      "participants": [
        "Shade"
      ],
      "type": "cone",
      "base": [
        0.0,
        0.0,
        "top_t"
      ],
      "axis": [
        0.0,
        0.0,
        1.0
      ],
      "radius": "(2 * r_top) / 2",
      "top_radius": "(2 * r_bulb) / 2",
      "height": "shoulder_z - top_t",
      "operation": "cut"
    },
    {
      "id": 5,
      "name": "Cylinder3",
      "suppressed": false,
      "param_names": [
        "d11",
        "d12"
      ],
      "participants": [
        "Shade"
      ],
      "type": "cylinder",
      "base": [
        0.0,
        0.0,
        "shoulder_z"
      ],
      "axis": [
        0.0,
        0.0,
        1.0
      ],
      "radius": "(2 * r_bulb) / 2",
      "height": "height - shoulder_z + 1 mm",
      "operation": "cut"
    },
    {
      "id": 6,
      "name": "Cylinder4",
      "suppressed": false,
      "param_names": [
        "d13",
        "d14"
      ],
      "participants": [
        "Shade"
      ],
      "type": "cylinder",
      "base": [
        0.0,
        0.0,
        "-1 mm"
      ],
      "axis": [
        0.0,
        0.0,
        1.0
      ],
      "radius": "(stem_d + fit) / 2",
      "height": "top_t + 2 mm",
      "operation": "cut"
    },
    {
      "id": 7,
      "name": "Box1",
      "suppressed": false,
      "param_names": [
        "d15",
        "d16",
        "d17"
      ],
      "participants": [
        "Shade"
      ],
      "type": "box",
      "corner": [
        "-(lug_w + fit) / 2",
        "-stem_d / 2 - lug_h - fit",
        "-1 mm"
      ],
      "length": "lug_w + fit",
      "width": "stem_d + 2 * (lug_h + fit)",
      "height": "top_t + 2 mm",
      "operation": "cut"
    },
    {
      "id": 8,
      "name": "Cylinder5",
      "suppressed": false,
      "param_names": [
        "d18",
        "d19"
      ],
      "participants": [
        "Shade"
      ],
      "type": "cylinder",
      "base": [
        "vent_r * 0.866025",
        "vent_r * 0.5",
        "-1 mm"
      ],
      "axis": [
        0.0,
        0.0,
        1.0
      ],
      "radius": "(vent_d) / 2",
      "height": "top_t + 2 mm",
      "operation": "cut"
    },
    {
      "id": 9,
      "name": "Cylinder6",
      "suppressed": false,
      "param_names": [
        "d20",
        "d21"
      ],
      "participants": [
        "Shade"
      ],
      "type": "cylinder",
      "base": [
        "vent_r * 0.0",
        "vent_r * 1.0",
        "-1 mm"
      ],
      "axis": [
        0.0,
        0.0,
        1.0
      ],
      "radius": "(vent_d) / 2",
      "height": "top_t + 2 mm",
      "operation": "cut"
    },
    {
      "id": 10,
      "name": "Cylinder7",
      "suppressed": false,
      "param_names": [
        "d22",
        "d23"
      ],
      "participants": [
        "Shade"
      ],
      "type": "cylinder",
      "base": [
        "vent_r * -0.866025",
        "vent_r * 0.5",
        "-1 mm"
      ],
      "axis": [
        0.0,
        0.0,
        1.0
      ],
      "radius": "(vent_d) / 2",
      "height": "top_t + 2 mm",
      "operation": "cut"
    },
    {
      "id": 11,
      "name": "Cylinder8",
      "suppressed": false,
      "param_names": [
        "d24",
        "d25"
      ],
      "participants": [
        "Shade"
      ],
      "type": "cylinder",
      "base": [
        "vent_r * -0.866025",
        "vent_r * -0.5",
        "-1 mm"
      ],
      "axis": [
        0.0,
        0.0,
        1.0
      ],
      "radius": "(vent_d) / 2",
      "height": "top_t + 2 mm",
      "operation": "cut"
    },
    {
      "id": 12,
      "name": "Cylinder9",
      "suppressed": false,
      "param_names": [
        "d26",
        "d27"
      ],
      "participants": [
        "Shade"
      ],
      "type": "cylinder",
      "base": [
        "vent_r * -0.0",
        "vent_r * -1.0",
        "-1 mm"
      ],
      "axis": [
        0.0,
        0.0,
        1.0
      ],
      "radius": "(vent_d) / 2",
      "height": "top_t + 2 mm",
      "operation": "cut"
    },
    {
      "id": 13,
      "name": "Cylinder10",
      "suppressed": false,
      "param_names": [
        "d28",
        "d29"
      ],
      "participants": [
        "Shade"
      ],
      "type": "cylinder",
      "base": [
        "vent_r * 0.866025",
        "vent_r * -0.5",
        "-1 mm"
      ],
      "axis": [
        0.0,
        0.0,
        1.0
      ],
      "radius": "(vent_d) / 2",
      "height": "top_t + 2 mm",
      "operation": "cut"
    }
  ],
  "next_id": 14,
  "next_component_color_index": 0
}