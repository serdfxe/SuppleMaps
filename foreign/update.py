from foreign.excel import Excel


def update(path):
    Excel.open(path)

    Excel.update()
