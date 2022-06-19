from random import random
from pycat.core import Window, Sprite, Color, Label, Scheduler, KeyCode
from pycat.experimental.movement import FourWayMovementController as Controller
from typing import List
from enum import Enum, auto
from os import path 
import random

w = Window(width=512,height=1024, background_image="Level_0.png", enforce_window_limits=False, is_sharp_pixel_scaling=True)

class States(Enum):
    start = auto()
    game = auto()
    win = auto()
    lose = auto()

Gstate = States.start

class ScrollableLevel:
    def __init__(self, backgrounds: List[str]):
        self.backgrounds = [w.create_sprite(image=b) for b in backgrounds]
        for i, s in enumerate(self.backgrounds):
            s.x = w.center.x
            s.y = w.center.y + i*w.height

    def on_update(self):
        for background in self.backgrounds:
            if background.y <= -w.height / 2:
                background.y += len(self.backgrounds)*w.height
            background.y -= 3


level = ScrollableLevel(["Level_0.png","Level_0.png"])

class Playbo(Sprite):
    global Gstate
    def on_create(self):
        self.image = "start.png"
        self.scale = 2
        self.layer  = 10
        self.position = w.center
        self.y = self.y - 48

    def on_update(self, dt):
        if Gstate == States.start:
            self.is_visible = True
        if Gstate != States.start:
            self.is_visible = False
    
    def on_left_click(self):
        global Gstate
        if Gstate is States.start:
            Gstate = States.game
        if Gstate == States.game:
            Scheduler.update(level.on_update)

class Player(Sprite):
    class Statep (Enum):
        normal = auto()
        health = auto()
        hit = auto()

    global Gstate
    def on_create(self):
        self.movement_controller = Controller(w, speed_factor=25)
        self.image = "ship_0000.png"
        self.add_tag("Player")
        self.layer = 9
        self.scale = 3.2
        self.position = w.center
        self.y = self.y - 200
        self.is_visible = False
        self.btime = 0
        self.reload = 0.36
        self.health = 26
        self.pl = w.create_label()
        self.pl.x = 0
        self.pl.y = w.height
        self.pl.text =  ("Player's HP:" + str(self.health))
        self.pl.is_visible = False 
        self.state = Player.Statep.normal
        
    def on_update(self, dt):
        global Gstate
        if Gstate == States.game:
            if self.state == Player.Statep.normal:
                self.btime += dt
                self.is_visible = True
                self.pl.is_visible = True 
                self.position += self.movement_controller.get_movement_delta(dt)
                if self.btime > self.reload:
                    pbullet = w.create_sprite(Bullet)
                    pbullet.position = self.position
                    self.btime = 0
            elif self.state == Player.Statep.health:
                pass
            elif self.state == Player.Statep.hit:
                pass
            if self.health < 1:
                Gstate = States.lose
        elif Gstate != States.game:
            self.is_visible = False
            self.pl.is_visible = False

class Helper(Sprite): 
    global Gstate
    def on_create(self):
        self.movement_controller = Controller(w, speed_factor=25)
        self.image = "ship_0002.png"
        self.layer = 9
        self.scale = 1.6
        self.y = player.y
        self.butime = 0 
        self.reload = 0.36
        self.is_visible = False

    def on_update(self, dt):
        self.butime += dt
        if Gstate == States.game:
            self.is_visible = True
            self.position += self.movement_controller.get_movement_delta(dt)
            if self.butime > self.reload:
                hbullet = w.create_sprite(Bullet)
                hbullet.position = self.position
                self.butime = 0
        elif Gstate != States.game:
            self.is_visible = False

class Aid(Sprite):
    
    def on_create(self):
        self.image = "aid,png"
        self.layer = 9
        self.scale = 1.6
        self.count = 0
        self.rtime = 0
        self.reload = random.randint(1,1)
        self.goto_random_position_in_region(12, w.height, 500, w.height)

        
    def on_update(self, dt):
        global Gstate
        if Gstate == States.game:
            self.y -= 10
            if self.count == 0:
                self.rtime += dt
                if self.rtime > self.reload:
                    w.create_sprite(Aid)
                    self.count += 1
            if self.is_touching_any_sprite_with_tag("Player"):
                self.delete()
                player.state = player.Statep.health
                player.health += 5
                player.pl.text = ("Player's HP:" + str(player.health)) 
                self.count = 0
        if self.y < 0: 
            self.delete()
            self.count = 0
        

