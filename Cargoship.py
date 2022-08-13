from re import I
from turtle import left
from numpy import trace
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
toolcount = 0
howmanytr = 0
howmanysh = 0

class Title(Sprite):
    global Gstate
    def on_create(self):
        self.image = "title.png"
        self.scale = 0.42
        self.layer  = 10
        self.position = w.center
        self.x = self.x - 128
        self.y = self.y + 272
        # self.tl01 = w.create_label()
        # self.tl01.font_size = 29
        # self.tl01.text = ("Cargo Ship")
        # self.tl01.color = Color.BLACK
        # self.tl01.position = self.position 
        # self.tl01.x = self.x + self.tl01.content_width/2
        # self.tl01.y = self.y + 38
        # self.tl02 = w.create_label()
        # self.tl02.font_size = 29
        # self.tl02.text = ("Defence Training")
        # self.tl02.color = Color.BLACK
        # self.tl02.position = self.position
        # self.tl02.x = self.x + self.tl02.content_width/2 - 96
        # self.tl02.y = self.y - 16


    def on_update(self, dt):
        if Gstate == States.start:
            self.is_visible = True
            # self.tl01.is_visible = True
            # self.tl02.is_visible = True
        if Gstate != States.start:
            self.is_visible = False
            # self.tl01.is_visible = False
            # self.tl02.is_visible = False

class Titleword(Sprite):
    global Gstate
    def on_create(self):
        self.image = "shrimptitleword.png"
        self.scale = 0.75
        self.layer  = 10
        self.position = w.center
        self.x = self.x +  59
        self.y = self.y + 243
        
    def on_update(self, dt):
        if Gstate == States.start:
            self.is_visible = True
        if Gstate != States.start:
            self.is_visible = False

class Playbo(Sprite):
    global Gstate
    def on_create(self):
        self.image = "start.png"
        self.scale = 2
        self.layer  = 10
        self.position = w.center
        self.y = self.y - 48
        self.time = 0
        self.thinking = 6
        self.tools = 0    
    
    def on_update(self, dt):
        if Gstate == States.start:
            self.is_visible = True
        if Gstate != States.start:
            self.is_visible = False
        self.time += dt
        if self.time > self.thinking:
            a = random.randint(1,100)
            if a > 50:
                w.create_sprite(Box)
                self.time = 0
            elif a <= 50:
                w.create_sprite(Aid)
                self.time = 0
                

    
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
        self.layer = 11
        self.scale = 3.2
        self.position = w.center
        self.y = self.y - 200
        self.is_visible = False
        self.btime = 0
        self.reload = 0.36
        self.htime = 0
        self.hendtime = 2.5
        self.gtime = 0
        self.gendtime = 1.5
        self.ttime = 0
        self.tcount = 0
        self.tendtime = 11
        self.ftime = 0
        self.freload = 0.36
        self.health = 26
        self.pl = w.create_label()
        self.pl.x = 0
        self.pl.y = w.height
        self.pl.text =  ("Player's HP:" + str(self.health))
        self.pl.is_visible = False 
        self.state = Player.Statep.normal
        self.rgb = self.color
        self.boost = False
        
    def on_update(self, dt):
        global Gstate, howmanytr,howmanysh, trlabel
        if Gstate == States.game:
            self.btime += dt
            if howmanysh > 0:
                if w.is_key_down(KeyCode.Z):
                    tr = w.create_sprite(Tropedo)
                    self.detectr(tr)
                    tr.position = self.position
                    howmanysh = 0
                    shlabel.text = ("Shoot Amount:" + str(howmanysh))

            if self.btime > self.reload:
                    pbullet = w.create_sprite(Bullet)
                    pbullet.position = self.position
                    self.btime = 0
            if self.boost == True:
                self.ttime += dt
                if self.tcount == 0:
                    self.movement_controller._speed_factor = 0
                    self.position = self.position
                    self.bullet01 = w.create_sprite(NotHelper)
                    self.bullet01.position = self.position
                    self.bullet01.x -= 32
                    self.bullet01.is_visible = False
                    self.bullet02 = w.create_sprite(NotHelper)
                    self.bullet02.position = self.position
                    self.bullet02.x += 32
                    self.bullet02.is_visible = False
                    self.movement_controller._speed_factor = 25
                    self.tcount += 1 
                if self.ttime > self.tendtime:
                    self.bullet01.delete()
                    self.bullet02.delete()
                    self.boost = False
                    self.ttime = 0
                    self.tcount = 0 
            if self.state == Player.Statep.normal:
                self.movement_controller._speed_factor = 25
                self.position += self.movement_controller.get_movement_delta(dt)
                self.is_visible = True
                self.pl.is_visible = True 
            elif self.state == Player.Statep.health:
                self.position += self.movement_controller.get_movement_delta(dt)
                self.htime += dt
                self.flash(dt ,Color.GREEN)
                if self.htime > self.hendtime:
                    self.state = player.Statep.normal
                    self.color = self.rgb
                    self.htime = 0
            elif self.state == Player.Statep.hit:
                self.position += self.movement_controller.get_movement_delta(dt)
                self.gtime += dt
                self.flash(dt ,(255 ,0 , 0))
                if self.gtime > self.gendtime:
                    self.state = player.Statep.normal
                    self.color = self.rgb
                    self.gtime = 0
            
            if self.health < 1:
                Gstate = States.lose
        elif Gstate != States.game:
            self.is_visible = False
            self.pl.is_visible = False

    def flash(self, dt, color):
        self.ftime += dt
        if color == Color.GREEN:
            self.color = Color.GREEN
        elif color == (255 ,0 , 0):
            self.color = (255 ,0 , 0)
        if self.ftime > self.freload:
            self.is_visible = not self.is_visible
            self.time = 0
    
    def detectr(self,tr):
        global Tropedo, howmanysh
        if howmanysh == 1:
            tr.image = "rocket1.png"
            tr.disappear = 0.5
        if howmanysh == 2:
            tr.image = "rocket2.png"
            tr.disappear = 1
        if howmanysh == 3:
            tr.image = "rocket3.png"
            tr.disappear = 1.72
        if howmanysh == 4:
            tr.image = "rocket4.png"
            tr.disappear = 2.56

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

