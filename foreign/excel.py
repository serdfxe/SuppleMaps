import pandas as pd

from app.database import *

from app.models.map import *



class Excel:
    file = None
    @classmethod
    def open(cls, file_name):

        f = pd.ExcelFile(file_name)

        cls.file = f
        cls.file_name = file_name

        if f:
            print("Open file success!")
        else:
            TimeoutError("Did not open file!!")

    @classmethod
    def update(cls):
        if not cls.file: TimeoutError("Did not open file!!")

        p = cls.file.parse()

        name = cls.file.sheet_names[0]

        t = eval(name if all(ii not in name for ii in "().") else TimeoutError(f"Incorrect sheet name '{name}' !!!"))

        f = pd.read_excel(cls.file_name, name)

        for row in f.iterrows():
            #print(i[1]["name"])
            t.update(t.filter(id=row[1]["id"]).first(), **{n: row[1][n] for n in row[1].keys()})

        print("Done!!!")
