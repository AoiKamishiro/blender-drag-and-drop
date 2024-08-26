# ------------------------------------------------------------------------------------------
#  Copyright (c) Natsuneko. All rights reserved.
#  Licensed under the MIT License. See LICENSE in the project root for license information.
# ------------------------------------------------------------------------------------------

# pyright: reportGeneralTypeIssues=false
# pyright: reportUnknownArgumentType=false
# pyright: reportUnknownMemberType=false
# pyright: reportInvalidTypeForm=false

import bpy

from bpy.props import BoolProperty, EnumProperty, FloatProperty, StringProperty
from bpy.types import Context

from .super import ImportWithDefaultsBase, ImportsWithCustomSettingsBase, VIEW3D_MT_Space_Import_BASE
from ..interop import get_current_preset, has_official_api, list_presets, load_preset, log, parse_bool, parse_int, parse_float


class ImportUSDWithDefaults(ImportWithDefaultsBase):
    bl_idname = "object.import_usd_with_defaults"
    bl_label = "Import Wavefront USD File (Experimental)"

    def execute(self, context: Context):
        bpy.ops.wm.usd_import(filepath=self.filepath())
        return {"FINISHED"}


class ImportUSDWithCustomSettings(ImportsWithCustomSettingsBase):
    bl_idname = "object.import_usd_with_custom_settings"
    bl_label = "Import Wavefront USD File (Experimental)"

    relative_path: BoolProperty(default=True, name="Relative Path")
    scale: FloatProperty(default=1.0, min=0.0001, max=1000, name="Scale")
    set_frame_range: BoolProperty(default=True, name="Set Frame Range")
    import_cameras: BoolProperty(default=True, name="Cameras")
    import_curves: BoolProperty(default=True, name="Curves")
    import_lights: BoolProperty(default=True, name="Lights")
    import_materials: BoolProperty(default=True, name="Materials")
    import_meshes: BoolProperty(default=True, name="Meshes")
    import_volumes: BoolProperty(default=True, name="Volumes")
    import_shapes: BoolProperty(default=True, name="Shapes")
    import_skeletons: BoolProperty(default=True, name="Skeletons")
    import_blendshapes: BoolProperty(default=True, name="Blend Shapes")
    import_subdiv: BoolProperty(default=False, name="Subdivision")
    import_instance_proxies: BoolProperty(default=True, name="Import Instance Proxies")
    import_visible_only: BoolProperty(default=True, name="Visible Primitives Only")
    create_collection: BoolProperty(default=False, name="Create Collection")
    read_mesh_uvs: BoolProperty(default=True, name="UV Coordinates")
    read_mesh_colors: BoolProperty(default=True, name="Color Attributes")
    read_mesh_attributes: BoolProperty(default=True, name="Mesh Attributes")
    prim_path_mask: StringProperty(default="", name="Path Mask")
    import_guide: BoolProperty(default=False, name="Guide")
    import_proxy: BoolProperty(default=True, name="Proxy")
    import_render: BoolProperty(default=True, name="Render")
    import_all_materials: BoolProperty(default=False, name="Import All Materials")
    import_usd_preview: BoolProperty(default=True, name="Import USD Preview")
    set_material_blend: BoolProperty(default=True, name="Set Material Blend")
    light_intensity_scale: FloatProperty(default=1.0, min=0.0001, max=10000, name="Light Intensity Scale")
    mtl_name_collision_mode: EnumProperty(
        default="MAKE_UNIQUE",
        name="Material Name Collision",
        items=[
            ("MAKE_UNIQUE", "Make Unique", ""),
            ("REFERENCE_EXISTING", "Reference Existing", ""),
        ],
    )
    import_textures_mode: EnumProperty(
        default="IMPORT_PACK",
        name="Import Textures",
        items=[
            ("IMPORT_NONE", "None", ""),
            ("IMPORT_PACK", "Packed", ""),
            ("IMPORT_COPY", "Copy", ""),
        ],
    )
    import_textures_dir: StringProperty(default="//textures/", name="Textures Directory")
    tex_name_collision_mode: EnumProperty(
        default="USE_EXISTING",
        name="File Name Collision",
        items=[("USE_EXISTING", "Use Existing", ""), ("OVERWRITE", "Overwrite", "")],
    )

    def draw(self, context: Context):
        column, box = self.get_heading_column("Data Types")
        column.prop(self, "import_cameras")
        column.prop(self, "import_curves")
        column.prop(self, "import_lights")
        column.prop(self, "import_materials")
        column.prop(self, "import_meshes")
        column.prop(self, "import_volumes")
        column.prop(self, "import_shapes")
        column.prop(self, "import_skeletons")
        column.prop(self, "import_blendshapes")

        column = self.get_column(box=box)
        column.prop(self, "prim_path_mask")
        column.prop(self, "scale")

        column, box = self.get_heading_column("Mesh Data")
        column.prop(self, "read_mesh_uvs")
        column.prop(self, "read_mesh_colors")
        column.prop(self, "read_mesh_attributes")

        column, _ = self.get_heading_column("Include", box=box)
        column.prop(self, "import_subdiv")
        column.prop(self, "import_instance_proxies")
        column.prop(self, "import_visible_only")
        column.prop(self, "import_guide")
        column.prop(self, "import_proxy")
        column.prop(self, "import_render")

        column, _ = self.get_heading_column("Options", box=box)
        column.prop(self, "set_frame_range")
        column.prop(self, "relative_path")
        column.prop(self, "create_collection")

        column = self.get_column(box=box)
        column.prop(self, "light_intensity_scale")

        column, box = self.get_heading_column("Materials")
        column.prop(self, "import_all_materials")
        column.prop(self, "import_usd_preview")

        usd_preview = column.column()
        usd_preview.enabled = self.import_usd_preview
        usd_preview.prop(self, "set_material_blend")

        column = self.get_column(box=box)
        column.prop(self, "mtl_name_collision_mode")

        column = self.get_column()
        column.prop(self, "import_textures_mode")

        texture_mode_copy = column.column()
        texture_mode_copy.enabled = self.import_textures_mode == "IMPORT_COPY"
        texture_mode_copy.prop(self, "import_textures_dir")
        texture_mode_copy.prop(self, "tex_name_collision_mode")

    def execute(self, context: Context):
        bpy.ops.wm.usd_import(
            filepath=self.filepath(),
            relative_path=self.relative_path,
            scale=self.scale,
            set_frame_range=self.set_frame_range,
            import_cameras=self.import_cameras,
            import_curves=self.import_curves,
            import_lights=self.import_lights,
            import_materials=self.import_materials,
            import_meshes=self.import_meshes,
            import_volumes=self.import_volumes,
            import_shapes=self.import_shapes,
            import_skeletons=self.import_skeletons,
            import_blendshapes=self.import_blendshapes,
            import_subdiv=self.import_subdiv,
            import_instance_proxies=self.import_instance_proxies,
            import_visible_only=self.import_visible_only,
            create_collection=self.create_collection,
            read_mesh_uvs=self.read_mesh_uvs,
            read_mesh_colors=self.read_mesh_colors,
            read_mesh_attributes=self.read_mesh_attributes,
            prim_path_mask=self.prim_path_mask,
            import_guide=self.import_guide,
            import_proxy=self.import_proxy,
            import_render=self.import_render,
            import_all_materials=self.import_all_materials,
            import_usd_preview=self.import_usd_preview,
            set_material_blend=self.set_material_blend,
            light_intensity_scale=self.light_intensity_scale,
            mtl_name_collision_mode=self.mtl_name_collision_mode,
            import_textures_mode=self.import_textures_mode,
            import_textures_dir=self.import_textures_dir,
            tex_name_collision_mode=self.tex_name_collision_mode,
        )

        return {"FINISHED"}


