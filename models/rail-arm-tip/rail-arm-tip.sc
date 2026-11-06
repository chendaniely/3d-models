{
  "format": "solidcraft/48",
  "name": "rail-arm-tip",
  "units": "mm",
  "params": [
    {
      "name": "dowel_d",
      "expr": "25.4 mm",
      "unit": "mm",
      "comment": "the rail's and the arm's dowel: 1 inch as saved; the page offers 3/4 in and 25 mm",
      "model": false
    },
    {
      "name": "clearance",
      "expr": "0.4 mm",
      "unit": "mm",
      "comment": "added to the dowel for every bore: the coupon's hole that fit",
      "model": false
    },
    {
      "name": "bore_d",
      "expr": "dowel_d + clearance",
      "unit": "mm",
      "comment": "every cup's and socket's bore",
      "model": false
    },
    {
      "name": "cap_wall",
      "expr": "7 mm",
      "unit": "mm",
      "comment": "plastic round the dowel, room above for the wedge's groove",
      "model": false
    },
    {
      "name": "cap_d",
      "expr": "bore_d + 2 * cap_wall",
      "unit": "mm",
      "comment": "the cap's outside",
      "model": false
    },
    {
      "name": "cap_l",
      "expr": "50 mm",
      "unit": "mm",
      "comment": "the cap's length along the arm",
      "model": false
    },
    {
      "name": "bore_depth",
      "expr": "42 mm",
      "unit": "mm",
      "comment": "how far the arm goes into the cap",
      "model": false
    },
    {
      "name": "groove_w",
      "expr": "8 mm",
      "unit": "mm",
      "comment": "the wedge's groove along the top of the bore",
      "model": false
    },
    {
      "name": "taper",
      "expr": "0.04",
      "unit": "",
      "comment": "each wedge's and its groove's slope, 1 in 25",
      "model": false
    },
    {
      "name": "room_in",
      "expr": "2 mm",
      "unit": "mm",
      "comment": "the groove's depth above the dowel at the bore's end",
      "model": false
    },
    {
      "name": "wedge_l",
      "expr": "bore_depth + 5 mm",
      "unit": "mm",
      "comment": "the wedge's length",
      "model": false
    },
    {
      "name": "wedge_in",
      "expr": "room_in + clearance / 2 + 15 mm * taper",
      "unit": "mm",
      "comment": "the wedge's thin end: seated 15 mm short of the bore's end on a nominal dowel",
      "model": false
    },
    {
      "name": "cord_d",
      "expr": "6 mm",
      "unit": "mm",
      "comment": "the light's cord: a guess until it's measured",
      "model": false
    },
    {
      "name": "free_d",
      "expr": "cord_d + 0.5 mm",
      "unit": "mm",
      "comment": "the stem's bore above its grip",
      "model": false
    },
    {
      "name": "slot_w",
      "expr": "cord_d + 0.2 mm",
      "unit": "mm",
      "comment": "the slot into the free bore: the cord slides in",
      "model": false
    },
    {
      "name": "grip_d",
      "expr": "cord_d - 0.6 mm",
      "unit": "mm",
      "comment": "the stem's grip: a hole narrower than the cord",
      "model": false
    },
    {
      "name": "press_w",
      "expr": "cord_d - 1.5 mm",
      "unit": "mm",
      "comment": "the slot the cord is pressed through into the grip",
      "model": false
    },
    {
      "name": "grip_l",
      "expr": "10 mm",
      "unit": "mm",
      "comment": "the grip's length, at the stem's foot",
      "model": false
    },
    {
      "name": "keel_w",
      "expr": "cord_d + 6 mm",
      "unit": "mm",
      "comment": "the keel under the cap, round the cord's channel",
      "model": false
    },
    {
      "name": "keel_z",
      "expr": "-(bore_d / 2 + cord_d + 4.5 mm)",
      "unit": "mm",
      "comment": "the keel's underside",
      "model": false
    },
    {
      "name": "mouth_w",
      "expr": "cord_d - 1 mm",
      "unit": "mm",
      "comment": "the keel channel's mouth: the cord snaps in",
      "model": false
    },
    {
      "name": "stem_d",
      "expr": "22 mm",
      "unit": "mm",
      "comment": "the stem down to the light",
      "model": false
    },
    {
      "name": "stem_l",
      "expr": "40 mm",
      "unit": "mm",
      "comment": "the stem's length below the keel",
      "model": false
    },
    {
      "name": "stem_x",
      "expr": "cap_l - stem_d / 2 - 3 mm",
      "unit": "mm",
      "comment": "the stem's axis along the arm",
      "model": false
    },
    {
      "name": "foot_z",
      "expr": "keel_z - stem_l",
      "unit": "mm",
      "comment": "the stem's foot",
      "model": false
    },
    {
      "name": "lug_w",
      "expr": "5 mm",
      "unit": "mm",
      "comment": "each lug the shade turns onto",
      "model": false
    },
    {
      "name": "lug_h",
      "expr": "3 mm",
      "unit": "mm",
      "comment": "how far each lug stands out from the stem",
      "model": false
    },
    {
      "name": "lug_t",
      "expr": "3 mm",
      "unit": "mm",
      "comment": "each lug's height",
      "model": false
    },
    {
      "name": "clip_t",
      "expr": "8 mm",
      "unit": "mm",
      "comment": "a cord clip's length along the arm",
      "model": false
    }
  ],
  "features": [
    {
      "id": 1,
      "name": "Cylinder1",
      "suppressed": false,
      "body_names": [
        "Arm tip"
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
        1.0,
        0.0,
        0.0
      ],
      "radius": "(cap_d) / 2",
      "height": "cap_l",
      "operation": "new_body"
    },
    {
      "id": 2,
      "name": "Box1",
      "suppressed": false,
      "param_names": [
        "d3",
        "d4",
        "d5"
      ],
      "participants": [
        "Arm tip"
      ],
      "type": "box",
      "corner": [
        0.0,
        "-keel_w / 2",
        "keel_z"
      ],
      "length": "cap_l",
      "width": "keel_w",
      "height": "-keel_z",
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
        "Arm tip"
      ],
      "type": "cylinder",
      "base": [
        "stem_x",
        0.0,
        "foot_z"
      ],
      "axis": [
        0.0,
        0.0,
        1.0
      ],
      "radius": "(stem_d) / 2",
      "height": "stem_l + 2 mm",
      "operation": "join"
    },
    {
      "id": 4,
      "name": "Box2",
      "suppressed": false,
      "param_names": [
        "d8",
        "d9",
        "d10"
      ],
      "participants": [
        "Arm tip"
      ],
      "type": "box",
      "corner": [
        "stem_x - lug_w / 2",
        "-stem_d / 2 - lug_h",
        "foot_z"
      ],
      "length": "lug_w",
      "width": "stem_d + 2 * lug_h",
      "height": "lug_t",
      "operation": "join"
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
        "Arm tip"
      ],
      "type": "cylinder",
      "base": [
        "-1 mm",
        0.0,
        0.0
      ],
      "axis": [
        1.0,
        0.0,
        0.0
      ],
      "radius": "(bore_d) / 2",
      "height": "bore_depth + 1 mm",
      "operation": "cut"
    },
    {
      "id": 6,
      "name": "Box3",
      "suppressed": false,
      "param_names": [
        "d13",
        "d14",
        "d15"
      ],
      "participants": [
        "Arm tip"
      ],
      "type": "box",
      "corner": [
        "-1 mm",
        "-(cord_d + 1 mm) / 2",
        "keel_z + 2 mm"
      ],
      "length": "stem_x + 1 mm",
      "width": "cord_d + 1 mm",
      "height": "cord_d + 1 mm",
      "operation": "cut"
    },
    {
      "id": 7,
      "name": "Box4",
      "suppressed": false,
      "param_names": [
        "d16",
        "d17",
        "d18"
      ],
      "participants": [
        "Arm tip"
      ],
      "type": "box",
      "corner": [
        "-1 mm",
        "-mouth_w / 2",
        "keel_z - 0.5 mm"
      ],
      "length": "stem_x + 1 mm",
      "width": "mouth_w",
      "height": "3 mm",
      "operation": "cut"
    },
    {
      "id": 8,
      "name": "Cylinder4",
      "suppressed": false,
      "param_names": [
        "d19",
        "d20"
      ],
      "participants": [
        "Arm tip"
      ],
      "type": "cylinder",
      "base": [
        "stem_x",
        0.0,
        "foot_z + grip_l"
      ],
      "axis": [
        0.0,
        0.0,
        1.0
      ],
      "radius": "(free_d) / 2",
      "height": "stem_l - grip_l + cord_d",
      "operation": "cut"
    },
    {
      "id": 9,
      "name": "Box5",
      "suppressed": false,
      "param_names": [
        "d21",
        "d22",
        "d23"
      ],
      "participants": [
        "Arm tip"
      ],
      "type": "box",
      "corner": [
        "stem_x - stem_d / 2 - 1 mm",
        "-slot_w / 2",
        "foot_z + grip_l + 0.25 mm"
      ],
      "length": "stem_d / 2 + 1 mm",
      "width": "slot_w",
      "height": "stem_l - grip_l + 1.75 mm",
      "operation": "cut"
    },
    {
      "id": 10,
      "name": "Cylinder5",
      "suppressed": false,
      "param_names": [
        "d24",
        "d25"
      ],
      "participants": [
        "Arm tip"
      ],
      "type": "cylinder",
      "base": [
        "stem_x",
        0.0,
        "foot_z - 1 mm"
      ],
      "axis": [
        0.0,
        0.0,
        1.0
      ],
      "radius": "(grip_d) / 2",
      "height": "grip_l + 1.5 mm",
      "operation": "cut"
    },
    {
      "id": 11,
      "name": "Box6",
      "suppressed": false,
      "param_names": [
        "d26",
        "d27",
        "d28"
      ],
      "participants": [
        "Arm tip"
      ],
      "type": "box",
      "corner": [
        "stem_x - stem_d / 2 - 1 mm",
        "-press_w / 2",
        "foot_z - 1 mm"
      ],
      "length": "stem_d / 2 + 1 mm",
      "width": "press_w",
      "height": "grip_l + 1.5 mm",
      "operation": "cut"
    },
    {
      "id": 12,
      "name": "Sketch1",
      "suppressed": false,
      "type": "sketch",
      "plane": {
        "type": "origin",
        "name": "XZ"
      },
      "sketch": {
        "points": [
          {
            "id": "origin",
            "pos": [
              0.0,
              0.0
            ],
            "fixed": true
          },
          {
            "id": "p1",
            "pos": [
              -1.0,
              -10.7
            ],
            "fixed": true,
            "exprs": {
              "y": "-dowel_d / 2 + 2 mm"
            }
          },
          {
            "id": "p2",
            "pos": [
              42.5,
              -10.7
            ],
            "fixed": true,
            "exprs": {
              "x": "bore_depth + 0.5 mm",
              "y": "-dowel_d / 2 + 2 mm"
            }
          },
          {
            "id": "p3",
            "pos": [
              42.5,
              -14.68
            ],
            "fixed": true,
            "exprs": {
              "x": "bore_depth + 0.5 mm",
              "y": "-dowel_d / 2 - room_in + 0.5 mm * taper"
            }
          },
          {
            "id": "p4",
            "pos": [
              -1.0,
              -16.419999999999998
            ],
            "fixed": true,
            "exprs": {
              "y": "-dowel_d / 2 - room_in - (bore_depth + 1 mm) * taper"
            }
          }
        ],
        "curves": [
          {
            "id": "l1",
            "type": "line",
            "a": 1,
            "b": 2,
            "construction": false
          },
          {
            "id": "l2",
            "type": "line",
            "a": 2,
            "b": 3,
            "construction": false
          },
          {
            "id": "l3",
            "type": "line",
            "a": 3,
            "b": 4,
            "construction": false
          },
          {
            "id": "l4",
            "type": "line",
            "a": 4,
            "b": 1,
            "construction": false
          }
        ],
        "constraints": [],
        "counters": {
          "l": 4,
          "p": 4
        }
      }
    },
    {
      "id": 13,
      "name": "Extrude1",
      "suppressed": false,
      "param_names": [
        "d29"
      ],
      "type": "extrude",
      "sketch": 12,
      "profiles": {
        "type": "all"
      },
      "extent": {
        "distance": "groove_w",
        "convention": "total_distance",
        "direction": "symmetric"
      },
      "operation": "cut",
      "targets": [
        "Arm tip"
      ]
    },
    {
      "id": 14,
      "name": "Sketch2",
      "suppressed": false,
      "param_names": [
        "d30"
      ],
      "type": "sketch",
      "plane": {
        "type": "offset",
        "base": {
          "type": "origin",
          "name": "YZ"
        },
        "distance": "-40 mm"
      },
      "sketch": {
        "points": [
          {
            "id": "origin",
            "pos": [
              0.0,
              0.0
            ],
            "fixed": true
          },
          {
            "id": "p1",
            "pos": [
              0.0,
              -63.4
            ],
            "fixed": true,
            "exprs": {
              "y": "foot_z"
            }
          },
          {
            "id": "p2",
            "pos": [
              47.0,
              -63.4
            ],
            "fixed": true,
            "exprs": {
              "x": "wedge_l",
              "y": "foot_z"
            }
          },
          {
            "id": "p3",
            "pos": [
              47.0,
              -58.72
            ],
            "fixed": true,
            "exprs": {
              "x": "wedge_l",
              "y": "foot_z + wedge_in + wedge_l * taper"
            }
          },
          {
            "id": "p4",
            "pos": [
              0.0,
              -60.6
            ],
            "fixed": true,
            "exprs": {
              "y": "foot_z + wedge_in"
            }
          }
        ],
        "curves": [
          {
            "id": "l1",
            "type": "line",
            "a": 1,
            "b": 2,
            "construction": false
          },
          {
            "id": "l2",
            "type": "line",
            "a": 2,
            "b": 3,
            "construction": false
          },
          {
            "id": "l3",
            "type": "line",
            "a": 3,
            "b": 4,
            "construction": false
          },
          {
            "id": "l4",
            "type": "line",
            "a": 4,
            "b": 1,
            "construction": false
          }
        ],
        "constraints": [],
        "counters": {
          "l": 4,
          "p": 4
        }
      }
    },
    {
      "id": 15,
      "name": "Extrude2",
      "suppressed": false,
      "body_names": [
        "Tip wedge"
      ],
      "param_names": [
        "d31"
      ],
      "type": "extrude",
      "sketch": 14,
      "profiles": {
        "type": "all"
      },
      "extent": {
        "distance": "groove_w - 0.4 mm",
        "convention": "total_distance",
        "direction": "positive"
      },
      "operation": "new_body"
    },
    {
      "id": 16,
      "name": "Cylinder6",
      "suppressed": false,
      "body_names": [
        "Cord clip 1"
      ],
      "param_names": [
        "d32",
        "d33"
      ],
      "type": "cylinder",
      "base": [
        "80 mm",
        "-80 mm",
        "foot_z"
      ],
      "axis": [
        0.0,
        0.0,
        1.0
      ],
      "radius": "(dowel_d + 5 mm) / 2",
      "height": "clip_t",
      "operation": "new_body"
    },
    {
      "id": 17,
      "name": "Cylinder7",
      "suppressed": false,
      "param_names": [
        "d34",
        "d35"
      ],
      "participants": [
        "Cord clip 1"
      ],
      "type": "cylinder",
      "base": [
        "80 mm",
        "-80 mm + -(dowel_d / 2 + cord_d / 2 + 3.5 mm)",
        "foot_z"
      ],
      "axis": [
        0.0,
        0.0,
        1.0
      ],
      "radius": "(cord_d + 5 mm) / 2",
      "height": "clip_t",
      "operation": "join"
    },
    {
      "id": 18,
      "name": "Cylinder8",
      "suppressed": false,
      "param_names": [
        "d36",
        "d37"
      ],
      "participants": [
        "Cord clip 1"
      ],
      "type": "cylinder",
      "base": [
        "80 mm",
        "-80 mm",
        "foot_z - 1 mm"
      ],
      "axis": [
        0.0,
        0.0,
        1.0
      ],
      "radius": "(dowel_d + 0.2 mm) / 2",
      "height": "clip_t + 2 mm",
      "operation": "cut"
    },
    {
      "id": 19,
      "name": "Box7",
      "suppressed": false,
      "param_names": [
        "d38",
        "d39",
        "d40"
      ],
      "participants": [
        "Cord clip 1"
      ],
      "type": "box",
      "corner": [
        "80 mm - 0.425 * dowel_d",
        "-80 mm",
        "foot_z - 1 mm"
      ],
      "length": "0.85 * dowel_d",
      "width": "dowel_d",
      "height": "clip_t + 2 mm",
      "operation": "cut"
    },
    {
      "id": 20,
      "name": "Cylinder9",
      "suppressed": false,
      "param_names": [
        "d41",
        "d42"
      ],
      "participants": [
        "Cord clip 1"
      ],
      "type": "cylinder",
      "base": [
        "80 mm",
        "-80 mm + -(dowel_d / 2 + cord_d / 2 + 3.5 mm)",
        "foot_z - 1 mm"
      ],
      "axis": [
        0.0,
        0.0,
        1.0
      ],
      "radius": "(cord_d + 0.5 mm) / 2",
      "height": "clip_t + 2 mm",
      "operation": "cut"
    },
    {
      "id": 21,
      "name": "Box8",
      "suppressed": false,
      "param_names": [
        "d43",
        "d44",
        "d45"
      ],
      "participants": [
        "Cord clip 1"
      ],
      "type": "box",
      "corner": [
        "80 mm - (cord_d - 1 mm) / 2",
        "-80 mm + -(dowel_d / 2 + cord_d / 2 + 3.5 mm) - cord_d",
        "foot_z - 1 mm"
      ],
      "length": "cord_d - 1 mm",
      "width": "cord_d",
      "height": "clip_t + 2 mm",
      "operation": "cut"
    },
    {
      "id": 22,
      "name": "Cylinder10",
      "suppressed": false,
      "body_names": [
        "Cord clip 2"
      ],
      "param_names": [
        "d46",
        "d47"
      ],
      "type": "cylinder",
      "base": [
        "120 mm",
        "-80 mm",
        "foot_z"
      ],
      "axis": [
        0.0,
        0.0,
        1.0
      ],
      "radius": "(dowel_d + 5 mm) / 2",
      "height": "clip_t",
      "operation": "new_body"
    },
    {
      "id": 23,
      "name": "Cylinder11",
      "suppressed": false,
      "param_names": [
        "d48",
        "d49"
      ],
      "participants": [
        "Cord clip 2"
      ],
      "type": "cylinder",
      "base": [
        "120 mm",
        "-80 mm + -(dowel_d / 2 + cord_d / 2 + 3.5 mm)",
        "foot_z"
      ],
      "axis": [
        0.0,
        0.0,
        1.0
      ],
      "radius": "(cord_d + 5 mm) / 2",
      "height": "clip_t",
      "operation": "join"
    },
    {
      "id": 24,
      "name": "Cylinder12",
      "suppressed": false,
      "param_names": [
        "d50",
        "d51"
      ],
      "participants": [
        "Cord clip 2"
      ],
      "type": "cylinder",
      "base": [
        "120 mm",
        "-80 mm",
        "foot_z - 1 mm"
      ],
      "axis": [
        0.0,
        0.0,
        1.0
      ],
      "radius": "(dowel_d + 0.2 mm) / 2",
      "height": "clip_t + 2 mm",
      "operation": "cut"
    },
    {
      "id": 25,
      "name": "Box9",
      "suppressed": false,
      "param_names": [
        "d52",
        "d53",
        "d54"
      ],
      "participants": [
        "Cord clip 2"
      ],
      "type": "box",
      "corner": [
        "120 mm - 0.425 * dowel_d",
        "-80 mm",
        "foot_z - 1 mm"
      ],
      "length": "0.85 * dowel_d",
      "width": "dowel_d",
      "height": "clip_t + 2 mm",
      "operation": "cut"
    },
    {
      "id": 26,
      "name": "Cylinder13",
      "suppressed": false,
      "param_names": [
        "d55",
        "d56"
      ],
      "participants": [
        "Cord clip 2"
      ],
      "type": "cylinder",
      "base": [
        "120 mm",
        "-80 mm + -(dowel_d / 2 + cord_d / 2 + 3.5 mm)",
        "foot_z - 1 mm"
      ],
      "axis": [
        0.0,
        0.0,
        1.0
      ],
      "radius": "(cord_d + 0.5 mm) / 2",
      "height": "clip_t + 2 mm",
      "operation": "cut"
    },
    {
      "id": 27,
      "name": "Box10",
      "suppressed": false,
      "param_names": [
        "d57",
        "d58",
        "d59"
      ],
      "participants": [
        "Cord clip 2"
      ],
      "type": "box",
      "corner": [
        "120 mm - (cord_d - 1 mm) / 2",
        "-80 mm + -(dowel_d / 2 + cord_d / 2 + 3.5 mm) - cord_d",
        "foot_z - 1 mm"
      ],
      "length": "cord_d - 1 mm",
      "width": "cord_d",
      "height": "clip_t + 2 mm",
      "operation": "cut"
    },
    {
      "id": 28,
      "name": "Cylinder14",
      "suppressed": false,
      "body_names": [
        "Cord clip 3"
      ],
      "param_names": [
        "d60",
        "d61"
      ],
      "type": "cylinder",
      "base": [
        "160 mm",
        "-80 mm",
        "foot_z"
      ],
      "axis": [
        0.0,
        0.0,
        1.0
      ],
      "radius": "(dowel_d + 5 mm) / 2",
      "height": "clip_t",
      "operation": "new_body"
    },
    {
      "id": 29,
      "name": "Cylinder15",
      "suppressed": false,
      "param_names": [
        "d62",
        "d63"
      ],
      "participants": [
        "Cord clip 3"
      ],
      "type": "cylinder",
      "base": [
        "160 mm",
        "-80 mm + -(dowel_d / 2 + cord_d / 2 + 3.5 mm)",
        "foot_z"
      ],
      "axis": [
        0.0,
        0.0,
        1.0
      ],
      "radius": "(cord_d + 5 mm) / 2",
      "height": "clip_t",
      "operation": "join"
    },
    {
      "id": 30,
      "name": "Cylinder16",
      "suppressed": false,
      "param_names": [
        "d64",
        "d65"
      ],
      "participants": [
        "Cord clip 3"
      ],
      "type": "cylinder",
      "base": [
        "160 mm",
        "-80 mm",
        "foot_z - 1 mm"
      ],
      "axis": [
        0.0,
        0.0,
        1.0
      ],
      "radius": "(dowel_d + 0.2 mm) / 2",
      "height": "clip_t + 2 mm",
      "operation": "cut"
    },
    {
      "id": 31,
      "name": "Box11",
      "suppressed": false,
      "param_names": [
        "d66",
        "d67",
        "d68"
      ],
      "participants": [
        "Cord clip 3"
      ],
      "type": "box",
      "corner": [
        "160 mm - 0.425 * dowel_d",
        "-80 mm",
        "foot_z - 1 mm"
      ],
      "length": "0.85 * dowel_d",
      "width": "dowel_d",
      "height": "clip_t + 2 mm",
      "operation": "cut"
    },
    {
      "id": 32,
      "name": "Cylinder17",
      "suppressed": false,
      "param_names": [
        "d69",
        "d70"
      ],
      "participants": [
        "Cord clip 3"
      ],
      "type": "cylinder",
      "base": [
        "160 mm",
        "-80 mm + -(dowel_d / 2 + cord_d / 2 + 3.5 mm)",
        "foot_z - 1 mm"
      ],
      "axis": [
        0.0,
        0.0,
        1.0
      ],
      "radius": "(cord_d + 0.5 mm) / 2",
      "height": "clip_t + 2 mm",
      "operation": "cut"
    },
    {
      "id": 33,
      "name": "Box12",
      "suppressed": false,
      "param_names": [
        "d71",
        "d72",
        "d73"
      ],
      "participants": [
        "Cord clip 3"
      ],
      "type": "box",
      "corner": [
        "160 mm - (cord_d - 1 mm) / 2",
        "-80 mm + -(dowel_d / 2 + cord_d / 2 + 3.5 mm) - cord_d",
        "foot_z - 1 mm"
      ],
      "length": "cord_d - 1 mm",
      "width": "cord_d",
      "height": "clip_t + 2 mm",
      "operation": "cut"
    }
  ],
  "next_id": 34,
  "next_component_color_index": 0
}