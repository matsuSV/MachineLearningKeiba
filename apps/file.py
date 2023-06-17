import pickle
import pandas as pd


def write(content):
    with open("../outputs/results.txt", "a", encoding="UTF-8") as f:
        f.write(content + "\n")


def read():
    with open("../outputs/results.txt", "r", encoding="UTF-8") as f:
        return map(lambda v: v.strip(), f.readlines())


def write_dict(content):
    with open('../outputs/results.pickle', 'wb') as f:
        pickle.dump(content, f, protocol=pickle.HIGHEST_PROTOCOL)


def read_dict():
    with open('../outputs/results.pickle', 'rb') as f:
        data = {}
        try:
            data = pickle.load(f)
        except EOFError:
            data = {}

        return data


def to_pickle(df):
    df.to_pickle('../outputs/df.pickle')
    return pd.read_pickle('../outputs/df.pickle')
