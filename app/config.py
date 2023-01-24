authforms = {
    "signup": {"title": "Регистрация", "subtitle": "Введите данные для регистрации.", "ref": ["Уже есть аккаунт?", "/signin"], "form": [
        ("first_label", "Почта"),
        ("text_input", "email", "Введите почту..."),
        ("label", "Пароль"),
        ("pass_input", "password", "Введите пароль..."),
        ("submit", "Зарегистрироваться")]},

    "signin": {"title": "Авторизация", "subtitle": "Введите данные для входа.", "ref": ["Ещё нет аккаунта?", "/signup"], "form": [
        ("first_label", "Почта"),
        ("text_input", "email", "Введите почту..."),
        ("label", "Пароль"),
        ("pass_input", "password", "Введите пароль..."),
        ("check_box", "rememberme", "Запомнить при следующем входе?"),
        ("ref", "forgotpassword", "Забыли пароль?"),
        ("two_btn", (("submit_btn", "Войти"), ("redirect_btn", "Войти по почте", "enterbymail")))]},
}