import pygame
from pygame.locals import *
from utils import load_images

pygame.init()

# character :
class Player:
        live = True
        speed = 15

        left = False
        right = False
        up = False
        down = False

        width = 40
        height = 40
        size = (width,height)

        sonido_f = pygame.mixer.Sound("music/muerte.mp3")

        speed_sprite = 0.1

        def __init__(self, window_size, pos_init=None):
                if pos_init:
                        self.x, self.y = pos_init
                else:
                        self.x = window_size[0]//2 - 45
                        self.y = window_size[1]//2 - 25
                
                self.rect = pygame.Rect(self.x,self.y, self.width, self.height)

                self.images = load_images(['images/player/player10.png', 'images/player/player11.png'], size=self.size)
                self.images_up = load_images(['images/player/player0.png', 'images/player/player1.png', 'images/player/player2.png'], size=self.size)
                self.images_down = load_images(['images/player/player3.png', 'images/player/player4.png', 'images/player/player5.png'], size=self.size)
                self.images_left = load_images(['images/player/player8.png', 'images/player/player9.png'], size=self.size)
                self.images_right = load_images(['images/player/player6.png', 'images/player/player7.png'], size=self.size)
                        
                self.actual = 0
                self.image = self.images[self.actual]
        
        def down_key(self,key):
                if key == K_LEFT:
                        self.left = True
                if key == K_RIGHT:
                        self.right = True
                if key == K_UP:
                        self.up = True
                if key == K_DOWN:
                        self.down = True
                        
        def up_key(self,key):
                if key == K_LEFT:
                        self.left = False
                if key == K_RIGHT:
                        self.right = False
                if key == K_UP:
                        self.up = False
                if key == K_DOWN:
                        self.down = False
                        
        def moving(self):
                if self.left:
                        self.rect.x -= self.speed
                if self.right:
                        self.rect.x += self.speed
                if self.up:
                        self.rect.y -= self.speed
                if self.down:
                        self.rect.y += self.speed
                        
        def moving_player(self, screen):
                now = self.images
                
                if self.left:
                        now = self.images_left
                if self.right:
                        now = self.images_right
                if self.up:
                        now = self.images_up
                if self.down:
                        now = self.images_down
                        
                self.moving()
                screen.blit(self.image, self.get_position())
                self.changues_img(now)
                        
        def changues_img(self, sprites):
                if self.actual >= len(sprites):
                        self.actual = 0
                self.image = sprites[int(self.actual)]
                self.actual += self.speed_sprite
                
        def get_position(self):
                return (self.rect.x, self.rect.y)
        
        def set_position(self,x,y):
                self.rect.topleft = [x, y]
                
        def get_collider(self):
                return self.rect

        def set_player_live(self, live):
                self.live = live
                self.sonido_f.play()
                
        def player_live(self):
                return self.live


     
class Player_room(Player):
        def __init__(self, window_size, limits, pos_init=None):
                super().__init__(window_size, pos_init)
                self.limits = limits # [120,1050,50,500] # left, right, top, botton
                self.speed = 5
                        
        def moving(self):                         
                if self.left and self.rect.x > self.limits[0]:
                        self.rect.x -= self.speed
                if self.right and self.rect.x < self.limits[1]:
                        self.rect.x += self.speed
                if self.up and self.rect.y > self.limits[2]:
                        self.rect.y -= self.speed
                if self.down and self.rect.y < self.limits[3]:
                        self.rect.y += self.speed                


class Player_Run:
        floor = True
        font = pygame.font.Font(None,30)
        recorrido = 0

        width = 40
        height = 40

        const_up = 15
        up = 0
        down = 1
        
        def __init__(self,window_size, floor_pos):
                self.window_size = window_size
                self.floor_pos = floor_pos
                self.x, self.y = window_size[0]//2 - 200, window_size[1]//2 -20
                
                self.collider = pygame.Rect(self.x,self.y, self.width, self.height)
                self.images = load_images(['images/player/player6.png', 'images/player/player7.png'], size=(self.width, self.height), bg_color=(255,255,255))
                self.img = self.images[0]
                self.current = 0
                self.speed_sprite = 0.2
                self.limit_sprites = len(self.images)
                
        def down_key(self,key):
                if key == K_UP and not self.floor:
                        self.up = self.const_up
                        self.floor = True
                        
        def moving_player(self, screen):
                if self.floor:
                        self.collider.y -= self.up
                        self.up -= self.down

                if self.collider.y + self.height > self.floor_pos:
                        self.collider.y = self.floor_pos - self.height + 1

                self.recorrido += 1
                
                self.sprites(screen)
                
                message = self.font.render('metros: '+ str(self.recorrido), 1, (0, 0, 0))
                screen.blit(message, (self.window_size[0]-150, 10))

        def sprites(self, screen):
                screen.blit(self.img, self.get_position())
                self.img = self.images[int(self.current)]
                self.current += self.speed_sprite
                if self.current >= self.limit_sprites:
                        self.current = 0
                
        def get_collider(self):
                return self.collider
        
        def get_position(self):
                return (self.collider.x, self.collider.y)
