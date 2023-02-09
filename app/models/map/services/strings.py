def get_time_str(time: int) -> str:

    hours = time // 60
    minutes = time % 60 

    s = ""

    if hours:
        s += f"{hours} ч "

    if minutes:
        s += f"{minutes} мин"
    
    return s


def get_dist_str(dist: int) -> str:
    if dist > 1000:
        return f"{dist//100/10} км".replace(".", ",")

    return f"{dist//10*10} м"
