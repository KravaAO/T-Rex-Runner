from pygame import *
import time as t
import random

init()
font.init()

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
    def random_group(self):
        pass

    def update(self):
        pass

img_reset = transform.scale(image.load('img/reset.png'), (80, 50))

cactuses = list()
cactus_l = Enemy(['img/cactus.png'], random.randint(1200, 1600), 360, 60, 80)
cactus_b = Enemy(['img/cactus_big.png'], random.randint(1650, 2300), 340, 70, 100)
cactuses.append(cactus_l)
cactuses.append(cactus_b)

size = (800, 500)
window = display.set_mode(size)
display.set_caption('dino')
clock = time.Clock()

font1 = font.Font('NFPixels-Regular.otf', 30)


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
dino.rect.width -= 40
score = 0
hight_score = 0
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE and not is_jump and dino.rect.y == 350:
                is_jump = True
                start_jump = t.time()
        if e.type == MOUSEBUTTONDOWN and finish:
            score = 0
            cactuses = list()
            cactus_l = Enemy(['img/cactus.png'], random.randint(1200, 1600), 360, 60, 80)
            cactus_b = Enemy(['img/cactus_big.png'], random.randint(1650, 2300), 340, 70, 100)
            cactuses.append(cactus_l)
            cactuses.append(cactus_b)
            dino = GameSprite(dino_frames, 100, 350, 100, 100)
            finish = False

    if not finish:
        text = font1.render(f'HI{int(hight_score)} {int(score)}', True, (0, 0, 0))
        window.fill((255, 255, 255))
        window.blit(text, (630, 40))
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

        new_time = t.time()

        if is_jump:
             dino.rect.y -= 8
        if dino.rect.y < 100:
            is_jump = False
        if dino.rect.y < 350 and not is_jump:
            dino.rect.y += 8

        # Оновлення анімації динозавра
        if not is_jump:
            if new_time - start_time > 0.2:
                dino.do_animate()
                start_time = t.time()

        score+=0.1
        if score > hight_score:
            hight_score = score

        dino.reset(window)

        for cactus in cactuses:
            cactus.rect.x -= 8
            cactus.reset(window)
            if cactus.rect.x < -40:
                cactus.rect.x = random.randint(900, 1400)
            if cactus.rect.colliderect(dino):
                finish = True

    if finish:
        dino = GameSprite(['img/dino_game_over.png'], dino.rect.x, dino.rect.y, 100, 100)
        dino.reset(window)
        font2 = font.Font('NFPixels-Regular.otf', 60)
        text_lose = font2.render('Game over!', True, (0, 0, 0))
        window.blit(text_lose, (250, 150))
        window.blit(img_reset, (350, 250))

    display.update()
    clock.tick(60)

quit()
