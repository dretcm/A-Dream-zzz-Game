import pygame, sys
from pygame.locals import *
import random
from phase_room import Game_Room
from phase_shoot import Game_Shoot

pygame.init()
pygame.mixer.init()


class Game:
        clock = pygame.time.Clock()

        WINDOW_SIZE = (1300,650)

        screen = pygame.display.set_mode(WINDOW_SIZE,0,32)

        pygame.mixer.music.load('music/naruto.mp3')
        pygame.mixer.music.set_volume(0.2)

        music_on = False

        def run_game(self):
                self.background_music()
                        
                while not Game_Room(self.WINDOW_SIZE):
                        self.restart_game()
                        
                while not Game_Shoot(self.WINDOW_SIZE):
                        self.restart_game()

                if self.push_button(text='Ganaste!!! jugar de nuevo ?'):
                        self.run_game()
                else:
                        self.exit_game()
                        
        def restart_game(self, text=' Quieres jugar de nuevo? '):
                pygame.mixer.music.stop()
                        
                if not self.push_button(text):
                        self.exit_game()
                        
                self.background_music()
                        
        def push_button(self, text ='nothing'):

                font = pygame.font.Font(None,70)

                midle_x, midle_y = list(map(lambda x: x//2, self.WINDOW_SIZE))

                pos_yes = (midle_x-110, midle_y+50)
                yes = pygame.Rect(pos_yes[0], pos_yes[1], 90,50)
                message_yes = font.render('Yes', 1, (0,0,0))

                pos_no = (midle_x+20, midle_y+50)
                no = pygame.Rect(pos_no[0], pos_no[1], 80,50)
                message_no = font.render('No', 1, (0,0,0))
                
                message = font.render(text,1,(0,0,0))
                lenght = message.get_width()
                pos_msg = (midle_x//2,midle_y-40)

                self.screen.fill((0,0,0))

                while True:
                        for event in pygame.event.get():
                                if event.type == QUIT:
                                        self.exit_game()
                                if event.type == MOUSEBUTTONDOWN:
                                        if event.button == 1 and yes.collidepoint(event.pos):
                                                return True
                                        if event.button == 1 and no.collidepoint(event.pos):
                                                return False
                                                
                        pygame.draw.rect(self.screen, (255,100,0), yes)
                        self.screen.blit(message_yes, pos_yes)
                        
                        pygame.draw.rect(self.screen, (255,100,0), no)
                        self.screen.blit(message_no, pos_no)
                        
                        pygame.draw.rect(self.screen, (255,255,255), [pos_msg[0], pos_msg[1],lenght, 60])
                        self.screen.blit(message, pos_msg)
                        
                        pygame.display.update()
                        self.clock.tick(30)
                        
        def exit_game(self):
                pygame.quit()
                sys.exit()

        def background_music(self):
                if self.music_on:
                        pygame.mixer.music.play(loops=-1, start=6)
                        

if __name__ == '__main__':
        game = Game()
        game.music_on = game.push_button(text=' Quieres Musica de fondo ? ')
        game.run_game()
