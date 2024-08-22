import pygame
import random
import spritesheet
import button

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 1680, 945
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2D Runner Game")

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Buttons
button_resume = button.Button(82, SCREEN_HEIGHT/2+200, (pygame.image.load('sprites/buttons/button_resume.png').convert_alpha()), 1)
# Her
button_F = button.Button(SCREEN_WIDTH/2-608, SCREEN_HEIGHT/2-82, (pygame.image.load('sprites/buttons/button_F.png').convert_alpha()), 1)
ela = button.Button(SCREEN_WIDTH/2-608, SCREEN_HEIGHT/2-226, (pygame.image.load('sprites/buttons/ela.png').convert_alpha()), 1)
# Him
button_M = button.Button(SCREEN_WIDTH/2-203, SCREEN_HEIGHT/2-82, (pygame.image.load('sprites/buttons/button_M.png').convert_alpha()), 1)
ele = button.Button(SCREEN_WIDTH/2-203, SCREEN_HEIGHT/2-226, (pygame.image.load('sprites/buttons/ele.png').convert_alpha()), 1)
# Them
button_NB = button.Button(SCREEN_WIDTH/2+202, SCREEN_HEIGHT/2-82, (pygame.image.load('sprites/buttons/button_NB.png').convert_alpha()), 1)
elu = button.Button(SCREEN_WIDTH/2+202, SCREEN_HEIGHT/2-226, (pygame.image.load('sprites/buttons/elu.png').convert_alpha()), 1)

