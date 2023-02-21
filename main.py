import os
import sys
import pygame
import random
#  события для игры
SPAWN_ASTEROID = pygame.USEREVENT + 1
DEATH = pygame.USEREVENT + 2
DIFFICULTY_UP = pygame.USEREVENT + 3

pygame.init()
size = width, height = 500, 500
screen = pygame.display.set_mode(size)


#  функция загрузки картинки
def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


#  следующие несколько функций - отрисовка разных меню
def draw_menu():
    screen.blit(header_text_part1, header_text_part1.get_rect(center=(200, 90)))
    screen.blit(header_text_part2, header_text_part1.get_rect(center=(200, 120)))
    screen.blit(header_text_part3, header_text_part1.get_rect(center=(200, 150)))
    screen.blit(header_text_part4, header_text_part1.get_rect(center=(200, 180)))
    screen.blit(header_text_part5, header_text_part1.get_rect(center=(200, 210)))

    best_score_text = font2.render(f'Best score: {best_score}', False, 'white')
    best_time_text = font2.render(f'Best time: {int(best_time)}s', False, 'white')
    screen.blit(best_score_text, best_score_text.get_rect(center=(250, 250)))
    screen.blit(best_time_text, best_time_text.get_rect(center=(250, 270)))

    pygame.draw.rect(screen, 'black', (150, 300, 200, 50))
    pygame.draw.rect(screen, 'black', (150, 355, 200, 50))
    screen.blit(play_text, play_text.get_rect(center=(250, 325)))
    screen.blit(settings_text, settings_text.get_rect(center=(250, 380)))


def draw_settings():

    pygame.draw.rect(screen, 'black', (100, 100, 300, 300))
    pygame.draw.rect(screen, (20, 0, 100), (150, 340, 200, 50))
    pygame.draw.rect(screen, (20, 0, 100), (197, 140, 100, 50))

    if asteroids_mod2:
        pygame.draw.rect(screen, 'white', (205, 145, 40, 40))
    else:
        pygame.draw.rect(screen, 'white', (250, 145, 40, 40))

    main_menu_text = font1.render('Main menu', True, 'white')
    spaceship_color_text = font3.render('Spaceship model:', True, 'white')

    screen.blit(main_menu_text, main_menu_text.get_rect(center=(250, 365)))
    screen.blit(asteroids_mod_text, asteroids_mod_text.get_rect(center=(220, 120)))
    screen.blit(on_text, on_text.get_rect(center=(150, 160)))
    screen.blit(off_text, off_text.get_rect(center=(350, 160)))
    screen.blit(spaceship_color_text, spaceship_color_text.get_rect(center=(190, 230)))

    pygame.draw.rect(screen, (20, 0, 100), (115, 250, 80, 80), width=2)
    pygame.draw.rect(screen, (20, 0, 100), (210, 250, 80, 80), width=2)
    pygame.draw.rect(screen, (20, 0, 100), (305, 250, 80, 80), width=2)

    if spaceship.color == 'white':
        pygame.draw.rect(screen, 'white', (115, 250, 80, 80), width=2)
    elif spaceship.color == 'red':
        pygame.draw.rect(screen, 'white', (210, 250, 80, 80), width=2)
    elif spaceship.color == 'blue':
        pygame.draw.rect(screen, 'white', (305, 250, 80, 80), width=2)

    images.draw(screen)


def draw_game_over_screen():

    background_sprite_group.draw(screen)
    pygame.draw.rect(screen, 'black', (100, 100, 300, 300))
    pygame.draw.rect(screen, (20, 0, 100), (150, 310, 200, 50))
    game_over_text = font1.render('GAME OVER!', True, 'white')
    main_menu_text = font1.render('Main menu', True, 'white')
    best_score_text = font2.render(f'Best score: {best_score}', True, 'white')
    best_time_text = font2.render(f'Best time: {int(best_time)}s', True, 'white')

    screen.blit(main_menu_text, main_menu_text.get_rect(center=(250, 335)))
    screen.blit(game_over_text, game_over_text.get_rect(center=(250, 150)))
    screen.blit(score_text, score_text.get_rect(center=(250, 200)))
    screen.blit(best_score_text, best_score_text.get_rect(center=(250, 220)))
    screen.blit(time_text, time_text.get_rect(center=(250, 240)))
    screen.blit(best_time_text, best_time_text.get_rect(center=(250, 260)))


