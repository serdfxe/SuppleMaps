from foreign.update import update

def run():
    path = input("Введите путь к файлу: ")

    if not input(path+"?"):
        update(path)
    else:
        print("Proccess stopped!")