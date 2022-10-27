import time

class Note:
    def __init__(self, name):
        self.name = name


class Tonleiter:
    def __init__(self, key, mode):
        self.key = key
        self.mode = mode
        self.major = [0, 2, 4, 5, 7, 9, 11]
        self.minor = [0, 2, 3, 5, 7, 8, 10]

        self.tonleiter = []
        self.stufenakkorde = {}

    def erstelle_tonleiter(self):
        noten = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        tonleiter = []
        start = None
        for idx, key in enumerate(noten):
            if key == self.key:
                start = idx
        for add in range(start):
            noten.append(noten[add])
        for pop in range(start):
            noten.pop(0)
        if self.mode == 'major':
            for i in range(7):
                tonleiter.append(noten[self.major[i]])
        elif self.mode == 'minor':
            for i in range(7):
                tonleiter.append(noten[self.minor[i]])
        print(f'Key: {self.key}\t\t Mode: {self.mode}')
        self.tonleiter = tonleiter
        print(self.tonleiter)
        time.sleep(0.5)

    def erstelle_stufenakkorde(self):
        akkorde = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII']
        for idx, note in enumerate(self.tonleiter):
            prime =
        pass

    """def erstelle_stufenakkorde(self):
        akkorde = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII']
        stufenakkorde = {akkorde[0]: [],
                         akkorde[1]: [],
                         akkorde[2]: [],
                         akkorde[3]: [],
                         akkorde[4]: [],
                         akkorde[5]: [],
                         akkorde[6]: []}
        for idx, akkord in enumerate(akkorde):
            print(idx, akkord)
            break
        print(stufenakkorde)
        pass"""


t = Tonleiter('D', 'major')
t.erstelle_tonleiter()
t.erstelle_stufenakkorde()

t.key = 'C'
t.erstelle_tonleiter()

t.key = 'A'
t.mode = 'minor'
t.erstelle_tonleiter()

t.key = 'E'
t.erstelle_tonleiter()
