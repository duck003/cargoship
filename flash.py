from pycat.core import Window, Sprite
from enum import Enum, auto

w = Window()


class State(Enum):
    FLASH = auto()
    ON = auto()


class Button(Sprite):
    def on_create(self):
        self.scale = 100
        self.x = 100
        self.y = 100
        self.label = w.create_label(font_size=10, color=(0, 0, 0))
        self.set_text('click me')

    def set_text(self, text):
        self.label.text = text
        self.label.x = self.x - self.label.content_width/2
        self.label.y = self.y + self.label.content_height/2

    def on_left_click(self):
        if test.state is State.ON:
            test.state = State.FLASH

        elif test.state is State.FLASH:
            test.state = State.ON
            test.is_visible = True

        self.set_text(str(test.state))


class Test(Sprite):
    def on_create(self):
        self.scale = 200
        self.position = w.center
        self.state = State.ON
        self.flash_time = 0.2
        self.time = 0

    def on_update(self, dt):
        if self.state is State.FLASH:
            self.time += dt
            if self.time > self.flash_time:
                self.is_visible = not self.is_visible
                self.time = 0


w.create_sprite(Button)
test = w.create_sprite(Test)
w.run()