def draw_pause_menu():

    pygame.draw.rect(screen, 'black', (100, 100, 300, 300))
    pygame.draw.rect(screen, (20, 0, 100), (125, 130, 250, 60))
    pygame.draw.rect(screen, (20, 0, 100), (125, 220, 250, 60))
    pygame.draw.rect(screen, (20, 0, 100), (125, 310, 250, 60))
    main_menu_text = font1.render('MAIN MENU', True, 'white')

    screen.blit(back_to_game_text, back_to_game_text.get_rect(center=(250, 160)))
    screen.blit(settings_text, settings_text.get_rect(center=(250, 250)))
    screen.blit(main_menu_text, main_menu_text.get_rect(center=(250, 340)))


#  функция работы настроек игры
def settings(settings_on):
    global asteroids_mod2
    background_sprite_group.draw(screen)

    while settings_on:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if (x > 150) and (x < 351) and (y > 340) and (y < 391):
                    settings_on = False
                    main_menu()
                if (x > 197) and (x < 298) and (y > 140) and (y < 191):
                    change_ast_mod()
                if (x > 115) and (x < 186) and (250 < y < 331):
                    spaceship.change_color("white")
                if (210 < x < 291) and (250 < y < 331):
                    spaceship.change_color("red")
                if (305 < x < 386) and (250 < y < 331):
                    spaceship.change_color("blue")

        draw_settings()

        pygame.display.flip()


#  функция перехода из одного астероидного режима в другой
def change_ast_mod():
    global asteroids_mod2
    if asteroids_mod2:
        asteroids_mod2 = False
        pygame.draw.rect(screen, (20, 0, 100), (205, 145, 40, 40))
        pygame.draw.rect(screen, 'white', (250, 145, 40, 40))
    else:
        asteroids_mod2 = True
        pygame.draw.rect(screen, 'white', (205, 145, 40, 40))
        pygame.draw.rect(screen, (20, 0, 100), (250, 145, 40, 40))


#  функция главного меню
def main_menu(settings_on=False):
    global play
    global new_start
    global difficulty

    spaceship.rect.x = 215
    spaceship.rect.y = 440
    spaceship.speed = (0, 0)
    scorer.score = 0
    border.cnt = 0

    background_sprite_group.draw(screen)
    while not play and not settings_on:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if (x > 150) and (x < 351) and (y > 300) and (y < 351):
                    difficulty = 0
                    play = True
                    new_start = True
                if (x > 150) and (x < 351) and (y > 355) and (y < 406):
                    settings_on = True
                    settings(settings_on)

        draw_menu()

        pygame.display.flip()


#  возможность перехода в главное меню при game over
def go_to_main_menu():
    global play
    global best_score
    global best_time
    go_to_main_menu = False

    draw_game_over_screen()

    pygame.display.flip()
    while not go_to_main_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if (x > 150) and (x < 351) and (y > 310) and (y < 361):
                    play = False
                    all_sprites.update()
                    go_to_main_menu = True
                    main_menu()
        asteroids_on_screen.update()
        ammos_on_screen.update()


#  меню паузы, переход в главное меню, настройки и возвращение к игре
def pause_menu():
    global play
    pause_menu_open = True
    while pause_menu_open:

        draw_pause_menu()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if (125 < x < 376) and (130 < y < 191):
                    pause_menu_open = False
                if (125 < x < 376) and (220 < y < 281):
                    pause_menu_open = False
                    play = False
                    all_sprites.update()
                    settings(True)
                if (125 < x < 376) and (310 < y < 371):
                    pause_menu_open = False
                    play = False
                    all_sprites.update()
                    main_menu()

        pygame.display.flip()


#  изображение корабля
class SpaceshipImage(pygame.sprite.Sprite):

    def __init__(self, color, coords, *group):
        super().__init__(*group)
        if color == 'white':
            self.image = load_image("korabl.png")
        elif color == 'red':
            self.image = load_image("red_korabl.png")
        elif color == 'blue':
            self.image = load_image("blue_korabl.png")
        self.image = pygame.transform.scale(self.image, (80, 80))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = coords