class ImportUSDWithPresetSettings(ImportUSDWithCustomSettings):
    bl_idname = "object.import_usd_with_preset_settings"
    bl_label = "Import Wavefront USD File (Experimental)"
    extension = "usd"

    def get_presets(self, context: Context) -> list[tuple[str, str, str]]:
        return [(p, p, p) for p in list_presets("operator\\wm.usd_import")]

    def execute(self, context: Context):
        presetName: str = get_current_preset(self.extension)
        preset: str = bpy.utils.preset_find(name=presetName, preset_path="operator\\wm.usd_import")

        log(f"Using preset: {preset}")

        config: dict[str, str] = load_preset(preset)

        if config.get("relative_path", None) is not None:
            self.relative_path = parse_bool(config.get("relative_path"))

        if config.get("scale", None) is not None:
            self.scale = parse_float(config.get("scale"))

        if config.get("set_frame_range", None) is not None:
            self.set_frame_range = parse_bool(config.get("set_frame_range"))

        if config.get("import_cameras", None) is not None:
            self.import_cameras = parse_bool(config.get("import_cameras"))

        if config.get("import_curves", None) is not None:
            self.import_curves = parse_bool(config.get("import_curves"))

        if config.get("import_lights", None) is not None:
            self.import_lights = parse_bool(config.get("import_lights"))

        if config.get("import_materials", None) is not None:
            self.import_materials = parse_bool(config.get("import_materials"))

        if config.get("import_meshes", None) is not None:
            self.import_meshes = parse_bool(config.get("import_meshes"))

        if config.get("import_volumes", None) is not None:
            self.import_volumes = parse_bool(config.get("import_volumes"))

        if config.get("import_shapes", None) is not None:
            self.import_shapes = parse_bool(config.get("import_shapes"))

        if config.get("import_skeletons", None) is not None:
            self.import_skeletons = parse_bool(config.get("import_skeletons"))

        if config.get("import_blendshapes", None) is not None:
            self.import_blendshapes = parse_bool(config.get("import_blendshapes"))

        if config.get("import_subdiv", None) is not None:
            self.import_subdiv = parse_bool(config.get("import_subdiv"))

        if config.get("import_instance_proxies", None) is not None:
            self.import_instance_proxies = parse_bool(config.get("import_instance_proxies"))

        if config.get("import_visible_only", None) is not None:
            self.import_visible_only = parse_bool(config.get("import_visible_only"))

        if config.get("create_collection", None) is not None:
            self.create_collection = parse_bool(config.get("create_collection"))

        if config.get("read_mesh_uvs", None) is not None:
            self.read_mesh_uvs = parse_bool(config.get("read_mesh_uvs"))

        if config.get("read_mesh_colors", None) is not None:
            self.read_mesh_colors = parse_bool(config.get("read_mesh_colors"))

        if config.get("read_mesh_attributes", None) is not None:
            self.read_mesh_attributes = parse_bool(config.get("read_mesh_attributes"))

        if config.get("prim_path_mask", None) is not None:
            self.prim_path_mask = config.get("prim_path_mask")

        if config.get("import_guide", None) is not None:
            self.import_guide = parse_bool(config.get("import_guide"))

        if config.get("import_proxy", None) is not None:
            self.import_proxy = parse_bool(config.get("import_proxy"))

        if config.get("import_render", None) is not None:
            self.import_render = parse_bool(config.get("import_render"))

        if config.get("import_all_materials", None) is not None:
            self.import_all_materials = parse_bool(config.get("import_all_materials"))

        if config.get("import_usd_preview", None) is not None:
            self.import_usd_preview = parse_bool(config.get("import_usd_preview"))

        if config.get("set_material_blend", None) is not None:
            self.set_material_blend = parse_bool(config.get("set_material_blend"))

        if config.get("light_intensity_scale", None) is not None:
            self.light_intensity_scale = parse_float(config.get("light_intensity_scale"))

        if config.get("mtl_name_collision_mode", None) is not None:
            self.mtl_name_collision_mode = config.get("mtl_name_collision_mode")

        if config.get("import_textures_mode", None) is not None:
            self.import_textures_mode = config.get("import_textures_mode")

        if config.get("import_textures_dir", None) is not None:
            self.import_textures_dir = config.get("import_textures_dir")

        if config.get("tex_name_collision_mode", None) is not None:
            self.tex_name_collision_mode = config.get("tex_name_collision_mode")

        super().execute(context)
        return {"FINISHED"}


