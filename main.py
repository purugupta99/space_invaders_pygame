#!/usr/bin/python

import pygame
import sys
import random
from time import sleep
from pygame.locals import *
from spaceship import *
from alien import *
from missile import *

display_height = 480
display_width = 640

pygame.init()

clock = pygame.time.Clock()
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Space Invaders')

black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 150)
red = (150, 0, 0)
green = (0, 150, 0)
bright_green = (255, 0, 0)
bright_red = (255, 0, 0)
bright_blue = (0, 0, 255)

myfont = pygame.font.SysFont('Jokerman', 30)
largeText = pygame.font.SysFont('Comic Sans MS', 115)
mediumText = pygame.font.SysFont('Times', 30)
smallText = pygame.font.SysFont('Times', 20)
decorateText = pygame.font.SysFont('Jokerman', 40)
background = pygame.image.load("space.jpg")

ship = Spaceship(display_width/16-30, display_height-30, myfont, black)
ship_width = ship.getWidth()
ship_height = ship.getHeight()

pause = False

x_cord = []
y_cord = []
aliens = []
missile = []
for i in range(int(display_width/16-20), display_width, 80):
    x_cord.append(i)

for i in range(int(display_height/16-10), int(display_width/6), 60):
    y_cord.append(i+30)

possible_cord = set()
for i in x_cord:
    for j in y_cord:
        possible_cord.add((i, j))

start_time = pygame.time.get_ticks()
rand = random.sample((possible_cord), 1)

aliens.append(Alien(rand[0][0], rand[0][1], myfont, black, start_time))
enemy_height = aliens[0].getHeight()
enemy_width = aliens[0].getWidth()


def scoreDisplay(score):
    score_font = pygame.font.SysFont("Helvetica", 30, "bold")
    score_surface = score_font.render("SCORE:"+str(score), False, (255, 0, 0))
    gameDisplay.blit(score_surface, (display_width /
                                     2-score_surface.get_width()/2, 5))


def exitPython():
    pygame.quit()
    quit()


