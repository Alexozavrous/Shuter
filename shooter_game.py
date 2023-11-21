#Создай собственный Шутер!

from pygame import *

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect_x = player_x
        self.rect_y = player_y
    def reset(self):
        window.blit(self.image,(self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < 620:
            self.rect.x += self.speed
        
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

lost = 0

score = 0
font.init()
font1 = font.SysFont('Arial', 80)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))



class Enemy(GameSprite):
    def update(self):
        global lost
        if self.rect.y <= 500:
            self.rect.y += self.speed
        if self.rect.y > 500:
            self.rect.x = randint(80, 620)
            self.rect.y = 0
            lost = lost + 1


class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()


ship = Player('rocket.png', 600, 5, 80, 100, 10)

from random import *
monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy('ufo.png', randint(80, 620), -40, 80, 50, randint(1, 5))
    monsters.add(monster)

asteroids = sprite.Group()
for i in range(1, 3):
    asteroid = Enemy('asteroid.png', randint(80, 620), -40, 80, 50, randint(1, 5))
    asteroids.add(asteroid)

bullets = sprite.Group()



window = display.set_mode((700, 500))
display.set_caption("шутер")
background = transform.scale(image.load("galaxy.jpg"), (700, 500))



mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

run = True

clock = time.Clock()
FPS = 60


finish = False
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE: 
                ship.fire()
                

    if finish != True:
        window.blit(background,(0,0))
        text = font1.render('Счёт:' + str(score), 1, (255, 255, 225))
        window.blit(text, (10, 20))

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score + 1
            monster = Enemy('asteroid.png', randint(80, 620), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

        if sprite.spritecollide(ship, monsters, False) or lost >= 3:
            finish = True #проиграли, ставим фон и больше не управляем спрайтами.
            window.blit(lose, (200, 200))
      
        if sprite.spritecollide(ship, asteroids, False) or lost >= 3:
            finish = True #проиграли, ставим фон и больше не управляем спрайтами.
            window.blit(lose, (200, 200))

        if score >= 10:
            finish = True
            window.blit(win, (200, 200))


        text_lose = font1.render('Пропущено:' + str(lost), 1, (255, 255, 225))
        window.blit(text_lose, (10, 50))
        
        ship.update()
        monsters.update()
        bullets.update()
        asteroids.update()

        ship.reset()
        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)

    display.update()
    clock.tick(FPS)




