from base64 import decode
from app.database import *

from app.models.map import *

from foreign.config import *


def init_pois():
    with open(POI_INFO_FILE, encoding="utf-8") as f:
        s = f.readlines()

        s = [i.split() for i in s]

        coordinates = [(float(i[-2]), float(i[-1])) for i in s]

        names = [" ".join(i[:-2]) for i in s]
        
        return coordinates, names


def init_distances():
    with open(DISTANCES_FILE, encoding="utf-8") as f:
        s = f.readlines()

        s = [[float(ii) for ii in i.split()] for i in s]
        
        return s

def update_poi_info(c, n):
    for i in zip(c, n):
        Poi.new(name=i[-1], lat=i[0][0], lon=i[0][1], time=30)

def update_graph(m):
    for i in range(len(m)):
        for ii in range(len(m[i])):
            DistanceList.new(start_id=i+1, end_id=ii+1, distance=m[i][ii])

def graph_init():
    print("Starting grapg initialization . . .")

    c, n = init_pois()

    m = init_distances()

    update_poi_info(c, n)

    update_graph(m)
