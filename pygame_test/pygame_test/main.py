import pygame
from sys import exit
from random import randint


#starts up the program (sets up everything that needs to be set up behind the scenes)
pygame.init()
pygame.font.init()


screen_height = 400
screen_width = 672

#makes a new screen
screen = pygame.display.set_mode((screen_width,screen_height))


#initializes the clock function
clock = pygame.time.Clock()

#sets assets up
background = pygame.image.load("pygame_test/assets/background.png")
castle = pygame.image.load("pygame_test/assets/castle.png")
platform = pygame.image.load("pygame_test/assets/road.png")
player_sprites = [pygame.image.load("pygame_test/assets/player.png"),
          pygame.image.load("pygame_test/assets/player_att_1.png"),
          pygame.image.load("pygame_test/assets/player_att_2.png")]
player = player_sprites[0]
enemy_sprites = [pygame.image.load("pygame_test/assets/enemy.png"),
                 pygame.image.load("pygame_test/assets/en_att_anim_1.png"),
                 pygame.image.load("pygame_test/assets/en_att_anim_2.png")]
enemy = enemy_sprites[0]

lizard_death = pygame.mixer.Sound("pygame_test/assets/lizard_death.wav")
lizard_death.set_volume(0.3)
lizard_hurt = pygame.mixer.Sound("pygame_test/assets/lizard_hurt.mp3")
lizard_hurt.set_volume(0.3)
player_hurt = pygame.mixer.Sound("pygame_test/assets/player_hurt.wav")
player_hurt.set_volume(0.6)
background_music = pygame.mixer.music.load("pygame_test/assets/background.mp3")
pygame.mixer.music.play(-1,0.0)

blue = (0,0,128)
font = pygame.font.SysFont('freesansbold.ttf', 32)

#the entity positions initially
player_pos = [200, 376]
enemy_pos = [700, 376]

#variables initial values
plr_lvl = 1
plr_dmg = plr_lvl
plr_health = 100
wave = 1
current_exp = 0
enemy_dmg = 5
enemy_health = 3
castle_health = 100
enemies_left = 1
player_gravity = 0
plr_att_cd = 0
enemy_cd = 0
player_dir = "right"
enemy_dir = "left"
enemies_to_spawn = 3
new_wave = True
game_over = False
kill_enemy = False


def enemy_animate(enemy_cd, enemy):
    global plr_health
    if enemy_cd == 180:
        #add first animation frame
        enemy = enemy_sprites[1]
        
    if enemy_cd == 150:
        enemy = enemy_sprites[2]
        #add last animation frame
        if plr_collision.colliderect(enemy_collision):
            plr_health = plr_health - 20
            player_hurt.play()
            
        #check for damage
        
    if enemy_cd == 110:
        enemy = enemy_sprites[0]
        #reset character to idle animation
    # print(plr_health)
    return enemy

def player_animate(plr_att_cd, player):
    global enemy_health
    global kill_enemy
    if plr_att_cd == 59:
        #add first animation frame
        player = player_sprites[1]
        
    if plr_att_cd == 50:
        player = player_sprites[2]
        #add last animation frame
        if plr_collision.colliderect(enemy_collision):
           enemy_health = enemy_health - 1
           lizard_hurt.play()
           if enemy_health <= 0:
                enemy_pos[0] = 700
                enemy_health = 3
                lizard_death.play()
            
        #check for damage
        
    if plr_att_cd == 35:
        player = player_sprites[0]
        #reset character to idle animation
    # print(plr_health)
    return player

    
    
