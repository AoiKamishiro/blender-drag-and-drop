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

from bpy.props import BoolProperty, IntProperty
from bpy.types import Context

from .super import ImportWithDefaultsBase, ImportsWithCustomSettingsBase, VIEW3D_MT_Space_Import_BASE
from ..interop import get_current_preset, has_official_api, list_presets, load_preset, log, parse_bool, parse_int


class ImportDAEWithDefaults(ImportWithDefaultsBase):
    bl_idname = "object.import_dae_with_defaults"
    bl_label = "Import DAE File"

    def execute(self, context: Context) -> Set[str] | Set[int]:
        bpy.ops.wm.collada_import(filepath=self.filepath())
        return {"FINISHED"}


class ImportDAEWithCustomSettings(ImportsWithCustomSettingsBase):
    bl_idname = "object.import_dae_with_custom_settings"
    bl_label = "Import DAE File"

    # Properties based on Blender v4.0.0 (ordered by parameters on documents)
    import_units: BoolProperty(default=False, name="Import Units")
    custom_normals: BoolProperty(default=True, name="Custom Normals")
    fix_orientation: BoolProperty(default=False, name="Fix Leaf Bones")
    find_chains: BoolProperty(default=False, name="Find Bone Chains")
    auto_connect: BoolProperty(default=False, name="Auto Connect")
    min_chain_length: IntProperty(default=0, name="Minimum Chain Length")
    keep_bind_info: BoolProperty(default=False, name="Keep Bind Info")

    import_data_options_section: BoolProperty(default=True, name="Import Data Options")
    armature_options_section: BoolProperty(default=True, name="Armature Options")

    def draw(self, context: Context):
        # Import Data Options Section
        column, state = self.get_expand_column("import_data_options_section")
        if state:
            column.prop(self, "import_units")
            column.prop(self, "custom_normals")

        # Armature Options Section
        column, state = self.get_expand_column("armature_options_section")
        if state:
            column.prop(self, "fix_orientation")
            column.prop(self, "find_chains")
            column.prop(self, "auto_connect")
            column.prop(self, "min_chain_length")

        column = self.get_column()
        column.prop(self, "keep_bind_info")

    def execute(self, context: Context) -> Set[str] | Set[int]:
        bpy.ops.wm.collada_import(
            filepath=self.filepath(),
            import_units=self.import_units,
            custom_normals=self.custom_normals,
            fix_orientation=self.fix_orientation,
            find_chains=self.find_chains,
            auto_connect=self.auto_connect,
            min_chain_length=self.min_chain_length,
            keep_bind_info=self.keep_bind_info,
        )

        return {"FINISHED"}


class ImportDAEWithPresetSettings(ImportDAEWithCustomSettings):
    bl_idname = "object.import_dae_with_preset_settings"
    bl_label = "Import DAE File"
    extension = "dae"

    def get_presets(self, context: Context) -> list[tuple[str, str, str]]:
        return [(p, p, p) for p in list_presets("operator\\wm.collada_import")]

    def execute(self, context: Context):
        presetName: str = get_current_preset(self.extension)
        preset: str = bpy.utils.preset_find(name=presetName, preset_path="operator\\wm.collada_import")

        log(f"Using preset: {preset}")

        config: dict[str, str] = load_preset(preset)

        if config.get("import_units", None) is not None:
            self.import_units = parse_bool(config.get("import_units"))

        if config.get("custom_normals", None) is not None:
            self.custom_normals = parse_bool(config.get("custom_normals"))

        if config.get("fix_orientation", None) is not None:
            self.fix_orientation = parse_bool(config.get("fix_orientation"))

        if config.get("find_chains", None) is not None:
            self.find_chains = parse_bool(config.get("find_chains"))

        if config.get("auto_connect", None) is not None:
            self.auto_connect = parse_bool(config.get("auto_connect"))

        if config.get("min_chain_length", None) is not None:
            self.min_chain_length = parse_int(config.get("min_chain_length"))

        if config.get("keep_bind_info", None) is not None:
            self.keep_bind_info = parse_bool(config.get("keep_bind_info"))

        super().execute(context)
        return {"FINISHED"}


class VIEW3D_MT_Space_Import_DAE(VIEW3D_MT_Space_Import_BASE):
    bl_label = "Import Collada File"

    @staticmethod
    def format():
        return "dae"


OPERATORS: list[type] = [
    ImportDAEWithDefaults,
    ImportDAEWithCustomSettings,
    ImportDAEWithPresetSettings,
    VIEW3D_MT_Space_Import_DAE,
]


if has_official_api():

    class VIEW3D_FH_Import_DAE(bpy.types.FileHandler):
        bl_idname = "VIEW3D_FH_Import_DAE"
        bl_label = "Import Collada File"
        bl_import_operator = "object.drop_event_listener"
        bl_file_extensions = ".dae"

        @classmethod
        def poll_drop(cls, context: bpy.types.Context | None) -> bool:
            if context is None:
                return False
            return context and context.area and context.area.type == "VIEW_3D"

    OPERATORS.append(VIEW3D_FH_Import_DAE)
