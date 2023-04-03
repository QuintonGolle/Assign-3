import pygame
from sys import exit

pygame.init()

screen = pygame.display.set_mode((800,400))

clock = pygame.time.Clock()

#gameplay variables
plr_lvl = 1
plr_dmg = plr_lvl
plr_health = 100
wave = 1
current_exp = 0
enemy_dmg = 5
enemy_health = 3
castle_health = 100
enemies_left = 1



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
            
    
            
    pygame.display.update()
    clock.tick(60)


#structure of game:

#set up player movement controller (left, right, jump)
#set up the attack animation (played on left mouse click)

#set wave, plr_lvl variable to 1 at the beginning of program
#show the current wave at the top left of the screen
#show "[LEVEL] Knight [HP]" above the characters head

#summon monsters on random platforms equal to the current wave + 2 (up for change)
#add 25 to player xp when an enemy is killed by the player
#the enemies deal 5 damage to the player, and 5 to the castle
#
#formula for calculating level
# current_exp = 200
# def experience(level):
# 
#     exp = 0
#     for i in range(1, level):
#         exp += (i + 300 * 2 ** (i / 7)) // 4
#     if current_exp >= exp:
#         level = level + 1
#     return int(level)
# current_lvl = experience(3)

#once there are no more enemies left in a single wave, begin the next wave
# continute this process until the player, or the castle has died
#quit the game