class VIEW3D_MT_Space_Import_USD(VIEW3D_MT_Space_Import_BASE):
    bl_label = "Import Universal Scene Description File"

    @staticmethod
    def format():
        return "usd"


class VIEW3D_MT_Space_Import_USDA(VIEW3D_MT_Space_Import_BASE):
    bl_label = "Import Universal Scene Description File"

    @staticmethod
    def format():
        return "usd"


class VIEW3D_MT_Space_Import_USDC(VIEW3D_MT_Space_Import_BASE):
    bl_label = "Import Universal Scene Description File"

    @staticmethod
    def format():
        return "usd"


class VIEW3D_MT_Space_Import_USDZ(VIEW3D_MT_Space_Import_BASE):
    bl_label = "Import Universal Scene Description File"

    @staticmethod
    def format():
        return "usd"


OPERATORS: list[type] = [
    ImportUSDWithDefaults,
    ImportUSDWithCustomSettings,
    ImportUSDWithPresetSettings,
    VIEW3D_MT_Space_Import_USD,
    VIEW3D_MT_Space_Import_USDA,
    VIEW3D_MT_Space_Import_USDC,
    VIEW3D_MT_Space_Import_USDZ,
]

if has_official_api():

    class VIEW3D_FH_Import_USD(bpy.types.FileHandler):
        bl_idname = "VIEW3D_FH_Import_USD"
        bl_label = "Import Universal Scene Description File"
        bl_import_operator = "object.drop_event_listener"
        bl_file_extensions = ".usd"

        @classmethod
        def poll_drop(cls, context: bpy.types.Context | None) -> bool:
            if context is None:
                return False
            return context and context.area and context.area.type == "VIEW_3D"

    class VIEW3D_FH_Import_USDA(bpy.types.FileHandler):
        bl_idname = "VIEW3D_FH_Import_USDA"
        bl_label = "Import Universal Scene Description File"
        bl_import_operator = "object.drop_event_listener"
        bl_file_extensions = ".usda"

        @classmethod
        def poll_drop(cls, context: bpy.types.Context | None) -> bool:
            if context is None:
                return False
            return context and context.area and context.area.type == "VIEW_3D"

    class VIEW3D_FH_Import_USDC(bpy.types.FileHandler):
        bl_idname = "VIEW3D_FH_Import_USDC"
        bl_label = "Import Universal Scene Description File"
        bl_import_operator = "object.drop_event_listener"
        bl_file_extensions = ".usdc"

        @classmethod
        def poll_drop(cls, context: bpy.types.Context | None) -> bool:
            if context is None:
                return False
            return context and context.area and context.area.type == "VIEW_3D"

    class VIEW3D_FH_Import_USDZ(bpy.types.FileHandler):
        bl_idname = "VIEW3D_FH_Import_USDZ"
        bl_label = "Import Universal Scene Description File"
        bl_import_operator = "object.drop_event_listener"
        bl_file_extensions = ".usdz"

        @classmethod
        def poll_drop(cls, context: bpy.types.Context | None) -> bool:
            if context is None:
                return False
            return context and context.area and context.area.type == "VIEW_3D"

    OPERATORS.extend(
        [
            VIEW3D_FH_Import_USD,
            VIEW3D_FH_Import_USDA,
            VIEW3D_FH_Import_USDC,
            VIEW3D_FH_Import_USDZ,
        ]
    )
