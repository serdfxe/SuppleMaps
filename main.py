from tkinter import E
import flask

app = Flask()

@app.get("/users")
def list_users():
    return []

@app.get("/users/{id}")
def get_user_by_id(id: int):
    ...

@app.get("/users")
def create_users():
    return []

@app.get("/users/{id}")
def list_users(id: int):
    ...

if __name__ == "__main__":
    app.run()