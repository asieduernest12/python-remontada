from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from fastapi_sqlalchemy import DBSessionMiddleware, db
from alembic import command
from alembic.config import Config
from fastapi.middleware.cors import CORSMiddleware
import os
from fastapi.responses import JSONResponse
import logging
from starlette.requests import Request
from alembic import context

DATABASE_URL = "sqlite:///./db/todo.db"

Base = declarative_base()

class TodoItem(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)

    def toTodoItem(self):
        return TodoItemCreate(id=self.id,title=self.title,description=self.description)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI()
router = APIRouter()
# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add middleware to return all internal errors when in development
if os.getenv("ENV") == "development":
    @router.middleware("http")
    async def catch_exceptions_middleware(request, call_next):
        try:
            return await call_next(request)
        except Exception as e:
            return JSONResponse(
                status_code=500,
                content={"detail": str(e)},
            )

app.add_middleware(DBSessionMiddleware, db_url=DATABASE_URL)

class TodoItemCreate(BaseModel):
    id: Optional[int]
    title: str
    description: str
    
    @classmethod
    def from_orm(cls, todo_item: TodoItem):
        return cls(
            id=todo_item.id,
            title=todo_item.title,
            description=todo_item.description
        )

@router.on_event("startup")
def on_startup():
    try:
        # Create the database tables
        Base.metadata.create_all(bind=engine)
        # Run migrations
        alembic_cfg = Config("alembic.ini")
        alembic_cfg.set_main_option("sqlalchemy.url", DATABASE_URL)
        command.upgrade(alembic_cfg, "head")
        logger.info("Startup: Database tables created and migrations applied.")
    except Exception as e:
        logger.error(f"Startup error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Startup error: {str(e)}")

@router.on_event("shutdown")
def on_shutdown():
    try:
        db.session.close()
        logger.info("Shutdown: Database session closed.")
    except Exception as e:
        logger.error(f"Shutdown error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Shutdown error: {str(e)}")


@router.get('/hello')
def hello():
    return 'world'

@router.post("/todos/", response_model=TodoItemCreate)
def create_todo(todo: TodoItemCreate):
    db_todo = TodoItem(title=todo.title, description=todo.description)
    db.session.add(db_todo)
    db.session.commit()
    db.session.refresh(db_todo)
    return TodoItemCreate(**db_todo.__dict__)

@router.get("/todos/", response_model=List[TodoItemCreate])
def read_todos(skip: int = 0, limit: int = 10):
    todos = db.session.query(TodoItem).offset(skip).limit(limit).all()
    todos = [TodoItemCreate(**vars(todo)) for todo in todos]
    return todos

@router.get("/todos/{todo_id}", response_model=TodoItemCreate)
def read_todo(todo_id: int):
    todo = db.session.query(TodoItem).filter(TodoItem.id == todo_id).first()
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return TodoItemCreate(**(todo.__dict__))

@router.put("/todos/{todo_id}", response_model=TodoItemCreate)
def update_todo(todo_id: int, todo: TodoItemCreate):
    db_todo = db.session.query(TodoItem).filter(TodoItem.id == todo_id).first()
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    db_todo.title = todo.title
    db_todo.description = todo.description
    db.session.commit()
    db.session.refresh(db_todo)
    return TodoItemCreate(**vars(db_todo))

@router.delete("/todos/{todo_id}", response_model=TodoItemCreate)
def delete_todo(todo_id: int):
    db_todo = db.session.query(TodoItem).filter(TodoItem.id == todo_id).first()
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.session.delete(db_todo)
    db.session.commit()
    return TodoItemCreate(**vars(db_todo))


app.include_router(router)