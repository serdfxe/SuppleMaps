from base64 import decode
from app.database import *

from app.models.map import *

from foreign.config import *


def drop_all():
    for i in (Poi, PoiType, DistanceList):
        i.delete_all()

def init_types():
    with open(POI_INFO_FILE, encoding="utf-8") as f:
        s = f.readlines()

        s = [i.split("|") for i in s]

        types = [i[1] for i in s]
        
        return set(types)

def update_types(ts):
    for i in ts:
        PoiType.new(name=i)


def init_pois():
    with open(POI_INFO_FILE, encoding="utf-8") as f:
        s = f.readlines()

        s = [i.split("|") for i in s]

        info = [[[float(i[-2]), float(i[-1])]] + i[:-2] for i in s]
        
        return info


def init_distances():
    with open(DISTANCES_FILE, encoding="utf-8") as f:
        s = f.readlines()

        s = [[float(ii) for ii in i.split()] for i in s]
        
        return s

def update_poi_info(info):#name, type_name, image, description):
    for i in info:
        Poi.update(Poi.filter(name=i[1]).first(), marker_lat=i[0][0], marker_lon=i[0][1])
    #s = {"павильон": 40, "музей": 60, "пруд": 20, "фонтан": 15, "храм": 30, "развлечения": 40}
    #for i in info:
    #    Poi.new(name=i[1], lat=i[0][0], lon=i[0][1], time=s[i[2]], image=i[3], description=i[4], type_id=PoiType.filter(name=i[2]).first().id)

def update_graph(m):
    for i in range(len(m)):
        for ii in range(len(m[i])):
            DistanceList.new(start_id=i+1, end_id=ii+1, distance=m[i][ii])

def graph_init():
    print("Starting graph initialization . . .")

    #drop_all()

    #ts = init_types()

    #update_types(ts)

    i = init_pois()

    #m = init_distances()

    update_poi_info(i)

    #update_graph(m)

def update_short_names():

    with open("foreign/sn.txt", encoding="utf-8") as f:
        s = f.readlines()

        s = [i.split() for i in s]

        for i in s:
            p = Poi.filter(id=int(i[0]) + 1).first()
            
            Poi.update(p, short_name = " ".join(i[1:]))

def poi_info_init():
    with open("foreign/history (2).txt", encoding="utf-8") as f:
        s = f.readlines()

        s = [(int(i.split()[0]), " ".join(i.split()[1:])) for i in s]

        for i in s:
            Poi.update(Poi.filter(id=i[0]).first(), history=i[1])