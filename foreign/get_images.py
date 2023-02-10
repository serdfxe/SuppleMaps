from app.database import *

from app.models.map import *

from requests_html import HTMLSession

def get_images():
    session = HTMLSession()

    n_of_poi = len(Poi.all())
    for i in range(1, n_of_poi+1):
        name = Poi.filter(id=i).first().name
        url = "https://vdnh.ru/search/?q=" + '+'.join(name.split())
        #print(url)
        html_search = session.get(url).text
        link = "https://vdnh.ru" + html_search[html_search.find("<div class='search-result-item' data-when-visible><a href='")+59:]
        link = link[:link.find("'")]
        html = session.get(link).text
        gallery = html[html.find('<div class="detail-gallery" data-slider data-slider-nav="on-hover" data-slider-adjust>')+86:]
        gallery = gallery[:gallery.find('<div')]
        #print(gallery)
        images = ["https://vdnh.ru" + img[:img.find('"')] for img in gallery.split('<img src="')[1:]]
        images_str = ' '.join(images[:min(len(images), 3)])
        with Poi.uow:
                Poi.uow.session.query(Poi).filter_by(id = i).update({"image": images_str})
                Poi.uow.commit()
