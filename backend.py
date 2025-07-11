from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent import agent
import os

app = FastAPI(title="Agente Multifuente API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Input model
class QueryInput(BaseModel):
    question: str

@app.post("/ask")
async def ask_agent(payload: QueryInput):
    question = payload.question.strip()
    if not question:
        return {"success": False, "error": "La pregunta no puede estar vacía."}
    try:
        response = agent.invoke({"input": question})
        return {"success": True, "response": response["output"]}
    except Exception as e:
        return {"success": False, "error": f"Error: {str(e)}"}

@app.get("/", response_class=HTMLResponse)
async def root():
    return FileResponse("index.html")

@app.get("/app.js")
async def get_js():
    return FileResponse("app.js", media_type="application/javascript")

