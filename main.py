import pygame, sys
from random import choice
# If score % 5 == 0: opponent_speed += 1
def move_ball():
    global ball, screen_width, screen_height, ball_direction
    ball.center += int(ball_speed) * ball_direction

    if ball.colliderect(player) or ball.colliderect(opponent):
        ball_direction.x *= -1

    if ball.bottom >= screen_height:
        ball_direction.y *= -1
    elif ball.top <= 0:
        ball_direction.y *= -1

def move_player():
    global player
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and player.y > 0:
        player.y -= 8
    elif keys[pygame.K_DOWN] and player.bottom < screen_height:
        player.y += 8

def move_opponent():
    if opponent.y <= 0:
        opponent.y = 0
    elif opponent.y + opponent.height >= screen_height:
        opponent.bottom = screen_height
    
    ball_vector = pygame.Vector2(ball.center)
    opponent_vector = pygame.Vector2(opponent.center)

    if ball.x <= screen_width/2 and ball_direction.x == -1:
        opponent_direction = (ball_vector - opponent_vector).normalize()
        opponent.y += opponent_speed * opponent_direction.y

def reset():
    global ball_direction
    ball.center = (screen_width/2,screen_height/2)
    player.topleft = (screen_width-10,screen_height/2-60)
    opponent.topleft = (0,screen_height/2-60)
    ball_direction = pygame.Vector2(0,0)

def update_speed():
    global opponent_speed, ball_speed,can_speed
    if player_score % 2 == 0 and opponent_speed < 15:
        if can_speed:
            opponent_speed += 1
            ball_speed += 0.5
            can_speed = False
    else:
        can_speed = True


def display_score():
    font = pygame.font.Font(None,50)
    player_score_surf = font.render(str(player_score),True, 'grey')
    opponent_score_surf = font.render(str(opponent_score),True, 'grey')
    screen.blit(player_score_surf,(screen_width/2 + player_score_surf.get_width() + 10, 0))
    screen.blit(opponent_score_surf,(screen_width/2 - opponent_score_surf.get_width() - 10, 0))

if __name__ == '__main__':
    pygame.init()
    screen_width = 1000
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Pong')
    clock = pygame.time.Clock()
    run = True

    ball_direction = pygame.Vector2(choice([-1,1]),choice([-1,1]))
    opponent_speed = 8
    ball_speed = 8
    can_speed = True

    # Ball / Player / Opponent / middle thing
    ball = pygame.Rect(screen_width/2-15,screen_height/2-15,30,30)
    player = pygame.Rect(screen_width-10,screen_height/2-60,10,120)
    opponent = pygame.Rect(0,screen_height/2-60,10,120)
    middle_thing = pygame.Surface((5,screen_height))
    middle_thing_rect = middle_thing.get_rect(center = (screen_width/2, screen_height/2))
    middle_thing.fill((200,200,200))
    
    player_score = 0
    opponent_score = 0


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if not run and not ball_direction:
                if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        ball_direction = pygame.Vector2(choice([-1,1]),choice([-1,1]))

        if ball.right >= screen_width:
            opponent_score += 1
            run = False
            reset()

        elif ball.left <= 0:
            player_score += 1
            run = False
            reset()
        
        update_speed()

        move_ball()
        move_opponent()
        move_player()

        screen.fill('#242424')
        screen.blit(middle_thing, middle_thing_rect)
        display_score()
        pygame.draw.ellipse(screen,(255,255,255),ball)
        pygame.draw.rect(screen,(200,200,200),player)
        pygame.draw.rect(screen,(200,200,200),opponent)

        pygame.display.flip()
        clock.tick(60)
