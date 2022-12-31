
import bpy


from . import LIST_Radiant_Tags

modules = [LIST_Radiant_Tags]

def register():
    for module in modules:

        module.register()

def unregister():
    for module in modules:
        module.unregister()

if __name__ == "__main__":
    register()