class NotHelper(Sprite): 
    global Gstate
    def on_create(self):
        self.movement_controller = Controller(w, speed_factor=25)
        self.image = "ship_0002.png"
        self.layer = -1
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
        self.image = "aid.png"
        self.layer = 9
        self.scale = 0.16
        self.count = 0
        self.rtime = 0
        self.reload = 1
        self.goto_random_position_in_region(12, w.height, 500, w.height)
        self.y = w.height + self.height

        
    def on_update(self, dt):
        global Gstate, toolcount
        if Gstate == States.game:
            self.y -= 4
            if self.is_touching_any_sprite_with_tag("Player"):
                toolcount += 1
                self.delete()
                player.state = player.Statep.health
                player.health += 5 
                player.pl.text = ("Player's HP:" + str(player.health))
            if self.y < 0: 
                self.delete()
        elif Gstate != States.game:
            self.delete()

class TropedoState(Enum):
        shooting = auto()
        boom = auto()
    

class Tropedo(Sprite):

    def on_create(self):
        self.image = "rocket1.png"
        self.layer = 9  
        self.scale = 0.11
        self.count = 0
        self.state = TropedoState.shooting
        self.position  = player.position
        self.ftime = 0
        self.dtime = 0
        self.explode = 0.36
        self.disappear = 0.5
        
    def on_update(self, dt):
        global Gstate, toolcount,howmanysh
        if Gstate == States.game:
            if self.state == TropedoState.shooting:  
                self.y += 9
                if w.is_key_down(KeyCode.X):
                    self.state = TropedoState.boom
                if self.y > w.height: 
                    self.delete() 
            if self.state == TropedoState.boom:
                self.boom(dt)
                if self.is_touching_any_sprite_with_tag("Boss"):
                    boss.ehealth -= 0.1 
                    boss.el.text = ("Boss's HP:" + str(boss.ehealth)) 
        elif Gstate != States.game:
            self.delete()
        
    
    
    def boom(self, dt):
        self.image = "explode.png"
        self.scale = 0.46
        self.ftime += dt
        if self.ftime > self.explode:
            self.is_visible = not self.is_visible
            self.ftime = 0
        self.dtime += dt
        if self.dtime > self.disappear:
            self.state = TropedoState.shooting
            self.delete()
        
