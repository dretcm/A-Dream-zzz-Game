import pygame, sys, random
from pygame.locals import *
from player import Player_Run
from utils import exit_keys, Dialog, load_images

pygame.init()

class Obstaculos:
        t = 0
        limit = 20
        ago = 20
        times = [30, 40, 50, 60]
        speed = 10

        height = 40
        width = 10
        def __init__(self, window_size, floor_pos):
                self.window_size = window_size
                self.floor_pos = floor_pos - self.height
                self.obs = []
        def update_obstaculos(self,screen, player): 
                aux = []
                for i in self.obs:
                        pygame.draw.rect(screen, (0,255,0), i)
                        i.x -= self.speed
                        if i.colliderect(player.get_collider()):
                                return True
                        if i.x > 0:
                                aux.append(i)
                                
                self.obs = aux.copy()
                
                if self.t < self.limit:
                        self.t += 1
                else:
                        obstaculo = pygame.Rect(self.window_size[0] + 100, self.floor_pos, self.width, self.height)
                        self.obs.append(obstaculo)
                        self.t = 0
                        self.speed += 0.2
                        self.ago = self.limit
                        self.limit = random.choice(self.times)
                        while self.limit == self.ago:
                                self.limit = random.choice(self.times)
                return False

def Game_Run():
        clock = pygame.time.Clock()
        fps = 30
        
        screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        WINDOW_SIZE = pygame.display.get_window_size()

        door_pos = (WINDOW_SIZE[0]//2 - 320, WINDOW_SIZE[1]//2 - 100)
        door_images = load_images(['images/objects/portal0.png', 'images/objects/portal1.png', 'images/objects/portal2.png'])
        door_images = list(map(lambda img: pygame.transform.rotate(img, 230), door_images))
        door_limit = len(door_images)
        door = door_images[0]
        door_sprite = 0
        door_speed_sprite = 0.2
        door_on = True
        door_time = 200

        floor_pos = WINDOW_SIZE[1] - 20
        floor = pygame.Rect(0,floor_pos,WINDOW_SIZE[0],50)
        
        player = Player_Run(WINDOW_SIZE, floor_pos)
        obstaculos = Obstaculos(WINDOW_SIZE, floor_pos)
        obs = True

        dialog = Dialog((0,0,0))
        dialog.message(['por ahora debo huir'])

        color = 255
        cambio = 400
        op = True

        message = 300
        message2 = 700
        meta = 950
        
        while True:
                for event in pygame.event.get():
                        exit_keys(event)
                        if event.type == KEYDOWN:
                                player.down_key(event.key)
                                

                if player.recorrido < cambio:
                        if op:
                                if color < 255:
                                        color += 1
                        else:
                                if color > 127:
                                        color -= 1                       
                else:
                        cambio += 400
                        op = not op

                                
                screen.fill((color,color,color))

                if door_on:
                        if door_time == 0:
                                door_on = False
                        door_time -= 1
                        screen.blit(door, door_pos)
                        door = door_images[int(door_sprite)]
                        door_sprite += door_speed_sprite
                        if door_sprite >= door_limit:
                                door_sprite = 0
                                
                
                player.moving_player(screen)
                pygame.draw.rect(screen, (255,128,0), floor)
                
                if player.get_collider().colliderect(floor):
                        player.floor = False

                if obstaculos.update_obstaculos(screen, player):
                        return False
                
                if player.recorrido == message:
                        dialog.message(['mmm...','la pistola que recogi tiene...','3 balas!', ':,v   '])
                if player.recorrido == message2:
                        dialog.message(['no podre correr para siempre','tengo que enfrentarlos'])
                if player.recorrido > meta:
                        return True
                
                dialog.stream(screen, player.get_position())
                
                pygame.display.update()
                clock.tick(fps)

if __name__ == '__main__':
        print(Game_Run())
        pygame.quit()

