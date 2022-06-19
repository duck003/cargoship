from typing import List
from pycat.core import Window, Scheduler

w = Window(width=752, height=608, enforce_window_limits=False)


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


def img_file(i): return f'test/png/Level_{i}.png'


level = ScrollableLevel(3*[img_file(0)]+2*[img_file(1), img_file(2)])
Scheduler.update(level.on_update)
w.run()
