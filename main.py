from fastapi import FastAPI,Depends,Request
from models.request import List,UserLoginRequest,UserRequest
from auth.auth_handler import signJWT
from auth.auth_bearer import JWTBearer
from sqlalchemy.orm import Session
from database.db import session_local
from models import model
import bcrypt

def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()

salt = bcrypt.gensalt()
app = FastAPI()

@app.get("/get", dependencies=[Depends(JWTBearer())])
async def getAllTodo(db :Session =Depends(get_db)):
    todos = db.query(model.TodoList).all()
    if len(todos) == 0:
        return {"message" : "Empty , no todo task added currently"}
    return {"data" : todos}


@app.get("/get/{id}", dependencies=[Depends(JWTBearer())])
async def getOneTodo(id: int , db : Session = Depends(get_db)):
    todo = db.query(model.TodoList).filter(model.TodoList.id == id).first()
    if todo is None:
        return {"message" : "No task with this ID exists"}
    return {todo}


@app.post("/add", dependencies=[Depends(JWTBearer())])
async def addTodo(req : Request ,list : List ,db : Session = Depends(get_db) ):
    todo = model.TodoList(title = list.title)
    db.add(todo)
    db.commit()
    return {"message" : "Voila !! The Todo Task has been succesfully added"}

@app.put("/update/{id}", dependencies=[Depends(JWTBearer())])
async def updateTodo(id:int, db : Session = Depends(get_db)):
    todo = db.query(model.TodoList).filter(model.TodoList.id == id).first()
    if todo is None:
        return {"message" : "No task with this ID exists"}
    todo.complete = not todo.complete
    db.commit()
    return {"message" : f"The status of Task with ID:{id} has been changed"}


@app.delete("/remove/{id}", dependencies=[Depends(JWTBearer())])
async def deleteTodo(id : int , db: Session = Depends(get_db)):
    todo = db.query(model.TodoList).filter(model.TodoList.id == id).first()
    if todo is None:
        return {"message" : "No task with this ID exists"}
    db.delete(todo)
    db.commit()
    return {"message" : f"The Task with Id:{id} has been deleted."}
    

@app.post("/user/signup")
def create_user(user: UserRequest, db:Session=Depends(get_db)):
    res = bytes(user.password, 'utf-8')
    hashed_password = bcrypt.hashpw(res,salt)
    useradd = model.User(fullname = user.fullname , email = user.email , password = hashed_password)
    db.add(useradd)
    db.commit()
    token = signJWT(user.email)
    return {"message" : "User Created" , "Token" : token}


@app.post("/user/login")
def user_login(user: UserLoginRequest , db : Session = Depends(get_db)):
    
    temp_user = db.query(model.User).filter(model.User.email==user.email).first()
    if temp_user is None:
        return {"message" : "User with this email is not registered yet."}

    pass_true = bcrypt.checkpw(user.password.encode('utf-8'),temp_user.password.encode('utf-8'))

    if pass_true:
        token=signJWT(user.email)
        return {"message" : "Login Successful","Token" : token}
    return {
        "message": "Wrong Password"
    }
