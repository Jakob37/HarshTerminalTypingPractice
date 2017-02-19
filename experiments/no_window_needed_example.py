#!/usr/bin/env python3

import os
import sys
os.environ["SDL_VIDEODRIVER"] = 'dummy'

import pygame

if 1:
    import pygame.display
    pygame.display.init()
    screen = pygame.display.set_mode((1,1))


while True:
    # pygame.clock.tick(50)

    state = pygame.key.get_pressed()
    hits = [c for c in state if c != 0]
    if len(hits) > 0:
        print(hits)

    for event in pygame.event.get():

        print('eval')

        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            print('key pressed!')



