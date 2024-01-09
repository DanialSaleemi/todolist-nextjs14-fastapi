from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(docs_url="/api/docs", openapi_url="/api/openapi.json")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
def health_check():
    return {"status": "success", "message" : "Hello from fastapi proxy server"} 

# class TodoItem(BaseModel):
#     id: int
#     title: str
#     completed: bool

# class createTodoItem(BaseModel):
#     title: str
#     completed: bool

# class updateTodoItem(BaseModel):
#     title: str
#     completed: bool

# class deleteTodoItem(BaseModel):
#     id: int