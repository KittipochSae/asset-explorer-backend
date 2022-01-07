import pandas as pd


def load_data(r):
    print("Loading Grids")
    df = pd.read_csv('app/grids_kv.csv')
    df.apply(lambda x: r.set("grid-" + x['key'], x['value']), axis=1)
    print("Loading Landpoints")
    df = pd.read_csv('app/landpoints_kv.csv')
    df.apply(lambda x: r.set("landpoint-" + x['key'], x['value']), axis=1)
    df = None
    print("Finish Loading")
