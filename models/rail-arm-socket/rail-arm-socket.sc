{
  "format": "solidcraft/48",
  "name": "rail-arm-socket",
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
      "name": "wall",
      "expr": "5 mm",
      "unit": "mm",
      "comment": "the carrier's U wall (rail-carrier)",
      "model": false
    },
    {
      "name": "r_o",
      "expr": "bore_d / 2 + wall",
      "unit": "mm",
      "comment": "the carrier's outside radius (rail-carrier)",
      "model": false
    },
    {
      "name": "carrier_l",
      "expr": "110 mm",
      "unit": "mm",
      "comment": "the carrier's height (rail-carrier)",
      "model": false
    },
    {
      "name": "dt_base",
      "expr": "12 mm",
      "unit": "mm",
      "comment": "the carrier's dovetail where it meets the carrier (rail-carrier)",
      "model": false
    },
    {
      "name": "dt_top",
      "expr": "18 mm",
      "unit": "mm",
      "comment": "the carrier's dovetail at its face (rail-carrier)",
      "model": false
    },
    {
      "name": "dt_h",
      "expr": "6 mm",
      "unit": "mm",
      "comment": "how far the carrier's dovetail stands out (rail-carrier)",
      "model": false
    },
    {
      "name": "fit",
      "expr": "0.3 mm",
      "unit": "mm",
      "comment": "the slot's clearance round the dovetail, each side",
      "model": false
    },
    {
      "name": "top_t",
      "expr": "6 mm",
      "unit": "mm",
      "comment": "the block's closed top, which rests on the dovetail's top",
      "model": false
    },
    {
      "name": "front_t",
      "expr": "5 mm",
      "unit": "mm",
      "comment": "the block in front of the slot",
      "model": false
    },
    {
      "name": "block_w",
      "expr": "32 mm",
      "unit": "mm",
      "comment": "the block's width",
      "model": false
    },
    {
      "name": "block_x",
      "expr": "r_o + fit",
      "unit": "mm",
      "comment": "the block's back face, just clear of the carrier",
      "model": false
    },
    {
      "name": "boss_x",
      "expr": "block_x + dt_h + fit + front_t",
      "unit": "mm",
      "comment": "the block's front face, where the boss starts",
      "model": false
    },
    {
      "name": "arm_z",
      "expr": "70 mm",
      "unit": "mm",
      "comment": "the arm's axis above the block's bottom",
      "model": false
    },
    {
      "name": "socket_depth",
      "expr": "54 mm",
      "unit": "mm",
      "comment": "how far the arm goes in: at least 51 mm (2 inches)",
      "model": false
    },
    {
      "name": "end_t",
      "expr": "6 mm",
      "unit": "mm",
      "comment": "the boss's closed end, behind the arm",
      "model": false
    },
    {
      "name": "boss_wall",
      "expr": "7 mm",
      "unit": "mm",
      "comment": "plastic round the arm, room above for the wedge's groove",
      "model": false
    },
    {
      "name": "boss_d",
      "expr": "bore_d + 2 * boss_wall",
      "unit": "mm",
      "comment": "the boss's outside",
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
      "expr": "socket_depth + 20 mm",
      "unit": "mm",
      "comment": "the wedge's length",
      "model": false
    },
    {
      "name": "wedge_in",
      "expr": "room_in + clearance / 2 + 20 mm * taper",
      "unit": "mm",
      "comment": "the wedge's thin end: seated 20 mm short of the bore's end on a nominal dowel",
      "model": false
    }
  ],
  "features": [
    {
      "id": 1,
      "name": "Box1",
      "suppressed": false,
      "body_names": [
        "Arm socket"
      ],
      "param_names": [
        "d1",
        "d2",
        "d3"
      ],
      "type": "box",
      "corner": [
        "block_x",
        "-block_w / 2",
        0.0
      ],
      "length": "dt_h + fit + front_t",
      "width": "block_w",
      "height": "carrier_l + top_t",
      "operation": "new_body"
    },
    {
      "id": 2,
      "name": "Sketch1",
      "suppressed": false,
      "param_names": [
        "d4"
      ],
      "type": "sketch",
      "plane": {
        "type": "offset",
        "base": {
          "type": "origin",
          "name": "XY"
        },
        "distance": "-1 mm"
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
              15.899999999999999,
              -6.3
            ],
            "fixed": true,
            "exprs": {
              "x": "r_o - 2 mm",
              "y": "-dt_base / 2 - fit"
            }
          },
          {
            "id": "p2",
            "pos": [
              24.2,
              -9.3
            ],
            "fixed": true,
            "exprs": {
              "x": "r_o + dt_h + fit",
              "y": "-dt_top / 2 - fit"
            }
          },
          {
            "id": "p3",
            "pos": [
              24.2,
              9.3
            ],
            "fixed": true,
            "exprs": {
              "x": "r_o + dt_h + fit",
              "y": "dt_top / 2 + fit"
            }
          },
          {
            "id": "p4",
            "pos": [
              15.899999999999999,
              6.3
            ],
            "fixed": true,
            "exprs": {
              "x": "r_o - 2 mm",
              "y": "dt_base / 2 + fit"
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
      "id": 3,
      "name": "Extrude1",
      "suppressed": false,
      "param_names": [
        "d5"
      ],
      "type": "extrude",
      "sketch": 2,
      "profiles": {
        "type": "all"
      },
      "extent": {
        "distance": "carrier_l + 1 mm",
        "convention": "total_distance",
        "direction": "positive"
      },
      "operation": "cut",
      "targets": [
        "Arm socket"
      ]
    },
    {
      "id": 4,
      "name": "Cylinder1",
      "suppressed": false,
      "param_names": [
        "d6",
        "d7"
      ],
      "participants": [
        "Arm socket"
      ],
      "type": "cylinder",
      "base": [
        "boss_x - 2 mm",
        0.0,
        "arm_z"
      ],
      "axis": [
        1.0,
        0.0,
        0.0
      ],
      "radius": "(boss_d) / 2",
      "height": "end_t + socket_depth + 2 mm",
      "operation": "join"
    },
    {
      "id": 5,
      "name": "Cylinder2",
      "suppressed": false,
      "param_names": [
        "d8",
        "d9"
      ],
      "participants": [
        "Arm socket"
      ],
      "type": "cylinder",
      "base": [
        "boss_x + end_t",
        0.0,
        "arm_z"
      ],
      "axis": [
        1.0,
        0.0,
        0.0
      ],
      "radius": "(bore_d) / 2",
      "height": "socket_depth + 1 mm",
      "operation": "cut"
    },
    {
      "id": 6,
      "name": "Sketch2",
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
              35.0,
              -80.7
            ],
            "fixed": true,
            "exprs": {
              "x": "boss_x + end_t - 0.5 mm",
              "y": "-arm_z - dowel_d / 2 + 2 mm"
            }
          },
          {
            "id": "p2",
            "pos": [
              90.5,
              -80.7
            ],
            "fixed": true,
            "exprs": {
              "x": "boss_x + end_t + socket_depth + 1 mm",
              "y": "-arm_z - dowel_d / 2 + 2 mm"
            }
          },
          {
            "id": "p3",
            "pos": [
              90.5,
              -86.92
            ],
            "fixed": true,
            "exprs": {
              "x": "boss_x + end_t + socket_depth + 1 mm",
              "y": "-arm_z - dowel_d / 2 - room_in - (socket_depth + 1.5 mm) * taper"
            }
          },
          {
            "id": "p4",
            "pos": [
              35.0,
              -84.7
            ],
            "fixed": true,
            "exprs": {
              "x": "boss_x + end_t - 0.5 mm",
              "y": "-arm_z - dowel_d / 2 - room_in"
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
      "id": 7,
      "name": "Extrude2",
      "suppressed": false,
      "param_names": [
        "d10"
      ],
      "type": "extrude",
      "sketch": 6,
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
        "Arm socket"
      ]
    },
    {
      "id": 8,
      "name": "Sketch3",
      "suppressed": false,
      "param_names": [
        "d11"
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
              74.0,
              0.0
            ],
            "fixed": true,
            "exprs": {
              "x": "wedge_l"
            }
          },
          {
            "id": "p2",
            "pos": [
              74.0,
              5.96
            ],
            "fixed": true,
            "exprs": {
              "x": "wedge_l",
              "y": "0 mm + wedge_in + wedge_l * taper"
            }
          },
          {
            "id": "p3",
            "pos": [
              0.0,
              3.0
            ],
            "fixed": true,
            "exprs": {
              "y": "0 mm + wedge_in"
            }
          },
          {
            "id": "l1.start",
            "pos": [
              0.0,
              0.0
            ],
            "fixed": false
          }
        ],
        "curves": [
          {
            "id": "l1",
            "type": "line",
            "a": 4,
            "b": 1,
            "construction": false
          },
          {
            "id": "l2",
            "type": "line",
            "a": 1,
            "b": 2,
            "construction": false
          },
          {
            "id": "l3",
            "type": "line",
            "a": 2,
            "b": 3,
            "construction": false
          },
          {
            "id": "l4",
            "type": "line",
            "a": 3,
            "b": 4,
            "construction": false
          }
        ],
        "constraints": [
          {
            "id": "k1",
            "type": "coincident",
            "p": 0,
            "q": 4
          }
        ],
        "counters": {
          "k": 1,
          "l": 4,
          "p": 3
        }
      }
    },
    {
      "id": 9,
      "name": "Extrude3",
      "suppressed": false,
      "body_names": [
        "Arm wedge"
      ],
      "param_names": [
        "d12"
      ],
      "type": "extrude",
      "sketch": 8,
      "profiles": {
        "type": "all"
      },
      "extent": {
        "distance": "groove_w - 0.4 mm",
        "convention": "total_distance",
        "direction": "positive"
      },
      "operation": "new_body"
    }
  ],
  "next_id": 10,
  "next_component_color_index": 0
}