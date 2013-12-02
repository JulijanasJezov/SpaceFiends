#!/usr/bin/env python
#References for sprites: http://kryptid.deviantart.com/art/Spaceship-Sprite-Package-117026929
#http://www.freewebs.com/leaderslash/sprites.htm
#Reference for background: http://loadpaper.com/id27914/space-twitter-background-backgrounds-twitterevolutions-1920x1024-pixel.html

import sys, glob
import pygame
import random
from pygame.locals import *
from pygame.sprite import Sprite

WIDTH = 640
HEIGHT = 480
FPS = 30

class Enemy(Sprite):
        def __init__(self, position):
                Sprite.__init__(self)
                self.image = pygame.image.load("enemy.png")
                self.rect = self.image.get_rect()
                self.rect.left = position
                self.velocity = 5
                
        def update(self):
                self.rect.move_ip(self.velocity, 0)
                if self.rect.right > WIDTH:
                        self.velocity = -5
                        self.rect.top += 50
                elif self.rect.left < 0:
                        self.velocity = 5
                        self.rect.top += 50
               
class Enemy_attack(Sprite):
        def __init__(self):
                Sprite.__init__(self)
                self.image = pygame.image.load("enbullet.png")
                self.rect = self.image.get_rect()
                self.velocity = 0
                
        def update(self):
                self.rect.move_ip(0, 10)
                if self.rect.bottom > HEIGHT + 20:
                        self.kill()

class Asteroid(Sprite):
        def __init__(self):
                Sprite.__init__(self)
                self.image = pygame.image.load("asteroid.png")
                self.rect = self.image.get_rect()                
                self.rect.left = 0
                self.velocity = [0, 0]
                
        def update(self):
                self.rect.move_ip(self.velocity[0], self.velocity[1])
                if self.rect.bottom > HEIGHT + 100:
                        self.kill()
        

class Spaceship(Sprite):
        def __init__(self):
                Sprite.__init__(self)
                self.x = 300
                self.y = 450
                self.image = pygame.image.load("spaceship.png")
                self.rect = self.image.get_rect()
                self.rect.center = (self.x, self.y)
                self.velocity = 0

        def left(self):
                self.velocity -= WIDTH/48
                

        def right(self):
                self.velocity += WIDTH/48
		
        def update(self):
                self.rect.move_ip(self.velocity, 0)
                # move only within the screen border
                self.rect.left = max(0, self.rect.left)
                self.rect.right = min(WIDTH, self.rect.right)
                #print self.rect
                
class Bullet(Sprite):
        def __init__(self):
                Sprite.__init__(self)
                self.image = pygame.image.load("bullet.png")
                self.rect = self.image.get_rect()
                self.rect.center = Spaceship().rect.center
                self.velocity = 0

        def shoot(self):
                self.velocity = 0
                self.velocity -= 10

        def update(self):
                self.rect.move_ip(0, self.velocity)
                if self.rect.top < 0:
                        self.kill()
                
class GameOver(Sprite):
        def __init__(self):
                Sprite.__init__(self)
                self.font = pygame.font.Font(None, 50)
                self.image = self.font.render("GAME OVER!", True, (255,200,0))
                self.rect = self.image.get_rect()
                self.rect.move_ip(200, 200)

class Score(Sprite):
        def __init__(self, time):
                Sprite.__init__(self)
                self.font = pygame.font.Font(None, 50)
                score = pygame.time.get_ticks() - time
                score = 50000 - score
                self.image = self.font.render("Your Score is {0}".format(score), True, (255,200,0))
                self.rect = self.image.get_rect()
                self.rect.move_ip(150, 200)
                

