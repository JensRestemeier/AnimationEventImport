

bl_info = {
    "name": "Export Animation Events",
    "author": "Jens Ch. Restemeier",
    "blender": (2, 58, 0),
    "location": "File > Import-Export",
    "description": "Export Animation Events to XML",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "support": 'COMMUNITY',
    "category": "Import-Export"}

if "bpy" in locals():
    import imp
    if "export_events" in locals():
        imp.reload(export_events)


import bpy
from bpy.props import (StringProperty)
from bpy_extras.io_utils import (ExportHelper)

class ExportAnimEvents(bpy.types.Operator, ExportHelper):
    """Export Animation Events to XML"""

    bl_idname = "export_events.xml"
    bl_label = 'Export Events XML'
    bl_options = {'PRESET'}

    filename_ext = ".xml"
    filter_glob = StringProperty(
            default="*.xml",
            options={'HIDDEN'},
            )

    check_extension = True

    def execute(self, context):
        from . import export_events

        keywords = self.as_keywords(ignore=("check_existing",
                                            "filter_glob",
                                            ))
        
        return export_events.save(self, context, **keywords)


def menu_func_export(self, context):
    self.layout.operator(ExportAnimEvents.bl_idname, text="Anim Events (.xml)")


def register():
    bpy.utils.register_module(__name__)

    bpy.types.INFO_MT_file_export.append(menu_func_export)


def unregister():
    bpy.utils.unregister_module(__name__)

    bpy.types.INFO_MT_file_export.remove(menu_func_export)

if __name__ == "__main__":
    register()
