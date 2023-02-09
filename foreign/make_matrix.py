from app.database import *

from app.models.map import *

from graphh import GraphHopper
import time
from math import isnan

gh_client = GraphHopper(api_key='55489304-0f25-429b-99e5-bb9806361343')

def get_path_len(st, fn):
    res = gh_client.route([st, fn], vehicle='foot')
    return int(res['paths'][0]['distance'])

def make_matrix():
    n_of_poi = len(Poi.all())
    
    for i in range(1, n_of_poi+1):
        p1 = Poi.filter(id=i).first()
        if not(isnan(p1.entrance_lat)) and not(isnan(p1.entrance_lon)): coords1 = (p1.entrance_lat, p1.entrance_lon)
        else: coords1 = (p1.marker_lat, p1.marker_lon)
        for j in range(i, n_of_poi+1):
            p2 = Poi.filter(id=j).first()   
            if not(isnan(p2.entrance_lat)) and not(isnan(p2.entrance_lon)): coords2 = (p2.entrance_lat, p2.entrance_lon)
            else: coords2 = (p2.marker_lat, p2.marker_lon)
            if i == j: dist = 0
            else:
                f = False
                while not f:
                    try:
                        dist = get_path_len(coords1, coords2)
                        f = True
                    except Exception:
                        time.sleep(5)    
            with DistanceList.uow:
                DistanceList.uow.session.query(DistanceList).filter_by(start_id = i, end_id = j).update({"distance": dist})
                DistanceList.uow.commit()

                DistanceList.uow.session.query(DistanceList).filter_by(start_id = j, end_id = i).update({"distance": dist})
                DistanceList.uow.commit()
        done = (2*n_of_poi-i+1)*i//2
        all = (n_of_poi+1)*n_of_poi//2
        print(f"{round(done/all*100, 2)}% done")
        
    
            