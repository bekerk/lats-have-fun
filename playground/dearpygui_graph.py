#!/usr/bin/env python3

import json

import dearpygui.dearpygui as dpg

dpg.create_context()
NODE_IDS = []
SCROLL_PAN_STEP = 100
START_COLOR = (0, 0, 150)
END_COLOR = (0, 150, 0)


def set_themes():
    themes = {}
    with dpg.theme() as start_node_theme:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(
                dpg.mvNodeCol_TitleBar, START_COLOR, category=dpg.mvThemeCat_Nodes
            )
            themes["start_node_theme"] = start_node_theme

    with dpg.theme() as end_node_theme:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(
                dpg.mvNodeCol_TitleBar, END_COLOR, category=dpg.mvThemeCat_Nodes
            )
            themes["end_node_theme"] = end_node_theme

    return themes


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


def layout(tree, level=0, spacing=(254, 254), next_x=None, reward_node_id=None):
    if next_x is None:
        next_x = {"value": 0}

    if tree["reward"] == 1:
        reward_node_id = tree["id"]

    child_positions = []
    for child in tree["children"]:
        child_result = layout(child, level + 1, spacing, next_x, reward_node_id)
        child_positions.append(child_result)

        if child_result[2] is not None:
            reward_node_id = child_result[2]

    if child_positions:
        x = sum(cp[0] for cp in child_positions) / len(child_positions)
    else:
        x = next_x["value"]
        next_x["value"] += 1

    dpg.set_item_pos(tree["id"], (x * spacing[0], level * spacing[1]))

    return (x, level, reward_node_id)


def bind_themes(head, final_node, themes):
    dpg.bind_item_theme(head, themes.get("start_node_theme"))
    if final_node is not None:
        dpg.bind_item_theme(final_node, themes.get("end_node_theme"))


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
    head = tree["id"]
    themes = set_themes()
    draw(tree, NODE_IDS)
    link(tree)
    _x, _y, final_node = layout(tree)
    bind_themes(head, final_node, themes)


dpg.set_primary_window("Tree", True)

dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
