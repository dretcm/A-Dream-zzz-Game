import pygame, sys
from pygame.locals import *
import random, math

from player import Player
from utils import Dialog, exit_keys


pygame.init()
pygame.mixer.init()


class Direccion:  # base class
        resultante_x = 0
        resultante_y = 0
        
        x = 0
        y = 0
        
        h = 0
        k = 0
        
        theta = 0
        x_cos = 0
        y_sin = 0
        
        magnitud = 0

        collider = pygame.Rect(0,0,0,0)
        
        def mover_collider(self):
                self.collider.x = (self.magnitud * self.x_cos) + self.h
                self.collider.y = (self.magnitud * self.y_sin) + self.k
                
        def vector_respecto_al_origen(self):
                # (resultante_x, resultante_y) = (x - h, y - k)
                self.resultante_x = self.x - self.h
                self.resultante_y = self.y - self.k
        
        def calcular_theta(self):
                # [0 - 180]   : +
                # (180 - 360] : -
                
                # atan2: [-pi,pi] # atan: [-pi/2, pi/2]
                self.theta =  math.degrees(math.atan2(self.resultante_y, self.resultante_x))
                
                if self.theta < 0:
                        self.theta += 360.0
                        
        def calcular_angulo(self):
                self.calcular_theta()
                self.x_cos = math.cos(math.radians(self.theta))
                self.y_sin = math.sin(math.radians(self.theta))

        def get_collider(self):
                return self.collider
        
        def get_position(self):
                return (self.collider.x, self.collider.y)
        

