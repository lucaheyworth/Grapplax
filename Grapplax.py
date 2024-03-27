from ursina import *
from ursina import camera
import random
from pygame import mixer
from ursina.prefabs.hot_reloader import *
from ursina.prefabs.platformer_controller_2d import PlatformerController2d


app = Ursina()
window.borderless = False
window.fullscreen = True
window.entity_counter.disable()
window.collider_counter.disable()
window.fps_counter.disable()
Sky()
camera.orthographic = True
camera.fov = 20
Text.default_font = "Python\\Grapplax\\Font.otf"
ground = Entity(model='cube', color=color.hex("#266D20"), z=-.1, y=-1, origin_y=.5, scale=(1000,100,10), collider='box', ignore=True)

random.seed(4)
player = PlatformerController2d()
player.x = 1
player.y = raycast(player.world_position, player.down).world_point[1] + .01
player.texture = load_texture('Grapply.png')
camera.add_script(SmoothFollow(target=player, offset=[0,5,-30], speed=4))

input_handler.bind('right arrow', 'd')
input_handler.bind('left arrow', 'a')
input_handler.bind('up arrow', 'space')
input_handler.bind('gamepad dpad right', 'd')
input_handler.bind('gamepad dpad left', 'a')
input_handler.bind('gamepad a', 'space')

current_level = 1
game_over = False
code_ran = False
code_ran_2 = False
grapples = 3
grapple_counter = Text(text=f'Grapples: {grapples}', origin=(-.5, .5), position=(-.89, .5), scale=1)

def update():
    global current_level
    global grapples
    global game_over 
    global hp
    player.hp = 5
    if player.y > 5 and game_over == False:
        camera.y += 0.04
    if grapples == 0:
        game_over = True
        Text(text=f"You died from running out of grapples!", position=(-.3, .19), scale=2)
    if player.hp == 0:
        game_over = True
        Text(text=f"You died from EleKill!", position=(-.3, .18), scale=2)
    if game_over == True:
        game_over = True
        player.disable()
        if held_keys["right mouse"]:
            quit()
        global code_ran
        if not code_ran:
            Text(text=f"GAME OVER!", color=color.red, position=(-.3, .15), scale=3)
            Text(text=f"Press F5 to try again.", position=(-.3, -.25), scale=2) 
            Text(text=f"Right click to quit.", position=(-.3, -.19), scale=2) 
            Text(text=f"You got to level: "+str(current_level), position=(-.3, .30), scale=2)
            mixer.init()
            mixer.Sound("Python\\Grapplax\\Game over.mp3").play()
            code_ran = True 
    #TODO: implement {GAMEOVER > Fall off the screen} or clamp(pygame)
    if current_level == 1 and player.y > 75:
        scene.disable()
        camera.y = 0
        global code_ran_2
        if not code_ran_2:
            mixer.init()
            mixer.Sound("Python\\Grapplax\\Game over.mp3").play()
            code_ran_2 = True
        current_level = 2
        levels()
    elif current_level == 2 and player.y > 100:
        current_level = 3
    elif current_level == 3 and player.y > 125:
        current_level = 4
    elif current_level == 4 and player.y > 150:
        current_level = 5
    elif current_level == 5 and player.y > 175:
        current_level = 6
    elif current_level == 6 and player.y > 200:
        current_level = 7

class Platform(Entity):
    def __init__(self, position=(0, 0)):
        super().__init__(parent=scene, model="quad", collider="box", position=position, texture=load_texture("Platform.png"))

    def on_click(self):
        global grapples
        if grapples > 0:
            grapples -= 1
            grapple_counter.text = ("Grapples: "+str(grapples))
            target_position = self.position + Vec3(0, self.scale.y / 2 + player.scale.y / 2, 0)
            player.animate_position(target_position, duration=0.5, curve=curve.out_cubic)
            mixer.init()
            global whoosh
            whoosh = mixer.Sound("Python\\Grapplax\\Whoosh.mp3")
            whoosh.play()

class Grapple(Entity):
    def __init__(self, position=(0, 0)):
        super().__init__(parent=scene, model="quad", texture=load_texture("Grapple.png"), collider="box", position=position)

    def update(self):
        if player.intersects(self):
            global grapples
            mixer.init()
            if whoosh.play == True:
                whoosh.stop()
            mixer.Sound("Python\\Grapplax\\PickUp.mp3").play()
            grapples += 1
            grapple_counter.text = ("Grapples: "+str(grapples))
            self.disable()

class SuperGrapple(Entity):
    def __init__(self, position=(0, 0)):
        super().__init__(parent=scene, model="quad", scale=(2, 2), texture=load_texture("Grapple.png"), collider="box", position=position)

    def update(self):
        if player.intersects(self):
            global grapples
            mixer.init()
            if whoosh.play == True:
                whoosh.stop()
            PickUpSound = mixer.Sound("Python\\Grapplax\\PickUp.mp3")
            PickUpSound.set_volume(2)
            PickUpSound.play()
            grapples += 3
            grapple_counter.text = ("Grapples: "+str(grapples))
            self.disable()
        
code_ran_1 = False

class EleKill(Entity):
    def __init__(self, position=(0,0), power=0):
        super().__init__(parent=scene, model="quad", scale=(power*1.5), texture=load_texture("EleKill.png"), collider="box", position=position)
        self.power = power
        self.speed = 0.1
        self.direction = 1

    def update(self):
        if Platform.intersects(self):
            self.direction *= -1

        if player.intersects(self):
            global hp
            player.hp = 5
            player.hp -= self.power
            global code_ran_1
            if not code_ran_1:
                x = random.uniform(-.89, .89)
                y = random.uniform(-.5, .5)
                scale = random.uniform(0, 4)
                coords = (x, y)
                Text(text=f"-{self.power}", color=color.red, position=coords, scale=scale)
                code_ran_1 = True

        self.x += self.speed * self.direction 

        if self.x >= 17:
            self.direction = -1
        elif self.x <= -17:
            self.direction = 1

    
    def on_click(self):
        self.blink(color.white, 0.1)
        mixer.init()
        mixer.Sound("Python\\Grapplax\\Spark.mp3").play()               
            
class levels:
    if current_level == 1:
        Platform((7, 5))
        Grapple((11, 8))
        Platform((13, 7))
        Platform((17, 10))
        Platform((-15, 17))
        Platform((-12, 22))
        SuperGrapple((-7, 16))
        Platform((-5, 12))
        Platform((5, 21))
        Grapple((5, 23))
        Platform((0, 18))
        Platform((12, 25))
        Platform((9, 28))
        Platform((17, 34))
        Platform((-17, 36))
        Grapple((8, 42))
        Platform((12, 39))
        Platform((5, 41))
        EleKill((-17, 39), (1))
        Platform((-3, 38))
        Platform((-1, 43))
        Platform((-2, 48))
        SuperGrapple((0, 45))
        Platform((16, 44))
        Platform((-15, 41))
        Platform((-7, 51))
        Platform((11, 50))
        Platform((15, 52))
        Grapple((13, 51))
        Platform((-17, 57))
        Platform((-11, 55))
        Platform((9, 60))
        Platform((4, 62))
        Grapple((5, 63))
        EleKill((17, 58), (2))
        Platform((0, 68))
        Platform((-15, 73))
        Grapple((-7, 74))
        Platform((3, 76))
    elif current_level == 2:
        Platform((6, 7))
        EleKill((0, 0), 2)
            
levels()

app.run()
