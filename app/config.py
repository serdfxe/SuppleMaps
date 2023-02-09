
authforms = {
    "signup": {"title": "Регистрация", "subtitle": "Введите данные для регистрации.", "ref": ["Уже есть аккаунт?", "/signin"], "form": [
        ("first_label", "Почта"),
        ("text_input", "email", "Введите почту..."),
        ("label", "Пароль"),
        ("pass_input", "password", "Введите пароль..."),
        ("ref", "signin", "Уже есть аккаунт?"),
        ("submit", "Зарегистрироваться")]},

    "signin": {"title": "Авторизация", "subtitle": "Введите данные для входа.", "ref": ["Ещё нет аккаунта?", "/signup"], "form": [
        ("first_label", "Почта"),
        ("text_input", "email", "Введите почту..."),
        ("label", "Пароль"),
        ("pass_input", "password", "Введите пароль..."),
        # ("check_box", "rememberme", "Запомнить при следующем входе?"),
        # ("ref", "forgotpassword", "Забыли пароль?"),
        ("ref", "signup", "Ещё нет аккаунта?"),
        ("submit", "Войти")]},
}

map_style = dict(
    voyager_nolabels = {
        "tiles":'https://{s}.basemaps.cartocdn.com/rastertiles/voyager_nolabels/{z}/{x}/{y}{r}.png', 
        "attr":'&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>'
        },

    thunderforest_outdoorss = {
        'tiles':'https://{s}.tile.thunderforest.com/outdoors/{z}/{x}/{y}.png?apikey=b2657f580b7c4e5c9832cf371031763a', 
        'attr':'&copy; <a href="http://www.thunderforest.com/%22%3EThunderforest</a>, &copy; <a href="https://www.openstreetmap.org/copyright%22%3EOpenStreetMap</a> contributors'
        },

    satellite = {
        'tiles': 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', 
        'attr': 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community',
        'css': """
        .marker-text {
            white-space: break-spaces;
            font-size:11pt;
            transition: font-size 0.25s;
            transition: width 0.25s;
            text-align: center;
            -moz-text-shadow:0 0 10px #c00; -webkit-text-shadow:0 0 10px #c00; text-shadow:0 0 10px white;
            font-weight: 700;
            text-shadow: 0 0 10px #101727; 
            color: white;
        }
        """
        },

    topo = {
        'tiles': 'https://api.maptiler.com/maps/topo-v2/{z}/{x}/{y}@2x.png?key=HE0hiltCVg2gETfdEctd', 
        'attr': '<a href="https://www.maptiler.com/copyright/" target="_blank">&copy; MapTiler</a> <a href="https://www.openstreetmap.org/copyright" target="_blank">&copy; OpenStreetMap contributors</a>'
        },

    streets = {
        "tiles": "https://api.maptiler.com/maps/streets-v2/256/{z}/{x}/{y}@2x.png?key=HE0hiltCVg2gETfdEctd", 
        "attr": '<a href="https://www.maptiler.com/copyright/" target="_blank">&copy; MapTiler</a> <a href="https://www.openstreetmap.org/copyright" target="_blank">&copy; OpenStreetMap contributors</a>'
        },

    osm = {
        "tiles": "OpenStreetMap",
        "attr": None
    },
)

side_bar_components = {
    "Главная": "main",
    "Личный кабинет": "account",
    "Карта": "map",
    "Поиск": "search",
    "Статические пути": "static_path",
    "Настройки": "settings",
    "История": "history",
    #"": "img/sidebar/",
}