#  корабль
class Spaceship(pygame.sprite.Sprite):
    image = load_image("korabl.png")

    def __init__(self, color, *group):
        super().__init__(*group)
        self.image = Spaceship.image
        self.rect = self.image.get_rect()
        self.rect.x = 215
        self.rect.y = 440
        self.speed = (0, 0)
        self.color = color
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect = self.rect.move(self.speed)
        self.rect.x = self.rect.x % 500

    def change_color(self, color):
        if color == 'white':
            self.image = load_image("korabl.png")
            self.color = color
        elif color == 'red':
            self.image = load_image("red_korabl.png")
            self.color = color
        elif color == 'blue':
            self.image = load_image("blue_korabl.png")
            self.color = color


#  обычный астероид
class Asteroid(pygame.sprite.Sprite):
    image = load_image("asteroid.png")

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Asteroid.image
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, 450)
        self.rect.y = 0
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        global play
        self.rect = self.rect.move(0, 3)
        if pygame.sprite.collide_mask(self, spaceship):
            ev = pygame.event.Event(DEATH)
            pygame.event.post(ev)
        if not play:
            self.kill()


#  астероид случайного размера
class RandomSizedAsteroid(pygame.sprite.Sprite):
    image = load_image("asteroid.png")

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Asteroid.image
        self.size = random.randint(25, 60)
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, 500 - self.size)
        self.rect.y = 0
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        global play
        self.rect = self.rect.move(0, int(3 * (50 / self.size)))
        if pygame.sprite.collide_mask(self, spaceship):
            ev = pygame.event.Event(DEATH)
            pygame.event.post(ev)
        if not play:
            self.kill()


#  барьер, означающий, что астероид пролетел на базу
class Border(pygame.sprite.Sprite):

    def __init__(self, *group):
        super().__init__(*group)
        self.image = pygame.Surface((500, 10))
        self.image.fill((200, 200, 200))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 490
        self.cnt = 0

    def update(self):
        if pygame.sprite.spritecollide(self, asteroids_on_screen, True):
            self.cnt += 1


#  патрон
class Ammo(pygame.sprite.Sprite):
    image = load_image("ammo.png")

    def __init__(self, coords, *group):
        super().__init__(*group)
        self.image = Ammo.image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = coords
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        global play
        self.rect = self.rect.move(0, -5)
        if pygame.sprite.spritecollideany(self, asteroids_on_screen):
            if pygame.sprite.collide_mask(self, pygame.sprite.spritecollideany(self, asteroids_on_screen)):
                scorer.add_score()
                pygame.sprite.spritecollideany(self, asteroids_on_screen).kill()
                self.kill()
        if self.rect.y < -10:
            self.kill()
        if not play:
            self.kill()


#  задний фон
class BackgroundImage(pygame.sprite.Sprite):
    image = load_image("background.png")

    def __init__(self, *group):
        super().__init__(*group)
        self.image = BackgroundImage.image
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0


#  Счетчик
class Scorer():
    def __init__(self):
        self.score = 0

    def add_score(self):
        self.score += 1


#  формирование объектов-спрайтов и их сбор в группы
asteroids_on_screen = pygame.sprite.Group()
ammos_on_screen = pygame.sprite.Group()
border_sprite_group = pygame.sprite.Group()
spaceship_sprite_group = pygame.sprite.Group()
background_sprite_group = pygame.sprite.Group()
border = Border(border_sprite_group)
spaceship = Spaceship('white', spaceship_sprite_group)
background = BackgroundImage(background_sprite_group)
# переменные для работы
scorer = Scorer()
best_score = 0
difficulty = 0
time = 0
new_start = False
best_time = 0
asteroids_mod2 = False

