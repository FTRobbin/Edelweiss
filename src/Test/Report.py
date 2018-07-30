import jsonpickle

def Report():
    with open('../data/benchmark.json', 'r') as f:
        content = f.read()
        data = jsonpickle.decode(content)
    current_data=data["c0efb8065b77597ba136ed0682d1579c5b14562584ca44af2c34b59206925d4e"]
    current_data.print()
    