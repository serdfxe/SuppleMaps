from app.database import *

from app.models.map import *

def replace_desc():
    n_of_poi = len(Poi.all())
    for i in range(1, n_of_poi+1):
        desc = Poi.filter(id=i).first().description
        desc = desc.replace('<h2>', '<h1>').replace('</h2>', '</h1>').replace('<p>', '<h2>').replace('</p>', '</h2>')

        hist = Poi.filter(id=i).first().history
        hist = hist.replace('<h2>', '<h1>').replace('</h2>', '</h1>').replace('<p>', '<h2>').replace('</p>', '</h2>')
        with Poi.uow:
            Poi.uow.session.query(Poi).filter_by(id=i).update({"description": desc})
            Poi.uow.commit()

            Poi.uow.session.query(Poi).filter_by(id=i).update({"history": hist})
            Poi.uow.commit()
        