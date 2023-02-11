import pickle


def write(content):
    with open("result.txt", "a", encoding="UTF-8") as f:
        f.write(content + "\n")


def read():
    with open("result.txt", "r", encoding="UTF-8") as f:
        return map(lambda v: v.strip(), f.readlines())


def write_dict(content):
    with open('result.pickle', 'wb') as f:
        pickle.dump(content, f, protocol=pickle.HIGHEST_PROTOCOL)


def read_dict():
    with open('result.pickle', 'rb') as f:
        data = {}
        try:
            data = pickle.load(f)
        except EOFError:
            data = {}

        return data