class Bullet(Direccion):  # Hijo(Padre) : hereda los atributos y metodos del padre.
        speed = 25
        limit = 700

        radius = 10
        surf = pygame.Surface((radius*2,radius*2))
        pygame.draw.circle(surf, (255,0,0), (radius,radius), radius)
        surf.set_colorkey((0,0,0))
        
        def __init__(self, vector_position, player_position):
                self.collider= pygame.Rect(0,0,self.radius*2,self.radius*2)
                
                self.h, self.k = player_position
                self.x, self.y = vector_position
                
                self.vector_respecto_al_origen()
                self.calcular_angulo()
                
        def shoot(self, screen):
                if self.magnitud < self.limit:
                        self.mover_collider()

                        x,y = tuple(map(lambda pos: pos+self.radius, self.get_position()))
                        pygame.draw.circle(screen, (255,255, 0), (x,y), self.radius//2)
                        screen.blit(self.surf, self.get_position(), special_flags=pygame.BLEND_RGB_ADD)
                        
                        self.magnitud += self.speed
                        
                        return True
                else:
                        return False

        def deactivate_bullet(self):
                self.magnitud = self.limit + 1 


class Gun(Direccion):
        bullets = []
        bullets_activate = []

        store = 3
        limit_store = 30
        ammunition = 3

        cursor = pygame.image.load('images/cursor.png')
        cursor.set_colorkey((255,255,255))

        sound = pygame.mixer.Sound('music/shoot_sound.mp3')

        def __init__(self, player):
                pygame.mouse.set_visible(False)
                self.player_size = (player.width//2 - 20, player.height//2 - 10)
                self.gun_img = pygame.transform.scale(pygame.image.load('images/gun2.png'), (40,40))
                

        def gun_blit(self, screen, player_position):
                self.h, self.k = player_position
                self.x, self.y = pygame.mouse.get_pos()
                
                self.vector_respecto_al_origen()
                self.calcular_theta()

                aux_img = pygame.transform.rotate(self.gun_img, 360-self.theta)

                midle = self.get_midle(player_position)

                mouse_x, mouse_y = pygame.mouse.get_pos()
                
                pygame.draw.aaline(screen, (0,255,0), (midle[0]+10, midle[1]+10), (mouse_x, mouse_y))
                screen.blit(aux_img, midle)

                screen.blit(self.cursor, (mouse_x-10, mouse_y-10))
                

        def update_gun(self, screen, player_position):
                self.gun_blit(screen, player_position)
                
                if self.bullets:
                        for bullet in self.bullets:
                                if bullet.shoot(screen):
                                        self.bullets_activate.append(bullet)
                                        
                        self.bullets = self.bullets_activate.copy() # usamos ".copy()" para evitar la mismidad
                        self.bullets_activate = []

        def activate_gun(self, vector_position, player_position):
                if self.store > 0:
                        self.sound.play()
                        midle = self.get_midle(player_position)
                        bullet = Bullet(vector_position, midle)
                        
                        self.bullets.append(bullet)

                        self.store -= 1

        def get_midle(self, player_position):
                return tuple(map(lambda x,y: x+y, player_position, self.player_size))
                        
        def reload_ammunition(self, i=0):  # recursividad
                if self.ammunition == i:
                        pass
                else:
                        if self.store < self.limit_store:
                                self.store += 1
                                self.reload_ammunition(i+1)

                        
        def get_ammunition(self):
                return self.store

        def get_colliders(self):
                return self.bullets
        
        
class Enemy(Direccion):
        range_speed = [5, 10, 15, 20]
        width = 100
        height = 80
        
        def __init__(self, size_screen):
                begin = -10
                
                if random.randint(0,1):
                        self.h = random.choice([begin, size_screen[0]])
                        self.k = random.randint(begin, size_screen[1])
                else:
                        self.h = random.randint(begin, size_screen[0])
                        self.k = random.choice([begin, size_screen[1]])

                self.collider = pygame.Rect(self.h, self.k, self.width, self.height)
                
                img = random.choice(['images/otaku_1.png', 'images/otaku_2.png','images/viejo.png','images/rosel.png'])
                self.enemy_image = pygame.transform.scale(pygame.image.load(img), (self.width, self.height))
                
                self.magnitud = random.choice(self.range_speed)
        
        def follow_player(self, screen, player_position):
                self.x, self.y = player_position
                self.h, self.k = self.get_position()
                
                self.vector_respecto_al_origen()
                self.calcular_angulo()

                self.mover_collider()

                screen.blit(self.enemy_image, self.get_position())


class Orda:
        enemys = []
        enemys_activate = []
        
        t = 0
        limit_t = 50

        score = 0
        font = pygame.font.Font(None,50)
        
        def __init__(self, size_screen):
                self.size_screen = size_screen

        def update_enemys(self, screen, player, pistol):
                for enemy in self.enemys:
                        enemy.follow_player(screen, player.get_position())

                        state = True
                        for bullet in pistol.get_colliders():
                                if enemy.get_collider().colliderect(bullet.get_collider()):
                                        bullet.deactivate_bullet()
                                        state = False
                                        #enemy.magnitud = -5
                        if state:
                               self.enemys_activate.append(enemy)
                        else:
                                self.score += 1
                               
                        if enemy.get_collider().colliderect(player.get_collider()):
                                print('end game')
                                player.set_player_live(False)
                                
                self.enemys = self.enemys_activate.copy()  # usamos ".copy()" para evitar la mismidad
                self.enemys_activate = []

                if self.t < self.limit_t:
                        self.t += 1
                else:
                        self.activate_enemy()
                        self.t = 0

                self.show_score(screen)

        def activate_enemy(self):
                enemy = Enemy(self.size_screen)
                self.enemys.append(enemy)

        def show_score(self, screen):
                message = self.font.render('simpaticos: '+ str(self.score), 1, (0,0, 0))
                screen.blit(message, (self.size_screen[0]-250,10))

        def get_score(self):
                return self.score
        def finish_orda(self):
                del(self.enemys)

                
# boss:
class Boss(Direccion):
        width = 300
        height = 180

        speed = 20

        fase = 1

        win = False

        # fase aparicion:
        boss_sound = pygame.mixer.Sound('music/boss_sound.mp3')
        boss_hurt = pygame.mixer.Sound('music/boss_hurt.mp3')
        boss_hurt.set_volume(0.5)
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

        eye_boss = pygame.image.load('images/heart_boss.png')
        eye_boss.set_colorkey((255,255,255))

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
                                self.boss_sound.play()
                                self.hurt = True
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
                                        if self.fase == 1 and self.hurt:
                                                self.boss_sound.stop()
                                                self.boss_hurt.play()
                                                self.hurt = False
                                        if self.fase == 3 and self.fuego:
                                                self.boss_image = pygame.transform.scale(pygame.image.load(self.img_fuego), (self.width, self.height))
                                                self.fuego = False
                                                self.end.play()

        def fase_screamer(self, screen, player, pistol):
                if self.t < self.limit_t2:
                        cubos_activos = []
                        screen.blit(self.fondo, (0,0))
                        for cubo in self.cubos:
                                screen.blit(self.eye_boss, cubo.topleft)
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


class Municion:    
        a = 0
        b = 0

        width = 50
        height = 40

        t = 0
        limit_t = 100

        state = False

        municion_image = pygame.transform.scale(pygame.image.load('images/ammunition.png'), (width, height))
        municion_image.set_colorkey((255,255,255))
        
        collider = pygame.Rect(0,0,width,height)

        font = pygame.font.Font(None,50)

        sound = pygame.mixer.Sound("music/reload_ammunition.mp3")


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
                        self.sound.play()
                        pistol.reload_ammunition()
                        self.state = False

                self.show_ammunition(pistol.get_ammunition(), screen)

        def show_ammunition(self, n, screen):
                message = self.font.render('PISTOL: '+ str(n), 1, (0,0, 0))
                screen.blit(message, (10,10))

        def get_position(self):
                return (self.collider.x, self.collider.y)


def Game_Shoot():
        clock = pygame.time.Clock()
        fps = 30

        screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        WINDOW_SIZE = pygame.display.get_window_size()

        limite = 10
                        
        player = Player(WINDOW_SIZE)
        municion = Municion(WINDOW_SIZE)
        pistol = Gun(player)
        orda = Orda(WINDOW_SIZE)
        boss = Boss(WINDOW_SIZE)

        dialog = Dialog((0,0,0))
        dialog.message(['aqui y ahora!!!', 'vengan!!!'])
                
        while True:
                for event in pygame.event.get():
                        exit_keys(event)
                        if event.type == KEYDOWN:
                                player.down_key(event.key)
                        if event.type == MOUSEBUTTONDOWN  and event.button == 1:
                                pistol.activate_gun(pygame.mouse.get_pos(), player.get_position())
                        if event.type == KEYUP:
                                player.up_key(event.key)

                screen.fill((128, 128, 128))

                if orda.get_score() < limite:
                        orda.update_enemys(screen, player, pistol)
                else:
                        if boss.get_activate_boss():
                                boss.update_boss(screen, player, pistol)
                        else:
                                boss.activate_boss()
                                orda.finish_orda()
                        if boss.get_win():
                                pygame.mouse.set_visible(True)
                                return True

                player.moving_player(screen)
                if not player.player_live():
                        pygame.mouse.set_visible(True)
                        return False
                        
                pistol.update_gun(screen, player.get_position())
                municion.aparece_en_mapa(screen, player, pistol)

                dialog.stream(screen, player.get_position())
                        
                pygame.display.update()
                clock.tick(fps)
                        

if __name__ == '__main__':
        print(Game_Shoot())
        pygame.quit()

