from fastapi import FastAPI, Body, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from api._database import engine
from api._schema import Todolist
from api._module import createTodoItem, TodoItem, deleteTodoItem
from typing import Union, List
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

app = FastAPI(docs_url="/api/docs", openapi_url="/api/openapi.json")


updateitemtype = Union[Todolist, None]

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

class updateTodoItem(BaseModel):
    title: str = ''
    completed: bool = False


# define content for error
def missingitemexception(item_id: int):
    return {"Message": f"Item with id = {str(item_id)} does not exist"}



# get list of all todo items
@app.get("/api/todos", response_model=List[TodoItem])
def get_todos() -> List[TodoItem]:       
    """
    Retrieve all todo items from the API.

    Returns:
        list[TodoItem]: A list of todo items.

    Raises:
        HTTPException: If the list is empty.

    """
    with Session(engine) as session:
        items : List[Todolist] = session.query(Todolist).all()
        if len(items) > 0:
            list_todos : List[TodoItem] = []
            for item in items:
                list_todos.append(TodoItem(id=item.id, title=item.title, completed=item.completed))
            return list_todos
        else:
            raise HTTPException(status_code=404, detail="List is empty")                         

# get a specific item by item id
@app.get("/api/todos/{item_id}", response_model=TodoItem)
def get_todo_by_id(item_id: int) -> Todolist:
    """
    Retrieves a todo item by its ID.

    Parameters:
        item_id (int): The ID of the todo item to retrieve.

    Returns:
        Todolist: The retrieved todo item.

    Raises:
        HTTPException: If the todo item with the specified ID does not exist.
    """
    with Session(engine) as session:
        item : Todolist = session.query(Todolist).filter(Todolist.id == item_id).one()
        if item:            
            return item
        else:
            raise HTTPException(status_code=404, detail=missingitemexception(item_id))                         

# add an item
@app.post("/api/todos", response_model=TodoItem)
def additem(item: str = Body(embed=True)) -> TodoItem:
    """
    Add a new item to the todo list.
    Parameters:
      - item (str): The title of the item to add.
    Returns:
      - Todolist: The newly added item.
    """
    with Session(engine) as session:
        new_item : Todolist = Todolist(title=item, completed=False)
        session.add(new_item)
        session.commit()
        return TodoItem(id=new_item.id, title=new_item.title, completed=new_item.completed)

# update an item
@app.patch("/api/todos/{item_id}", response_model=TodoItem)
def update_item(item_id : int, item : updateTodoItem = Body(embed=True)) -> TodoItem:

    """
    Updates a todo item with the given item ID.

    Parameters:
        item_id (int): The ID of the item to be updated.
        item (updateTodoItem): The updated item data.

    Returns:
        TodoItem: The updated todo item.

    Raises:
        HTTPException: If the item with the given ID does not exist.
    """
    with Session(engine) as session:
            update_item : Todolist = session.query(Todolist).filter(Todolist.id == item_id).one()
            if update_item:
                update_item.title = item.title if item.title else update_item.title
                update_item.completed = item.completed if item.completed != update_item.completed else update_item.completed
                session.commit()
                return TodoItem(id=update_item.id, title=update_item.title, completed=update_item.completed) # updateditem
            else:
                raise HTTPException(status_code=404, detail=missingitemexception(item_id))
        
# delete an item
@app.delete("/api/todos/{item_id}", response_model=TodoItem)
def delete_item(item_id: int) -> TodoItem:
    """
    Deletes a todo item with the given item_id.

    Parameters:
        item_id (int): The ID of the todo item to be deleted.

    Returns:
        TodoItem: The deleted todo item.

    Raises:
        HTTPException: If the todo item with the given item_id is not found.
    """
    with Session(engine) as session:
        try:
            todos: Todolist = session.query(Todolist).filter(Todolist.id == item_id).one()
            if todos:
                session.delete(todos)
                session.commit()
                session.flush()
                session.close()
            deleted_item: TodoItem = TodoItem(id=todos.id, title=todos.title, completed=todos.completed)
            return deleted_item
        except NoResultFound:
            raise HTTPException(status_code=404, detail=missingitemexception(item_id))
            

# delete all items
@app.delete("/api/todos", response_model=dict)
def delete_list() -> dict:
    """
    Deletes all items in the todo list.

    Parameters:
    None

    Returns:
    If the list is successfully deleted, it returns a dictionary with an "INFO" key. 
    The value of the "INFO" key is a string that indicates the number of rows deleted.
    If there are no items in the list, it returns a string indicating that there are no items available.
    """
    with Session(engine) as session:
        rows_deleted = session.query(Todolist).delete()
        session.commit()
        if rows_deleted > 0:
            return {"INFO": f"List is empty, No. of rows deleted: {rows_deleted}"}
        else:
            return {"INFO": "No items available in the list"}
