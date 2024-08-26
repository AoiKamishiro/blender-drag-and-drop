# ------------------------------------------------------------------------------------------
#  Copyright (c) Natsuneko. All rights reserved.
#  Licensed under the MIT License. See LICENSE in the project root for license information.
# ------------------------------------------------------------------------------------------

# pyright: reportGeneralTypeIssues=false
# pyright: reportUnknownArgumentType=false
# pyright: reportUnknownMemberType=false
# pyright: reportInvalidTypeForm=false

from __future__ import annotations

from .formats import CLASSES
from .interop import try_load, selections
from bpy.props import BoolProperty, EnumProperty
from bpy.types import AddonPreferences, Context
from typing import Callable


items: list[str] = [
    "This addon uses C++ DLL code. Please check DLL publisher and DO NOT replace it.",
    "The C++ DLL hooks calls to certain functions in Blender.exe in order to receive events on drop.",
    "This is the desired behavior as Blender itself does not provide any events for drops.",
    "If you disable the add-on, these behaviors are restored.",
]

formats = [c for c in CLASSES if "WithPresetSettings" in c.__name__]
list_presets: dict[str, Callable[[Context], list[tuple[str, str, str]]]] = {c.extension: c.get_presets for c in formats}


class DragAndDropPreferences(AddonPreferences):
    bl_idname = __package__

    def callback(self, context: Context):
        try_load()
        pass

    is_accept: BoolProperty(name="Accept", default=False, update=callback)

    for c in list_presets:
        exec(f"{c.lower()}_disp_option: EnumProperty(name='Show Import Message', items=selections, default=selections[0][0])")
        exec(f"{c.lower()}_preset: EnumProperty(name='Operator Preset', items=list_presets['{c}'])")

    def draw(self, context: Context):
        layout = self.layout
        column = layout.column()

        column.label(text="Please check the following sections before using this addon:")

        for i, label in enumerate(items):
            column.label(text=f"{i+1}. {label}")

        column.prop(
            self,
            "is_accept",
            text="Using this addon with an understanding of the above",
        )

        column.separator_spacer()

        column.label(text="You can choose whether to display import settings during model import.")

        for c in list_presets:
            row = column.row()
            row.prop(self, f"{c.lower()}_disp_option", text=f"{c.upper()}")
            if getattr(self, f"{c.lower()}_disp_option") == "NEVERCUSTOM":
                row.prop(self, f"{c.lower()}_preset", text="Preset")
        return
