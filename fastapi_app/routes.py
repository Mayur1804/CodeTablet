from fastapi import APIRouter,Query
from fastapi.responses import StreamingResponse, FileResponse
from pydantic import BaseModel
from agent.graph import agent
import json
import shutil
from agent.tools import set_project_root
from datetime import datetime
from pathlib import Path
import os

router = APIRouter()


class BuildRequest(BaseModel):
    user_prompt: str
    recursion_limit: int = 100



from fastapi import Query

@router.get("/download")
def download_project(project_name: str = Query(...)):

    project_path = Path.cwd() / project_name
    zip_path = str(project_path) + ".zip"

    if os.path.exists(zip_path):
        os.remove(zip_path)

    shutil.make_archive(str(project_path), 'zip', str(project_path))

    return FileResponse(
        path=zip_path,
        media_type="application/zip",
        filename=os.path.basename(zip_path)
    )




@router.post("/build/stream")
async def stream_build(request: BuildRequest):

    # 🔥 Create project folder ONLY ONCE
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    project_folder = Path.cwd() / f"generated_project_{timestamp}"

    set_project_root(str(project_folder))

    project_name = project_folder.name


    def event_generator():

        for event in agent.stream(
            {"user_prompt": request.user_prompt},
            {"recursion_limit": request.recursion_limit}
        ):
            for node_name, output in event.items():

                data = {"node": node_name,
                "project_name": project_name
                }

                yield "data: " + json.dumps(data) + "\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )
