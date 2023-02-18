from fuzzywuzzy import process
from fuzzywuzzy import fuzz

def search(sourse:list, s:str):
    return sorted([(i,fuzz.WRatio(i,s)) for i in sourse if fuzz.WRatio(i,s)>=60], key = lambda x: x[1], reverse=True)
