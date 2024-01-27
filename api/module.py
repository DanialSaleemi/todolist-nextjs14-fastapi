from pydantic import BaseModel

# define the todo item model
class TodoItem(BaseModel):
    id: int
    title: str
    completed: bool

class createTodoItem(BaseModel):
    title: str

class updateTodoItem(BaseModel):
    title: str
    completed: bool

class deleteTodoItem(BaseModel):
    id: int

