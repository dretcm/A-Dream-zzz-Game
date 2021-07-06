import pygame, sys, time, random
from pygame.locals import *
from utils import load_images, Dialog, exit_keys
from player import Player_room

pygame.init()

# pc : input :

class InputText:
        font = pygame.font.Font(None, 30)
        input_box = [500, 140, 140, 40]
        color = pygame.Color((0,255,0))
        text = ''
        message = ''

        def set_keyboard(self,event):
                if event.key == K_RETURN:
                        self.message = self.text
                        self.text = ''
                        return True
                elif event.key == K_BACKSPACE:
                        self.text = self.text[:-1]
                else:
                        self.text += event.unicode
                return False
                                        
        def run_input(self, display):                             
                txt = self.font.render('PASSWORD', True, self.color)
                txt_surface = self.font.render(self.text, True, self.color)
                
                width = max(200, txt_surface.get_width()+10)
                self.input_box[2] = width
                
                x,y = self.input_box[0], self.input_box[1]
                
                display.blit(txt, (x, y-40))
                display.blit(txt_surface, (x+5, y+5))
                pygame.draw.rect(display, self.color, self.input_box, 2) 
                pygame.draw.rect(display, self.color, (x - 20 , y-60, width + 40, 120), 2)
                
        def get_message(self):
                return self.message

class Cpu:
        width = 100
        height = 50

        pc_img = load_images(['images/pc.png'],(width, height))[0]
        guia_img = pygame.image.load('images/objects/guia.png')
        guia_pos = (300,220)
        
        x = 750
        y = 100
        
        pc_collider = pygame.Rect(x,y, width,height)

        on = False
        
        display = None
        entry = InputText()

        def activate(self):
                self.entry.run_input(self.display)
                self.display.blit(self.guia_img, self.guia_pos)
                
        def position(self):
                return (self.x,self.y)
        
        def can_entry(self):
                return self.on

        def interact(self, player, display):
                collider = self.pc_collider.colliderect(player)
                if collider:
                        self.on = True
                        self.display = display
                        self.activate()
                else:
                        self.on = False

