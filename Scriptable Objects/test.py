from ursina import *


class PlayerHand(Entity):
    def __init__(self):
        super().__init__(
            #parent = camera.ui,
            model = 'quad',
            scale = (1, 1),
            origin = (-.5, .5),
            position = (-.3,.4),
            texture = 'white_cube',
            texture_scale = (1,1),
            color = color.dark_gray
            )


def update():
    pass


def rota():
    camera.rotation_x += -5
    print(camera.rotation_x)


def rota_orig():
    camera.rotation_x = 0


app = Ursina()

p = Entity(model='cube', color=color.white, scale=(10,10,.5), texture='holz')
rot = Button(
    parten=camera.ui,
    scale=(.2,.2),
    color=color.yellow,
    position=(.8,0),
    on_click=rota)

res = Button(
    parten=camera.ui,
    scale=(.2,.2),
    color=color.blue,
    position=(.8,-.2),
    on_click=rota_orig)

camera.rotation_x = -45
camera.position = (0, -20, -20)

app.run()