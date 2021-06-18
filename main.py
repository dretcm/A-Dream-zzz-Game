import pygame, sys
from pygame.locals import *
import random

from Mods import *


pygame.init()
pygame.mixer.init()

# boss:
class Boss(Direccion):
        width = 300
        height = 180

        speed = 17

        fase = 1

        win = False

        # fase aparicion:
        aparicion = 3

        state = True
        boss = False

        t = 0
        limit_t = 100

        # fase screamer:
        state_2 = True
        fondo = None
        grito = pygame.mixer.Sound("music/grito.mp3")
        limit_t2 = 100

        # boss con fuego
        end = pygame.mixer.Sound("music/boss_end.mp3")
        img_fuego = 'images/explocion.png'
        fuego = True
        
        def __init__(self, size_screen):
                self.size_screen = size_screen
                
                img = 'images/boss.png'
                self.boss_image = pygame.transform.scale(pygame.image.load(img), (self.width, self.height))

                img_fondo = 'images/screamer.png'
                self.fondo = pygame.transform.scale(pygame.image.load(img_fondo), self.size_screen)


        def reload_position(self):
                begin = -80
                
                if random.randint(0,1):
                        self.h = random.choice([begin, self.size_screen[0]+50])
                        self.k = random.randint(begin, self.size_screen[1]+50)
                else:
                        self.h = random.randint(begin, self.size_screen[0]+50)
                        self.k = random.choice([begin, self.size_screen[1]+50])

                self.collider = pygame.Rect(self.h, self.k, self.width, self.height)
                self.magnitud = self.speed
                
        
        def follow_player(self, screen, player_position):
                self.x, self.y = player_position
                self.h, self.k = self.get_position()
                
                self.vector_respecto_al_origen()
                self.calcular_angulo()

                self.mover_collider()

                screen.blit(self.boss_image, self.get_position())

        def update_boss(self, screen, player, pistol):
                if self.fase == 1:
                        self.fase_aparicion(screen, player, pistol)
                elif self.fase == 2:
                        if self.state_2:
                                self.generar_cubos()
                                self.grito.play()
                                self.state_2 = False
                        self.fase_screamer(screen, player, pistol)
                elif self.fase == 3:
                        self.fase_aparicion(screen, player, pistol)
                else:
                        self.win = True
                                                
        def fase_aparicion(self, screen, player, pistol):
                if self.aparicion == 0:
                        self.fase += 1
                        self.t = 0
                        self.aparicion = 1
                else:   
                        if self.state:
                                self.state = False
                                self.reload_position()
                        else:
                                self.follow_player(screen, player.get_position())
                                if self.collider.colliderect(player.get_collider()):
                                        player.set_player_live(False)
                                for bullet in pistol.get_colliders():
                                        if self.collider.colliderect(bullet.get_collider()):
                                                bullet.deactivate_bullet()
                                                self.magnitud = -self.speed
                                                        
                                if self.magnitud < 0:
                                        if self.t < self.limit_t:
                                                        self.t += 1
                                        else:
                                                self.t = 0
                                                self.reload_position()
                                                self.state = True
                                                self.aparicion -= 1
                                        if self.fase == 3 and self.fuego:
                                                self.boss_image = pygame.transform.scale(pygame.image.load(self.img_fuego), (self.width, self.height))
                                                self.fuego = False
                                                self.end.play()

        def fase_screamer(self, screen, player, pistol):
                if self.t < self.limit_t2:
                        cubos_activos = []
                        screen.blit(self.fondo, (0,0))
                        for cubo in self.cubos:
                                pygame.draw.rect(screen, (255,0,0), cubo)
                                state = True
                                for bullet in pistol.get_colliders():
                                        if cubo.colliderect(bullet.get_collider()):
                                                bullet.deactivate_bullet()
                                                state = False
                                if state:
                                        cubos_activos.append(cubo)
                        self.cubos = cubos_activos.copy()
                                                
                        if len(self.cubos) == 0:
                                self.fase += 1
                                self.t = 0
                                self.grito.stop()
                        self.t += 1
                else:
                        player.set_player_live(False)
                        
        def generar_cubos(self):
                self.cubos = []
                width = 100
                height = 80
                for i in range(3):
                        x, y = random.randint(0,self.size_screen[0]-50),random.randint(0,self.size_screen[1]-30)
                        rect = pygame.Rect(x,y,width,height)
                        self.cubos.append(rect)
        
        def get_activate_boss(self):
                return self.boss
        
        def activate_boss(self):
                self.boss = True
                
        def get_win(self):
                return self.win


        
# player:
class Player:
        live = True
        speed = 15

        left = False
        right = False
        up = False
        down = False

        width = 100
        height = 80
        player_image = pygame.transform.scale(pygame.image.load('images/player_1.png'), (width, height))

        sonido_f = pygame.mixer.Sound("music/muerte.mp3")

        def __init__(self, window_size):
        
                self.x = window_size[0]//2 - 45
                self.y = window_size[1]//2 - 25
                
                self.collider = pygame.Rect(self.x,self.y, self.width, self.height)
        
        def down_key(self,key):
                if key == K_a:
                        self.left = True
                if key == K_d:
                        self.right = True
                if key == K_w:
                        self.up = True
                if key == K_s:
                        self.down = True
                        
        def up_key(self,key):
                if key == K_a:
                        self.left = False
                if key == K_d:
                        self.right = False
                if key == K_w:
                        self.up = False
                if key == K_s:
                        self.down = False
                        
        def moving_player(self, screen):
                
                if self.left:
                        self.x -= self.speed
                if self.right:
                        self.x += self.speed
                if self.up:
                        self.y -= self.speed
                if self.down:
                        self.y += self.speed
                        
                self.collider.x = self.x
                self.collider.y = self.y
                screen.blit(self.player_image, self.get_position())
                
        def get_position(self):
                return (self.x, self.y)
        
        def set_position(self,x,y):
                self.x = x
                self.y = y

        def get_collider(self):
                return self.collider

        def set_player_live(self, live):
                self.live = live
                self.sonido_f.play()
                
        def player_live(self):
                return self.live


