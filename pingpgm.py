from pygame import*

win_width = 600
win_height = 500
window = display.set_mode((win_width, win_height))
background = (255, 255, 255)
window.fill(background)
display.set_caption('Ping-pong')

run =True
gameover = False
clock = time.Clock()
FPS = 8

mixer.init()
mixer.music.load('music.mp3')
mixer.music.set_volume(0.100)
mixer.music.play()

class GameSprites(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, width, height):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (width, height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprites):
    def control_r(self): #player 2
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - 150:
            self.rect.y += self.speed

    def control_l(self): #player 1
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < win_height - 150:
            self.rect.y += self.speed

paddle_l = Player('platform.png', 30, 20, 30, 50, 150)
paddle_r = Player('platform.png', 520, 20, 30, 50, 150)
ball = Player('ball.png', 200, 200, 4, 50, 50)

speed_x = 15
speed_y = 15

win_aud = mixer.Sound('wins.mp3')

font.init()
font = font.Font(None, 70)

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False

    if not gameover:
        window.fill(background)

        paddle_l.reset()
        paddle_r.reset()
        ball.reset()

        paddle_r.control_r()
        paddle_l.control_l()

        #ball
        ball.rect.x += speed_x
        ball.rect.y += speed_y

        if ball.rect.y > win_height - 50 or ball.rect.y < 0:
            speed_y *= -1

        if ball.rect.x < 0:
            win_aud.play()
            speed_x *= -1
            lose1 = font.render('Right player win!', True, (0,0,0))
            window.blit(lose1, (120,200))
            gameover = True

        if ball.rect.x > win_width - 55:
            win_aud.play()
            speed_x *= -1
            lose1 = font.render('Left player win!', True, (0,0,0))
            window.blit(lose1, (120,200))
            gameover=True

        if sprite.collide_rect(paddle_l, ball) or sprite.collide_rect(paddle_r, ball):
            speed_x *= -1

        display.update()
        clock.tick(FPS)