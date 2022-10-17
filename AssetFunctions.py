# Python API - https://docs.unrealengine.com/5.0/en-US/PythonAPI/
# import AssetFunctions
# import importlib
# importlib.reload(AssetFunctions)
# AssetFunctions.import_my_assets()

import unreal


# unreal.EditorAssetLibrary
# https://docs.unrealengine.com/5.0/en-US/PythonAPI/class/EditorAssetLibrary.html
def save_asset():
    unreal.EditorAssetLibrary.save_asset('/Game/Textures/T_Texture01', only_if_is_dirty=False)


def save_directory():
    unreal.EditorAssetLibrary.save_directory('/Game/Textures', only_if_is_dirty=True)


# unreal.Package
# https://docs.unrealengine.com/5.0/en-US/PythonAPI/class/Package.html
def get_package_from_path():
    return unreal.load_package('/Game/Textures/T_Texture01')


# unreal.EditorLoadingAndSavingUtils
# https://docs.unrealengine.com/5.0/en-US/PythonAPI/class/EditorLoadingAndSavingUtils.html
def get_all_dirty_packages():
    packages = unreal.Array(unreal.Package)
    for x in unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages():
        packages.append(x)
    for x in unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages():
        packages.append(x)
    return packages


def save_all_dirty_packages(show_dialog=False):
    if show_dialog:
        unreal.EditorLoadingAndSavingUtils.save_dirty_packages_with_dialog(save_map_packages=True, save_content_packages=True)
    else:
        unreal.EditorLoadingAndSavingUtils.save_dirty_packages(save_map_packages=True, save_content_packages=True)


def save_packages(packages=[], show_dialog=False):
    if show_dialog:
        unreal.EditorLoadingAndSavingUtils.save_dirty_packages_with_dialog(packages, only_dirty=False)  # only_dirty=False:
    else:                                                                                               # looks like that it's not
        unreal.EditorLoadingAndSavingUtils.save_packages(packages, only_dirty=False)                    # working properly at the moment


# Sadly "unreal.Package.set_dirty_flag(is_dirty=True)" is currently not available in python, only c++


texture1_tga = 'F:/Projects/Repo/Python/Unreal/PythonScripts/Assets/T_Texture01.jpg'
texture2_tga = 'F:/Projects/Repo/Python/Unreal/PythonScripts/Assets/T_Texture02.jpg'
static_mesh_fbx = 'F:/Projects/Repo/Python/Unreal/PythonScripts/Assets/SM_Mesh01.fbx'
skeletal_mesh_fbx = 'F:/Projects/Repo/Python/Unreal/PythonScripts/Assets/SK_Mesh01.fbx'
animation_fbx = 'F:/Projects/Repo/Python/Unreal/PythonScripts/Assets/SK_Anim01.fbx'


def import_my_assets():
    # task1 = build_import_task(texture1_tga, '/Game/Textures')
    # task2 = build_import_task(texture2_tga, '/Game/Textures')
    # static_mesh_task = build_import_task(static_mesh_fbx, '/Game/StaticMeshes', build_static_mesh_import_options())
    # skeletal_mesh_task = build_import_task(skeletal_mesh_fbx, '/Game/SkeletalMeshes', build_skeletal_mesh_import_options())
    animation_task = build_import_task(animation_fbx, '/Game/Animations', build_animation_import_options('/Game/SkeletalMeshes/SK_Mesh01_Skeleton.SK_Mesh01_Skeleton'))
    execute_import_tasks([animation_task])


# unreal.AssetImportTask
# https://docs.unrealengine.com/5.0/en-US/PythonAPI/class/AssetImportTask.html
def build_import_task(filename, destination_path, options=None):
    task = unreal.AssetImportTask()
    task.set_editor_property('automated', True)
    task.set_editor_property('destination_name', '')
    task.set_editor_property('destination_path', destination_path)
    task.set_editor_property('filename', filename)
    task.set_editor_property('replace_existing', True)
    task.set_editor_property('save', True)
    task.set_editor_property('options', options)
    return task


# unreal.AssetTools
# https://docs.unrealengine.com/5.0/en-US/PythonAPI/class/AssetTools.html
def execute_import_tasks(tasks):
    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks(tasks)
    for task in tasks:
        for path in task.get_editor_property('imported_object_paths'):
            print('Imported: %s' % path)


