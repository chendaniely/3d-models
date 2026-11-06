{
  "format": "solidcraft/48",
  "name": "rail-feet",
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
      "name": "cup_wall",
      "expr": "4 mm",
      "unit": "mm",
      "comment": "plastic round each cup",
      "model": false
    },
    {
      "name": "cup_od",
      "expr": "bore_d + 2 * cup_wall",
      "unit": "mm",
      "comment": "a cup's outside",
      "model": false
    },
    {
      "name": "floor_t",
      "expr": "5 mm",
      "unit": "mm",
      "comment": "a cup's closed end",
      "model": false
    },
    {
      "name": "low_depth",
      "expr": "25 mm",
      "unit": "mm",
      "comment": "how far the rail stands in the bottom cup",
      "model": false
    },
    {
      "name": "high_depth",
      "expr": "64 mm",
      "unit": "mm",
      "comment": "the top cup's depth: the rail lifts into it past the bottom cup's rim",
      "model": false
    },
    {
      "name": "insert_min",
      "expr": "25 mm",
      "unit": "mm",
      "comment": "the least the rail's top stays in the top cup",
      "model": false
    },
    {
      "name": "lift_room",
      "expr": "low_depth + 3 mm",
      "unit": "mm",
      "comment": "how far the rail must rise to clear the bottom cup's rim",
      "model": false
    },
    {
      "name": "plate_t",
      "expr": "10 mm",
      "unit": "mm",
      "comment": "the plate on the wall",
      "model": false
    },
    {
      "name": "plate_w",
      "expr": "40 mm",
      "unit": "mm",
      "comment": "the plate's width",
      "model": false
    },
    {
      "name": "tab_h",
      "expr": "22 mm",
      "unit": "mm",
      "comment": "each plate beyond its cup, behind the rail, where its screw goes",
      "model": false
    },
    {
      "name": "screw_d",
      "expr": "5 mm",
      "unit": "mm",
      "comment": "each plate's screw hole: #8 or #10 wood screws, 3/16 in toggle bolts",
      "model": false
    },
    {
      "name": "head_d",
      "expr": "10.5 mm",
      "unit": "mm",
      "comment": "the counterbore round each screw's head",
      "model": false
    },
    {
      "name": "head_h",
      "expr": "3 mm",
      "unit": "mm",
      "comment": "a pan or washer head's height",
      "model": false
    },
    {
      "name": "cap_h",
      "expr": "2 mm",
      "unit": "mm",
      "comment": "a printed cap's height, pressed in over the head",
      "model": false
    },
    {
      "name": "head_depth",
      "expr": "head_h + cap_h",
      "unit": "mm",
      "comment": "the counterbore's depth: the head, then its cap",
      "model": false
    },
    {
      "name": "pin_d",
      "expr": "4 mm",
      "unit": "mm",
      "comment": "the bottom cup's floor: a hole for a #6 screw up into the rail's end",
      "model": false
    },
    {
      "name": "pin_head_d",
      "expr": "8 mm",
      "unit": "mm",
      "comment": "the counterbore under the floor for that screw's head",
      "model": false
    },
    {
      "name": "pin_head_h",
      "expr": "3 mm",
      "unit": "mm",
      "comment": "that counterbore's depth",
      "model": false
    },
    {
      "name": "cord_w",
      "expr": "7 mm",
      "unit": "mm",
      "comment": "the cord's groove up the back of the bottom foot",
      "model": false
    },
    {
      "name": "cord_depth",
      "expr": "7 mm",
      "unit": "mm",
      "comment": "the groove's depth: at least the cord's thickness and 1 mm",
      "model": false
    },
    {
      "name": "cord_y",
      "expr": "-9.5 mm",
      "unit": "mm",
      "comment": "the cord groove's centre, beside the screw",
      "model": false
    },
    {
      "name": "spacing_less",
      "expr": "low_depth + high_depth + tab_h - (lift_room + high_depth - insert_min) / 2",
      "unit": "mm",
      "comment": "the top screw goes the rail's length less this above the bottom screw",
      "model": false
    },
    {
      "name": "spacing_tol",
      "expr": "(high_depth - insert_min - lift_room) / 2",
      "unit": "mm",
      "comment": "how far either way the top screw may be off",
      "model": false
    },
    {
      "name": "top_y",
      "expr": "70 mm",
      "unit": "mm",
      "comment": "the top foot sits beside the bottom foot, for printing",
      "model": false
    }
  ],
  "features": [
    {
      "id": 1,
      "name": "Cylinder1",
      "suppressed": false,
      "body_names": [
        "Bottom foot"
      ],
      "param_names": [
        "d1",
        "d2"
      ],
      "type": "cylinder",
      "base": [
        0.0,
        "0 mm",
        0.0
      ],
      "axis": [
        0.0,
        0.0,
        1.0
      ],
      "radius": "(cup_od) / 2",
      "height": "floor_t + low_depth",
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
        "Bottom foot"
      ],
      "type": "box",
      "corner": [
        "-standoff + plate_t - 0.5 mm",
        "0 mm - (cup_od - 8 mm) / 2",
        0.0
      ],
      "length": "standoff - plate_t + 1 mm",
      "width": "cup_od - 8 mm",
      "height": "floor_t + low_depth",
      "operation": "join"
    },
    {
      "id": 3,
      "name": "Box2",
      "suppressed": false,
      "param_names": [
        "d6",
        "d7",
        "d8"
      ],
      "participants": [
        "Bottom foot"
      ],
      "type": "box",
      "corner": [
        "-standoff",
        "0 mm - plate_w / 2",
        0.0
      ],
      "length": "plate_t",
      "width": "plate_w",
      "height": "floor_t + low_depth + tab_h",
      "operation": "join"
    },
    {
      "id": 4,
      "name": "Cylinder2",
      "suppressed": false,
      "param_names": [
        "d9",
        "d10"
      ],
      "participants": [
        "Bottom foot"
      ],
      "type": "cylinder",
      "base": [
        0.0,
        "0 mm",
        "floor_t"
      ],
      "axis": [
        0.0,
        0.0,
        1.0
      ],
      "radius": "(bore_d) / 2",
      "height": "low_depth + 1 mm",
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
        "Bottom foot"
      ],
      "type": "cylinder",
      "base": [
        "-standoff - 1 mm",
        "0 mm",
        "floor_t + low_depth + tab_h / 2"
      ],
      "axis": [
        1.0,
        0.0,
        0.0
      ],
      "radius": "(screw_d) / 2",
      "height": "plate_t + 2 mm",
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
        "Bottom foot"
      ],
      "type": "cylinder",
      "base": [
        "-standoff + plate_t - head_depth",
        "0 mm",
        "floor_t + low_depth + tab_h / 2"
      ],
      "axis": [
        1.0,
        0.0,
        0.0
      ],
      "radius": "(head_d) / 2",
      "height": "head_depth + 1 mm",
      "operation": "cut"
    },
    {
      "id": 7,
      "name": "Cylinder5",
      "suppressed": false,
      "body_names": [
        "Top foot"
      ],
      "param_names": [
        "d15",
        "d16"
      ],
      "type": "cylinder",
      "base": [
        0.0,
        "top_y",
        0.0
      ],
      "axis": [
        0.0,
        0.0,
        1.0
      ],
      "radius": "(cup_od) / 2",
      "height": "floor_t + high_depth",
      "operation": "new_body"
    },
    {
      "id": 8,
      "name": "Box3",
      "suppressed": false,
      "param_names": [
        "d17",
        "d18",
        "d19"
      ],
      "participants": [
        "Top foot"
      ],
      "type": "box",
      "corner": [
        "-standoff + plate_t - 0.5 mm",
        "top_y - (cup_od - 8 mm) / 2",
        0.0
      ],
      "length": "standoff - plate_t + 1 mm",
      "width": "cup_od - 8 mm",
      "height": "floor_t + high_depth",
      "operation": "join"
    },
    {
      "id": 9,
      "name": "Box4",
      "suppressed": false,
      "param_names": [
        "d20",
        "d21",
        "d22"
      ],
      "participants": [
        "Top foot"
      ],
      "type": "box",
      "corner": [
        "-standoff",
        "top_y - plate_w / 2",
        0.0
      ],
      "length": "plate_t",
      "width": "plate_w",
      "height": "floor_t + high_depth + tab_h",
      "operation": "join"
    },
    {
      "id": 10,
      "name": "Cylinder6",
      "suppressed": false,
      "param_names": [
        "d23",
        "d24"
      ],
      "participants": [
        "Top foot"
      ],
      "type": "cylinder",
      "base": [
        0.0,
        "top_y",
        "floor_t"
      ],
      "axis": [
        0.0,
        0.0,
        1.0
      ],
      "radius": "(bore_d) / 2",
      "height": "high_depth + 1 mm",
      "operation": "cut"
    },
    {
      "id": 11,
      "name": "Cylinder7",
      "suppressed": false,
      "param_names": [
        "d25",
        "d26"
      ],
      "participants": [
        "Top foot"
      ],
      "type": "cylinder",
      "base": [
        "-standoff - 1 mm",
        "top_y",
        "floor_t + high_depth + tab_h / 2"
      ],
      "axis": [
        1.0,
        0.0,
        0.0
      ],
      "radius": "(screw_d) / 2",
      "height": "plate_t + 2 mm",
      "operation": "cut"
    },
    {
      "id": 12,
      "name": "Cylinder8",
      "suppressed": false,
      "param_names": [
        "d27",
        "d28"
      ],
      "participants": [
        "Top foot"
      ],
      "type": "cylinder",
      "base": [
        "-standoff + plate_t - head_depth",
        "top_y",
        "floor_t + high_depth + tab_h / 2"
      ],
      "axis": [
        1.0,
        0.0,
        0.0
      ],
      "radius": "(head_d) / 2",
      "height": "head_depth + 1 mm",
      "operation": "cut"
    },
    {
      "id": 13,
      "name": "Cylinder9",
      "suppressed": false,
      "param_names": [
        "d29",
        "d30"
      ],
      "participants": [
        "Bottom foot"
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
      "radius": "(pin_d) / 2",
      "height": "floor_t + 2 mm",
      "operation": "cut"
    },
    {
      "id": 14,
      "name": "Cylinder10",
      "suppressed": false,
      "param_names": [
        "d31",
        "d32"
      ],
      "participants": [
        "Bottom foot"
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
      "radius": "(pin_head_d) / 2",
      "height": "pin_head_h + 1 mm",
      "operation": "cut"
    },
    {
      "id": 15,
      "name": "Box5",
      "suppressed": false,
      "param_names": [
        "d33",
        "d34",
        "d35"
      ],
      "participants": [
        "Bottom foot"
      ],
      "type": "box",
      "corner": [
        "-standoff - 1 mm",
        "cord_y - cord_w / 2",
        "-1 mm"
      ],
      "length": "cord_depth + 1 mm",
      "width": "cord_w",
      "height": "floor_t + low_depth + tab_h + 2 mm",
      "operation": "cut"
    },
    {
      "id": 16,
      "name": "Cylinder11",
      "suppressed": false,
      "body_names": [
        "Cap 1"
      ],
      "param_names": [
        "d36",
        "d37"
      ],
      "type": "cylinder",
      "base": [
        "45 mm",
        "-12 mm",
        0.0
      ],
      "axis": [
        0.0,
        0.0,
        1.0
      ],
      "radius": "(head_d - 0.1 mm) / 2",
      "height": "cap_h",
      "operation": "new_body"
    },
    {
      "id": 17,
      "name": "Cylinder12",
      "suppressed": false,
      "body_names": [
        "Cap 2"
      ],
      "param_names": [
        "d38",
        "d39"
      ],
      "type": "cylinder",
      "base": [
        "45 mm",
        "12 mm",
        0.0
      ],
      "axis": [
        0.0,
        0.0,
        1.0
      ],
      "radius": "(head_d - 0.1 mm) / 2",
      "height": "cap_h",
      "operation": "new_body"
    }
  ],
  "next_id": 18,
  "next_component_color_index": 0
}