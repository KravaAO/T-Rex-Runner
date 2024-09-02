from pygame import *
import time as t

init()


class GameSprite:
    def __init__(self, img_list, x, y, width, height):
        self.images = [transform.scale(image.load(img), (width, height)) for img in img_list]
        self.rect = self.images[0].get_rect()
        self.rect.x = x
        self.rect.y = y
        self.current_image = 0

    def do_animate(self):
        self.current_image += 1
        if self.current_image >= len(self.images):
            self.current_image = 0

    def reset(self, window):
        window.blit(self.images[self.current_image], (self.rect.x, self.rect.y))

    def draw_rect(self):
        draw.rect(window, (250, 0, 0), self.rect, 5, 5)

class Enemy(GameSprite):
    def update(self):
        pass


cactus = Enemy(['img/cactus.png'], 900, 360, 60, 80)


size = (800, 500)
window = display.set_mode(size)
display.set_caption('dino')
clock = time.Clock()


dino_frames = ['img/dino_run_1.png', 'img/dino_run_2.png']
dino = GameSprite(dino_frames, 100, 350, 100, 100)

floor1 = transform.scale(image.load('img/floor.png'), (800, 100))
floor1_rect = floor1.get_rect()
floor2 = transform.scale(image.load('img/floor.png'), (800, 100))
floor2_rect = floor2.get_rect()
floor3 = transform.scale(image.load('img/floor.png'), (800, 100))
floor3_rect = floor3.get_rect()

floor1_rect.x = -300
floor2_rect.x = 300
floor3_rect.x = 600

game = True
start_time = t.time()
is_jump = False
start_jump = 0
finish = False
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE and not is_jump:
                is_jump = True
                start_jump = t.time()
    if not finish:
        window.fill((250, 250, 250))

        floor1_rect.x -= 8
        floor2_rect.x -= 8
        floor3_rect.x -= 8
        window.blit(floor1, (floor1_rect.x, 400))
        window.blit(floor2, (floor2_rect.x, 400))
        window.blit(floor3, (floor3_rect.x, 400))
        if floor1_rect.x < -550:
            floor1_rect.x = 800
        if floor2_rect.x < -550:
            floor2_rect.x = 800
        if floor3_rect.x < -550:
            floor3_rect.x = 800

        if is_jump:
            dino.rect.y -= 5
        new_time = t.time()

        if new_time - start_jump > 0.5:
            is_jump = False

        if dino.rect.y < 350 and not is_jump:
             dino.rect.y += 5

        # Оновлення анімації динозавра
        if not is_jump:
            if new_time - start_time > 0.2:
                dino.do_animate()
                start_time = t.time()

        dino.reset(window)

        cactus.rect.x -= 8
        cactus.reset(window)
        #cactus.draw_rect()
        #dino.draw_rect()
        if cactus.rect.x < -80:
            cactus.rect.x = 900

    if cactus.rect.colliderect(dino.rect):
        finish = True

    display.update()
    clock.tick(60)

quit()
