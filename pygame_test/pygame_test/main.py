import pygame
from sys import exit
from random import randint


#starts up the program (sets up everything that needs to be set up behind the scenes)
pygame.init()
pygame.font.init()

#variables for screen size
screen_height = 400
screen_width = 672

#makes a new screen
screen = pygame.display.set_mode((screen_width,screen_height))


#initializes the clock function
clock = pygame.time.Clock()

#sets assets up (gives every image a variable)
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

#sets up all the sound, sets volume and gives each sound a variable
lizard_death = pygame.mixer.Sound("pygame_test/assets/lizard_death.wav")
lizard_death.set_volume(0.3)
lizard_hurt = pygame.mixer.Sound("pygame_test/assets/lizard_hurt.mp3")
lizard_hurt.set_volume(0.3)
player_hurt = pygame.mixer.Sound("pygame_test/assets/player_hurt.wav")
player_hurt.set_volume(0.6)
background_music = pygame.mixer.music.load("pygame_test/assets/background.mp3")
pygame.mixer.music.play(-1,0.0)

#chooses font size, font and color
blue = (0,0,128)
font = pygame.font.SysFont('freesansbold.ttf', 32)
diff_font = pygame.font.SysFont('freesansbold.ttf', 18)

#a function to animate the enemy attack based on the cooldown of the attack
def enemy_animate(enemy_cd, enemy):
    global plr_health
    if enemy_cd == 180:
        #add first animation frame
        enemy = enemy_sprites[1]
        
    if enemy_cd == 150:
        enemy = enemy_sprites[2]
        #add last animation frame, all effects happen if collision between the enemy and player happen in this frame (damage to player, sound effects)
        if plr_collision.colliderect(enemy_collision):
            plr_health = plr_health - 20
            player_hurt.play()
        
    if enemy_cd == 110:
        enemy = enemy_sprites[0]
        #reset character to idle animation
    return enemy

#function that animated player attack based on the player attack cooldown
def player_animate(plr_att_cd, player):
    global enemy_health
    global kill_enemy
    global score
    if plr_att_cd == 59:
        #add first animation frame
        player = player_sprites[1]
        
    if plr_att_cd == 50:
        player = player_sprites[2]
        #add last animation frame, checks for collision between player and enemy
        if plr_collision.colliderect(enemy_collision):
           #if collided, subract from enemy health, play hurt sound
           enemy_health = enemy_health - 1
           lizard_hurt.play()
           #if the enemy dies, reset them to their origional position off screen, reset health and add to player score
           if enemy_health <= 0:
                enemy_pos[0] = 700
                enemy_health = 3
                lizard_death.play()
                score = score + 1 
        
    if plr_att_cd == 35:
        player = player_sprites[0]
        #reset character to idle animation
    return player

#shows the controls on screen for 3 seconds before the game starts
for i in range(180):
    
    titlescreen_1  = font.render('A = Left', True,(255,255,255))
    screen.blit(titlescreen_1, (0,0))
    titlescreen_2  = font.render('D = Right', True,(255,255,255))
    screen.blit(titlescreen_2, (0,20))
    titlescreen_3  = font.render('Space = Jump', True,(255,255,255))
    screen.blit(titlescreen_3, (0,40))
    titlescreen_4  = font.render('Right ctrl = Player Attack', True,(255,255,255))
    screen.blit(titlescreen_4, (0,60))

    pygame.display.update()
    clock.tick(60)
   

#while loop to reset game    
while True:    
    #variables initial values
    game_over = False
    plr_lvl = 1
    plr_dmg = plr_lvl
    plr_health = 100
    score = 0
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

    #the entity positions initially
    player_pos = [200, 376]
    enemy_pos = [700, 376]
    #the main game while loop      
    while True:
        #checks if the game has ended or not
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
            #if the player is within a certain range, set the cooldown to 180 which will start the attack function
            if enemy_cd == 0 and ((x_diff > 15 and x_diff < 40)  or (x_diff < -15 and x_diff > -40)):
                enemy_cd = 180
            #check if enemy has detected the time to attack    
            if enemy_cd > 0:
                enemy = enemy_animate(enemy_cd, enemy)
                enemy_cd -= 1
                #if enemy has attacked and player health is 0 or below, end the game (put game over on the screen for 5 seconds, set game over to true)    
                if plr_health <= 0:
                    for i in range(300):
                        t_seconds = i / 60
                        text = font.render('Game Over', False, (0, 0, 0))
                        timer = font.render('Restarting...' , False, (0, 0, 0))
                        screen.blit(text, (360, 200))
                        screen.blit(timer, (360, 220))
                        game_over = True
                        #updates the display
                        pygame.display.update()
                        #utilizes the clock function to make sure the while loop only runs 60 times a second (60fps)
                        clock.tick(60)
            #check if enemy has reached the castle, if it has, subract from castle health        
            if enemy_pos[0] < 197:
                castle_health = castle_health - 10
                if castle_health <= 0:
                    for i in range(300):
                        t_seconds = i / 60
                        text = font.render('Game Over', False, (0, 0, 0))
                        timer = font.render('Restarting...' , False, (0, 0, 0))
                        screen.blit(text, (360, 200))
                        screen.blit(timer, (360, 220))
                        game_over = True
                        #updates the display
                        pygame.display.update()
                        #utilizes the clock function to make sure the while loop only runs 60 times a second (60fps)
                        clock.tick(60)
                enemy_pos[0] = 700
        # if game over is not false, break out of the main game loop and reset the game        
        else:
            break    
        #display player health, castle health, and game score on screen
        health = font.render('Castle health '+ str(castle_health), True, (0, 0, 0))
        screen.blit(health, (0,0))

        player_health = diff_font.render('health: '+str(plr_health),True,(0,0,0) )
        screen.blit(player_health, (player_pos[0]-25,player_pos[1]- 25))

        game_score = font.render('score: ' +str(score), True,(0,0,0))
        screen.blit(game_score, (500,0))


        #updates the display
        pygame.display.update()
        #utilizes the clock function to make sure the while loop only runs 60 times a second (60fps)
        clock.tick(60)