class Box(Sprite):
    
    def on_create(self):
        self.image = "box.png"
        self.layer = 9
        self.scale = 0.16
        self.count = 0
        self.rtime = 0
        self.reload = 1
        self.goto_random_position_in_region(12, w.height, 500, w.height)
        self.y = w.height + self.height

        
    def on_update(self, dt):
        global Gstate, toolcount
        if Gstate == States.game:
            self.y -= 4
            if self.is_touching_any_sprite_with_tag("Player"):
                toolcount += 1
                self.delete()
                player.boost = True
            if self.y < 0: 
                self.delete()
        elif Gstate != States.game:
            self.delete()


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
            if player.state == Player.Statep.normal:
                if self.is_touching_any_sprite_with_tag("Player"):
                    self.delete() 
                    player.health -= 1 
                    player.pl.text = ("Player's HP:" + str(player.health)) 
                    player.state = player.Statep.hit
        elif Gstate != States.game:
            self.delete()


class Boss(Sprite): 
    class Stateb(Enum):
        normal = auto()
        insane = auto()

    class Move(Enum):
        left1 = auto()
        right2 = auto()
        right3 = auto()
        left4 = auto()

    def on_create(self):
        self.movement_controller = Controller(w, speed_factor=25)
        self.image = "shrimprship_0003.png"
        self.add_tag("Boss")
        self.layer = 10
        # self.scale = 6.8
        self.scale = 0.37
        self.rotation = 180
        self.position = w.center
        self.y = self.y + 324
        self.is_visible = False
        self.stime = 0
        self.reload = 0.42
        self.ehealth = 600
        self.line  = self.ehealth/2
        self.mstate = self.Move.left1
        self.mtime = 0
        self.state = Boss.Stateb.normal
        self.el = w.create_label()
        self.el.x = 336
        self.el.y = w.height
        self.el.text = ("Boss's HP:" + str(self.ehealth))
        self.el.is_visible = False
    
    def on_update(self, dt):
        global Gstate
        self.stime += dt 
        self.mtime += dt
        if Gstate == States.game:
            if self.mtime < 5:
                self.mstate = self.Move.left1
            if self.mtime >= 5 and self.mtime < 10:
                self.mstate = self.Move.right2
            if self.mtime >= 10 and self.mtime < 15:               
                self.mstate = self.Move.right3
            if self.mtime >= 15 and self.mtime < 20:
                self.mstate = self.Move.left4
            if self.mtime > 21:
                self.mstate = self.Move.left1
                self.mtime = 0
            
            if self.mstate is self.Move.left1:
                self.move(self.mstate)
            if self.mstate is self.Move.right2:
                self.move(self.mstate)
            if self.mstate is self.Move.right3:
                self.move(self.mstate)
            if self.mstate is self.Move.left4:
                self.move(self.mstate)
            
            if self.ehealth < self.line:
                self.state = boss.Stateb.insane
            if self.state == boss.Stateb.normal:
                self.is_visible = True
                self.el.is_visible = True 
                if self.stime > self.reload:
                    ebullet = w.create_sprite(Eullet)
                    ebullet.position = self.position
                    ebullet.point_toward_sprite(player)
                    self.stime = 0
            if self.state == boss.Stateb.insane:
                self.is_visible = True
                self.el.is_visible = True 
                if self.stime > self.reload:
                    boss.reload = 0.21
                    ebullet01 = w.create_sprite(Eullet)
                    ebullet01.position = self.position
                    ebullet01.point_toward_sprite(player)
                    ebullet02 = w.create_sprite(Eullet)
                    ebullet02.position = self.position
                    ebullet02.x += 96
                    ebullet02.point_toward_sprite(player)
                    ebullet03 = w.create_sprite(Eullet)
                    ebullet03.position = self.position
                    ebullet03.x -= 96
                    ebullet03.point_toward_sprite(player)
                    self.stime = 0
            
            if self.ehealth < 1:
                Gstate = States.win    
        elif Gstate != States.game:
            self.is_visible = False
            self.el.is_visible = False
    
    def move(self, mstater):
        if mstater is self.Move.left1 or mstater is self.Move.left4:
            self.x -= 0.12
        if mstater is self.Move.right2 or mstater is self.Move.right3:
            self.x += 0.12

