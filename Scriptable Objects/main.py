from ursina import *
from PIL import Image, ImageDraw, ImageFont
import test


def template(image, gruppe):
    pic = Image.open('assets/else.png')
    if gruppe == 'Sgl':
        temp = Image.open('assets/sgl.png')
    else:
        temp = Image.open('assets/bearb.png')
    return Image.blend(temp, pic, .5)


class ScriptableCard(Entity):
    def __init__(self, image, name, gruppe, pers, erle):
        super().__init__(
            model='quad',
            scale=(2, 3),
            texture=template(image, gruppe)
        )
        self.name = name
        self.gruppe = gruppe
        self.pers = pers
        self.erle = erle


app = Ursina()
card = ScriptableCard('else', 'Ulla', 'Sgl', 3, 4)
app.run()