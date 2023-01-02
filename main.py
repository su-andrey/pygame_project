import os
from war import start as s_t
import pygame

missed = pygame.sprite.Group()

fire_on_ship = pygame.sprite.Group()


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
                s_t(5)
                self.cnt += 1
                self.board[y][x] = 2
            else:
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


def draw_text():
    font = pygame.font.Font(pygame.font.match_font('arial'), 50)
    text_surface = font.render(str(brd.cnt), True, 'white')
    text_rect = text_surface.get_rect()
    text_rect.midtop = (10, 0)
    screen.blit(text_surface, text_rect)


if __name__ == '__main__':
    pygame.init()
    size = 750, 700
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Морской бой')
    brd = Board(10, 10)
    cell_size = 70
    running = True
    while running:
        screen.fill('black')
        draw_text()
        brd.render(screen)
        fire_on_ship.draw(screen)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                brd.get_click(event.pos)

