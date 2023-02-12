from flask_login import login_user
from app.models.user.services.pattern_matching import is_valid_email, is_valid_password

from app.models.user.services.security import get_password_hash, generate_token

from app.models.user import User

from app.models.notification import Notification


def check_password(email: str, password: str):
    user = User.filter(email=email).first()
    if not user: return False
    return user.password_hash == get_password_hash(password)

def login(data) -> Notification:
    email = data.get("email")
    password = data.get("password")
    user = User.filter(email=email).first()
    remember = True if data.get("rememberme") else False

    if password in ("", None) or email in (None, ""): 
        return Notification("Ошибка!", "Пожалуйлся введите почту и пароль.", "error", 1)

    if check_password(email, password):
        login_user(user, remember=remember)
        return Notification("Успешно!", "Вход произведён успешно!", "success", 0)

    return Notification("Ошибка!", "Wrong email or password ", "error", 1)
        

def create_user(name: str, email: str, password: str):
    new_user = User.new(name=name, email=email, password_hash=get_password_hash(password))

    return new_user

def register_user(data:dict):
    email = data["email"]
    password = data.get["password"]

    if password is None or password == "" or email is None or email == "":
        return Notification("Ошибка!", "Пожалуйлся введите почту и пароль.", "error", 1)
    
    if email == '' or not is_valid_email(email):
        return Notification("Ошибка!", "Некорректная почта.", "error", 1)
    
    is_valid = is_valid_password(password)
    if is_valid is not True:
        return Notification("Успешно!", is_valid, "error", 1)
    
    if User.filter(email=email).first():
        return Notification("Ошибка!", "Эта почта уже занята, выберите другую.", "error", 1)

    user = create_user(email.split("@")[0], email, password)
    return Notification("Успешно!", "Успешная регистрация пользователя!", "success", 0, (user,))