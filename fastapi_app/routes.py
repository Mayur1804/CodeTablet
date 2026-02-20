from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from agent.graph import agent
import json

router = APIRouter()

class BuildRequest(BaseModel):
    user_prompt: str
    recursion_limit: int = 100


@router.post("/build/stream")
async def stream_build(request: BuildRequest):

    def event_generator():

        for event in agent.stream(
            {"user_prompt": request.user_prompt},
            {"recursion_limit": request.recursion_limit}
        ):
            for node_name, output in event.items():

                data = {
                    "node": node_name,
                    "output": str(output)
                }

                json_data = json.dumps(data)

                yield "data: " + json_data + "\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream"
    )
