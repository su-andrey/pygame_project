import json
import os
import random
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
        string_rendered = font.render(line, True, pygame.Color('green'))
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
        self.rect.centerx, self.rect.y = pos[0] // brd.cell_size * brd.cell_size + brd.cell_size / 2, pos[
            1] // brd.cell_size * brd.cell_size
        self.mask = pygame.mask.from_surface(self.image)


class Board:
    def __init__(self, width, height):
        self.width = width
        self.cnt = 0
        self.height = height
        self.start_by_save = False
        self.start_cnt = 0
        try:
            with open('data/save.json', 'r') as f:
                tmp_data = json.load(f)
                if tmp_data['hard'] != 11:
                    self.start_cnt = tmp_data['start_cnt']
                    self.board = tmp_data['tmp']
                    self.hard_level = tmp_data['hard']
                    self.times = tmp_data['time']
                    self.cnt = tmp_data['cnt']
                    self.start_by_save = True
                    self.cell_size = 70
            if not self.start_by_save:
                name = (ip.main(
                    'Введите имя файла, в котором лежит карта, для просмотра рекородов введите records сложность'))
                if 'records' not in name and 'delete res from' not in name:
                    self.load_level(name)
                elif 'records' in name:
                    ip.main(name)
                else:
                    file = open('data/admin_pswd.txt')
                    if name.split()[-1] == file.read():
                        delete_key = name.split()[-2]
                        with open('data/res.json', 'r') as cat_file:
                            data = json.load(cat_file)
                            if delete_key.isdigit():
                                data[delete_key] = []
                            else:
                                for i in range(1, 11):
                                    data[str(i)] = []
                        with open('data/res.json', 'w') as file:
                            json.dump(data, file)
                        try:
                            start_screen(size[0], size[1], txt, 'fon_1.jpg')
                        except NameError:
                            ip.main('Success')
                            exit()
                    else:
                        pass
        except FileNotFoundError:
            name = f'default{random.randint(0, 3)}.txt'
            self.load_level(name)
        self.cell_size = 70
        if not self.start_by_save:
            self.times = [0, 0]

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
            if self.check(x, y) != 2:
                if self.check(x, y):
                    pygame.mixer.music.pause()
                    s_t(brd.hard_level)
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
                                     (i * self.cell_size + self.cell_size - 3, j * self.cell_size + self.cell_size - 3),
                                     width=5)
                    pygame.draw.line(screen, 'red', (i * self.cell_size, j * self.cell_size + self.cell_size - 3),
                                     (i * self.cell_size + self.cell_size - 3, j * self.cell_size + 3), width=5)

    def alive(self):
        cnt = 0
        for elem in self.board:
            cnt += sum(elem)
        return cnt


def draw_text(text, coord):
    font = pygame.font.Font(pygame.font.match_font('Arial'), 50)
    text_surface = font.render(text, True, 'white')
    text_rect = text_surface.get_rect()
    text_rect.midtop = coord
    screen.blit(text_surface, text_rect)


def change_time():
    brd.times[1] = int(time.time() - start_time) - 60 * brd.times[0]
    if brd.times[1] >= 60:
        brd.times[0] += 1
        brd.times[1] -= 60


def save():
    with open('data/save.json', 'r') as save_file:
        data = json.load(save_file)
        data['start_cnt'] = brd.start_cnt
        data['tmp'] = brd.board
        data['hard'] = brd.hard_level
        data['time'] = brd.times
        data['cnt'] = brd.cnt
    with open('data/save.json', 'w') as file:
        json.dump(data, file)


def delete():
    with open('data/save.json', 'r') as save_file:
        data = json.load(save_file)
        data['tmp'] = []
        data['hard'] = 11
        data['time'] = []
    with open('data/save.json', 'w') as file:
        json.dump(data, file)


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
            if not brd.start_by_save:
                brd.hard_level = int(
                    ip.main('Введите желаемы уровень сложности от 1 до 10'))
                if brd.hard_level < 1:
                    brd.hard_level = 1
                elif brd.hard_level > 10:
                    brd.hard_level = 10
                break
            else:
                break
        except:
            pass
    if not brd.start_by_save:
        brd.start_cnt = brd.alive()
    start_time = time.time() - (int(brd.times[0]) * 60 + int(brd.times[1]))
    while brd.alive() != brd.start_cnt * 2:
        screen.fill('black')
        change_time()
        draw_text(':'.join([str(elem) for elem in brd.times]), (714, 0))
        brd.alive()
        draw_text(str(brd.cnt), (714, 650))
        brd.render(screen)
        fire_on_ship.draw(screen)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save()
                exit()
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LCTRL] and keys[pygame.K_s]:
                    save()
                if keys[pygame.K_LCTRL] and keys[pygame.K_d]:
                    delete()
            if event.type == pygame.MOUSEBUTTONDOWN:
                brd.get_click(event.pos)

    change_time()
    res_time = ':'.join(str(elem) for elem in brd.times)
    pygame.mixer.music.load('data/fanf.mp3')
    pygame.mixer.music.play(-1)
    txt = [f"Враг был повержен всего за {brd.cnt} выстрелов и {res_time} минут!", "Поздравляю!"]
    with open('data/res.json', 'r') as cat_file:
        data = json.load(cat_file)
        data[str(brd.hard_level)].append(res_time)
        if sorted(data[str(brd.hard_level)], key=len)[0] == res_time:
            txt.append("А кроме того, ты установил новый рекорд в данной категории!")
            txt.append(f"Для просмотра всех рекордов на стартовом экране введи records 0")
    with open('data/res.json', 'w') as file:
        json.dump(data, file)
    start_screen(size[0], size[1], txt, 'fon_1.jpg')
    delete()
