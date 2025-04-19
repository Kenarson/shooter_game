from pygame import *
from random import randint

win_width = 700
win_height = 500
window = display.set_mode((win_width,win_height))
display.set_caption('Space Shooter')
background = transform.scale(image.load("galaxy.jpg"),(win_width,win_height))

class GameSprite(sprite.Sprite):
    def __init__(self, player_img, player_x, player_y, size_x, size_y, player_spd):
        super().__init__()
        self.image = transform.scale(image.load(player_img), (size_x,size_y))
        self.speed = player_spd
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx - 7 , self.rect.top,15,20,-20)
        bullets.add(bullet)

bullets = sprite.Group()

lost = 10
score = 0
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost - 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        
        if self.rect.y < 0:
            self.kill

player = Player("rocket.png", win_width - win_width / 1.75 , win_height - 100,80,100,10)

boss_alien = Enemy("alienevil.png",  win_width - win_width / 1.34 ,-20,200,150,randint(1,5))

run = True
clock = time.Clock()
FPS = 30

monsters = sprite.Group()
for i in range(1,6):
    monster = Enemy("ufo.png",randint(80, win_width - 80),-40,80,50,randint(1,5))
    monsters.add(monster)

font.init()
font1 = font.Font(None, 36)

font2 = font.Font(None, 80)

win = font2.render("YOU WIN!", True, (255, 255, 255))
lose = font2.render("YOU LOSE!", True, (180, 0, 0))

finish = False

boss_hp = 10
player_hp = 10


while run:
    for e in event.get():
        if e.type == QUIT:
            run = False

        elif e.type == MOUSEBUTTONDOWN:
            if e.button == 1:
                # fire_sound.play()
                player.fire()

        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                # fire_sound.play()
                player.fire()

    if not finish:    

        window.blit(background,(0,0))

        text = font1.render("Score: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        text_lose = font1.render("Health: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))


        player.reset()
        player.update()

        monsters.update()
        monsters.draw(window)

        bullets.draw(window)
        bullets.update()

        if score >= 15:
            boss_alien.reset()
            boss_alien.update()
            if sprite.spritecollide(boss_alien, bullets, True, collided=None):
                boss_hp -= 1
                print(boss_hp)
            

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score + 1
            monster = Enemy("ufo.png",randint(80,win_width - 80), -40, 80, 50, randint(1,5))
            monsters.add(monster)

         

        if sprite.collide_rect(player, boss_alien):
            finish = True
            window.blit(lose, (200,200))

        if sprite.spritecollide(player, monsters, True):
           lost -= 1
            

        # if player_hp <= 0:
        #     finish = True
        #     window(lose,(200,200))

        if lost <= 0:
            finish = True
            window.blit(lose, (200,200))

        if boss_hp <= 0:
            finish = True
            window.blit(win, (200,200))

        display.update()

    clock.tick(FPS)