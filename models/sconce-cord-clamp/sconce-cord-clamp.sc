{
  "format": "solidcraft/48",
  "name": "sconce-cord-clamp",
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
      "expr": "0.2 mm",
      "unit": "mm",
      "comment": "a snug slide; the bolt closes the split to grip",
      "model": false
    },
    {
      "name": "ring_wall",
      "expr": "5 mm",
      "unit": "mm",
      "comment": "plastic around the dowel",
      "model": false
    },
    {
      "name": "ring_len",
      "expr": "20 mm",
      "unit": "mm",
      "comment": "the ring's length along the dowel",
      "model": false
    },
    {
      "name": "split",
      "expr": "3 mm",
      "unit": "mm",
      "comment": "the gap the bolt closes",
      "model": false
    },
    {
      "name": "ear_t",
      "expr": "6 mm",
      "unit": "mm",
      "comment": "each clamping ear's thickness",
      "model": false
    },
    {
      "name": "ear_len",
      "expr": "11 mm",
      "unit": "mm",
      "comment": "how far the ears stand out from the ring, on its side",
      "model": false
    },
    {
      "name": "bolt_d",
      "expr": "4.4 mm",
      "unit": "mm",
      "comment": "clearance for an M4 bolt",
      "model": false
    },
    {
      "name": "cord_d",
      "expr": "6 mm",
      "unit": "mm",
      "comment": "the light's cord, measured: 6 mm is a guess until it is",
      "model": false
    },
    {
      "name": "under_gap",
      "expr": "cord_d + 4 mm",
      "unit": "mm",
      "comment": "room under the dowel for the cord to reach the hole",
      "model": false
    },
    {
      "name": "grip_d",
      "expr": "cord_d - 0.6 mm",
      "unit": "mm",
      "comment": "the hole the cord hangs from: a little tight, so it grips",
      "model": false
    },
    {
      "name": "slot_w",
      "expr": "cord_d - 1.5 mm",
      "unit": "mm",
      "comment": "the slot the cord is pressed in through: tighter still",
      "model": false
    },
    {
      "name": "shelf_len",
      "expr": "18 mm",
      "unit": "mm",
      "comment": "how far the cord shelf reaches beyond the ring",
      "model": false
    },
    {
      "name": "shelf_w",
      "expr": "18 mm",
      "unit": "mm",
      "comment": "the cord shelf's width",
      "model": false
    },
    {
      "name": "shelf_t",
      "expr": "8 mm",
      "unit": "mm",
      "comment": "the cord shelf's thickness",
      "model": false
    },
    {
      "name": "web_w",
      "expr": "8 mm",
      "unit": "mm",
      "comment": "the web joining the ring to the shelf",
      "model": false
    },
    {
      "name": "bore_d",
      "expr": "dowel_d + clearance",
      "unit": "mm",
      "comment": "the ring's bore",
      "model": false
    },
    {
      "name": "ring_d",
      "expr": "bore_d + 2 * ring_wall",
      "unit": "mm",
      "comment": "the ring's outside diameter",
      "model": false
    },
    {
      "name": "shelf_top",
      "expr": "-dowel_d / 2 - under_gap",
      "unit": "mm",
      "comment": "the shelf's top face, below the dowel's axis",
      "model": false
    }
  ],
  "features": [
    {
      "id": 1,
      "name": "Cylinder1",
      "suppressed": false,
      "body_names": [
        "Cord clamp"
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
      "radius": "(ring_d) / 2",
      "height": "ring_len",
      "operation": "new_body"
    },
    {
      "id": 2,
      "name": "Box1",
      "suppressed": false,
      "body_names": [
        "Ears"
      ],
      "param_names": [
        "d3",
        "d4",
        "d5"
      ],
      "type": "box",
      "corner": [
        0.0,
        "bore_d / 2",
        "-split / 2 - ear_t"
      ],
      "length": "ring_len",
      "width": "ring_d / 2 + ear_len - bore_d / 2",
      "height": "split + 2 * ear_t",
      "operation": "new_body"
    },
    {
      "id": 3,
      "name": "Box2",
      "suppressed": false,
      "body_names": [
        "Web"
      ],
      "param_names": [
        "d6",
        "d7",
        "d8"
      ],
      "type": "box",
      "corner": [
        0.0,
        "-web_w / 2",
        "shelf_top"
      ],
      "length": "ring_len",
      "width": "web_w",
      "height": "-bore_d / 2 - 1 mm - shelf_top",
      "operation": "new_body"
    },
    {
      "id": 4,
      "name": "Box3",
      "suppressed": false,
      "body_names": [
        "Shelf"
      ],
      "param_names": [
        "d9",
        "d10",
        "d11"
      ],
      "type": "box",
      "corner": [
        0.0,
        "-shelf_w / 2",
        "shelf_top - shelf_t"
      ],
      "length": "ring_len + shelf_len",
      "width": "shelf_w",
      "height": "shelf_t",
      "operation": "new_body"
    },
    {
      "id": 5,
      "name": "Combine1",
      "suppressed": false,
      "type": "combine",
      "target": "Cord clamp",
      "tools": [
        "Ears",
        "Web",
        "Shelf"
      ],
      "operation": "join",
      "keep_tools": false
    },
    {
      "id": 6,
      "name": "Cylinder2",
      "suppressed": false,
      "body_names": [
        "Bore"
      ],
      "param_names": [
        "d12",
        "d13"
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
      "height": "ring_len + 2 mm",
      "operation": "new_body"
    },
    {
      "id": 7,
      "name": "Box4",
      "suppressed": false,
      "body_names": [
        "Split"
      ],
      "param_names": [
        "d14",
        "d15",
        "d16"
      ],
      "type": "box",
      "corner": [
        "-1 mm",
        0.0,
        "-split / 2"
      ],
      "length": "ring_len + 2 mm",
      "width": "ring_d / 2 + ear_len + 1 mm",
      "height": "split",
      "operation": "new_body"
    },
    {
      "id": 8,
      "name": "Cylinder3",
      "suppressed": false,
      "body_names": [
        "Bolt hole"
      ],
      "param_names": [
        "d17",
        "d18"
      ],
      "type": "cylinder",
      "base": [
        "ring_len / 2",
        "ring_d / 2 + ear_len / 2 - 0.5 mm",
        "-split / 2 - ear_t - 1 mm"
      ],
      "axis": [
        0.0,
        0.0,
        1.0
      ],
      "radius": "(bolt_d) / 2",
      "height": "split + 2 * ear_t + 2 mm",
      "operation": "new_body"
    },
    {
      "id": 9,
      "name": "Cylinder4",
      "suppressed": false,
      "body_names": [
        "Cord hole"
      ],
      "param_names": [
        "d19",
        "d20"
      ],
      "type": "cylinder",
      "base": [
        "ring_len + shelf_len / 2",
        0.0,
        "shelf_top - shelf_t - 1 mm"
      ],
      "axis": [
        0.0,
        0.0,
        1.0
      ],
      "radius": "(grip_d) / 2",
      "height": "shelf_t + 2 mm",
      "operation": "new_body"
    },
    {
      "id": 10,
      "name": "Box5",
      "suppressed": false,
      "body_names": [
        "Cord slot"
      ],
      "param_names": [
        "d21",
        "d22",
        "d23"
      ],
      "type": "box",
      "corner": [
        "ring_len + shelf_len / 2 - slot_w / 2",
        0.0,
        "shelf_top - shelf_t - 1 mm"
      ],
      "length": "slot_w",
      "width": "shelf_w / 2 + 1 mm",
      "height": "shelf_t + 2 mm",
      "operation": "new_body"
    },
    {
      "id": 11,
      "name": "Combine2",
      "suppressed": false,
      "type": "combine",
      "target": "Cord clamp",
      "tools": [
        "Bore",
        "Split",
        "Bolt hole",
        "Cord hole",
        "Cord slot"
      ],
      "operation": "cut",
      "keep_tools": false
    }
  ],
  "next_id": 12,
  "next_component_color_index": 0
}