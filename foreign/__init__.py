from foreign.update import update
from foreign.make_matrix import make_matrix
def run():
    make_matrix()

    return
    path = input("Введите путь к файлу: ")

    if not input(path+"?"):
        update(path)
    else:
        print("Proccess stopped!")