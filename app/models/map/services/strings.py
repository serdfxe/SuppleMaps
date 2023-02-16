def get_time_str(time: int) -> str:
    hours = time // 60
    minutes = time % 60 

    s = ""
    if hours: s += f"{hours} ч "
    if minutes: s += f"{minutes} мин"
    
    return s


def get_dist_str(dist: int) -> str:
    if dist > 1000:
        return f"{dist//100/10} км".replace(".", ",")
    else:
        return f"{dist//10*10} м"

def compress_desc(desc: str, max_width:int, max_height:int):
    compessed = desc
    desc = desc.split()
    temp_w, temp_h = 0,0
    for i in range(len(desc)):
        temp_w += len(desc[i])
        if temp_w > max_width:
            temp_h += 1
            temp_w = len(desc[i])
        if temp_h > max_height:
            compessed = ' '.join(desc[:i]) + '...'
            break
    return compessed