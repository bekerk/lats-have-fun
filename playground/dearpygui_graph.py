#! /usr/bin/env python3

import json
import dearpygui.dearpygui as dpg

dpg.create_context()
NODE_IDS = []
SCROLL_PAN_STEP = 40


def draw(tree, node_ids, idx=0, level=0):
    with dpg.node(tag=tree["id"], label=tree["state"]):
        with dpg.node_attribute(
            tag=tree["id"] + "_in", attribute_type=dpg.mvNode_Attr_Input
        ):
            dpg.add_text(default_value=f"parent: {tree['parent']}", tag=tree["id"] + "_parent")

        with dpg.node_attribute(
            tag=tree["id"] + "_static", attribute_type=dpg.mvNode_Attr_Static
        ):
            dpg.add_text(default_value=f"value: {tree['value']}", tag=tree["id"] + "_value")
            dpg.add_text(
                default_value=f"visit_count: {tree['visit_count']}", tag=tree["id"] + "_visit_count"
            )
            dpg.add_text(default_value=f"reward: {tree['reward']}", tag=tree["id"] + "_reward")
            dpg.add_text(
                default_value=f"is_terminal: {tree['is_terminal']}", tag=tree["id"] + "_is_terminal"
            )

        with dpg.node_attribute(
            tag=tree["id"] + "_out", attribute_type=dpg.mvNode_Attr_Output
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
        dpg.set_item_pos(child["id"], (idx * 500, level * 500))
        format(child, idx + 1, level + 1)


def pan_nodes(sender, app_data, node_ids):
    delta_y = app_data * SCROLL_PAN_STEP

    for node_id in node_ids:
        x, y = dpg.get_item_pos(node_id)
        dpg.set_item_pos(node_id, (x, y + delta_y))


def click_handler(sender, app_data, node_ids):
    print(sender, app_data, node_ids)

    return None


with open("notebooks/lats_three_gods_tree.json", "r") as f:
    tree = json.load(f)

dpg.create_viewport(title="DearLATS", width=1000, height=1000)
dpg.setup_dearpygui()

with dpg.window(
    tag="Tree",
    label="Tree",
    width=1000,
    height=1000,
    no_scrollbar=False,
    horizontal_scrollbar=True,
):
    with dpg.node_editor(tag="dag"):
        draw(tree, NODE_IDS)
        link(tree)
        format(tree)

with dpg.handler_registry():
    dpg.add_mouse_wheel_handler(callback=pan_nodes, user_data=NODE_IDS)


dpg.set_primary_window("Tree", True)
dpg.configure_item("Tree", no_scrollbar=False, horizontal_scrollbar=True)

dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