class Bullet(Sprite):
    global Gstate
    def on_create(self):
        self.image = "tile_0000.png"
        self.layer = 9
        self.scale = 1.6
        self.speed = 10

    def on_update(self, dt):
        if Gstate == States.game:
            self.y += self.speed
            if self.y > w.height:
                self.delete() 
            if self.is_touching_any_sprite_with_tag("Boss"):
                self.delete() 
                boss.ehealth -= 1 
                boss.el.text = ("Boss's HP:" + str(boss.ehealth)) 
        elif Gstate != States.game:
            self.delete()

class Eullet(Sprite):
    global Gstate
    def on_create(self):
        self.image = "tile_0001.png"
        self.layer = 9
        self.scale = 0.23
        self.speed = 10
        
    def on_update(self, dt):
        if Gstate == States.game:
            self.move_forward(self.speed)
            if self.y < 0:
                self.delete()
            if self.is_touching_any_sprite_with_tag("Player"):
                self.delete() 
                player.health -= 1 
                player.pl.text = ("Player's HP:" + str(player.health)) 
        elif Gstate != States.game:
            self.delete()


class Boss(Sprite): 
    
    def on_create(self):
        self.movement_controller = Controller(w, speed_factor=25)
        self.image = "ship_0003.png"
        self.add_tag("Boss")
        self.layer = 10
        self.scale = 6.8
        self.rotation = 180
        self.position = w.center
        self.y = self.y + 324
        self.is_visible = False
        self.stime = 0
        self.reload = 0.42
        self.ehealth = 100
        self.el = w.create_label()
        self.el.x = 336
        self.el.y = w.height
        self.el.text = ("Boss's HP:" + str(self.ehealth))
        self.el.is_visible = False
    
    def on_update(self, dt):
        global Gstate
        self.stime += dt 
        if Gstate == States.game:
            self.is_visible = True
            self.el.is_visible = True 
            if self.stime > self.reload:
                ebullet = w.create_sprite(Eullet)
                ebullet.position = self.position
                ebullet.point_toward_sprite(player)
                self.stime = 0
            if self.ehealth < 1:
                Gstate = States.win
        elif Gstate != States.game:
            self.is_visible = False
            self.el.is_visible = False
    
        
class Return(Sprite):
    global Gstate
    def on_create(self):
        self.image = "return.png"
        self.scale = 0.49
        self.layer = 10
        self.x = w.width - 64
        self.y = 64
        self.la = w.create_label()
        self.la.x = w.width/2
        self.la.x = self.la.x - self.la.content_width/2
        self.la.y = w.height - 64
        self.la.font_size = 64 
        self.la.is_visible = False
        
        

    def on_update(self, dt):
        if Gstate is States.win:
            self.is_visible = True
            self.la.text = "Win"
            self.la.x = w.width/2
            self.la.x = self.la.x - self.la.content_width/2
            self.la.y = w.height - 64
            self.la.is_visible = True
        if Gstate is States.lose:
            self.is_visible = True
            self.la.text = "Lose"
            self.la.x = w.width/2
            self.la.x = self.la.x - self.la.content_width/2
            self.la.y = w.height - 64
            self.la.is_visible = True
        if Gstate is States.start:
            self.is_visible = False
            self.la.is_visible = False
    
    def on_left_click(self):
        global Gstate
        reset()
        if Gstate == States.win:
            Gstate = States.start
        if Gstate == States.lose:
            Gstate = States.start
    
def reset():
    boss.ehealth = 100
    boss.position = w.center
    boss.y = boss.y + 324
    boss.el.text = ("Boss's HP:" + str(boss.ehealth)) 
    player.health = 26
    player.position = w.center
    player.y = player.y - 200 
    player.pl.text =  ("Player's HP:" + str(player.health))
    helper01.x = player.x - 128 
    helper02.x = player.x + 128
        

class Scoreboard(Label):
    global Gstate
    def on_create(self):
        self.color = Color.CYAN
        self.text = "wiwiwiwiwiw"
        self.x = rbotton.la.x
        self.x = self.x - self.content_width*1.25
        self.y = rbotton.la.y - 64
        self.font_size = 48
        self.is_visible = False
    
    def on_update(self, dt):
        if Gstate is States.win:
            self.is_visible = True
        if Gstate is States.lose:
            self.is_visible = True
        if Gstate is States.start:
            self.is_visible = False

boss:Boss = w.create_sprite(Boss)
player = w.create_sprite(Player)
helper01 = w.create_sprite(Helper)
helper01.x = player.x - 128
helper02 = w.create_sprite(Helper)
helper02.x = player.x + 128
pbotton = w.create_sprite(Playbo)
rbotton = w.create_sprite(Return)
scoreboard = w.create_label(Scoreboard)
w.run()