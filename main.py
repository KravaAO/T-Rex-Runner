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


class AnimatedSprite(GameSprite):
    def __init__(self, images, x, y, width, height):
        super().__init__(images[0], x, y, width, height)
        # Використовуємо list comprehension для створення списку анімованих зображень
        # Синтаксис [expression for item in iterable] дозволяє створити новий список на основі існуючого ітерабельного об'єкта
        # У цьому випадку expression - це `transform.scale(image.load(img), (width, height))`, який масштабовує кожне зображення з `images`
        # `for img in images` - це ітерація по всіх елементах у списку `images`, і кожне зображення обробляється та додається до нового списку
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

player_images = ['img/dino_run_1.png', 'img/dino_run_2.png']
player = AnimatedSprite(player_images, 50, 340, 80, 100)

jump = False
jump_speed = 20
gravity = 1
y_velocity = 0

game = True
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE and not jump:
                jump = True
                y_velocity = -jump_speed

    if jump:
        player.rect.y += y_velocity
        y_velocity += gravity
        if player.rect.y >= 340:
            player.rect.y = 340
            jump = False

    window.fill((255, 255, 255))
    for floor in floors:
        floor.rect.x -= 8
        floor.reset()
        if floor.rect.x < -550:
            floor.rect.x = 800

    if not jump:
        player.do_animate()
    player.reset()

    display.update()
    clock.tick(60)

quit()
