import json


class Packer:
    def __init__(self, typ, user_id, name, data):
        self.typ = typ
        self.user_id = user_id
        self.name = name
        self.data = data

    def pack(self):
        package = json.dumps(self.__dict__)
        return package

    def unpack(self, package):
        data = json.loads(package)
        self.typ, self.user_id, self.name, self.data = data['typ'], data['user_id'], data['name'], data['data']
        return data


class UnPacker:
    def __init__(self):
        self.typ = None
        self.name = None
        self.user_id = None
        self.data = None

    def unpack(self, package):
        data = json.loads(package)
        self.typ, self.name, self.user_id, self.data = data['typ'], data['name'], data['user_id'], data['data']
        return data


if __name__ == '__main__':
    p = Packer('msg', 2509, 'Max', ('sack', 'nase'))
    print(f'{type(p)}: {p}')
    p = p.pack()
    print(f'{type(p)}: {p}')
    u = Packer(0, 0, 0, 0)
    print(f'{type(u)}: {u}')
    u = u.unpack(p)
    print(f'{type(u)}: {u}')
    print(u['data'][0])
