from app.models.user.services.pattern_matching import is_valid_email, is_valid_password

from app.models.user.services.security import get_password_hash, generate_token

from app.models.user import User

from app.models.notification import Notification


def check_password(email: str, password: str):
    user = User.filter(email=email).first()
    if not user: return False, None
    return user.password_hash == get_password_hash(password), user.id
        

def create_user(name: str, email: str, password: str):
    new_user = User.new(name=name, email=email, password_hash=get_password_hash(password))

    return new_user


def register_user(data):
    email = data.get("email")
    password = data.get("password")

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

    return Notification("Успешно!", "Успешная регистрация пользователя!", "success", 0, (user.id,))