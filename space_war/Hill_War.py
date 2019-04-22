# Imports
import pygame
import random

# Initialize game engine
pygame.init()


# Window
WIDTH = 1600
HEIGHT = 900
SIZE = (WIDTH, HEIGHT)
TITLE = "AlienBoy vs HillGirl"
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption(TITLE)


# Timer
clock = pygame.time.Clock()
refresh_rate = 60


# Colors
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (100, 255, 100)


# Fonts
FONT_SM = pygame.font.Font(None, 24)
FONT_MD = pygame.font.Font(None, 32)
FONT_LG = pygame.font.Font(None, 64)
FONT_XL = pygame.font.Font("assets/fonts/spacerangerboldital.ttf", 96)


# Images
ship_img = pygame.image.load('assets/images/alien scoot2.png').convert_alpha()
laser_img = pygame.image.load('assets/images/mrhankey.png').convert_alpha()
enemy_img = pygame.image.load('assets/images/crazyhill.png').convert_alpha()
bomb_img = pygame.image.load('assets/images/mail.png').convert_alpha()
paper_img = pygame.image.load('assets/images/Snooty.png').convert_alpha()
compboy_img = pygame.image.load('assets/images/compboy.jpg').convert_alpha()
gameover_img = pygame.image.load('assets/images/gameover.jpg').convert_alpha()
ween_img = pygame.image.load('assets/images/ween.jpg').convert_alpha()
x_img = pygame.image.load('assets/images/x.png').convert_alpha()
heart_img = pygame.image.load('assets/images/heart.png').convert_alpha()






# Sounds
EXPLOSION = pygame.mixer.Sound('assets/sounds/explosion.ogg')
POP = pygame.mixer.Sound('assets/sounds/fart.ogg')
SNEEZE = pygame.mixer.Sound('assets/sounds/donkeybot.ogg')
SNEEZE.set_volume(0.3)
SCREAM = pygame.mixer.Sound('assets/sounds/oof.ogg')
SCREAM.set_volume(1.0)
WIN = pygame.mixer.Sound('assets/sounds/win.ogg')
GAMEOVER = pygame.mixer.Sound('assets/sounds/gameover.ogg')



# Stages
START = 0
PLAYING = 1
END = 2