# unreal.FbxImportUI
# https://docs.unrealengine.com/5.0/en-US/PythonAPI/class/FbxImportUI.html
# unreal.FbxMeshImportData
# https://docs.unrealengine.com/5.0/en-US/PythonAPI/class/FbxStaticMeshImportData.html
# unreal.FbxStaticMeshImportData
# https://docs.unrealengine.com/5.0/en-US/PythonAPI/class/FbxMeshImportData.html
# https://docs.unrealengine.com/5.0/en-US/PythonAPI/class/FbxSkeletalMeshImportData.html
def build_static_mesh_import_options():
    options = unreal.FbxImportUI()
    # unreal.FbxImportUI
    options.set_editor_property('import_mesh', True)
    options.set_editor_property('import_textures', False)
    options.set_editor_property('import_materials', True)
    options.set_editor_property('import_as_skeletal', False)  # Static Mesh
    # unreal.FbxMeshImportData
    options.static_mesh_import_data.set_editor_property('import_translation', unreal.Vector(0.0, 0.0, 0.0))
    options.static_mesh_import_data.set_editor_property('import_rotation', unreal.Rotator(0.0, 0.0, 0.0))
    options.static_mesh_import_data.set_editor_property('import_uniform_scale', 1.0)
    # unreal.FbxStaticMeshImportData
    options.static_mesh_import_data.set_editor_property('combine_meshes', True)
    options.static_mesh_import_data.set_editor_property('generate_lightmap_u_vs', True)
    options.static_mesh_import_data.set_editor_property('auto_generate_collision', True)
    return options


# unreal.FbxImportUI
# https://docs.unrealengine.com/5.0/en-US/PythonAPI/class/FbxImportUI.html
# unreal.FbxMeshImportData
# https://docs.unrealengine.com/5.0/en-US/PythonAPI/class/FbxStaticMeshImportData.html
# unreal.FbxSkeletalMeshImportData
# https://docs.unrealengine.com/5.0/en-US/PythonAPI/class/FbxSkeletalMeshImportData.html
def build_skeletal_mesh_import_options():
    options = unreal.FbxImportUI()
    # unreal.FbxImportUI
    options.set_editor_property('import_mesh', True)
    options.set_editor_property('import_textures', True)
    options.set_editor_property('import_materials', True)
    options.set_editor_property('import_as_skeletal', True)  # Skeletal Mesh
    # unreal.FbxMeshImportData
    options.skeletal_mesh_import_data.set_editor_property('import_translation', unreal.Vector(0.0, 0.0, 0.0))
    options.skeletal_mesh_import_data.set_editor_property('import_rotation', unreal.Rotator(0.0, 0.0, 0.0))
    options.skeletal_mesh_import_data.set_editor_property('import_uniform_scale', 1.0)
    # unreal.FbxSkeletalMeshImportData
    options.skeletal_mesh_import_data.set_editor_property('import_morph_targets', True)
    options.skeletal_mesh_import_data.set_editor_property('update_skeleton_reference_pose', False)
    return options


# unreal.FbxImportUI
# https://docs.unrealengine.com/5.0/en-US/PythonAPI/class/FbxImportUI.html
# unreal.FbxAssetImportData
# https://docs.unrealengine.com/5.0/en-US/PythonAPI/class/FbxAssetImportData.html
# unreal.FbxAnimSequenceImportData
# https://docs.unrealengine.com/5.0/en-US/PythonAPI/class/FbxAnimSequenceImportData.html
# FBXAnimationLengthImportType
# https://docs.unrealengine.com/5.0/en-US/PythonAPI/class/FBXAnimationLengthImportType.html
def build_animation_import_options(skeleton_path):
    options = unreal.FbxImportUI()
    # unreal.FbxImportUI
    options.set_editor_property('import_animations', True)
    options.skeleton = unreal.load_asset(skeleton_path)
    # unreal.FbxMeshImportData
    options.anim_sequence_import_data.set_editor_property('import_translation', unreal.Vector(0.0, 0.0, 0.0))
    options.anim_sequence_import_data.set_editor_property('import_rotation', unreal.Rotator(0.0, 0.0, 0.0))
    options.anim_sequence_import_data.set_editor_property('import_uniform_scale', 1.0)
    # unreal.FbxAnimationSequenceImportData
    options.anim_sequence_import_data.set_editor_property('animation_length', unreal.FBXAnimationLengthImportType.FBXALIT_EXPORTED_TIME)
    options.anim_sequence_import_data.set_editor_property('remove_redundant_keys', False)
    return options