from pygame import *
import random

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

    def draw_rect(self):
        draw.rect(window, (255, 0, 0), self.rect)


class AnimatedSprite(GameSprite):
    def __init__(self, images, x, y, width, height):
        super().__init__(images[0], x, y, width, height)
        self.images = [transform.scale(image.load(img), (width, height)) for img in images]
        self.current_image = 0
        self.animation_speed = 0.1

    def do_animate(self):
        self.current_image += self.animation_speed
        if self.current_image >= len(self.images):
            self.current_image = 0
        self.image = self.images[int(self.current_image)]


size = (800, 500)
window = display.set_mode(size)
display.set_caption('dino')
clock = time.Clock()

floors = list()
for i in range(-300, 601, 300):
    floor = GameSprite('img/floor.png', i, 400, 800, 100)
    floors.append(floor)

cacti = [
    GameSprite('img/cactus.png', random.randint(1100, 1500), 350, 40, 80),
    GameSprite('img/cactus_big.png', random.randint(1300, 1700), 340, 60, 90)
]

restart_img = image.load('img/reset.png')

font1 = font.Font('NFPixels-Regular.otf', 25)

player_images = ['img/dino_run_1.png', 'img/dino_run_2.png']
player = AnimatedSprite(player_images, 50, 340, 80, 100)
player.rect.width -= 40

jump = False
jump_speed = 20
gravity = 1
y_velocity = 0

game = True
game_speed = 8
finish = False
score = 0
high_score = 0
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE and not jump:
                jump = True
                y_velocity = -jump_speed
        if e.type == MOUSEBUTTONDOWN and finish:
            finish = False
            game_speed = 8
            cacti = [
                GameSprite('img/cactus.png', random.randint(1100, 1500), 350, 40, 80),
                GameSprite('img/cactus_big.png', random.randint(1300, 1700), 340, 60, 90)
            ]
            player_images = ['img/dino_run_1.png', 'img/dino_run_2.png']
            player = AnimatedSprite(player_images, 50, 340, 80, 100)
            player.rect.width -= 40
            score = 0

    if not finish:
        if jump:
            player.rect.y += y_velocity
            y_velocity += gravity
            if player.rect.y >= 340:
                player.rect.y = 340
                jump = False

        window.fill((255, 255, 255))
        for floor in floors:
            floor.rect.x -= game_speed
            floor.reset()
            if floor.rect.x < -550:
                floor.rect.x = 800

        for cactus in cacti:
            cactus.rect.x -= game_speed
            cactus.reset()
            if cactus.rect.x < -50:
                cactus.rect.x = random.randint(1100, 1700)
            if cactus.rect.colliderect(player.rect):
                player_images = ['img/dino_game_over.png']
                player = AnimatedSprite(player_images, player.rect.x, player.rect.y, 80, 100)
                window.blit(restart_img, (330, 200))
                finish = True

        if not jump:
            player.do_animate()

        player.reset()
        score += game_speed * 0.1
        if score > high_score:
            high_score = score
        score_text = font1.render(f'{int(score)}/{int(high_score)}', True, (0, 0, 0))
        window.blit(score_text, (680, 20))

        game_speed += 0.001

    display.update()
    clock.tick(60)

quit()
