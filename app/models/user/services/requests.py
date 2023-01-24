from app.models.user import User

from app.models.user.login_manager import login_manager


def get_all_users():
    return User.all()

@login_manager.user_loader
def load_user(id):
    return User.filter(id=id).first()