class Return(Sprite):
    global Gstate
    def on_create(self):
        self.image = "return.png"
        self.scale = 0.49
        self.layer = 10
        self.x = w.width - 64
        self.y = 256
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


class Trlabel(Label):

    def on_create(self):
        self.x = 0
        self.y = w.height - player.pl.content_height
        self.layer = 9
        # self.font_size = 24
        self.color = Color.WHITE
        self.is_visible = False
        self.rtime = 0
        self.reload = 6
        self.text = ("Tropedo stroge:" + str(howmanytr))

    def on_update(self, dt: float):
        global howmanytr, howmanysh
        self.rtime += dt
        if howmanytr + howmanysh < 4:
            if self.rtime > self.reload:
                howmanytr += 1 
                self.rtime = 0
                trlabel.text =  ("Tropedo stroge:" + str(howmanytr))
        
        if Gstate is States.game:
            self.is_visible = True
        elif Gstate is not States.game:
            self.is_visible = False

class Uselabel(Label):

    def on_create(self):
        global howmanysh
        self.x = 0
        self.y = w.height - player.pl.content_height - trlabel.content_height
        self.layer = 9
        # self.font_size = 24
        self.color = Color.WHITE
        self.is_visible = False
        self.rtime = 0
        self.reload = 6
        self.text = ("Shoot Amount:" + str(howmanysh))

    def on_update(self, dt: float):
        global howmanysh,howmanytr,trlabel
        if Gstate is States.game:
            self.is_visible = True
            if w.is_key_down(KeyCode.A) and howmanytr > 0:
                howmanytr -= 1
                howmanysh += 1
                trlabel.text = ("Tropedo stroge:" + str(howmanytr))
                self.text = ("Shoot Amount:" + str(howmanysh))
            if w.is_key_down(KeyCode.S) and howmanysh > 0:
                howmanytr += 1
                howmanysh -= 1
                trlabel.text = ("Tropedo stroge:" + str(howmanytr))
                self.text = ("Shoot Amount:" + str(howmanysh))

        elif Gstate is not States.game:
            self.is_visible = False

            

class Scoreboard(Label):
    global Gstate
    def on_create(self):
        self.color = Color.CYAN
        self.layer = 11
        self.text = "Final Score"
        self.x = rbotton.la.x
        self.x = self.x - self.content_width*0.75
        self.y = rbotton.la.y - 128
        self.font_size = 32
        self.is_visible = False
    
    def on_update(self, dt):
        if Gstate is States.win:
            self.is_visible = True
        if Gstate is States.lose:
            self.is_visible = True
        if Gstate is States.start:
            self.is_visible = False

class Scoreboardboss(Label):
    global Gstate
    def on_create(self):
        self.color = Color.RED
        self.layer = 11
        self.text = "Final Score"
        self.time = 0
        self.atime = 2
        self.position = w.center
        self.x = self.x - self.content_width
        self.y = self.y - 32
        self.font_size = 42
        self.is_visible = False
    
    def on_update(self, dt):
        if Gstate is States.win:
            self.time += dt
            if self.time > self.atime:
                self.is_visible = True
                self.text = ("Boss's HP:" + str(0))
                self.position = w.center
                self.y = self.y + 128
                self.x = self.x - self.content_width/2
        if Gstate is States.lose:
            self.time += dt
            if self.time > self.atime:
                self.is_visible = True
                self.text = ("Boss's HP:" + str(boss.ehealth))
                self.position = w.center
                self.y = self.y + 128
                self.x = self.x - self.content_width/2
        if Gstate is States.start:
            self.is_visible = False
            self.time = 0