def main():
        pygame.init()
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        time = pygame.time.get_ticks()
        ast_attack = pygame.time.get_ticks()
        ast_attack += 2000
        position = 0
        encount = 0
 
        #create sprites
        bullet = Bullet()
        asteroid = Asteroid()
        enbullet = {}
        game_over = GameOver()
        bul_count_s = 0
        bul_count = 0
        player = Spaceship()
        enemy = {}
        for x in range (0, 10):
                position += 40
                enemy[x] = Enemy(position)

        #list of sprites to render
        sprites = pygame.sprite.RenderClear([player])
        enattacks = pygame.sprite.RenderClear()
        for x in range (0, 10):
                enemy[x].add(sprites)
                
        #load and draw background
        background = pygame.image.load("startbg.jpg")
        screen.blit(background, (0, 0))
        pygame.display.flip()

        #add bullet sprite
        def addBullet():
                if bullet.alive() == False:
                        bullet.add(sprites)
                        bullet.rect.center = player.rect.center
        start = True
        running = False
        scoreTime = 0

        #start screen
        while start:
                pygame.display.flip()
                for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN and event.key == K_RETURN:
                                start = False
                                scoreTime = pygame.time.get_ticks()
                                background = pygame.image.load("spacebck.jpg")
                                screen.blit(background, (0, 0))
                                ast_attack = pygame.time.get_ticks() + 2000
                                time = pygame.time.get_ticks() + 500
                                running = True

        #end screen
        def restart():
                background = pygame.image.load("gameend.jpg")
                screen.blit(background, (0, 0))
                sprites.update()
                sprites.draw(screen)
                running = False
                while True:
                        pygame.display.flip()
                        for event in pygame.event.get():
                                if event.type == pygame.KEYDOWN and event.key == K_RETURN:
                                        main()
        
        #controls
        key_map = {
		pygame.K_LEFT: [player.left, player.right],
		pygame.K_RIGHT: [player.right, player.left],
                pygame.K_SPACE: [addBullet, bullet.shoot]
	}
       
        while running:
                #set and display FPS
                clock.tick(FPS)
                pygame.display.set_caption("SPACE - {0:.2f} fps".format(clock.get_fps()))

                #animate sprites
                sprites.update()
                sprites.draw(screen)

		#display screen
                pygame.display.flip()

		#draw background over sprites
                sprites.clear(screen, background)

		#read events from the event queue
                for event in pygame.event.get():
			#on QUIT event, exit the main loop
                        if event.type == pygame.QUIT:
                                running = False
			#on key press
                        elif event.type == pygame.KEYDOWN and event.key in key_map:
                                key_map[event.key][0]()
			#on key release
                        elif event.type == pygame.KEYUP and event.key in key_map:
                                key_map[event.key][1]()

                #collisions
                for x in range (0, 9):
                        if pygame.sprite.collide_rect(enemy[x], player) == True:
                                player.kill()
                        

                for x in range (0, 10):
                        if pygame.sprite.collide_rect(enemy[x], bullet) == True and enemy[x].alive() == True:
                                enemy[x].kill()
                                bullet.kill()
                                bullet.rect.center = player.rect.center
                                encount += 1

                #controlling enemy attacks            
                if pygame.time.get_ticks() - time > 0:
                        rand_enemy = random.randint(0, 9)
                        if enemy[rand_enemy].alive() == True:
                                enbullet[bul_count] = Enemy_attack()
                                enbullet[bul_count].add(sprites)
                                enbullet[bul_count].rect.center = enemy[rand_enemy].rect.center
                                bul_count += 1
                                
                        time += 500
                for x in range (bul_count_s, bul_count):
                        if enbullet[x].rect.colliderect(player.rect):
                               player.kill()
                        
                if pygame.time.get_ticks() - ast_attack > 0:
                        hor_vel = random.randint(-5, 5)
                        vert_vel = random.randint(5, 10)
                        pos = random.randint(-100, 700)
                        asteroid.rect.left = pos
                        asteroid.rect.top = -50
                        asteroid.velocity = [hor_vel, vert_vel]
                        asteroid.add(sprites)
                        ast_attack += 2500
                        bul_count_s += 1

                if asteroid.rect.colliderect(player.rect):
                        player.kill()

                #game over/score         
                if player.alive() == False:
                        player.kill()
                        for x in range (0, 10):
                                enemy[x].kill()
                        sprites.remove(sprites)
                        sprites.add(game_over)
                        restart()
                elif encount == 10:
                        score = Score(scoreTime)
                        sprites.remove(sprites)
                        sprites.add(score)
                        restart()
                        
if __name__ == "__main__":
        main()
