import os

import pygame

width, height = 900, 900
all_sprites = pygame.sprite.Group()
pygame.init()
size = 1320, 750
x, y = 150, 150
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Парашют')


def load_image(name, colorkey=-1):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Sea(pygame.sprite.Sprite):
    image = load_image("sea.png")

    def __init__(self):
        super().__init__(all_sprites)
        self.image = Sea.image
        self.rect = self.image.get_rect()
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)
        # располагаем горы внизу
        self.rect.bottom = height


class Cannon(pygame.sprite.Sprite):
    image = load_image("cannon.png")

    def __init__(self):
        super().__init__(all_sprites)
        self.image = Cannon.image
        self.rect = self.image.get_rect()
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)
        # располагаем горы внизу
        self.rect.x = 450
        self.rect.y = 585


sea = Sea()
cannon = Cannon()
bullet = pygame.sprite.Group()
ship_1 = pygame.sprite.Group()


class Bullet(pygame.sprite.Sprite):
    image = load_image('bullet.png')

    def __init__(self, x):
        super().__init__(bullet)
        self.image = Bullet.image
        self.rect = self.image.get_rect()
        self.rect.x = x + 40
        self.rect.y = 580

    def update(self):
        if pygame.sprite.spritecollide(ship, bullet, True):
            ship.health = ship.health[:-1]
            expl = Explosion((self.rect.x + 30, self.rect.y - 80), 'sm')
            pygame.display.flip()
        self.rect.y -= 20
        if self.rect.y <= 0:
            self.kill()




class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        super().__init__(all_sprites)
        self.size = size
        self.image = load_image(f'regularExplosion00.png')
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.mask = pygame.mask.from_surface(self.image)
        self.go()

    def go(self):
        ct = pygame.time.Clock()
        for i in range(9):
            ct.tick(10)
            all_sprites.draw(screen)
            self.image = load_image(f'regularExplosion0{i}.png')
            pygame.display.flip()
        self.kill()
        pygame.display.flip()

class Ship(pygame.sprite.Sprite):
    image = load_image("ship.png")
    image_1 = image
    health = ['♥', '♥', '♥', '♥', '♥']
    image_2 = pygame.transform.flip(image, True, False)

    def __init__(self, pos):
        super().__init__(ship_1)
        self.image = Ship.image_1
        self.rect = self.image.get_rect()
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.y = 100
        self.x = self.rect.x

    def update(self):
        self.x += 20
        if ((self.x - (self.x) % 1000) // 1000) % 2:
            self.rect.x = 1000 - self.x % 1000
            self.image = self.image_2
        else:
            self.image = self.image_1
            self.rect.x = self.x % 1000


ship = Ship((55, 200))
all_sprites.add(ship)
running = True
clock = pygame.time.Clock()


def draw_text():
    font = pygame.font.Font(pygame.font.match_font('arial'), 50)
    text_surface = font.render(''.join(ship.health), True, 'red ')
    text_rect = text_surface.get_rect()
    text_rect.midtop = (80, 0)
    screen.blit(text_surface, text_rect)


while ship.health:
    all_sprites.draw(screen)
    clock.tick(30)
    ship_1.draw(screen)
    ship_1.update()
    draw_text()
    bullet.update()
    bullet.draw(screen)
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                if cannon.rect.x > 0:
                    cannon.rect.x -= 10
            if keys[pygame.K_RIGHT]:
                if cannon.rect.x < 1200:
                    cannon.rect.x += 10
            if keys[pygame.K_SPACE]:
                bullet.add(Bullet(cannon.rect.x))
