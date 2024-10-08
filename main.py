from pygame import *

init()


class GameSprite:
    def __init__(self, img, x, y, width, height):
        self.image = transform.scale(image.load(img), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.current_image = 0

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


size = (800, 500)
window = display.set_mode(size)
display.set_caption('dino')
clock = time.Clock()

floors = list()
for i in range(-300, 600, 300):
    floor = GameSprite('img/floor.png', i, 400, 800, 100)
    floors.append(floor)

game = True
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    window.fill((255, 255, 255))
    for floor in floors:
        floor.rect.x -= 8
        floor.reset()
        if floor.rect.x < -550:
            floor.rect.x = 800

    display.update()
    clock.tick(60)

quit()
