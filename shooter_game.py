from pygame import *
from random import randint
mixer.init()
font.init()

window = display.set_mode((700, 500))

background = transform.scale(image.load('galaxy.jpg'), (700, 500))
clock = time.Clock()

mixer.music.load('space.ogg')
fire_sound = mixer.Sound('fire.ogg')
font = font.Font(None, 35)
win = font.render('You win!', True, (232, 246, 57))
game_over = font.render('Game over', True, (245, 8, 39))
all_miss = 0
killed_count = 0
recharge = 0
health_boss = 10

class GameSprite(sprite.Sprite):
    def __init__(self, speed, picture, x, y):
        super().__init__()
        self.speed = speed
        self.image = transform.scale(image.load(picture), (80, 80))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Enemy_Boss(GameSprite):
    def __init__(self, speed, picture, x, y):
        super().__init__(speed, picture, x, y)
        self.image = transform.scale(image.load(picture), (200, 150))
    def update(self):
        global all_miss
        if self.rect.y >= 500:
            self.rect.y = 0
            self.rect.x = 250
            all_miss += 5
        self.rect.y += self.speed

class Player(GameSprite):
    def __init__(self, speed, picture, x, y):
        super().__init__(speed, picture, x, y)
        self.image = transform.scale(image.load(picture), (85, 135))
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x > 0:
            self.rect.x -= 9
        if keys_pressed[K_d] and self.rect.x < 620:
            self.rect.x += 9
    def fire(self):
        global bullets
        global recharge
        recharge += 1
        keys_pressed = key.get_pressed()
        if keys_pressed[K_SPACE] and recharge >= 13:
            # создаем объект пули
            bullet = Bullet(3, 'bullet.png', self.rect.x + 32, self.rect.y)
            # добавляем его в группу пуль
            bullets.add(bullet)
            recharge = 0

class Bullet(GameSprite):
    def __init__(self, speed, picture, x, y):
        super().__init__(speed, picture, x, y)
        self.image = transform.scale(image.load(picture), (20, 45))
    def update(self):
        if self.rect.y <= 0:
            self.kill()
        self.rect.y -= 3

class Meteor(GameSprite):
    def __init__(self, speed, picture, x, y):
        super().__init__(speed, picture, x, y)
    def update(self):
        global all_miss
        if self.rect.y >= 500:
            self.rect.y = 0
            self.rect.x = randint(100, 450)
            self.speed = randint(2,3)
            all_miss += 1
        self.rect.y += self.speed

rocket = Player(10, 'rocket.png', 350, 350)
enemy_boss = Enemy_Boss(1, 'ufo.png', 250, 0)
#meteor = Meteor(3, 'asteroid.png', 500, 0)
meteors = sprite.Group()
# группа пуль
bullets = sprite.Group()

for i in range(5):
    meteor = Meteor(3, 'asteroid.png', randint(100, 450), 0)
    meteors.add(meteor)

game = True
finish = False
mixer.music.play()
fire_sound.play()
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    if finish != True:

        sprites_list1 = sprite.spritecollide(rocket, meteors, False)
        sprites_list = sprite.groupcollide(meteors, bullets, True, True)

        for meteor in sprites_list:
            killed_count += 1
            meteor = Meteor(3, 'asteroid.png', randint(100, 450), 0)
            meteors.add(meteor)

        miss_counter = font.render('Всего пропусков:' + str(all_miss), True, (255, 255, 255))
        kill_counter = font.render('Убитых врагов:' + str(killed_count), True, (255, 255, 255))
        window.blit(background, (0, 0))
        window.blit(miss_counter, (0, 0))
        window.blit(kill_counter, (0, 20))
        rocket.reset()
        rocket.update()
        rocket.fire()
        meteors.update()
        meteors.draw(window)
        bullets.update()
        bullets.draw(window)

        #if killed_count == 15:
        #    finish = True
        #    window.blit(win, (300,240))

        if all_miss >= 8:
            finish = True
            window.blit(game_over, (290,240))

        for meteor in sprites_list1:
            finish = True
            window.blit(game_over, (290,240))
            
        if killed_count == 15:
            meteors.empty()
            enemy_boss.reset()
            enemy_boss.update()
        
        if sprite.spritecollide(enemy_boss, bullets, True):
            health_boss -= 1
        
        if health_boss == 0:
            finish = True
            window.blit(win, (300,240))

        clock.tick(60)
        display.update()