def button(msg, x, y, width, height, style, col_inac,
           col_ac, action=None, arg=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    global pause
    if action == hold:
        pause = True
    if x < mouse[0] < x+width and y < mouse[1] < y+height:
        pygame.draw.rect(gameDisplay, col_ac, (x, y, width, height), 0)
        if click[0] == 1 and action is not None and arg is not None:
            action(arg)
        elif click[0] == 1 and action is not None and arg is None:
            action()

    else:
        pygame.draw.rect(gameDisplay, col_inac, (x, y, width, height), 0)

    msg_surface = style.render(msg, True, white)
    msg_h = msg_surface.get_height()
    msg_w = msg_surface.get_width()
    gameDisplay.blit(msg_surface, (x+width/2-msg_w/2, y+height/2-msg_h/2))


def unpause():
    global pause
    pause = False


def hold():
    before_bullet = pygame.time.get_ticks()
    before_taser = pygame.time.get_ticks()
    decorate = []
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gameDisplay.fill(white)
        screen = largeText.render('PAUSED', True, black)
        gameDisplay.blit(screen, (display_width/2-screen.get_width() /
                                  2, display_height/3-screen.get_height()/2))
        height_rect = 50
        width_rect = 150

        after = pygame.time.get_ticks()
        if (after-before_taser >= 500):
            before_taser = after
            decorate.append(Taser(random.choice(x_cord),
                                  display_height, decorateText, black, -0.8))

        if (after-before_bullet >= 1000):
            before_bullet = after
            decorate.append(Bullet(random.choice(x_cord),
                                   display_height, decorateText, black, -0.4))

        for ammo in decorate:
            if ammo.y_pos <= 0:
                decorate.remove(ammo)
            ammo.moveUp()
            ammo.draw(gameDisplay)

        button("CONTINUE", display_width/2-width_rect/2, display_height/2,
               width_rect, height_rect, smallText, blue,
               bright_blue, unpause)
        button("QUIT", display_width/2-width_rect/2, display_height/2 +
               height_rect + 20, width_rect, height_rect, mediumText,
               red, bright_red, exitPython)

        pygame.display.flip()


def gameIntro():
    before_bullet = pygame.time.get_ticks()
    before_taser = pygame.time.get_ticks()
    intro = True
    decorate = []
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == K_q:
                    exitPython()

        gameDisplay.fill(white)
        gameName = largeText.render('Space Invaders', True, black)
        gameDisplay.blit(gameName, (display_width/2-gameName.get_width() /
                                    2, display_height/3 -
                                    gameName.get_height() / 2))
        height_rect = 50
        width_rect = 150

        after = pygame.time.get_ticks()
        if (after-before_taser >= 500):
            before_taser = after
            decorate.append(Taser(random.choice(x_cord),
                                  display_height, decorateText, black, -0.8))

        if (after-before_bullet >= 1000):
            before_bullet = after
            decorate.append(Bullet(random.choice(x_cord),
                                   display_height, decorateText, black, -0.4))

        for ammo in decorate:
            if ammo.y_pos <= 0:
                decorate.remove(ammo)
            ammo.moveUp()
            ammo.draw(gameDisplay)

        button("START", display_width/2-width_rect/2, display_height/2,
               width_rect, height_rect, mediumText, blue, bright_blue,
               game_loop, start_time)

        button("STOP", display_width/2-width_rect/2, display_height/2 +
               height_rect + 20, width_rect, height_rect,
               mediumText, red, bright_red, exitPython)

        pygame.display.flip()


def game_loop(start_time):
    gameExit = False
    score = 0
    while not gameExit:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True

            if event.type == pygame.KEYDOWN:
                if event.key == K_q:
                    gameExit = True

                if event.key == K_p:
                    global pause
                    pause = True
                    hold()

                if event.key == K_SPACE:
                    missile.append(Bullet(ship.x_pos+ship_width/2+2,
                                          ship.y_pos - ship_height -
                                          display_height/60, myfont,
                                          black, -display_height/40))

                if event.key == K_s:
                    missile.append(Taser(ship.x_pos+ship_width/2+2,
                                         ship.y_pos - ship_height -
                                         display_height/60, myfont,
                                         black, -display_height/20))

                x_lim_l = display_width/16 - ship_width/2
                x_lim_r = display_width - (display_width/8+ship_width+1)/2
                if event.key == K_a or event.key == K_LEFT:
                    if ship.x_pos > x_lim_l:
                        ship.moveLeft()

                if event.key == K_d or event.key == K_RIGHT:
                    if ship.x_pos < x_lim_r:
                        ship.moveRight()

        current_time = pygame.time.get_ticks()

        gameDisplay.fill(white)
        gameDisplay.blit(background, (0, 0))
        button('||', display_width*7/8-40, 7, 30, 30,
               mediumText, green, bright_green, hold)

        button('Q', display_width*7/8, 7, 30, 30,
               mediumText, green, bright_green, exitPython)
        ship.draw(gameDisplay)

        for enemy in aliens:
            enemy.draw(gameDisplay)
            if current_time - enemy.spawn_time >= 8000:
                aliens.remove(enemy)
                if enemy.tag:
                    score += 1

        for ammo in missile:
            if(ammo.y_pos <= 0):
                missile.remove(ammo)
            ammo.moveUp()
            ammo.draw(gameDisplay)
            for enemy in aliens:
                if ammo.hit(enemy.x_pos, enemy.y_pos +
                            enemy_height, enemy_width):
                    if ammo.type == 'bullet':
                        missile.remove(ammo)
                        aliens.remove(enemy)
                        score += 1
                    if ammo.type == 'taser' and not enemy.tag:
                        missile.remove(ammo)
                        enemy.x_pos += 5
                        enemy.spawn_time = 3000+current_time
                        enemy.tagged()

        scoreDisplay(score)
        pygame.display.flip()
        finish_time = pygame.time.get_ticks()
        if(finish_time-start_time >= 10000):
            start_time = finish_time

            used = set()
            for enemy in aliens:
                used.add((enemy.x_pos, enemy.y_pos))
            used = possible_cord-used
            rand_new = random.sample((used), 1)
            aliens.append(
                Alien(rand_new[0][0], rand_new[0][1],
                      myfont, black, start_time))


gameIntro()
game_loop(start_time)
pygame.quit()
quit()
