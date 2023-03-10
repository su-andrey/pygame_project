import os
import time

import pygame
width, height = 900, 900
all_sprites = pygame.sprite.Group()
x, y = 150, 150
size = 1320, 750
pygame.init()
sc = pygame.display.set_mode(size)
pygame.display.set_caption('Бой')
sound1 = pygame.mixer.Sound('data/mini_boom.mp3')
pygame.mixer.music.set_volume(5)
fight = pygame.mixer.Sound('data/fight.mp3')


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
    image = load_image("cannon1.png")

    def __init__(self):
        super().__init__(all_sprites)
        self.image = Cannon.image
        self.rect = self.image.get_rect()
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = 450
        self.rect.y = 585


sea = Sea()
cannon = Cannon()
bullet = pygame.sprite.Group()
ship_1 = pygame.sprite.Group()


class Bullet(pygame.sprite.Sprite):
    image = load_image('bullet.png')

    def __init__(self, x, y, sign):
        super().__init__(bullet)
        if sign == '-':
            self.image = Bullet.image
        else:
            self.image = pygame.transform.flip(Bullet.image, False, True)
        self.rect = self.image.get_rect()
        self.rect.x = x + 40
        self.rect.y = y
        self.sign = sign

    def update(self):
        if pygame.sprite.collide_mask(ship, self):
            self.kill()
            pygame.mixer.pause()
            sound1.play()
            pygame.mixer.unpause()
            ship.health = ship.health[:-1]
            Explosion(self.rect.center)
            pygame.display.flip()
        if pygame.sprite.collide_mask(cannon, self) and self.sign == '+':
            sound1.play()
            ship.health.append('♥')
            Explosion(self.rect.center)
            self.kill()
        elif self.sign == '-':
            self.rect.y -= 10 * 60 // 100
        else:
            self.rect.y += 10 * 60 // 100
        if self.rect.y <= 0 or self.rect.y >= height:
            self.kill()


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center):
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
            ct.tick(15)
            all_sprites.draw(sc)
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
        self.make_a_shot = False
        super().__init__(ship_1)
        self.image = Ship.image_1
        self.rect = self.image.get_rect()
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.y = 100
        self.x = self.rect.x

    def update(self):
        self.x += int(20 * 30 // 100)
        if ((self.x - self.x % 480) // 480) % 2:
            self.rect.x = 480 - self.x % 480
            self.image = self.image_2
        else:
            self.image = self.image_1
            self.rect.x = self.x % 480
        if cannon.rect.collidepoint((self.rect.x, cannon.rect.y)) or cannon.rect.collidepoint(
                (self.rect.x + 150, cannon.rect.y)):
            self.make_a_shot = True


ship = Ship((55, 200))
all_sprites.add(ship)
clock = pygame.time.Clock()


def draw_text():
    font = pygame.font.Font(pygame.font.match_font('arial'), 50)
    text_surface = font.render(''.join(ship.health), True, 'red ')
    text_rect = text_surface.get_rect()
    text_rect.midtop = (15 * len(ship.health), 0)
    sc.blit(text_surface, text_rect)


def start(health):
    fight.play()
    last_time_cannon, last_time_ship = 1, 1
    bullet = pygame.sprite.Group()
    ship.health = ['♥' for i in range(health)]
    clock = pygame.time.Clock()
    while ship.health:
        all_sprites.draw(sc)
        clock.tick(100)
        ship_1.draw(sc)
        ship_1.update()
        draw_text()
        bullet.update()
        bullet.draw(sc)
        pygame.display.flip()
        if ship.make_a_shot:
            ship.make_a_shot = False
            if time.time() - last_time_ship >= 2:
                last_time_ship = time.time()
                bullet.add(Bullet(ship.rect.x - 50, ship.rect.y + 196, '+'))
                bullet.add(Bullet(ship.rect.x + 150, ship.rect.y + 196, '+'))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            if cannon.rect.x > 29:
                cannon.rect.x -= 2
        if keys[pygame.K_RIGHT]:
            if cannon.rect.x < 601:
                cannon.rect.x += 2
        if keys[pygame.K_x]:
            if cannon.rect.x < 640:
                cannon.rect.x += 1
        if keys[pygame.K_z]:
            if cannon.rect.x > 9:
                cannon.rect.x -= 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if keys[pygame.K_SPACE]:
                if time.time() - last_time_cannon >= 0.5:
                    last_time_cannon = time.time()
                    bullet.add(Bullet(cannon.rect.x, cannon.rect.y, '-'))
    bullet = pygame.sprite.Group()
    fight.stop()
