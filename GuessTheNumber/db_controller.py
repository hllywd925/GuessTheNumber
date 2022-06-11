from tinydb import TinyDB, Query
import random


class DBController:
    def __init__(self):
        self.db = TinyDB('user_db.json', sort_keys=True, indent=4, separators=(',', ': '))
        self.User = Query()

    def login_check(self, name, passwort):
        user = self.db.search(self.User.name == str(name))
        if user:
            if passwort == user[0]['passwort']:
                return user[0]['user_id'], 'ACCESS GRANTED', True
            else:
                return '', 'WRONG PASSWORD', False
        else:
            return '',  'WRONG NAME', False

    def creating_new_user(self, data):
        user_id = self.giving_user_number()
        name = data[0]
        passwort = data[1]
        print(f'[DEBUG]: {name}, {passwort}')
        user = self.db.search(self.User.name == str(name))
        if not user:
            self.db.insert({
                'user_id': user_id,
                'name': str(name),
                'passwort': str(passwort),
                'status': True
            })
            return user_id, str(name), str(passwort), 'NEW USER CREATED', True
        else:
            return '', '', '', 'USER ALREADY EXIST', False

    def giving_user_number(self):
        while True:
            number = random.randrange(100001, 999999)
            result = self.db.search(self.User.number == number)
            if result:
                result = None
            if not result:
                break
        return number

    def db_restart(self):
        new_list = ['Max', 'Tim', 'Jan']
        self.db.truncate()
        for name in new_list:
            user_id = self.giving_user_number()
            self.db.insert({
                'user_id': user_id,
                'name': name,
                'passwort': '1',
                'status': True
            })


if __name__ == "__main__":
    d = DBController()
    d.db_restart()