#main game loop
while True:
    if game_over == False:
        #runs every time an action is made in the game window
        for event in pygame.event.get():
            #checks if that action is trying to quit the game
            if event.type == pygame.QUIT:
                #quits the pygame instance and then kills the code with exit()
                pygame.quit()
                exit()
        
        
        #puts all the surfaces on the screen with variable positions, also linked to collisions
        screen.blit(background, (0,0))
        screen.blit(castle, (0,-15))
        
        #setup the ground and the collision for it
        screen.blit(platform, (190,376))
        platform_rect = platform.get_rect(topleft = (190,376))
        
        enemy_collision = enemy.get_rect(midbottom = (enemy_pos[0],enemy_pos[1]))
        screen.blit(enemy, enemy_collision)
        
        #set up the player and the collision for it
        plr_collision = player.get_rect(midbottom = (player_pos[0],player_pos[1]))
        screen.blit(player, plr_collision)
        
        
        #checks if the player has collided with the ground (true/false)
        onGround = plr_collision.colliderect(platform_rect)
        
        #makes an array of all the key presses
        keys = pygame.key.get_pressed()
        
        #moves the player left when they press A
        if keys[pygame.K_a] and player_pos[0] > 197:
            player_pos[0] -= 3
            if player_dir == "right":
                player = pygame.transform.flip(player, True, False)
                player_dir = "left"
        
        #moves the player right when they press D
        if keys[pygame.K_d] and player_pos[0] < 668:
            player_pos[0] += 3
            if player_dir == "left":
                player = pygame.transform.flip(player, True, False)
                player_dir = "right"
        
        #makes the player jump when they press space as long as they are on the ground
        if keys[pygame.K_SPACE] and onGround == True:
            #makes the gravity negative so it moves the player up in a jumping fashion
            player_gravity = -13
            player_pos[1] += player_gravity
        
        #moves the player down at an amount that increases the longer they are in the air, only if they are not on the ground
        if onGround == False:
            player_gravity += 1
            player_pos[1] += player_gravity
        
        #does the attack process if the right control key is pressed and the attack isnt on cooldown
        if keys[pygame.K_RCTRL] and plr_att_cd == 0:
            slash = pygame.mixer.Sound("pygame_test/assets/slash.ogg")
            slash.set_volume(0.3)
            slash.play()        
            #sets the cooldown to 1 second
            plr_att_cd = 60
            
            
        
        #lowers the attack cooldown every frame (60 times a second)
        if plr_att_cd > 0:
            player = player_animate(plr_att_cd, player)
            plr_att_cd -= 1
            
        
        #calculates the distance from the player to the enemy
        x_diff = enemy_pos[0] - player_pos[0]
        y_diff = enemy_pos[1] - player_pos[1]
        
        #checkis if a player is far away, if they are then walk to the castle
        if (x_diff > 40 or x_diff < -40) and (y_diff < 10 or y_diff > -10):
            enemy_pos[0] -= 2
            #changes the direction of the enemy image to correspond with movement direction
            if enemy_dir == "right":
                enemy = pygame.transform.flip(enemy, True, False)
                enemy_dir = "left"
        #if they are close, and in the negative direction, then walk in the negative direction
        elif x_diff > 20:
            enemy_pos[0] -= 2
            if enemy_dir == "right":
                enemy = pygame.transform.flip(enemy, True, False)
                enemy_dir = "left"
        #if they are close, and in the positive direction, then walk in the positive direction
        elif x_diff < -20:
            enemy_pos[0] += 2
            if enemy_dir == "left":
                enemy = pygame.transform.flip(enemy, True, False)
                enemy_dir = "right"
        
        
        
        if enemy_cd == 0 and ((x_diff > 15 and x_diff < 40)  or (x_diff < -15 and x_diff > -40)):
            enemy_cd = 180
        
        # print(plr_att_cd)
        #print(near)
        # print(enemy_health)
            
        if enemy_cd > 0:
            enemy = enemy_animate(enemy_cd, enemy)
            enemy_cd -= 1
            if plr_health <= 0:
                game_over = True
                
        if enemy_pos[0] < 197:
            castle_health = castle_health - 10
            enemy_pos[0] = 700
        
        print(castle_health)
    else:
        text = font.render('Game Over', False, (0, 0, 0))
        screen.blit(text, (360, 200))

        

    #updates the display
    pygame.display.update()
    #utilizes the clock function to make sure the while loop only runs 60 times a second (60fps)
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