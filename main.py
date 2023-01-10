import os
import time
import pygame

import input as ip
from war import start as s_t

missed = pygame.sprite.Group()

fire_on_ship = pygame.sprite.Group()
pygame.mixer.music.load('data/corsars.mp3')
pygame.mixer.music.play(-1)
water = pygame.mixer.Sound('data/water.mp3')

def start_screen(width, height, intro_text, image_name):
    fon = pygame.transform.scale(load_image(image_name), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 26)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('blue'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()


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


class Missed_Mine(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__(missed)
        self.image = load_image("pngegg.png")
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.y = pos[0] // cell_size * cell_size + cell_size / 2, pos[
            1] // cell_size * cell_size
        self.mask = pygame.mask.from_surface(self.image)


class Board:
    def __init__(self, width, height):
        self.width = width
        self.cnt = 0
        self.height = height
        try:
            self.load_level(ip.main('Введи имя файла, в котором лежит карта'))
        except FileNotFoundError:
            self.load_level('ships.txt')
        self.cell_size = 70

    def load_level(self, filename):
        self.board = []
        filename = "data/" + filename
        # читаем уровень, убирая символы перевода строки
        with open(filename, 'r') as mapFile:
            lmap = [line.strip() for line in mapFile]
        for i in range(len(lmap)):
            tmp = []
            for j in range(len(lmap[i])):
                tmp.append(int(lmap[i][j]))
            self.board.append(tmp)

    def get_cell(self, pos):
        if pos[1] > 0 + self.cell_size * self.height or pos[0] > 0 + self.width * self.cell_size or pos[0] < 0 or \
                pos[1] < 0:
            return
        else:
            x = (pos[0]) // self.cell_size
            y = (pos[1]) // self.cell_size
            return x, y

    def get_click(self, pos):
        x, y = pos[0] // self.cell_size, pos[1] // self.cell_size
        if x < self.height and y < self.height:
            if self.check(x, y):
                pygame.mixer.music.pause()
                print('pause')
                s_t(hard_level)
                pygame.mixer.music.unpause()
                self.cnt += 1
                self.board[y][x] = 2
            else:
                if self.check(x, y) == 0:
                    water.play()
                    self.cnt += 1
                    missed.add(Missed_Mine(pos))

    def check(self, x, y):
        try:
            return self.board[y][x]
        except IndexError:
            return None

    def render(self, screen):
        missed.draw(screen)
        for i in range(self.height):
            for j in range(self.width):
                pygame.draw.rect(screen, 'white', (
                    j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size), 1)
                if self.board[j][i] == 2:
                    pygame.draw.line(screen, 'red', (i * self.cell_size, j * self.cell_size + 3),
                                     (i * self.cell_size + self.cell_size - 3, j * self.cell_size + cell_size - 3),
                                     width=5)
                    pygame.draw.line(screen, 'red', (i * self.cell_size, j * self.cell_size + cell_size - 3),
                                     (i * self.cell_size + cell_size - 3, j * self.cell_size + 3), width=5)

    def alive(self):
        cnt = 0
        for elem in self.board:
            cnt += sum(elem)
        return cnt


def draw_text(text, coord):
    font = pygame.font.Font(pygame.font.match_font('arial'), 50)
    text_surface = font.render(text, True, 'white')
    text_rect = text_surface.get_rect()
    text_rect.midtop = coord
    screen.blit(text_surface, text_rect)

def change_time():
    times[1] = int(time.time() - start_time) - 60 * times[0]
    if times[1] >= 60:
        times[0] += 1
        times[1] -= 60

if __name__ == '__main__':
    size = 750, 700
    brd = Board(10, 10)
    pygame.init()
    screen = pygame.display.set_mode(size)
    start_screen(size[0], size[1], ["Рад тебя здравстовать, дорогой игрок,",
                                    "Правила игры очень просты:",
                                    "Море размечено на квадраты, стреляй по ним.",
                                    "Попадешь - нанесешь ущерб врагу,",
                                    'Но так просто он не дастся!'], 'fon.jpg')
    pygame.display.set_caption('Морской бой')
    while 1:
        try:
            hard_level = int(ip.main('Введите желаемы уровень сложности, не меньший 1.'))
            break
        except:
            pass
    cell_size = 70
    start_cnt = brd.alive()
    start_time = time.time()
    times = [0, 0]
    while brd.alive() != start_cnt * 2:
        screen.fill('black')
        change_time()
        draw_text(':'.join([str(elem) for elem in times]), (714, 0))
        brd.alive()
        draw_text(str(brd.cnt), (10, 0))
        brd.render(screen)
        fire_on_ship.draw(screen)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                brd.get_click(event.pos)
    pygame.mixer.quit()
    pygame.mixer.music.load('data/fanf.mp3')
    pygame.mixer.music.play(-1)
    start_screen(size[0], size[1], ["Враг был повержен!", "Поздравляю!"], 'fon_2.jpg')
