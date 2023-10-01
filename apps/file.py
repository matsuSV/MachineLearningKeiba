import pickle
import pandas as pd


def write(content):
    with open("../outputs/results.txt", "a", encoding="UTF-8") as f:
        f.write(content + "\n")


def read():
    with open("../outputs/results.txt", "r", encoding="UTF-8") as f:
        return map(lambda v: v.strip(), f.readlines())


def write_races(content):
    with open('../outputs/results.pickle', 'wb') as f:
        pickle.dump(content, f, protocol=pickle.HIGHEST_PROTOCOL)


def read_all_races():
    try:
        with open('../outputs/results.pickle', 'rb') as f:
            return pickle.load(f)
    except (EOFError, FileNotFoundError):
        return {}


def to_pickle(df):
    df.to_pickle('../outputs/df.pickle')
    return pd.read_pickle('../outputs/df.pickle')
