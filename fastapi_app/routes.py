from fastapi import APIRouter
from pydantic import BaseModel
from agent.graph import agent

router = APIRouter()

class BuildRequest(BaseModel):
    user_prompt: str
    recursion_limit: int = 100


@router.post("/build")
async def build_project(request: BuildRequest):

    result = agent.invoke(
        {"user_prompt": request.user_prompt},
        {"recursion_limit": request.recursion_limit}
    )

    return {
        "status": "success",
        "message": "Project Generated Successfully",
        "result": str(result)
    }
