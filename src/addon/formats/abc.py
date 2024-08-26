# ------------------------------------------------------------------------------------------
#  Copyright (c) Natsuneko. All rights reserved.
#  Licensed under the MIT License. See LICENSE in the project root for license information.
# ------------------------------------------------------------------------------------------

# pyright: reportGeneralTypeIssues=false
# pyright: reportUnknownArgumentType=false
# pyright: reportUnknownMemberType=false
# pyright: reportInvalidTypeForm=false

from typing import Set
import bpy

from bpy.props import BoolProperty, FloatProperty
from bpy.types import Context

from .super import ImportWithDefaultsBase, ImportsWithCustomSettingsBase, VIEW3D_MT_Space_Import_BASE
from ..interop import get_current_preset, has_official_api, list_presets, load_preset, log, parse_bool, parse_float


class ImportABCWithDefaults(ImportWithDefaultsBase):
    bl_idname = "object.import_abc_with_defaults"
    bl_label = "Import ABC File"

    def execute(self, context: Context) -> Set[str] | Set[int]:
        bpy.ops.wm.alembic_import(filepath=self.filepath())
        return {"FINISHED"}


class ImportABCWithCustomSettings(ImportsWithCustomSettingsBase):
    bl_idname = "object.import_abc_with_custom_settings"
    bl_label = "Import ABC File"

    # Properties based on Blender v4.0.0 (ordered by parameters on documents)
    relative_path: BoolProperty(default=True, name="Relative Path")
    scale: FloatProperty(default=1.0, min=0.0001, max=1000, name="Scale")
    set_frame_range: BoolProperty(default=True, name="Set Frame Range")
    validate_meshes: BoolProperty(default=False, name="Validate Meshes")
    always_add_cache_reader: BoolProperty(default=False, name="Always Add Cache Reader")
    is_sequence: BoolProperty(default=False, name="Is Sequence")

    manual_transform_section: BoolProperty(default=True, name="Manual Transform")
    options_section: BoolProperty(default=True, name="Option")

    def draw(self, context: Context):
        # Manual Transform Section
        column, state = self.get_expand_column("manual_transform_section")

        if state:
            column.prop(self, "scale")

        # Options Section
        column, state = self.get_expand_column("options_section")

        if state:
            column.prop(self, "relative_path")
            column.prop(self, "set_frame_range")
            column.prop(self, "is_sequence")
            column.prop(self, "validate_meshes")
            column.prop(self, "always_add_cache_reader")

    def execute(self, context: Context) -> Set[str] | Set[int]:
        bpy.ops.wm.alembic_import(
            filepath=self.filepath(),
            relative_path=self.relative_path,
            scale=self.scale,
            set_frame_range=self.set_frame_range,
            validate_meshes=self.validate_meshes,
            always_add_cache_reader=self.always_add_cache_reader,
            is_sequence=self.is_sequence,
        )

        return {"FINISHED"}


class ImportABCWithPresetSettings(ImportABCWithCustomSettings):
    bl_idname = "object.import_abc_with_preset_settings"
    bl_label = "Import ABC File"
    extension = "abc"

    def get_presets(self, context: Context) -> list[tuple[str, str, str]]:
        return [(p, p, p) for p in list_presets("operator\\wm.alembic_import")]

    def execute(self, context: Context):
        presetName: str = get_current_preset(self.extension)
        preset = bpy.utils.preset_find(name=presetName, preset_path="operator\\wm.alembic_import")

        log(f"Using preset: {preset}")

        config: dict[str, str] = load_preset(preset)

        if config.get("relative_path", None) is not None:
            self.relative_path = parse_bool(config.get("relative_path"))

        if config.get("scale", None) is not None:
            self.scale = parse_float(config.get("scale"))

        if config.get("set_frame_range", None) is not None:
            self.set_frame_range = parse_bool(config.get("set_frame_range"))

        if config.get("validate_meshes", None) is not None:
            self.validate_meshes = parse_bool(config.get("validate_meshes"))

        if config.get("always_add_cache_reader", None) is not None:
            self.always_add_cache_reader = parse_bool(config.get("always_add_cache_reader"))

        if config.get("is_sequence", None) is not None:
            self.is_sequence = parse_bool(config.get("is_sequence"))

        super().execute(context)
        return {"FINISHED"}


class VIEW3D_MT_Space_Import_ABC(VIEW3D_MT_Space_Import_BASE):
    bl_label = "Import ABC File"

    @staticmethod
    def format():
        return "abc"


OPERATORS: list[type] = [
    ImportABCWithDefaults,
    ImportABCWithCustomSettings,
    ImportABCWithPresetSettings,
    VIEW3D_MT_Space_Import_ABC,
]

if has_official_api():

    class VIEW3D_FH_Import_ABC(bpy.types.FileHandler):
        bl_idname = "VIEW3D_FH_Import_ABC"
        bl_label = "Import ABC File"
        bl_import_operator = "object.drop_event_listener"
        bl_file_extensions = ".abc"

        @classmethod
        def poll_drop(cls, context: bpy.types.Context | None) -> bool:
            if context is None:
                return False
            return context and context.area and context.area.type == "VIEW_3D"

    OPERATORS.append(VIEW3D_FH_Import_ABC)
