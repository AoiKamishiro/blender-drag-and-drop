# ------------------------------------------------------------------------------------------
#  Copyright (c) Natsuneko. All rights reserved.
#  Licensed under the MIT License. See LICENSE in the project root for license information.
# ------------------------------------------------------------------------------------------

# pyright: reportGeneralTypeIssues=false
# pyright: reportUnknownArgumentType=false
# pyright: reportUnknownMemberType=false

import bpy
import ctypes
import os
import typing

is_load_native_library: bool = False
native_handler: ctypes.CDLL


def has_official_api() -> bool:
    return hasattr(bpy.types, "FileHandler")


def log(message: str):
    print(f"[DRAG-AND-DROP-SUPPORT] {message}")


def is_agree() -> bool:
    prefs = bpy.context.preferences.addons[__package__].preferences
    return typing.cast(bool, prefs.is_accept)


def try_load():
    global is_load_native_library
    global native_handler

    if has_official_api():
        return

    if is_agree():
        if is_load_native_library:
            log("native library already loaded")
            return

        try:
            dirname = os.path.dirname(__file__)
            native = os.path.join(dirname, "blender-injection.dll")
            native_handler = ctypes.cdll.LoadLibrary(native)
            is_load_native_library = True

            log("loaded native library because agree to security policy")

        except:
            is_load_native_library = False
    else:
        log("did not load native library because not agree to security policy")


def try_unload():
    global is_load_native_library
    global native_handler

    if is_load_native_library:
        import _ctypes

        try:
            _ctypes.FreeLibrary(native_handler._handle)
            log("native library unloaded")

            is_load_native_library = False

        except:
            log("failed to unload native library")


selections: list[tuple[str, str, str]] = [
    ("ASKALWAYS", "Ask Always", "Displays import settings each time"),
    ("NEVERDEFAULT", "Always Default Settings", "Always import with default settings without showing import settings"),
    ("NEVERCUSTOM", "Always Custom Settings", "Always import with custom settings without showing import settings"),
]


def get_msg_disp_mode(ext: str) -> str:
    prefs = bpy.context.preferences.addons[__package__].preferences
    if hasattr(prefs, f"{ext.lower()}_disp_option"):
        return typing.cast(str, getattr(prefs, f"{ext.lower()}_disp_option"))
    else:
        return selections[0][0]


def get_current_preset(ext: str) -> str:
    prefs = bpy.context.preferences.addons[__package__].preferences
    if hasattr(prefs, f"{ext.lower()}_preset"):
        return typing.cast(str, getattr(prefs, f"{ext.lower()}_preset"))
    else:
        return ""


def list_presets(preset_subdir: str) -> list[str]:
    preset_dir = os.path.join(bpy.utils.user_resource("SCRIPTS"), "presets", preset_subdir)

    if os.path.exists(preset_dir):
        presets = [f for f in os.listdir(preset_dir) if f.endswith(".py")]
        return [preset.replace(".py", "") for preset in presets]
    else:
        return []


def load_preset(preset_path: str) -> dict[str, str]:

    config: dict[str, str] = {}

    with open(preset_path, "r") as f:
        for line in f:
            line = line.strip()
            if "=" in line:
                key, value = line.split("=")
                key = key.strip()

                value = value.strip()

                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]
                elif value.startswith("'") and value.endswith("'"):
                    value = value[1:-1]

                value = value.strip()

                if not key.startswith("op."):
                    continue

                key = key.replace("op.", "")
                config[key] = value
        config[key] = value

    return config


def parse_bool(value: str | None) -> bool:
    if value is None:
        return False
    return value.lower() == "true"


def parse_float(value: str | None) -> float:
    if value is None:
        return 0.0
    try:
        return float(value)
    except:
        return 0.0
