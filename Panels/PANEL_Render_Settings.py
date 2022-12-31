import bpy

from Radiant import Utility_Functions

class RADIANT_PT_Render_Settings_Panel(bpy.types.Panel):
    """Quick Access for Render Settings"""
    bl_label = "Render Settings"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Radiant"
    bl_options = {"DEFAULT_CLOSED"}

    @classmethod
    def poll(cls, context):
        preferences = Utility_Functions.get_addon_preferences()
        return preferences.PANEL_Render_Settings_Panel

    def draw(self, context):

        layout = self.layout
        layout.prop(context.scene.render, "engine")

        if context.scene.render.engine == "BLENDER_EEVEE":

            layout.prop(context.scene.eevee, "use_bloom")
            layout.prop(context.scene.eevee, "use_gtao")
            if context.scene.eevee.use_gtao:
                layout.prop(context.scene.eevee, "gtao_distance")
                layout.prop(context.scene.eevee, "gtao_factor")


            layout.prop(context.scene.eevee, "use_ssr")

            if context.scene.eevee.use_ssr:
                layout.prop(context.scene.eevee, "use_ssr_refraction", text="Refraction")

            layout.separator()

        if context.scene.render.engine == "CYCLES":

            layout.prop(context.scene.cycles, "device")

            row = layout.row(align=True)

            row.prop(context.scene.cycles, "use_denoising")
            row.prop(context.scene.cycles, "denoiser", text="")

            row = layout.row(align=True)

            row.prop(context.scene.cycles, "use_preview_denoising")
            row.prop(context.scene.cycles, "preview_denoiser", text="")

        layout.prop(context.scene.render, "film_transparent")

        if context.scene.render.engine == "BLENDER_EEVEE":
            layout.separator()
            layout.label(text="Indirect Light")
            row = layout.row(align=True)
            row.operator("scene.light_cache_bake", text="Bake")
            row.operator("scene.light_cache_free", text="Free")









classes = [RADIANT_PT_Render_Settings_Panel]


def register():
  for cls in classes:
    bpy.utils.register_class(cls)


def unregister():
  for cls in classes:
    bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