class Objects:
        def __init__(self):
                font = pygame.font.Font(None, 150)
                # date:
                self.date_pos = (900,450)
                date_width = 60
                date_height = 50
                self.date_rect_img = load_images(['images/objects/obj0.png'],size=(date_width, date_height))[0]
                self.date_rect = pygame.Rect(self.date_pos[0], self.date_pos[1], date_width, date_height)
                self.date_img = load_images(['images/objects/date_content.png'])[0]
                self.date_img_pos = (450, 100)
                
                months = ['January', 'February','March','April','May','June','July','August','September','October','November','December']
                month = random.randint(0,11)
                
                self.text_month = font.render(months[month], 1, (0,0,0))
                self.text_month_pos = (500, 350)
                
                self.text_month_n = font.render(str(month+1), 1, (0,0,0))
                self.text_month_n_pos = (620,200)
                
                # dictionary
                self.dict_pos = (200,470)
                dict_width = 60
                dict_height = 40
                self.dict_rect_img = load_images(['images/objects/obj2.png'],size=(dict_width, dict_height))[0]
                self.dict_rect = pygame.Rect(self.dict_pos[0], self.dict_pos[1], dict_width, dict_height)
                self.dict_img = load_images(['images/objects/dict_content.png'])[0]
                self.dict_img_pos = (300, 100)

                dict_numbers = [4,2,4,2,3,0,3,4,1,2,1,26]
                dict_words = 'shdb.ntmfeaz'
                
                # list people
                self.list_pos = (400,80)
                list_width = 60
                list_height = 40
                self.list_rect_img = load_images(['images/objects/obj1.png'],size=(list_width, list_height))[0]
                self.list_rect = pygame.Rect(self.list_pos[0], self.list_pos[1], list_width, list_height)
                self.list_img = load_images(['images/objects/list_content.png'])[0]
                self.list_img_pos = (450, 100)

                list_numbers = [5,4,8,5]
                list_words = 'PSop'

                # ask
                self.ask_pos = (970,60)
                ask_width = 60
                ask_height = 40
                self.ask_rect_img = load_images(['images/objects/obj3.png'], size=(ask_width, ask_height))[0]
                self.ask_rect = pygame.Rect(self.ask_pos[0], self.ask_pos[1], ask_width, ask_height)

                
                ask_images = ['images/objects/ask_x.png', 'images/objects/ask_plus.png', 'images/objects/ask_minus.png', 'images/objects/ask_abc.png']
                puzzle = ['x','+','-','abc']
                op = random.randint(0,3)
                
                self.ask_img = load_images([ask_images[op]])[0]
                self.ask_img_pos = (450, 100)

                # table:
                self.table_img = load_images(['images/objects/table.png'])[0]
                self.table_img_pos = (300, 400)


                # reply
                reply = 0
                if puzzle[op] == 'abc':
                        reply = ''
                        reply += dict_words[month]
                        aux = month + 1
                        while aux > 4:
                                aux -= 4
                        reply += list_words[aux-1]
                        reply += months[month][0]
                elif puzzle[op] == 'x':
                        reply = dict_numbers[month]
                        aux = month + 1
                        while aux > 4:
                                aux -= 4
                        reply *= list_numbers[aux-1]
                        reply *= (month + 1)

                elif puzzle[op] == '+':
                        reply += dict_numbers[month]
                        aux = month + 1
                        while aux > 4:
                                aux -= 4
                        reply += list_numbers[aux-1]
                        reply += (month + 1)

                elif puzzle[op] == '-':
                        reply -= dict_numbers[month]
                        aux = month + 1
                        while aux > 4:
                                aux -= 4
                        reply -= list_numbers[aux-1]
                        reply -= (month + 1)
                else:
                        print(None)

                self.reply = reply
                print(reply)

        def update_objects(self, screen, collider):
                screen.blit(self.date_rect_img, self.date_pos)
                screen.blit(self.dict_rect_img, self.dict_pos) 
                screen.blit(self.list_rect_img, self.list_pos)
                screen.blit(self.ask_rect_img, self.ask_pos)
                screen.blit(self.table_img, self.table_img_pos)
                
                if self.date_rect.colliderect(collider):
                        screen.blit(self.date_img, self.date_img_pos)
                        screen.blit(self.text_month_n, self.text_month_n_pos)
                        screen.blit(self.text_month, self.text_month_pos)

                if self.dict_rect.colliderect(collider):
                        screen.blit(self.dict_img, self.dict_img_pos)

                if self.list_rect.colliderect(collider):
                        screen.blit(self.list_img, self.list_img_pos)

                if self.ask_rect.colliderect(collider):
                        screen.blit(self.ask_img, self.ask_img_pos)

        def get_reply(self):
                return str(self.reply)
        

def Game_Room():
        fps = 30
        clock = pygame.time.Clock()
        
        screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        WINDOW_SIZE = pygame.display.get_window_size()
        
        dialog = Dialog((255,255,255))
        message = ['donde estoy ?', 'debo salir de aqui!', 'pero como ?']
        dialog.message(message)

        objetos = Objects()

        computer = Cpu()
        player = Player_room(WINDOW_SIZE, [120,1050,50,500])

        bg = load_images(['images/background.png'], size=(1200,600))[0]

        door_images = load_images(['images/objects/portal0.png', 'images/objects/portal1.png', 'images/objects/portal2.png'])
        door = door_images[0]
        door_rect = pygame.Rect(500,10,200,50)
        door_sprite = 0
        door_speed_sprite = 0.2
        door_on = False

        while True:     
                for event in pygame.event.get():
                        exit_keys(event)
                        if event.type == KEYDOWN:
                                player.down_key(event.key)
                                if computer.can_entry():
                                        if computer.entry.set_keyboard(event):
                                                if computer.entry.get_message() == objetos.get_reply():
                                                        door_on = True
                                                else:
                                                        return False
                                                        
                        if event.type == KEYUP:
                                player.up_key(event.key)
                                                
                screen.fill((0,0,0))
                screen.blit(bg,(0,0))

                if door_on:
                        door = door_images[int(door_sprite)]
                        screen.blit(door, (door_rect.x, door_rect.y))
                        
                        door_sprite += door_speed_sprite
                        if int(door_sprite) >= len(door_images):
                                door_sprite = 0
                                
                        if door_rect.colliderect(player.get_collider()):
                                return True
                        
                screen.blit(computer.pc_img, computer.position())
                
                objetos.update_objects(screen, player.get_collider())
                        
                player.moving_player(screen)

                computer.interact(player.get_collider(), screen)

                dialog.stream(screen, player.get_position())

                pygame.display.update()
                clock.tick(fps)


if __name__ == '__main__':
        print(Game_Room())
        pygame.quit()

