
### EO-Learn / SentinelHub ###
from eolearn.core import (
    EOExecutor,
    FeatureType,
    SaveTask,
    OverwritePermission,
    EOWorkflow,
    linearly_connect_tasks
    )
from eolearn.io import VectorImportTask
from eolearn.geometry import VectorToRasterTask

def make_and_run_workflow(parcelles_path, bbox_list, resolution=10):
    print(Fore.MAGENTA + "\n⏳ EO Workflow init and run" + Style.RESET_ALL)
    vector_feature = FeatureType.VECTOR_TIMELESS, "RPG_REFERENCE"

    vector_import_task = VectorImportTask(vector_feature, parcelles_path)

    rasterization_task = VectorToRasterTask(
        vector_feature,
        (FeatureType.MASK_TIMELESS, "MASK"),
        values_column="code_group",
        raster_resolution=resolution,
        raster_dtype=np.uint8
    )

    save = SaveTask(EOPATCH_FOLDER, overwrite_permission=OverwritePermission.OVERWRITE_FEATURES)
    workflow_nodes = linearly_connect_tasks(
        vector_import_task, rasterization_task, save
    )

    workflow = EOWorkflow(workflow_nodes)
    input_node = workflow_nodes[0]
    save_node = workflow_nodes[-1]
    exec_args = []

    for idx, bbox in enumerate(bbox_list):
        exec_args.append(
            {
                input_node: {"bbox": bbox},
                save_node: {"eopatch_folder": f"eopatch_{idx}"}
            }
        )

    executor = EOExecutor(workflow, exec_args, save_logs=True)
    executor.run(workers=None)
    executor.make_report()
    print(f"✅ Workflow Done !")
