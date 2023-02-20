from foreign.update import update
from foreign.make_matrix import make_matrix
from foreign.place_markers import place_markers
from foreign.get_images import get_images
from foreign.replace_desc import replace_desc
from foreign.check_search import check_search

from app.models.map.services import *
from app.models.map import *
from random import choice, randint, choices, sample

def run():
    # place_markers()
    # return 
    # make_matrix()
    # return
    # get_images()
    # return
    # replace_desc()
    # return
    # check_search()
    # return

    Graph.init_graph()

    mtrx = Graph.matrix
    time_s = Graph.time_list
    path = get_path(mtrx,[57], time_s, 100000,[],False,1)[0]
    print(path)
    return
    path = input("Введите путь к файлу: ")

    if not input(path+"?"):
        update(path)
    else:
        print("Proccess stopped!")