# Player
player_size = 120
player_speed = 10
gender = ''
lives_initial = 3
lives = lives_initial
colliding = False
lanes = [SCREEN_WIDTH // 4, SCREEN_WIDTH // 2, (3 * SCREEN_WIDTH) // 4]
current_lane = 1  # Start in the middle lane
target_lane = current_lane
player_pos = [lanes[current_lane] - player_size // 2, SCREEN_HEIGHT - 2 * player_size]

# Player sprites
#base_player_sprites_running = spritesheet.SpriteSheet(pygame.image.load('sprites/player/base/sprite_sheet_base.png').convert_alpha())
#base_player_sprites_right = spritesheet.SpriteSheet(pygame.image.load('sprites/player/base/sprite_sheet_base_diagonal_R.png').convert_alpha())
#base_player_sprites_left = spritesheet.SpriteSheet(pygame.image.load('sprites/player/base/sprite_sheet_base_diagonal_L.png').convert_alpha())
#base_player_sprites_jumping = spritesheet.SpriteSheet(pygame.image.load('sprites/player/base/sprite_sheet_base_jumping.png').convert_alpha())
# Her
F_player_sprites_running = spritesheet.SpriteSheet(pygame.image.load('sprites/player/Fem/sprite_sheet_alex_F.png').convert_alpha())
F_player_sprites_right = spritesheet.SpriteSheet(pygame.image.load('sprites/player/Fem/sprite_sheet_alex_F_diagonal_R.png').convert_alpha())
F_player_sprites_left = spritesheet.SpriteSheet(pygame.image.load('sprites/player/Fem/sprite_sheet_alex_F_diagonal_L.png').convert_alpha())
F_player_sprites_jumping = spritesheet.SpriteSheet(pygame.image.load('sprites/player/Fem/sprite_sheet_alex_F_jumping.png').convert_alpha())
# Him
M_player_sprites_running = spritesheet.SpriteSheet(pygame.image.load('sprites/player/Masc/sprite_sheet_Alex_M.png').convert_alpha())
M_player_sprites_right = spritesheet.SpriteSheet(pygame.image.load('sprites/player/Masc/sprite_sheet_alex_M_diagonal_R.png').convert_alpha())
M_player_sprites_left = spritesheet.SpriteSheet(pygame.image.load('sprites/player/Masc/sprite_sheet_alex_M_diagonal_L.png').convert_alpha())
M_player_sprites_jumping = spritesheet.SpriteSheet(pygame.image.load('sprites/player/Masc/sprite_sheet_alex_M_jumping.png').convert_alpha())
# Them
NB_player_sprites_running = spritesheet.SpriteSheet(pygame.image.load('sprites/player/NB/sprite_sheet_alex_NB.png').convert_alpha())
NB_player_sprites_right = spritesheet.SpriteSheet(pygame.image.load('sprites/player/NB/sprite_sheet_alex_NB_diagonal_R.png').convert_alpha())
NB_player_sprites_left = spritesheet.SpriteSheet(pygame.image.load('sprites/player/NB/sprite_sheet_alex_NB_diagonal_L.png').convert_alpha())
NB_player_sprites_jumping = spritesheet.SpriteSheet(pygame.image.load('sprites/player/NB/sprite_sheet_alex_NB_jumping.png').convert_alpha())

# Player animation
player_animation_running = []
player_animation_right = []
player_animation_left = []
player_animation_jumping = []
PLAYER_ANIMATION_STEPS = 6
PLAYER_ANIMATION_SPEED = 100  # milliseconds
player_animation_current_frame = 0
player_current_animation = player_animation_running

# Sheets and animation
# Cyclist
obstacle_sprites_cyclist = spritesheet.SpriteSheet(pygame.image.load('sprites/NPCs/obstacle/sheet_obstacle_bicycle.png').convert_alpha())
npc_animation_cyclist = []
# Dog
obstacle_sprites_dog = spritesheet.SpriteSheet(pygame.image.load('sprites/NPCs/obstacle/sheet_obstacle_dog.png').convert_alpha())
npc_animation_dog = []

for x in range(PLAYER_ANIMATION_STEPS):
    npc_animation_cyclist.append(obstacle_sprites_cyclist.get_image(x, 60, 60, 4, BLACK))
    npc_animation_dog.append(obstacle_sprites_dog.get_image(x, 60, 60, 4, BLACK))

# Obstacles
obstacle_dog_speed = 7
obstacle_cyclist_speed = 10

# Background Image
background_image_temp = spritesheet.SpriteSheet(pygame.image.load('sprites/background/background.png').convert_alpha())
BACKGROUND = background_image_temp.get_image(0, 4200, 108000, 0.4, BLACK)
bg_y = 0
bg_speed = 4

# Using sprite groups for better performance
class ObstacleDog(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = npc_animation_dog[player_animation_current_frame]
        self.rect = self.image.get_rect(center=(x, y))
        self.collision_rect = self.rect.inflate(-self.rect.width // 1.25, -self.rect.height // 1.75)  # Smaller collision rectangle

    def update(self):
        self.image = npc_animation_dog[player_animation_current_frame]
        self.rect.y += obstacle_dog_speed
        self.collision_rect.midbottom = self.rect.midbottom  # Keep the collision rect at the bottom center of the sprite
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

class ObstacleCyclist(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = npc_animation_cyclist[player_animation_current_frame]
        self.rect = self.image.get_rect(center=(x, y))
        self.collision_rect = self.rect.inflate(-self.rect.width // 1.25, -self.rect.height // 1.75)  # Smaller collision rectangle

    def update(self):
        self.image = npc_animation_cyclist[player_animation_current_frame]
        self.rect.y += obstacle_cyclist_speed
        self.collision_rect.midbottom = self.rect.midbottom  # Keep the collision rect at the bottom center of the sprite
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

obstacles = pygame.sprite.Group()

def create_obstacle():
    cyclists = [o for o in obstacles if isinstance(o, ObstacleCyclist)]
    dogs = [o for o in obstacles if isinstance(o, ObstacleDog)]
    if len(cyclists) < 2:
        shuffled_lanes = lanes[:]
        random.shuffle(shuffled_lanes)  # Randomize the order of lanes to check
        for lane in shuffled_lanes:
            if any(cyclist.rect.centerx == lane for cyclist in cyclists):
                continue
            if len(cyclists) == 1:
                if lane == lanes[0] and cyclists[0].rect.centerx == lanes[1]:
                    continue
                if lane == lanes[2] and cyclists[0].rect.centerx == lanes[1]:
                    continue
                if lane == lanes[1] and cyclists[0].rect.centerx in [lanes[0], lanes[2]]:
                    continue
            if not any(dog.rect.centerx == lane for dog in dogs):
                y_pos = 0
                obstacle = ObstacleCyclist(lane, y_pos)
                obstacles.add(obstacle)
                return

    shuffled_lanes = lanes[:]
    random.shuffle(shuffled_lanes)  # Randomize the order of lanes to check
    for lane in shuffled_lanes:
        if not any(isinstance(obstacle, ObstacleDog) and obstacle.rect.centerx == lane for obstacle in obstacles):
            y_pos = 0
            obstacle = ObstacleDog(lane, y_pos)
            obstacles.add(obstacle)
            break

def detect_collision(player_rect, obstacle_list):
    for obstacle in obstacle_list:
        if player_rect.colliderect(obstacle.collision_rect):
            return obstacle
    return None

# Background scrolling function
def scroll_background():
    global bg_y
    bg_y += bg_speed
    screen.blit(BACKGROUND, (0, bg_y))
    screen.blit(BACKGROUND, (0, bg_y - 43200))

def menu():
    screen.fill(BLACK)
    button_F.draw(screen)
    ela.draw(screen)
    button_M.draw(screen)
    ele.draw(screen)
    button_NB.draw(screen)
    elu.draw(screen)
    pygame.display.flip()

# Function partially done by hand since GPT refuses to properly work.
def gender_selection():
    global player_animation_running, player_animation_right, player_animation_left, player_animation_jumping, gender
    if button_F.clicked:
        for x in range(PLAYER_ANIMATION_STEPS):
            player_animation_running.append(F_player_sprites_running.get_image(x, 60, 60, 4, BLACK))
            player_animation_right.append(F_player_sprites_right.get_image(x, 60, 60, 4, BLACK))
            player_animation_left.append(F_player_sprites_left.get_image(x, 60, 60, 4, BLACK))
            player_animation_jumping.append(F_player_sprites_jumping.get_image(x, 60, 60, 4, BLACK))
        gender = 'F'
    elif button_M.clicked:
        for x in range(PLAYER_ANIMATION_STEPS):
            player_animation_running.append(M_player_sprites_running.get_image(x, 60, 60, 4, BLACK))
            player_animation_right.append(M_player_sprites_right.get_image(x, 60, 60, 4, BLACK))
            player_animation_left.append(M_player_sprites_left.get_image(x, 60, 60, 4, BLACK))
            player_animation_jumping.append(M_player_sprites_jumping.get_image(x, 60, 60, 4, BLACK))
        gender = 'M'
    elif button_NB.clicked:
        for x in range(PLAYER_ANIMATION_STEPS):
            player_animation_running.append(NB_player_sprites_running.get_image(x, 60, 60, 4, BLACK))
            player_animation_right.append(NB_player_sprites_right.get_image(x, 60, 60, 4, BLACK))
            player_animation_left.append(NB_player_sprites_left.get_image(x, 60, 60, 4, BLACK))
            player_animation_jumping.append(NB_player_sprites_jumping.get_image(x, 60, 60, 4, BLACK))
        gender = 'NB'

def game_end(win): #ripped off from the original, since GPT refused to work and I didn't have enough time to make this better. Though I had to make some tweaks, of course.
    global game_state
    last_animation_update = pygame.time.get_ticks()
    player_animation_current_frame = 0
    test_for_first_time = True

    cutscene_sprite = spritesheet.SpriteSheet(pygame.image.load('sprites/cutscenes/sheets/sprite_sheet_skill_issue.png').convert_alpha())
    cutscene_animation = []

    if not win:
        ANIMATION_STEPS = 33
        button_menu = button.Button(SCREEN_WIDTH/2-82, SCREEN_HEIGHT/2+200, (pygame.image.load('sprites/buttons/button_menu.png').convert_alpha()), 1)

        #load the losing animation
        cutscene_sprite = spritesheet.SpriteSheet(pygame.image.load('sprites/cutscenes/sheets/sprite_sheet_skill_issue.png').convert_alpha())
        for x in range(ANIMATION_STEPS):
            cutscene_animation.append(cutscene_sprite.get_image(x, 420, 240, 4, BLACK))
    else:
        ANIMATION_STEPS = 49
        button_menu = button.Button(SCREEN_WIDTH*3/4-220, SCREEN_HEIGHT/2+145, (pygame.image.load('sprites/buttons/button_menu.png').convert_alpha()), 1)

        if gender == "F":
            #load the female Alex winning animation
            cutscene_sprite = spritesheet.SpriteSheet(pygame.image.load('sprites/cutscenes/sheets/sprite_sheet_win_F.png').convert_alpha())
            for x in range(ANIMATION_STEPS):
                cutscene_animation.append(cutscene_sprite.get_image(x, 420, 240, 4, BLACK))
        elif gender == "M":
            #load the male Alex winning animation
            cutscene_sprite = spritesheet.SpriteSheet(pygame.image.load('sprites/cutscenes/sheets/sprite_sheet_win_M.png').convert_alpha())
            for x in range(ANIMATION_STEPS):
                cutscene_animation.append(cutscene_sprite.get_image(x, 420, 240, 4, BLACK))
        elif gender == "NB":
            #load the enby Alex winning animation
            cutscene_sprite = spritesheet.SpriteSheet(pygame.image.load('sprites/cutscenes/sheets/sprite_sheet_win_NB.png').convert_alpha())
            for x in range(ANIMATION_STEPS):
                cutscene_animation.append(cutscene_sprite.get_image(x, 420, 240, 4, BLACK))
    
    run = True
    while run:
        screen.fill(BLACK)

        #updates the GIF
        current_time = pygame.time.get_ticks()
        if current_time - last_animation_update >= PLAYER_ANIMATION_SPEED:
            if player_animation_current_frame < ANIMATION_STEPS-1:
                player_animation_current_frame += 1
            else:
                player_animation_current_frame = 0
                if test_for_first_time and not win:
                    cutscene_animation = []
                    ANIMATION_STEPS = 6
                    cutscene_sprite = spritesheet.SpriteSheet(pygame.image.load('sprites/cutscenes/sheets/sprite_sheet_gameover.png').convert_alpha())
                    for x in range(ANIMATION_STEPS):
                        cutscene_animation.append(cutscene_sprite.get_image(x, 420, 240, 4, BLACK))
                elif test_for_first_time and win:
                    cutscene_animation = []
                    ANIMATION_STEPS = 0
                    if gender == "F":
                        #load the female Alex winning screen
                        cutscene_sprite = spritesheet.SpriteSheet(pygame.image.load('sprites/player/Fem/win_screen_F.png').convert_alpha())
                        cutscene_animation.append(cutscene_sprite.get_image(0, 1680, 945, 1, BLACK))
                    elif gender == "M":
                        #load the male Alex winning screen
                        cutscene_sprite = spritesheet.SpriteSheet(pygame.image.load('sprites/player/Masc/win_screen_M.png').convert_alpha())
                        cutscene_animation.append(cutscene_sprite.get_image(0, 1680, 945, 1, BLACK))
                    elif gender == "NB":
                        #load the enby Alex winning screen
                        cutscene_sprite = spritesheet.SpriteSheet(pygame.image.load('sprites/player/NB/win_screen_NB.png').convert_alpha())
                        cutscene_animation.append(cutscene_sprite.get_image(0, 1680, 945, 1, BLACK))
                
                pygame.mouse.set_visible(True)
                test_for_first_time = False
            
            last_animation_update = current_time

        #runs through all pygame events
        for event in pygame.event.get():
            #checks if the screen should be closed
            if event.type == pygame.QUIT:
                #stops the while
                run = False
                pygame.quit()
        

        if button_menu.clicked:
            reset_game()
            game_state = "MENU"
            return #I tried a few things, but it's not working.


        #actually updates the window. HAVE to be the last thing here.
        if test_for_first_time:
            screen.blit(cutscene_animation[player_animation_current_frame], (0, 0))
        elif win and not test_for_first_time:
            screen.blit(cutscene_animation[0], (0, 0))
            button_menu.draw(screen)
        elif not win:
            screen.blit(cutscene_animation[player_animation_current_frame], (0, 0))
            button_menu.draw(screen)

        pygame.display.update()

def reset_game():
    global current_lane, target_lane, player_pos, bg_y, obstacles, gender, lives, lives_initial, colliding
    global player_animation_current_frame, player_current_animation, player_animation_running, player_animation_right, player_animation_left, player_animation_jumping
    current_lane = 1
    target_lane = current_lane
    player_pos = [lanes[current_lane] - player_size // 2, SCREEN_HEIGHT - 2 * player_size]
    player_animation_current_frame = 0
    player_current_animation = player_animation_running
    bg_y = 0
    obstacles.empty()
    lives = lives_initial
    colliding = False
    gender = ''
    # Using ".empty()" only works for "groups", apparently
    player_animation_running = []
    player_animation_right = []
    player_animation_left = []
    player_animation_jumping = []

def game():
    global current_lane, target_lane, player_animation_current_frame, player_current_animation, lives, colliding
    player_rect = player_current_animation[player_animation_current_frame].get_rect(topleft=player_pos)
    collision_offset = 70  # Reduce the size by this amount from each side
    collision_rect = player_rect.inflate(-collision_offset*2, -collision_offset*2.5)  # Create the smaller collision rect
    moving = False
    last_animation_update = pygame.time.get_ticks()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return "QUIT"

        # Player input
        keys = pygame.key.get_pressed()
        if not moving and player_current_animation != player_animation_jumping:
            if keys[pygame.K_a] and current_lane > 0:
                target_lane = current_lane - 1
                player_current_animation = player_animation_left
                player_animation_current_frame = 0
                moving = True
            if keys[pygame.K_d] and current_lane < 2:
                target_lane = current_lane + 1
                player_current_animation = player_animation_right
                player_animation_current_frame = 0
                moving = True
            if keys[pygame.K_SPACE] or keys[pygame.K_w]:
                player_current_animation = player_animation_jumping
                player_animation_current_frame = 0

        # Smoothly move player to the target lane
        target_x = lanes[target_lane] - player_size - 7 // 2
        if player_rect.x < target_x:
            player_rect.x += player_speed
            if player_rect.x >= target_x:
                player_rect.x = target_x
                current_lane = target_lane
                if player_current_animation != player_animation_jumping:
                    player_current_animation = player_animation_running
                moving = False
        elif player_rect.x > target_x:
            player_rect.x -= player_speed
            if player_rect.x <= target_x:
                player_rect.x = target_x
                current_lane = target_lane
                if player_current_animation != player_animation_jumping:
                    player_current_animation = player_animation_running
                moving = False

        # Update collision_rect to follow player_rect
        collision_rect.topleft = (player_rect.left + collision_offset, player_rect.bottom - collision_offset)

        # Create new obstacles
        if random.randint(0, 60) < 1:
            create_obstacle()

        # Move and draw obstacles
        obstacles.update()

        # Detect collisions
        collision_obstacle = detect_collision(collision_rect, obstacles)
        if collision_obstacle:
            if isinstance(collision_obstacle, ObstacleCyclist) or player_current_animation != player_animation_jumping:
                if lives <= 0:
                    running = False
                    print("You died")
                    game_end(False)
                    return
                elif not colliding:
                    print("-1")
                    lives -= 1
                    colliding = True
        else: 
            colliding = False
                

        # Draw everything
        scroll_background()
        if bg_y >= 43200 - SCREEN_HEIGHT:
            running = False
            game_end(True)
            return

        obstacles.draw(screen)
        # Update and draw player animation
        current_time = pygame.time.get_ticks()
        if current_time - last_animation_update > PLAYER_ANIMATION_SPEED:
            player_animation_current_frame = (player_animation_current_frame + 1) % PLAYER_ANIMATION_STEPS
            last_animation_update = current_time
            # Check if jumping animation is finished
            if player_current_animation == player_animation_jumping and player_animation_current_frame == 0:
                player_current_animation = player_animation_running
        screen.blit(player_current_animation[player_animation_current_frame], player_rect.topleft)
        # pygame.draw.rect(screen, RED, collision_rect, 2)  # Draw collision_rect for debugging
        # Debugging: Draw collision rect for obstacles
        # for obstacle in obstacles:
        #     pygame.draw.rect(screen, RED, obstacle.collision_rect, 2)

        pygame.display.flip()
        clock.tick(FPS)

    return "MENU"

def main():
    game_state = "MENU"
    run = True
    while run:
        if game_state == "MENU":
            menu()
            gender_selection()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    return
                if gender == 'F' or gender == 'M' or gender == 'NB':
                    game_state = "GAME"
        elif game_state == "GAME":
            game_state = game()
        elif game_state == "QUIT":
            run = False
            return

if __name__ == "__main__":
    main()

pygame.quit()