class Municion:    
        a = 0
        b = 0

        width = 80
        height = 50

        t = 0
        limit_t = 100

        state = False

        municion_image = pygame.transform.scale(pygame.image.load('images/jabon.png'), (width, height))
        collider = pygame.Rect(0,0,width,height)

        font = pygame.font.Font(None,50)

        sounds = [pygame.mixer.Sound("music/ara_ara.mp3"),
                  pygame.mixer.Sound("music/kudasai.mp3"),
                  pygame.mixer.Sound("music/arigato.mp3")]

        def __init__(self, window_size):
                self.limite_a = window_size[0] - 45
                self.limite_b = window_size[1] - 25

        
        def aparece_en_mapa(self, screen, player, pistol):
                if self.t > self.limit_t:
                        self.collider.x = random.randint(self.a,self.limite_a)
                        self.collider.y = random.randint(self.b,self.limite_b)
                        self.t = 0
                        self.state = True
                else:
                        if not self.state:
                                self.t += 1

                if self.state:
                        screen.blit(self.municion_image, self.get_position())

                if self.collider.colliderect(player.get_collider()) and self.state:
                        random.choice(self.sounds).play()
                        pistol.reload_ammunition()
                        self.state = False

                self.show_ammunition(pistol.get_ammunition(), screen)

        def show_ammunition(self, n, screen):
                message = self.font.render('PISTOL: '+ str(n), 1, (0,0, 0))
                screen.blit(message, (10,10))

        def get_position(self):
                return (self.collider.x, self.collider.y)


class Game:
        clock = pygame.time.Clock()

        WINDOW_SIZE = (1200,600)

        screen = pygame.display.set_mode(WINDOW_SIZE,0,32)

        pygame.mixer.music.load('music/naruto.mp3')
        pygame.mixer.music.set_volume(0.2)

        music_on = False
        limite = 10

        def run_game(self):
                if self.music_on:
                        self.background_music()
                        
                player = Player(self.WINDOW_SIZE)
                municion = Municion(self.WINDOW_SIZE)
                pistol = Gun()
                orda = Orda(self.WINDOW_SIZE)
                boss = Boss(self.WINDOW_SIZE)
                
                while True:
                        for event in pygame.event.get():
                                if event.type == QUIT:
                                        self.exit_game()
                                if event.type == KEYDOWN:
                                        player.down_key(event.key)
                                        if event.key == K_SPACE:
                                                pistol.activate_gun(pygame.mouse.get_pos(), player.get_position())
                                if event.type == KEYUP:
                                        player.up_key(event.key)

                        self.screen.fill((128, 128, 128))

                        if orda.get_score() < self.limite:
                                orda.update_enemys(self.screen, player, pistol)
                        else:
                                if boss.get_activate_boss():
                                        boss.update_boss(self.screen, player, pistol)
                                else:
                                        boss.activate_boss()
                                        orda.finish_orda()
                                if boss.get_win():
                                        self.restart_game(text=' GANASTE !!! continuar ?')

                        player.moving_player(self.screen)
                        if not player.player_live():
                                self.restart_game()
                        
                        pistol.update_gun(self.screen, player.get_position())
                        municion.aparece_en_mapa(self.screen, player, pistol)
                        
                        pygame.display.update()
                        self.clock.tick(30)
                        
        def restart_game(self, text=' Quieres jugar de nuevo? '):
                if self.music_on:
                        pygame.mixer.music.stop()
                        
                if self.push_button(text):
                        self.run_game()
                else:
                        self.exit_game()
                        
        def push_button(self, text ='nothing'):

                font = pygame.font.Font(None,70)
                on = False

                midle_x, midle_y = list(map(lambda x: x//2, self.WINDOW_SIZE))

                pos_yes = (midle_x-110, midle_y+50)
                yes = pygame.Rect(pos_yes[0], pos_yes[1], 100,60)
                message_yes = font.render('Yes', 1, (0,0,0))

                pos_no = (midle_x+20, midle_y+50)
                no = pygame.Rect(pos_no[0], pos_no[1], 100,60)
                message_no = font.render('No', 1, (0,0,0))
                
                message = font.render(text,1,(0,0,0))
                lenght = message.get_width()
                pos_msg = (midle_x//2,midle_y-40)

                self.screen.fill((0,0,0))

                while True:
                        for event in pygame.event.get():
                                if event.type == QUIT:
                                        self.exit_game()
                                if event.type == pygame.MOUSEBUTTONDOWN:
                                        if event.button == 1 and yes.collidepoint(event.pos):
                                                print('you clicked the button yes')
                                                on = True
                                                return on
                                                
                                if event.type == pygame.MOUSEBUTTONDOWN:
                                        if event.button == 1 and no.collidepoint(event.pos):
                                                print('you clicked the button no')
                                                return on
                                                
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
                pygame.mixer.music.play(loops=-1, start=6)
                        

if __name__ == '__main__':
        game = Game()
        game.music_on = game.push_button(text=' Quieres Musica de fondo ? ')
        game.run_game()
