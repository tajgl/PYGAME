import pygame
import os
pygame.font.init()
pygame.mixer.init()


WIDTH, HEIGHT = 1200, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))     #sets dimensions of window
pygame.display.set_caption('GANGSTER GAME')       #names the window

WHITE = (255, 255, 255)
VIOLET = (134, 1, 175)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

BORDER = pygame.Rect(0, HEIGHT//2 - 5, WIDTH, 10)  #dimensions for border

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('assets', 'explode.mp3' ))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('assets','shooting.mp3' ))
END_SOUND = pygame.mixer.Sound(os.path.join('assets','tuff.mp3' ))

HEALTH_FONT = pygame.font.SysFont('freesansbold', 40)
WINNER_FONT = pygame.font.SysFont('freesansbold', 100)

FPS = 60
BULLET_V = 7
MAX_BULLETS = 3
V = 5

WHITE_HIT = pygame.USEREVENT + 1
BLACK_HIT = pygame.USEREVENT + 2 

WHITE_GUY_IMAGE = pygame.image.load(os.path.join('assets', 'white_guy.png')) 
WHITE_GUY = pygame.transform.rotate(pygame.transform.scale(WHITE_GUY_IMAGE, (70, 75)), 90)     #scales image

BLACK_GUY_IMAGE = pygame.image.load(os.path.join('assets', 'black_guy.png')) 
BLACK_GUY = pygame.transform.rotate(pygame.transform.scale(BLACK_GUY_IMAGE, (135, 80)), 90)     #scales image

IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'back.jpg')), (WIDTH,HEIGHT))

def draw_window(white, black, white_bullets, black_bullets, white_health, black_health):   #opens window
    WIN.fill(VIOLET)   #makes window violet
    WIN.blit(IMAGE, (0,0))
    pygame.draw.rect(WIN, BLACK, BORDER) #adds border

    white_health_text = HEALTH_FONT.render('HEALTH: ' + str(white_health), 1, WHITE)
    black_health_text = HEALTH_FONT.render('HEALTH: ' + str(black_health), 1, WHITE)
    WIN.blit(white_health_text, (WIDTH - white_health_text.get_width() - 10, 10))
    WIN.blit(black_health_text, (10, HEIGHT - black_health_text.get_height()- 10))

    WIN.blit(WHITE_GUY, (white.x, white.y))
    WIN.blit(BLACK_GUY, (black.x, black.y))   #opens image 

    for bullet in white_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet) #adds bullet

    for bullet in black_bullets:
        pygame.draw.rect(WIN, RED, bullet)  #adds bullet
    
    pygame.display.update()

def white_movement(keys_pressed, white): #moves and stops at borders
    if keys_pressed[pygame.K_a] and white.x - V > 0 :   #moves left
        white.x -= V
    if keys_pressed[pygame.K_d] and white.x + V + 70 < WIDTH :  #moves right
        white.x += V
    if keys_pressed[pygame.K_w] and white.y - V > 0: #moves up
        white.y -= V
    if keys_pressed[pygame.K_s] and white.y - V < BORDER.y - 70:    #moves down
        white.y += V

def black_movement(keys_pressed, black): #moves and stops at borders
    if keys_pressed[pygame.K_LEFT] and black.x - V > 0 :   #moves left
        black.x -= V
    if keys_pressed[pygame.K_RIGHT] and black.x + V + 70 < WIDTH:   #moves right
        black.x += V
    if keys_pressed[pygame.K_UP] and black.y + V > BORDER.y - 15:   #moves up
        black.y -= V
    if keys_pressed[pygame.K_DOWN] and black.y + V + 95 < HEIGHT:   #moves down
        black.y += V

def handle_bullets(white_bullets, black_bullets, white, black):  #if bullets hit
    for bullet in white_bullets:
        bullet.y += BULLET_V   
        if black.colliderect(bullet):
            pygame.event.post(pygame.event.Event(BLACK_HIT))
            white_bullets.remove(bullet)
        elif bullet.y > HEIGHT:
            white_bullets.remove(bullet)

    for bullet in black_bullets:
        bullet.y -= BULLET_V   
        if white.colliderect(bullet):
            pygame.event.post(pygame.event.Event(WHITE_HIT))   
            black_bullets.remove(bullet)
        elif bullet.y < 0:
            black_bullets.remove(bullet)

def draw_winner(text): #end text
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()/2, HEIGHT//2 - draw_text.get_height()/2)) #postion of text
    pygame.display.update()
    pygame.time.delay(5000) #delays text

def main():
    white = pygame.Rect(600, 50, 70, 75 )
    black = pygame.Rect(600, 550, 135, 80 )

    white_bullets= []
    black_bullets = []

    white_health = 10
    black_health = 10
    
    clock = pygame.time.Clock()
    run = True 
    while run:
        clock.tick(FPS)  #controls speed of loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:    
                run = False 
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(white_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(white.x + white.width//2, white.y + white.height - 2, 10, 5) #where bullet starts    
                    white_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                    
                if event.key == pygame.K_RCTRL and len(black_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(black.x + 40 , black.y + 30 - 2, 10, 5)    #where bullet starts
                    black_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == WHITE_HIT:
                white_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == BLACK_HIT:
                black_health -= 1
                BULLET_HIT_SOUND.play()

        winner_text = ""
        if white_health <= 0:
            winner_text = "WHITE SUCKS, BLACK WINS"  #game ending text
            END_SOUND.play() #my added sound

        if black_health <= 0:
            winner_text = "BLACK SUCKS, WHITE WINS"  #game ending text
            END_SOUND.play() #my addded sound

        if winner_text != "":
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        white_movement(keys_pressed, white)
        black_movement(keys_pressed, black)
        
        handle_bullets(white_bullets, black_bullets, white, black)
        
        draw_window(white, black, white_bullets, black_bullets, white_health, black_health)

    main()  #continues loop

if __name__ == "__main__": 
    main()

