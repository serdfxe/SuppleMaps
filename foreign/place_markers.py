from app.database import *

from app.models.map import *

import requests
import xml.etree.ElementTree as ET

def place_markers():
    n_of_poi = len(Poi.all())
    for i in range(1, n_of_poi+1):
        p = Poi.filter(id=i).first()
        coords = (p.marker_lat, p.marker_lon)
        url = f"https://nominatim.openstreetmap.org/reverse?lat={coords[0]}&lon={coords[1]}"
        r = requests.get(url)
        tree = ET.ElementTree(ET.fromstring(r.text))
        root = tree.getroot()
        box = [float(i) for i in root[0].attrib['boundingbox'].split(',')]
        new_marker = [(box[0]+box[1])/2 - 0.00001, (box[2]+box[3])/2 + 0.00001]
        
        if ((new_marker[0]-coords[0])**2 + (new_marker[1]-coords[1])**2)**0.5 * 63570 <= 20:
            with Poi.uow:
                Poi.uow.session.query(Poi).filter_by(id = i).update({"marker_lat": new_marker[0], "marker_lon": new_marker[1]})
                Poi.uow.commit()
        else:
            print(f"{p.name}    NOT FOUND")

