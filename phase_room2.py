import pygame, sys
from pygame.locals import *
from utils import load_images, Dialog, exit_keys
from player import Player_room

pygame.init()

class Objects:
        def __init__(self):
                # table:
                self.table_img = load_images(['images/objects/table.png'])[0]
                self.table_img_pos = (200, 150)

                # pistol
                self.pistol_pos = (500, 150)
                pistol_width, pistol_height = (50,30)
                self.pistol_img = pygame.transform.scale(pygame.image.load('images/gun2.png'), (pistol_width, pistol_height))
                self.pistol_rect = pygame.Rect(self.pistol_pos[0], self.pistol_pos[1], pistol_width, pistol_height)

                self.state_pistol = True

                # portal:

        def update_objects(self, screen, collider):
                screen.blit(self.table_img, self.table_img_pos)
                
                if self.pistol_rect.colliderect(collider):
                        self.state_pistol = False
                        
                if self.state_pistol:
                        screen.blit(self.pistol_img, self.pistol_pos)
                        return False
                else:
                        return True


                
def Game_Room2():
        fps = 30
        clock = pygame.time.Clock()
        
        screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        WINDOW_SIZE = pygame.display.get_window_size()
        
        dialog = Dialog((255,255,255))
        dialog.message(['otro cuarto!!!', 'pero hay ...', 'una pistola!!!'])

        objetos = Objects()

        player = Player_room(WINDOW_SIZE, [100, WINDOW_SIZE[0]-145, 100, WINDOW_SIZE[1]-145],(WINDOW_SIZE[0]//2, WINDOW_SIZE[1]-150))

        door_pos = (WINDOW_SIZE[0]//2-100, WINDOW_SIZE[1]-110)
        door_images = load_images(['images/objects/portal0.png', 'images/objects/portal1.png', 'images/objects/portal2.png'])
        door_images_out = list(map(lambda img: pygame.transform.rotate(img, 270), door_images))
        door = door_images_out[0]
        door_rect = pygame.Rect(WINDOW_SIZE[0]-120,280,50,200)
        door_sprite = 0
        sprite = 0
        door_speed_sprite = 0.2
        door_on = False

        while True:     
                for event in pygame.event.get():
                        exit_keys(event)
                        if event.type == KEYDOWN:
                                player.down_key(event.key)       
                        if event.type == KEYUP:
                                player.up_key(event.key)
                                                
                screen.fill((0,0,0))

                pygame.draw.rect(screen,(255,255,255),[100,100,WINDOW_SIZE[0]-200,WINDOW_SIZE[1]-200],2) # limits font

                if door_on:
                        door = door_images_out[int(door_sprite)]
                        screen.blit(door, (door_rect.x, door_rect.y))
                        
                        door_sprite += door_speed_sprite
                        if int(door_sprite) >= len(door_images):
                                door_sprite = 0
                                
                        if door_rect.colliderect(player.get_collider()):
                                break

                door = door_images[int(sprite)]
                screen.blit(door, (door_pos))
                        
                sprite += door_speed_sprite
                if int(sprite) >= len(door_images):
                        sprite = 0
                
                door_on = objetos.update_objects(screen, player.get_collider())
                        
                player.moving_player(screen)

                dialog.stream(screen, player.get_position())
                
                pygame.display.update()
                clock.tick(fps)


if __name__ == '__main__':
        print(Game_Room())
        pygame.quit()

