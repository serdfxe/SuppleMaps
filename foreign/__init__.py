from foreign.update import update
from foreign.make_matrix import make_matrix
from foreign.place_markers import place_markers
from foreign.get_images import get_images
def run():
    # place_markers()
    # return 
    # make_matrix()
    # return
    # get_images()
    # return
    path = input("Введите путь к файлу: ")

    if not input(path+"?"):
        update(path)
    else:
        print("Proccess stopped!")