import pygame
pygame.init()
import os

def path_file(filename):
    folder = os.path.abspath(__file__ + "/..")
    path = os.path.join(folder, filename)
    return path

WIN_WIDTH, WIN_HEIGHT = 700, 500 
FPS = 40

window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("game228")
clock = pygame.time.Clock()

background_image = pygame.transform.scale(pygame.image.load(path_file("images\\background.jpg")), (WIN_WIDTH, WIN_HEIGHT))

pygame.mixer.music.load(path_file("music\\fonova_musica.ogg"))
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

win_image = pygame.transform.scale(pygame.image.load(path_file("images\\win_image.jpg")), (WIN_WIDTH, WIN_HEIGHT))
win_music = pygame.mixer.Sound(path_file("music\\pobeda.ogg"))

lose_image = pygame.transform.scale(pygame.image.load(path_file("images\\lose_image.png")), (WIN_WIDTH, WIN_HEIGHT))
lose_music = pygame.mixer.Sound(path_file("music\\porazka.ogg"))
music_shot = pygame.mixer.Sound(path_file("music\\porazka.ogg"))

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, img):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.transform.scale(pygame.image.load(img), (width, height))

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Enemy(GameSprite):
    def __init__(self, x, y, width, height, img, speed, min_cord, max_cord, direction):
        super().__init__(x, y, width, height, img)
        self.speed = speed
        self.min_cord = min_cord
        self.max_cord = max_cord
        self.direction = direction

    def update(self):
        if self.direction == "left" or self.direction == "right":
            if self.direction == "right":
                self.rect.x += self.speed
            elif self.direction == "left":
                self.rect.x -= self.speed

            if self.rect.right >= self.max_cord:
                self.direction = "left"
            if self.rect.left <= self.min_cord:
                self.direction = "right"

        elif self.direction == "up" or self.direction == "down":
            if self.direction == "up":
                self.rect.y -= self.speed
            elif self.direction == "down":
                self.rect.y += self.speed

            if self.rect.top <= self.min_cord:
                self.direction = "down"
            if self.rect.bottom >= self.max_cord:
                self.direction = "up" 


class Player(GameSprite):
    def __init__(self, x, y, width, height, img):
        super().__init__(x, y, width, height, img)
        self.speed_x = 0
        self.speed_y = 0
        self.direction = "left"
        self.image_l = self.image 
        self.image_r = pygame.transform.flip(self.image, True, False)

    def shot(self):
        if self.direction == "right":
            bullet = Bullet(self.rect.right, self.rect.centery, 5, 5, path_file("images\\vorozhiy_tank.png"), 10)
            bullets.add(bullet)
        elif self.direction == "left":
            bullet = Bullet(self.rect.left, self.rect.centery, 5, 5, path_file("images\\vorozhiy_tank.png"), -10)
            bullets.add(bullet)


    def update(self):
        global walls
        if self.rect.right < WIN_WIDTH and self.speed_x > 0 or self.rect.left > 0 and self.speed_x < 0:
            self.rect.x += self.speed_x
        walls_touched = pygame.sprite.spritecollide(self, walls, False)
        if self.speed_x > 0:
            for wall in walls_touched:
                self.rect.right = min(self.rect.right, wall.rect.left)
        if self.speed_x < 0:
            for wall in walls_touched:
                self.rect.left = max(self.rect.left, wall.rect.right)

        if self.rect.top > 0 and self.speed_y < 0 or self.rect.bottom < WIN_HEIGHT and self.speed_y > 0:
            self.rect.y += self.speed_y
        walls_touched = pygame.sprite.spritecollide(self, walls, False)
        if self.speed_y < 0:
            for wall in walls_touched:
                self.rect.top = max(self.rect.top, wall.rect.bottom)
        if self.speed_y > 0:
            for wall in walls_touched:
                self.rect.bottom = min(self.rect.bottom, wall.rect.top)

class Bullet(GameSprite):
    def __init__(self, x, y, width, height, img, speed):
        super().__init__(x, y, width, height, img)
        self.speed = speed
    def update(self):
        self.rect.x += self.speed
        if self.rect.left >= WIN_WIDTH or self.rect.right <= 0:
            self.kill()

bullets = pygame.sprite.Group()



player = Player(100, 100, 100, 50,path_file("images\\tank.png"))
enemys = pygame.sprite.Group()
enemy1 = Enemy(400, 300, 100, 50,path_file("images\\vorozhiy_tank.png"), 5, 100, 400, "right")
enemys.add(enemy1)
enemy2 = Enemy(600, 100, 80, 50, path_file("images\\vorozhiy_tank.png"), 4, 100, 500, "down")
enemys.add(enemy2)
enemy3 = Enemy(500, 150, 100, 50, path_file("images\\vorozhiy_tank.png"), 4, 100, 500, "down")
enemys.add(enemy3)
enemy4 = Enemy(430, 250, 100, 50, path_file("images\\vorozhiy_tank.png"), 4, 100, 500, "down")
enemys.add(enemy4)
enemy5 = Enemy(480, 0, 100, 50, path_file("images\\vorozhiy_tank.png"), 6, 0, 500, "down")
enemys.add(enemy5)
enemy6 = Enemy(400, 200, 100, 50, path_file("images\\vorozhiy_tank.png"), 7, 0, 350, "right")
enemys.add(enemy6)
gold = GameSprite(600, 280, 50, 50, path_file("images\\gold.png"))

walls = pygame.sprite.Group()
wall1 = GameSprite(350, 0, 30, 300, path_file("images\\stina.jpg"))
walls.add(wall1)
wall2 = GameSprite(0, 390, 350, 30, path_file("images\\stina.jpg"))
walls.add(wall2)

game = True
play = True
while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                player.direction = "right"
                player.image = player.image_r
                player.speed_x = 5
            if event.key == pygame.K_a:
                player.direction = "left"
                player.image = player.image_l
                player.speed_x = -5
            if event.key == pygame.K_w:
                player.speed_y = -5
            if event.key == pygame.K_s:
                player.speed_y = 5
            if event.key == pygame.K_SPACE :
                player.shot()
                music_shot.play()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                player.speed_x = 0
            if event.key == pygame.K_a:
                player.speed_x = 0
            if event.key == pygame.K_w:
                player.speed_y = 0
            if event.key == pygame.K_s:
                player.speed_y = 0

                



    if play == True:
        window.blit(background_image, (0, 0))
        player.reset()

        walls.draw(window)
        

        enemys.draw(window)
        enemys.update()

        gold.reset()
        player.update()

        bullets.draw(window)
        bullets.update()

        if pygame.sprite.collide_rect(player, gold):
            play = False
            pygame.mixer.music.stop()
            win_music.play()
            window.blit(win_image, (0, 0))

        if pygame.sprite.spritecollide(player, enemys, False):
            play = False
            pygame.mixer.music.stop()
            lose_music.play()
            window.blit(lose_image, (0, 0))


        pygame.sprite.groupcollide(bullets, walls, True, False)
        pygame.sprite.groupcollide(bullets, enemys, True, True)
        
    clock.tick(FPS)      
    pygame.display.update()


#!brrr ksibidid dop dop dop dop yes yes yes skib skibidi dip skibidi diop 
    