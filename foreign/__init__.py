from foreign.update import update
from foreign.make_matrix import make_matrix
from foreign.place_markers import place_markers
from foreign.get_images import get_images
from foreign.replace_desc import replace_desc
from foreign.check_search import check_search
def run():
    # place_markers()
    # return 
    # make_matrix()
    # return
    # get_images()
    # return
    # replace_desc()
    # return
    check_search()
    return
    path = input("Введите путь к файлу: ")

    if not input(path+"?"):
        update(path)
    else:
        print("Proccess stopped!")