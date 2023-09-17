# ------------------------------------------------------------------------------------------
#  Copyright (c) Natsuneko. All rights reserved.
#  Licensed under the MIT License. See LICENSE in the project root for license information.
# ------------------------------------------------------------------------------------------

# pyright: reportGeneralTypeIssues=false
# pyright: reportUnknownArgumentType=false
# pyright: reportUnknownMemberType=false

from __future__ import annotations

import bpy
import os
import typing

from bpy.props import StringProperty  # type: ignore
from bpy.types import Context, Event, Operator

from .formats.super import ImportWithDefaultsBase, VIEW3D_MT_Space_Import_BASE

# formats that Blender does not supported by default
conditionals: typing.Dict[str, typing.Callable[[], bool]] = {
    "vrm": lambda: hasattr(bpy.ops.import_scene, "vrm"),
}


class DropEventListener(Operator):
    bl_idname = "object.drop_event_listener"
    bl_label = "Open File via Drag and Drop"

    filename: StringProperty()  # type: ignore

    def inflate(self, name: str):
        VIEW3D_MT_Space_Import_BASE.filename = self.filename  # type: ignore
        bpy.ops.wm.call_menu(name=name)  # type: ignore
        return

    def invoke(self, context: Context, event: Event):
        try:
            path = typing.cast(str, self.filename)  # type: ignore
            _, ext = os.path.splitext(path)

            if ext[1:] in conditionals:
                if not conditionals[ext[1:].lower()]():
                    return {"FINISHED"}

            # dynamically called importer
            name = f"VIEW3D_MT_Space_Import_{ext[1:].upper()}"
            self.inflate(name)
        except TypeError as e:
            print(e)

        return {"FINISHED"}


class ImportABCWithDefaults(ImportWithDefaultsBase):
    bl_idname = "object.import_abc_with_defaults"
    bl_label = "Import Alembic File"

    def execute(self, context: Context):
        bpy.ops.wm.alembic_import(filepath=self.filepath())  # type: ignore
        return {"FINISHED"}


class ImportBVHWithDefaults(ImportWithDefaultsBase):
    bl_idname = "object.import_bvh_with_defaults"
    bl_label = "Import Biovision Hierarchy File"

    def execute(self, context: Context):
        bpy.ops.import_anim.bvh(filepath=self.filepath())  # type: ignore
        return {"FINISHED"}


class ImportDAEWithDefaults(ImportWithDefaultsBase):
    bl_idname = "object.import_dae_with_defaults"
    bl_label = "Import Collada File"

    def execute(self, context: Context):
        bpy.ops.wm.collada_import(filepath=self.filepath())  # type: ignore
        return {"FINISHED"}


class ImportPLYWithDefaults(ImportWithDefaultsBase):
    bl_idname = "object.import_ply_with_defaults"
    bl_label = "Import PLY File"

    def execute(self, context: Context):
        bpy.ops.import_mesh.ply(filepath=self.filepath())  # type: ignore
        return {"FINISHED"}


class ImportSTLWithDefaults(ImportWithDefaultsBase):
    bl_idname = "object.import_stl_with_defaults"
    bl_label = "Import STL File"

    def execute(self, context: Context):
        bpy.ops.import_mesh.stl(filepath=self.filepath())  # type: ignore
        return {"FINISHED"}


class ImportSVGWithDefaults(ImportWithDefaultsBase):
    bl_idname = "object.import_svg_with_defaults"
    bl_label = "Import SVG File"

    def execute(self, context: Context):
        bpy.ops.import_curve.svg(filepath=self.filepath())  # type: ignore
        return {"FINISHED"}


class ImportUSDWithDefaults(ImportWithDefaultsBase):
    bl_idname = "object.import_svg_with_defaults"
    bl_label = "Import SVG File"

    def execute(self, context: Context):
        bpy.ops.wm.usd_import(filepath=self.filepath())  # type: ignore
        return {"FINISHED"}


class ImportX3DWithDefaults(ImportWithDefaultsBase):
    bl_idname = "object.import_x3d_with_defaults"
    bl_label = "Import X3D File"

    def execute(self, context: Context):
        bpy.ops.import_scene.x3d(filepath=self.filepath())  # type: ignore
        return {"FINISHED"}