class Scoreboardplayer(Label):
    global Gstate
    def on_create(self):
        self.layer = 11
        self.color = Color.RED
        self.text = "Final Score"
        self.position = w.center
        self.time = 0
        self.atime = 1
        self.x = self.x - self.content_width
        self.y = self.y + 32
        self.font_size = 42
        self.is_visible = False
    
    def on_update(self, dt):
        if Gstate is States.win:
            self.time += dt
            if self.time > self.atime:
                self.is_visible = True
                self.text = ("Player's HP:" + str(player.health))
                self.position = w.center
                self.x = self.x - self.content_width/2
                self.y = self.y + 192
        if Gstate is States.lose:
            self.time += dt
            if self.time > self.atime:
                self.is_visible = True
                self.text = ("Player's HP:" + str(player.health))
                self.position = w.center
                self.x = self.x - self.content_width/2
                self.y = self.y + 192
        if Gstate is States.start:
            self.is_visible = False
            self.time = 0

class Scoreboardtool(Label):
    global Gstate
    def on_create(self):
        self.layer = 11
        self.color = Color.RED
        self.text = "Final Score"
        self.position = w.center
        self.time = 0
        self.atime = 3
        self.x = self.x - self.content_width
        self.y = self.y + 32
        self.font_size = 42
        self.is_visible = False
    
    def on_update(self, dt):
        if Gstate is States.win:
            self.time += dt
            if self.time > self.atime:
                self.is_visible = True
                self.text = ("Used tool(s) :" + str(toolcount))
                self.position = w.center
                self.x = self.x - self.content_width/2
                self.y = self.y + 64
        if Gstate is States.lose:
            self.time += dt
            if self.time > self.atime:
                self.is_visible = True
                self.text = ("Used tool(s):" + str(toolcount))
                self.position = w.center
                self.x = self.x - self.content_width/2
                self.y = self.y + 64
        if Gstate is States.start:
            self.is_visible = False
            self.time = 0

def reset():
    global toolcount,howmanytr,howmanysh
    toolcount = 0
    howmanytr = 0
    howmanysh = 0
    boss.ehealth = 600
    boss.position = w.center
    boss.y = boss.y + 324
    boss.reload = 0.42
    boss.el.text = ("Boss's HP:" + str(boss.ehealth)) 
    boss.state = boss.Stateb.normal
    player.health = 26
    player.position = w.center
    player.y = player.y - 200 
    player.pl.text =  ("Player's HP:" + str(player.health))
    player.state = player.Statep.normal
    player.color = player.rgb
    player.htime = 0
    player.gtime = 0
    helper01.position = player.position
    helper01.x = player.x - 128 
    helper02.position = player.position
    helper02.x = player.x + 128
    player.boost = False
    if player.tcount == 1:
            player.bullet01.delete()
            player.bullet02.delete()
            player.ttime = 0
            player.tcount = 0
    

boss:Boss = w.create_sprite(Boss)
player = w.create_sprite(Player)
helper01 = w.create_sprite(Helper)
helper01.x = player.x - 128
helper02 = w.create_sprite(Helper)
helper02.x = player.x + 128
title = w.create_sprite(Title)
titleword = w.create_sprite(Titleword)
pbotton = w.create_sprite(Playbo)
rbotton = w.create_sprite(Return)
scoreboard = w.create_label(Scoreboard)
fboss = w.create_label(Scoreboardboss)
fplayer = w.create_label(Scoreboardplayer)
ftool = w.create_label(Scoreboardtool)
trlabel:Label = w.create_label(Trlabel)
shlabel:Label = w.create_label(Uselabel)
w.run()