# Game classes
class Ship(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.speed = 10

        self.health = 2
        

    def move_left(self):
        self.rect.x -= self.speed
    
    def move_right(self):
        self.rect.x += self.speed

    def move_up(self):
        self.rect.y -= self.speed
    
    def move_down(self):
        self.rect.y += self.speed


    def shoot(self):
        print("Pew!!")
        POP.play()

        laser = Laser(laser_img)
        laser.rect.centerx = self.rect.centerx
        laser.rect.centery = self.rect.top
        lasers.add(laser)

    def update(self):
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > WIDTH:
            self.rect.right = WIDTH

        '''check bombs'''
        hit_list = pygame.sprite.spritecollide(self, bombs, True,
                                               pygame.sprite.collide_mask)

        for hit in hit_list:
            self.health -= 1
        
        if self.health == 0:
            SCREAM.play()
            print("oooooooofffffff")
            self.kill()


class Laser(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()

        self.image = image
        self.rect = image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        
        self.speed = 8
        

    def update(self):
        self.rect.y -= self.speed

        if self.rect.bottom < 0:
            self.kill()

class Mob(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.health = 3

    def drop_bomb(self):
        print("pooie")
        SNEEZE.play()
        bomb = Bomb(bomb_img)
        bomb.rect.centerx = self.rect.centerx
        bomb.rect.centery = self.rect.bottom
        bombs.add(bomb)

    
    def update(self):
        hit_list = pygame.sprite.spritecollide(self, lasers, True, pygame.sprite.collide_mask)


        for hit in hit_list:
            self.health -= 1

        if self.health is 0:
            self.kill()
            player.score +=1
            fleet.speed += .75

class Bomb(pygame.sprite.Sprite):
    def __init__(self,image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = image.get_rect()
        self.speed = 4

    def update(self):
        self.rect.y += self.speed

        if self.rect.top > HEIGHT:
            self.kill()


class Fleet():
    def __init__(self, mobs):
        self.mobs = mobs
        self.speed = 3
        self.drop = 30
        self.moving_right = True
        self.drop_speed = 20
        self.drop_rate = 60 #lower is faster
        
    
    def move(self):
        hits_edge = False

        for m in mobs:
            if self.moving_right:
                m.rect.x += self.speed

                if m.rect.right >= WIDTH:
                    hits_edge = True

            else:
                m.rect.x -= self.speed

                if m.rect.left <= 0:
                    hits_edge = True

        if hits_edge:
            self.reverse()
    
    def reverse(self):
        self.moving_right = not self.moving_right

    def move_down(self):
        for m in mobs:
            m.rect.y += self.drop

    def choose_bomber(self):
        rand = random.randrange(self.drop_rate)
        mob_list = mobs.sprites()

        if len(mob_list) > 0 and rand == 0:
            bomber = random.choice(mob_list)
            bomber.drop_bomb()
    
    def update(self):
        self.move()
        self.choose_bomber()


# Game helper functions
def show_title_screen():
    screen.blit(compboy_img, (0,0))
    pygame.draw.rect(screen, WHITE, [280, 200, 1100, 100])
    title_text = FONT_XL.render("AlienBoy vs HillGirl", 1, BLACK)
    w = title_text.get_width()
    screen.blit(title_text, (WIDTH/2 - w/2, 200))
    
def show_end_screen():
    screen.blit(gameover_img, (0,0))
    score_txt = FONT_XL.render("SCORE:" + str(player.score), 1, GREEN)
    w = score_txt.get_width()
    screen.blit(score_txt, (WIDTH/2 - w/2, 700))

    restart_txt = FONT_XL.render("Press space to restart", 1, RED)
    w = restart_txt.get_width()
    screen.blit(restart_txt, (WIDTH/2 - w/2, 800))

def show_win_screen():
    screen.blit(ween_img, (0,0))
    score_txt = FONT_XL.render("SCORE:" + str(player.score), 1, RED)
    w = score_txt.get_width()
    screen.blit(score_txt, (WIDTH/2 - w/2, 700))

    restart_txt = FONT_XL.render("Press space to restart", 1, RED)
    w = restart_txt.get_width()
    screen.blit(restart_txt, (WIDTH/2 - w/2, 800))
    
def show_stats():
    score_txt = FONT_LG.render(str(player.score), 1, BLACK)
    screen.blit(score_txt, [20, 20])

def show_hearts():
    screen.blit(heart_img, (1100, 0))
    screen.blit(heart_img, (1200, 0))
    if ship.health < 2:
        screen.blit(x_img, (1200, 0))
    if ship.health < 1:
        screen.blit(x_img, (1100, 0))
    


def setup():
    global stage, done
    global player, ship, lasers, mobs, fleet, bombs
    
    ''' Make game objects '''
    ship = Ship(740, 800, ship_img)

    ''' Make sprite groups '''
    player = pygame.sprite.GroupSingle()
    player.add(ship)
    player.score = 0

    lasers = pygame.sprite.Group()
    bombs = pygame.sprite.Group()


    mob1 = Mob(100, 100, enemy_img)
    mob2 = Mob(300, 100, enemy_img)
    mob3 = Mob(500, 100, enemy_img)
    mob4 = Mob(700, 100, enemy_img)
    mob5 = Mob(900, 100, enemy_img)
    mob6 = Mob(1100, 100, enemy_img)
    mob7 = Mob(100, 200, enemy_img)
    mob8 = Mob(300, 100, enemy_img)
    mob9 = Mob(500, 200, enemy_img)
    mob10 = Mob(700, 200, enemy_img)
    mob11 = Mob(900, 200, enemy_img)
    mob12 = Mob(1100, 200, enemy_img)
    mob13 = Mob(300, 200, enemy_img)


    mobs = pygame.sprite.Group()
    mobs.add(mob1, mob2, mob3, mob4, mob5, mob6, mob7, mob8, mob9,mob10, mob11, mob12, mob13)

    fleet = Fleet(mobs)

    player.score = 0
    
    ''' set stage '''
    stage = START
    done = False

    
# Game loop
setup()

while not done:
    # Input handling (React to key presses, mouse clicks, etc.)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if stage == START:
                if event.key == pygame.K_SPACE:
                    stage = PLAYING
            elif stage == PLAYING:
                if event.key == pygame.K_SPACE:
                    ship.shoot()
            elif stage == END and len (player) ==0:
                if event.key == pygame.K_SPACE:
                    setup()
            elif stage == END:
                if event.key == pygame.K_SPACE:
                    setup()
            

    pressed = pygame.key.get_pressed()
        
    
    # Game logic (Check for collisions, update points, etc.)
    if stage == PLAYING:
        if pressed[pygame.K_LEFT]:
            ship.move_left()
        elif pressed[pygame.K_RIGHT]:
            ship.move_right()
        elif pressed[pygame.K_UP]:
            ship.move_up()
        elif pressed[pygame.K_DOWN]:
            ship.move_down()


        player.update()
        lasers.update()
        fleet.update()
        mobs.update()
        bombs.update()

        if len (player) == 0:
            stage = END
            print ("YOU SMELL")
            GAMEOVER.play()

        elif len (mobs) == 0:
            stage = END
            WIN.play()

        
    # Drawing code (Describe the picture. It isn't actually drawn yet.)
    screen.fill(BLACK)
    screen.blit(paper_img, (0,0))
    lasers.draw(screen)
    bombs.draw(screen)
    player.draw(screen)
    mobs.draw(screen)
    show_stats()
    show_hearts()

    
    if stage == START:
        show_title_screen()

    elif stage == END and len (player) == 0:
        show_end_screen()
        
    elif stage == END:
        show_win_screen()


        
    # Update screen (Actually draw the picture in the window.)
    pygame.display.flip()


    # Limit refresh rate of game loop 
    clock.tick(refresh_rate)


# Close window and quit
pygame.quit()

