import pygame
import random

from dino_runner.components.obstacles.bird import Bird
from dino_runner.components.obstacles.cactus import Cactus
from dino_runner.utils.constants import HAMMER_TYPE, SHIELD_TYPE


class ObstacleManager:
    def __init__(self):
        self.obstacles = []

    def update(self, game):
        if len(self.obstacles) == 0:
            self.obstacle_type_list = [Bird(), Cactus()]
            self.obstacles.append(random.choice(self.obstacle_type_list))
        
        for obstacle in self.obstacles:
            obstacle.update(game.game_speed, self.obstacles) 
            if  game.player.type == HAMMER_TYPE: 
                    game.player.dino_jump = False
                    game.player.dino_duck = True 
                    game.player.dino_rect.y += 100
                

            if game.player.dino_rect.colliderect(obstacle.rect):
                if game.player.type == SHIELD_TYPE:
                   self.obstacles.remove(obstacle)
                else: 
                    pygame.time.delay(250)
                    game.playing = False
                    game.death_count += 1 
                    break

    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen) 

    def reset_obstacles(self):
        self.obstacles = []