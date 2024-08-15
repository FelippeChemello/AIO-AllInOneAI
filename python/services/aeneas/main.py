import os
import tempfile
import json
from pathlib import Path
from fastapi import APIRouter, File, UploadFile, Form
from fastapi.responses import JSONResponse
from aeneas.executetask import ExecuteTask
from aeneas.task import Task
from aeneas.runtimeconfiguration import RuntimeConfiguration

router = APIRouter()

@router.post("/align")
async def align(text: str = Form(...), audio_file: UploadFile = File(...)):
    audio_file_path = Path(tempfile.mktemp(suffix=".wav"))
    text_file_path = Path(tempfile.mktemp(suffix=".txt"))
    sync_file_path = Path(tempfile.mktemp(suffix=".json"))

    with open(audio_file_path, "wb") as f:
        f.write(await audio_file.read())

    with open(text_file_path, "w") as f:
        f.write("\n".join(text.split()))

    config_string = "task_language=por|is_text_type=plain|os_task_file_level=3|os_task_file_format=json"
    rconf = RuntimeConfiguration()
    rconf[RuntimeConfiguration.MFCC_MASK_NONSPEECH] = "True"
    rconf[RuntimeConfiguration.MFCC_MASK_NONSPEECH_L3] = "True"

    task = Task(config_string=config_string)
    task.text_file_path_absolute = text_file_path
    task.audio_file_path_absolute = audio_file_path
    task.sync_map_file_path_absolute = sync_file_path

    ExecuteTask(task, rconf=rconf).execute()

    task.output_sync_map_file()

    with open(task.sync_map_file_path_absolute, "r") as f:
        sync_map = json.load(f)

    os.remove(audio_file_path)
    os.remove(text_file_path)
    os.remove(sync_file_path)

    return JSONResponse(content=sync_map)
