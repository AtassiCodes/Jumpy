import pygame
import os
import random

pygame.init()

screen_height = 1000
screen_width = int(screen_height * 0.75)

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Jumper!!')
print(pygame.display.get_window_size())
# set framerate
clock = pygame.time.Clock()
FPS = 120

# define game variables
GRAVITY = 1
max_platforms = 10
scroll_threshhold = 198
scroll = 0
jumping_height = 25
speed = 10
score = 0
fade_counter = 0

# define player action variables
moving_left = False
moving_right = False

# define colours
BG = (144, 201, 120)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


def text(text, font_size, colour, x, y):
    img = (pygame.font.Font('Fonts/Font.ttf', font_size)).render(text, True, colour)
    screen.blit(img, (x,y))

def draw_bg():
    background = pygame.image.load('Backgrounds/background.png').convert_alpha()
    screen.blit(background, (0, 0))
    pygame.draw.rect(screen, BLACK, (0, 0, screen_width, 75))
    text("Score   "+str(score), 30, WHITE, 20, 20)


platform_image = pygame.image.load('Blocks/Block-1.png').convert_alpha()

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.transform.scale(platform_image, (width, 50))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        pygame.draw.rect(screen, (0, 0, 0), (0, 850, screen_width, 850))

    def update(self, scroll):
        self.rect.y += scroll

        if self.rect.top > screen_height:
            self.kill()


platform_group = pygame.sprite.Group()
enemies_group = pygame.sprite.Group()

# create starting platform
# 300 pix difference + cross screen @ 300 wide = hard
platform = Platform((screen_width/2) + 75, screen_height - 300, 300)
platform_group.add(platform)

# enemies = Enemies(0, 300, 5, 10)