all_sprites = pygame.sprite.Group(spaceship, border)
#  настройка времени и fps
fps = 60
clock = pygame.time.Clock()
#  таймеры для событий
pygame.time.set_timer(DIFFICULTY_UP, 10000)
pygame.time.set_timer(SPAWN_ASTEROID, 2000)
#  шрифты для надписей
font1 = pygame.font.Font(None, 45)
font2 = pygame.font.Font(None, 25)
font3 = pygame.font.Font(None, 27)
font4 = pygame.font.Font(None, 35)
font5 = pygame.font.Font(None, 50)
#  заготовленные тексты интерфейса
play_text = font1.render('PLAY', False, (255, 255, 255))
settings_text = font1.render('SETTINGS', False, (255, 255, 255))
wave_num_text = font2.render(f'Wave: {difficulty + 1}', True, 'white')
asteroids_mod_text = font3.render(f'Asteroids different size:', True, 'white')
on_text = font4.render('ON', True, 'white')
off_text = font4.render('OFF', True, 'white')
back_to_game_text = font1.render('BACK TO GAME', True, 'white')
#  разделение заголовка на части для красоты :)
header_text_part1 = font5.render("Life", True, 'white')
header_text_part2 = font5.render("Of", True, 'white')
header_text_part3 = font5.render("The", True, 'white')
header_text_part4 = font5.render("Little", True, 'white')
header_text_part5 = font5.render("Spaceship", True, 'white')
#  картинки кораблей для настроек
images = pygame.sprite.Group()
white_ship_im = SpaceshipImage('white', (115, 250), images)
red_ship_im = SpaceshipImage('red', (210, 250), images)
blue_ship_im = SpaceshipImage('blue', (305, 250), images)
#  основные игровые флаги
play = False
running = True
#  основной игровой цикл
while running:

    background_sprite_group.draw(screen)
    if border.cnt >= 10:
        border.cnt = 0
        ev = pygame.event.Event(DEATH)
        pygame.event.post(ev)
    if not play:
        main_menu()

    time_text = font2.render(f'Your time: {int(time)}s', True, 'white')
    #   обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == SPAWN_ASTEROID:
            if asteroids_mod2:
                a = RandomSizedAsteroid()
                asteroids_on_screen.add(a)
                all_sprites.add(a)
            else:
                a = Asteroid()
                asteroids_on_screen.add(a)
                all_sprites.add(a)
        if event.type == DEATH:
            spaceship.rect.x = 215
            spaceship.rect.y = 440
            go_to_main_menu()
            scorer.score = 0
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                ammo = Ammo((spaceship.rect.x + 25, spaceship.rect.y), ammos_on_screen)
                all_sprites.add(ammo)
            if event.key == pygame.K_a:
                spaceship.speed = (-5, 0)
            if event.key == pygame.K_d:
                spaceship.speed = (5, 0)
            if event.key == pygame.K_ESCAPE:
                pause_menu()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_d:
                spaceship.speed = (0, 0)
        if event.type == DIFFICULTY_UP:
            difficulty += 1
            pygame.time.set_timer(SPAWN_ASTEROID, 0)
            pygame.time.set_timer(SPAWN_ASTEROID, 2000 - 100 * difficulty)
            print(difficulty)
            wave_num_text = font2.render(f'Wave: {difficulty + 1}', True, 'white')
    #  заготовка общей игровой информации игроку
    asteroids_missed_text = font2.render('Asteroids missed: ' + str(border.cnt) + '/10',
                                         True, 'white')
    score_text = font2.render(f'Your score: {scorer.score}', True, 'white')
    #  обновление счетчика лучшего счета
    if scorer.score > best_score:
        best_score = scorer.score
    wave_num_text = font2.render(f'Wave: {difficulty + 1}', True, 'white')
    #  отображение информации игроку
    screen.blit(asteroids_missed_text, (5, 5))
    screen.blit(score_text, (5, 25))
    screen.blit(wave_num_text, (5, 45))
    screen.blit(time_text, (5, 65))
    #  отрисовка
    all_sprites.draw(screen)
    all_sprites.update()

    pygame.display.flip()
    time_millis = clock.tick(fps)
    #  подсчет времени
    if play:
        time += time_millis / 1000
    #  обнуление времени, если новая игра
    if new_start:
        time = 0
        new_start = False
    #  обновление информации о времени
    if best_time < time:
        best_time = time

pygame.quit()
