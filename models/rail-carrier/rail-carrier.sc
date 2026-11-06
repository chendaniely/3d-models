{
  "format": "solidcraft/48",
  "name": "rail-carrier",
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
      "name": "standoff",
      "expr": "32 mm",
      "unit": "mm",
      "comment": "the rail's axis from the wall: room behind it for the cord",
      "model": false
    },
    {
      "name": "wall",
      "expr": "5 mm",
      "unit": "mm",
      "comment": "the U's wall",
      "model": false
    },
    {
      "name": "r_o",
      "expr": "bore_d / 2 + wall",
      "unit": "mm",
      "comment": "the U's outside radius",
      "model": false
    },
    {
      "name": "wall_gap",
      "expr": "1.5 mm",
      "unit": "mm",
      "comment": "between the U's arms and the wall, for a felt or rubber pad on each",
      "model": false
    },
    {
      "name": "carrier_l",
      "expr": "110 mm",
      "unit": "mm",
      "comment": "the carrier's height: long enough for the arm at 24 inches",
      "model": false
    },
    {
      "name": "groove_d",
      "expr": "2 mm",
      "unit": "mm",
      "comment": "the wedge's groove, cut into each arm",
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
      "name": "room_top",
      "expr": "4.5 mm",
      "unit": "mm",
      "comment": "the groove's depth behind the dowel at the carrier's top",
      "model": false
    },
    {
      "name": "wedge_l",
      "expr": "carrier_l + 10 mm",
      "unit": "mm",
      "comment": "the wedge's length",
      "model": false
    },
    {
      "name": "wedge_top",
      "expr": "room_top + clearance / 2 + 20 mm * taper",
      "unit": "mm",
      "comment": "the wedge's thin end: seated 20 mm below the top on a nominal dowel",
      "model": false
    },
    {
      "name": "wedge_w",
      "expr": "bore_d + 2 * groove_d - 0.5 mm",
      "unit": "mm",
      "comment": "the wedge's width, its wings in the grooves",
      "model": false
    },
    {
      "name": "channel",
      "expr": "standoff - wall_gap - dowel_d / 2 - room_top - carrier_l * taper",
      "unit": "mm",
      "comment": "the cord's channel behind the wedge, at its narrowest (the carrier's bottom)",
      "model": false
    },
    {
      "name": "dt_base",
      "expr": "12 mm",
      "unit": "mm",
      "comment": "the dovetail's width where it meets the carrier",
      "model": false
    },
    {
      "name": "dt_top",
      "expr": "18 mm",
      "unit": "mm",
      "comment": "the dovetail's width at its face",
      "model": false
    },
    {
      "name": "dt_h",
      "expr": "6 mm",
      "unit": "mm",
      "comment": "how far the dovetail stands out",
      "model": false
    }
  ],
  "features": [
    {
      "id": 1,
      "name": "Cylinder1",
      "suppressed": false,
      "body_names": [
        "Carrier"
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
      "radius": "(2 * r_o) / 2",
      "height": "carrier_l",
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
        "Carrier"
      ],
      "type": "box",
      "corner": [
        "-standoff + wall_gap",
        "-r_o",
        0.0
      ],
      "length": "standoff - wall_gap",
      "width": "2 * r_o",
      "height": "carrier_l",
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
        "Carrier"
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
      "radius": "(bore_d) / 2",
      "height": "carrier_l + 2 mm",
      "operation": "cut"
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
        "Carrier"
      ],
      "type": "box",
      "corner": [
        "-standoff - 1 mm",
        "-bore_d / 2",
        "-1 mm"
      ],
      "length": "standoff + 1 mm",
      "width": "bore_d",
      "height": "carrier_l + 2 mm",
      "operation": "cut"
    },
    {
      "id": 5,
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
              -10.7,
              1.0
            ],
            "fixed": true,
            "exprs": {
              "x": "-dowel_d / 2 + 2 mm"
            }
          },
          {
            "id": "p2",
            "pos": [
              -10.7,
              -111.0
            ],
            "fixed": true,
            "exprs": {
              "x": "-dowel_d / 2 + 2 mm",
              "y": "-carrier_l - 1 mm"
            }
          },
          {
            "id": "p3",
            "pos": [
              -17.16,
              -111.0
            ],
            "fixed": true,
            "exprs": {
              "x": "-dowel_d / 2 - room_top + 1 mm * taper",
              "y": "-carrier_l - 1 mm"
            }
          },
          {
            "id": "p4",
            "pos": [
              -21.64,
              1.0
            ],
            "fixed": true,
            "exprs": {
              "x": "-dowel_d / 2 - room_top - (carrier_l + 1 mm) * taper"
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
      "id": 6,
      "name": "Extrude1",
      "suppressed": false,
      "param_names": [
        "d11"
      ],
      "type": "extrude",
      "sketch": 5,
      "profiles": {
        "type": "all"
      },
      "extent": {
        "distance": "bore_d + 2 * groove_d",
        "convention": "total_distance",
        "direction": "symmetric"
      },
      "operation": "cut",
      "targets": [
        "Carrier"
      ]
    },
    {
      "id": 7,
      "name": "Sketch2",
      "suppressed": false,
      "type": "sketch",
      "plane": {
        "type": "origin",
        "name": "XY"
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
              -6.0
            ],
            "fixed": true,
            "exprs": {
              "x": "r_o - 2 mm",
              "y": "-dt_base / 2"
            }
          },
          {
            "id": "p2",
            "pos": [
              23.9,
              -9.0
            ],
            "fixed": true,
            "exprs": {
              "x": "r_o + dt_h",
              "y": "-dt_top / 2"
            }
          },
          {
            "id": "p3",
            "pos": [
              23.9,
              9.0
            ],
            "fixed": true,
            "exprs": {
              "x": "r_o + dt_h",
              "y": "dt_top / 2"
            }
          },
          {
            "id": "p4",
            "pos": [
              15.899999999999999,
              6.0
            ],
            "fixed": true,
            "exprs": {
              "x": "r_o - 2 mm",
              "y": "dt_base / 2"
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
      "id": 8,
      "name": "Extrude2",
      "suppressed": false,
      "param_names": [
        "d12"
      ],
      "type": "extrude",
      "sketch": 7,
      "profiles": {
        "type": "all"
      },
      "extent": {
        "distance": "carrier_l",
        "convention": "total_distance",
        "direction": "positive"
      },
      "operation": "join",
      "targets": [
        "Carrier"
      ]
    },
    {
      "id": 9,
      "name": "Sketch3",
      "suppressed": false,
      "param_names": [
        "d13"
      ],
      "type": "sketch",
      "plane": {
        "type": "offset",
        "base": {
          "type": "origin",
          "name": "YZ"
        },
        "distance": "40 mm"
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
              120.0,
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
              120.0,
              10.3
            ],
            "fixed": true,
            "exprs": {
              "x": "wedge_l",
              "y": "0 mm + wedge_top + wedge_l * taper"
            }
          },
          {
            "id": "p3",
            "pos": [
              0.0,
              5.5
            ],
            "fixed": true,
            "exprs": {
              "y": "0 mm + wedge_top"
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
      "id": 10,
      "name": "Extrude3",
      "suppressed": false,
      "body_names": [
        "Wedge"
      ],
      "param_names": [
        "d14"
      ],
      "type": "extrude",
      "sketch": 9,
      "profiles": {
        "type": "all"
      },
      "extent": {
        "distance": "wedge_w",
        "convention": "total_distance",
        "direction": "positive"
      },
      "operation": "new_body"
    }
  ],
  "next_id": 11,
  "next_component_color_index": 0
}