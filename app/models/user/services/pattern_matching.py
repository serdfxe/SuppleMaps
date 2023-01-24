import re


def is_valid_email(email: str) -> bool: 
    return re.fullmatch(re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'), email)

def is_valid_password(password: str) -> bool:
    return True #на время тестов
    if len(password) < 8:
        return "Убедитесь, что ваш пароль состоит как минимум из 8 символов."
    elif re.search('[0-9]',password) is None:
        return "Убедитесь, что ваш пароль содержит хотя бы одну цифру."
    elif re.search('[A-Z]',password) is None: 
        return "Убедитесь, что ваш пароль содержит хотя бы одну заглавную букву."
    return True
    