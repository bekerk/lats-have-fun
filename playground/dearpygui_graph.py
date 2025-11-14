#! /usr/bin/env python3

import json

import dearpygui.dearpygui as dpg

dpg.create_context()
NODE_IDS = []
SCROLL_PAN_STEP = 100


def draw(tree, node_ids, idx=0, level=0):
    with dpg.node(tag=tree["id"], label=tree["state"]):
        with dpg.node_attribute(
            tag=tree["id"] + "_in",
            attribute_type=dpg.mvNode_Attr_Input,
        ):
            dpg.add_text(
                default_value=f"parent: {tree['parent']}",
                tag=tree["id"] + "_parent",
            )

        with dpg.node_attribute(
            tag=tree["id"] + "_static",
            attribute_type=dpg.mvNode_Attr_Static,
        ):
            dpg.add_text(
                default_value=f"value: {tree['value']}",
                tag=tree["id"] + "_value",
            )
            dpg.add_text(
                default_value=f"visit_count: {tree['visit_count']}",
                tag=tree["id"] + "_visit_count",
            )
            dpg.add_text(
                default_value=f"reward: {tree['reward']}",
                tag=tree["id"] + "_reward",
            )

        with dpg.node_attribute(
            tag=tree["id"] + "_out",
            attribute_type=dpg.mvNode_Attr_Output,
        ):
            dpg.add_text(default_value="children")

    for child in tree["children"]:
        draw(child, node_ids, level + 1)

    node_ids.append(tree["id"])


def link(tree):
    for child in tree["children"]:
        dpg.add_node_link(tree["id"] + "_out", child["id"] + "_in", parent="dag")
        link(child)


def format(tree, idx=1, level=1):
    for idx, child in enumerate(tree["children"]):
        dpg.set_item_pos(child["id"], (idx * 500, level * 254))
        format(child, idx + 1, level + 1)


def move_right(_sender, _app_data, node_ids):
    for node_id in node_ids:
        x, y = dpg.get_item_pos(node_id)
        dpg.set_item_pos(node_id, (x - SCROLL_PAN_STEP, y))


def move_left(_sender, _app_data, node_ids):
    for node_id in node_ids:
        x, y = dpg.get_item_pos(node_id)
        dpg.set_item_pos(node_id, (x + SCROLL_PAN_STEP, y))


def move_up(_sender, _app_data, node_ids):
    for node_id in node_ids:
        x, y = dpg.get_item_pos(node_id)
        dpg.set_item_pos(node_id, (x, y + SCROLL_PAN_STEP))


def move_down(_sender, _app_data, node_ids):
    for node_id in node_ids:
        x, y = dpg.get_item_pos(node_id)
        dpg.set_item_pos(node_id, (x, y - SCROLL_PAN_STEP))


with dpg.handler_registry():
    dpg.add_key_press_handler(
        key=dpg.mvKey_Right,
        callback=move_right,
        user_data=NODE_IDS,
    )
    dpg.add_key_press_handler(
        key=dpg.mvKey_Left,
        callback=move_left,
        user_data=NODE_IDS,
    )
    dpg.add_key_press_handler(key=dpg.mvKey_Up, callback=move_up, user_data=NODE_IDS)
    dpg.add_key_press_handler(
        key=dpg.mvKey_Down,
        callback=move_down,
        user_data=NODE_IDS,
    )


with open("notebooks/lats_three_gods_tree.json") as f:
    tree = json.load(f)


dpg.create_viewport(title="DearLATS", width=1600, height=1200)
dpg.setup_dearpygui()

with (
    dpg.window(
        tag="Tree",
        label="Tree",
        width=1000,
        height=1000,
        no_scrollbar=False,
        horizontal_scrollbar=True,
    ),
    dpg.node_editor(tag="dag"),
):
    draw(tree, NODE_IDS)
    link(tree)
    format(tree)


dpg.set_primary_window("Tree", True)

dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
