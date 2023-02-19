from fuzzywuzzy import process
from fuzzywuzzy import fuzz

def search(sourse:list, s:str):
    ans = list()
    for i in range(len(sourse)):
        if fuzz.WRatio(sourse[i]["name"],s) >= 60:
            ans.append(sourse[i])
    return sorted(ans, key = lambda x: fuzz.WRatio(x["name"],s), reverse=True)
