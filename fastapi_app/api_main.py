from fastapi import FastAPI
from fastapi_app.routes import router

app = FastAPI(
    title="CodeTablet Agent API",
    version="1.0"
)

app.include_router(router)


@app.get("/")
def home():
    return {"message": "LangGraph Agent Running 🚀"}
