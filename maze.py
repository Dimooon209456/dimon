from pygame import *

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(65, 65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption('Maze')
backround = transform.scale(image.load("background.jpg"),(win_width, win_height))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys [K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys [K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys [K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys [K_DOWN] and self.rect.y < win_height - 80:
            self.rect.y += self.speed

class Enemy(GameSprite):
    direction = "left"
    def update(self):
        if self.rect.x <= 470:
            self.direction = "right"
        if self.rect.x >= win_width - 85:
            self.direction = "left"

        if self.direction == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

class Wall(sprite.Sprite):
    def __init__(self, color_1, color_2, color_3, wall_x, wall_y, wall_width, wall_height):
        super().__init__()
        self.color_1 = color_1
        self.color_2 = color_2
        self.color_3 = color_3
        self.width = wall_width
        self.height = wall_height
        self.image = Surface((self.width, self.height))
        self.image.fill((color_1, color_2, color_3))
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y
    def draw_wall(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
        #draw.rect(window, (self.color_1, self.color_2, self.color_3), (self.rect.x, self.rect.y))

player = Player('hero.png', 5, win_height -80, 4)
monster = Enemy('cyborg.png', win_width -80, 280, 2)
wall_0 = Wall(30, 30, 30, 200, 400, 350, 50)
treaser = GameSprite('treasure.png', win_width -120, win_height -80, 0)

game = True
finish = False
clock = time.Clock()
FPS = 60

font.init()
font = font.Font(None,70)
win = font.render('YOU WIN!', True, (255, 215, 0))
lose = font.render('YOU LOSE!', True, (180, 0, 0))

mixer.init()
mixer.music.load('jungles.ogg')
mixer.music.play

money = mixer.Sound('money.ogg')
kick = mixer.Sound('kick.ogg')

while game:
    for i in event.get():
        if i.type == QUIT:
            game = False

    if finish != True:
        window.blit(backround, (0, 0))
        player.update()
        monster.update()
        wall_0.draw_wall()
        player.reset()
        monster.reset()
        treaser.reset()

    if sprite.collide_rect(player, monster) or sprite.collide_rect(player, wall_0):
        finish = True
        window.blit(lose, (200, 200))
        kick.play()

    if sprite.collide_rect(player, treaser):
        finish = True
        window.blit(win, (200, 200))
        kick.play()

    display.update()
    clock.tick(FPS)