class Soldier(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.speed = speed
        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.in_air = True
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()

        # load all images for the players
        animation_types = ['Walking', 'Jumping', 'Fire']

        for animation in animation_types:
            # reset temporary list of images
            temp_list = []
            # count number of files in the folder
            num_of_frames = len(os.listdir(f'Characters/{animation}'))-1
            for i in range(num_of_frames):
                img = pygame.image.load(f'Characters/{animation}/{i}.png').convert_alpha()
                self.width = (int(img.get_width() * scale))
                self.height = (int(img.get_height() * scale))
                img = pygame.transform.scale(img, (self.width, self.height))
                temp_list.append(img)
            self.animation_list.append(temp_list)

        self.ani_image = self.animation_list[self.action][self.frame_index]
        self.rect = self.ani_image.get_rect()
        self.rect.center = (x, y)

    def move(self, moving_left, moving_right):
        # reset movement variables
        scroll = 0
        dx = 0
        dy = 0

        # assign movement variables if moving left or right
        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1

        # jump
        if self.jump == True and self.in_air == False:
            self.vel_y = -(jumping_height)
            self.jump = False
            self.in_air = True

        # apply gravity
        self.vel_y += GRAVITY
        # if self.vel_y >= 9.5:
        #     self.vel_y = 9.81
        dy += self.vel_y

        # check collision with platform

        for platform in platform_group:
            if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                if self.rect.bottom < platform.rect.centery:
                    if self.vel_y > 0:
                        self.rect.bottom = platform.rect.top
                        dy = 0
                        self.vel_y = -(jumping_height)

        # scroll threshold collision
        if self.rect.top <= scroll_threshhold:
            if self.vel_y < 0:
                scroll = -dy


        # update rectangle position
        self.rect.x += dx
        self.rect.y += dy + scroll

        return scroll

    def update_animation(self):
        # update animation
        ANIMATION_COOLDOWN = 120
        # update ani_image depending on current frame
        self.ani_image = self.animation_list[self.action][self.frame_index]
        # check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        # if the animation has run out the reset back to the start
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0

    def update_action(self, new_action):
        # check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            # update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self):
        screen.blit(pygame.transform.flip(self.ani_image, self.flip, False), self.rect)


player = Soldier(screen_width-100, 650, 3, speed)
fire1 = Soldier(23, 865, 3, 0)
fire2 = Soldier(73, 865, 3, 0)
fire3 = Soldier(123, 865, 3, 0)
fire4 = Soldier(173, 865, 3, 0)
fire5 = Soldier(223, 865, 3, 0)
fire6 = Soldier(273, 865, 3, 0)
fire7 = Soldier(323, 865, 3, 0)
fire8 = Soldier(373, 865, 3, 0)
fire9 = Soldier(423, 865, 3, 0)
fire10 = Soldier(473, 865, 3, 0)
fire11 = Soldier(523, 865, 3, 0)
fire12 = Soldier(573, 865, 3, 0)
fire13 = Soldier(623, 865, 3, 0)
fire14 = Soldier(673, 865, 3, 0)
fire15 = Soldier(723, 865, 3, 0)
fire16 = Soldier(773, 865, 3, 0)

run = True
while run:

    clock.tick(FPS)

    if player.alive:
        draw_bg()

        scroll = player.move(moving_left, moving_right)

        platform_group.draw(screen)
        platform_group.update(scroll)


        enemies_group.draw(screen)
        enemies_group.update()

        player.update_animation()
        player.draw()

        if scroll > 0:
            score += scroll//5

    # update player animations
        if player.in_air:
            player.update_action(1)  # 2: jump
        else:
            player.update_action(0)  # 1: run



        if player.rect.bottom > 850:
            player.alive = False
    else:
        fire1.alive = False
        if fade_counter < screen_width:

            fade_counter += 5

            pygame.draw.rect(screen, BLACK, (0, 0, fade_counter, screen_height/2))
            pygame.draw.rect(screen, BLACK, (screen_width - fade_counter, screen_height/2, fade_counter, screen_height/2))

        text("Game Over", 76, BLACK, 32, (screen_height/2)-125)
        text("Game Over", 75, RED, 35, (screen_height/2)-125)
        text("Score   "+str(score), 30, WHITE, 20, 20)
        text("Press space", 50, WHITE, ((screen_width/2)-250), (screen_height/2)+80)
        text("to continue", 50, WHITE, ((screen_width/2)-230), (screen_height/2)+140)

        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            player.alive = True
            fire1.alive = True
            score = 0
            scroll = 0
            fade_counter = 0
            # repositioning player
            player.rect.center = (screen_width-100, 650)
            platform_group.empty()
            platform = Platform((screen_width / 2) + 75, screen_height - 300, 300)
            platform_group.add(platform)

    if fire1.alive:
        fire1.update_animation()
        fire1.draw()
        if fire1.alive:
            fire1.update_action(2)

        fire2.update_animation()
        fire2.draw()
        if fire2.alive:
            fire2.update_action(2)

        fire3.update_animation()
        fire3.draw()
        if fire3.alive:
            fire3.update_action(2)

        fire4.update_animation()
        fire4.draw()
        if fire4.alive:
            fire4.update_action(2)

        fire5.update_animation()
        fire5.draw()
        if fire5.alive:
            fire5.update_action(2)

        fire6.update_animation()
        fire6.draw()
        if fire6.alive:
            fire6.update_action(2)

        fire7.update_animation()
        fire7.draw()
        if fire7.alive:
            fire7.update_action(2)

        fire8.update_animation()
        fire8.draw()
        if fire8.alive:
            fire8.update_action(2)

        fire9.update_animation()
        fire9.draw()
        if fire9.alive:
            fire9.update_action(2)

        fire10.update_animation()
        fire10.draw()
        if fire10.alive:
            fire10.update_action(2)

        fire11.update_animation()
        fire11.draw()
        if fire11.alive:
            fire11.update_action(2)

        fire12.update_animation()
        fire12.draw()
        if fire12.alive:
            fire12.update_action(2)

        fire13.update_animation()
        fire13.draw()
        if fire13.alive:
            fire13.update_action(2)

        fire14.update_animation()
        fire14.draw()
        if fire14.alive:
            fire14.update_action(2)

        fire15.update_animation()
        fire15.draw()
        if fire15.alive:
            fire15.update_action(2)

        fire16.update_animation()
        fire16.draw()
        if fire16.alive:
            fire16.update_action(2)

    if len(platform_group)<max_platforms:
        platform_width = random.randint(200,250)
        platform_x = random.randint(0,(screen_width-platform_width))
        platform_y = (platform.rect.y) - (random.randint(200, 300))
        before_y = platform_y
        platform_y = (platform.rect.y)-(random.randint(200,300))
        if (platform_y-before_y)>100:
            platform_y = 100

        platform = Platform(platform_x, platform_y, platform_width)
        platform_group.add(platform)


    for event in pygame.event.get():
        # quit game
        if event.type == pygame.QUIT:
            run = False
        # keyboard presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_LEFT:
                moving_left = True
            if event.key == pygame.K_RIGHT:
                moving_right = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_w and player.alive:
                player.jump = True
            if event.key == pygame.K_SPACE and player.alive:
                player.jump = True
            if event.key == pygame.K_UP and player.alive:
                player.jump = True
            if event.key == pygame.K_ESCAPE:
                run = False

        # keyboard button released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_LEFT:
                moving_left = False
            if event.key == pygame.K_RIGHT:
                moving_right = False
            if event.key == pygame.K_d:
                moving_right = False

    pygame.display.update()
pygame.quit()
