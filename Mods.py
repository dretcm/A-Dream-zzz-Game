import math, pygame, random

pygame.init()

class Direccion:  # Padre
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
        
        def calcular_angulo(self):
                # [0 - 180]   : +
                # (180 - 360] : -
                
                # atan2: [-pi,pi] # atan: [-pi/2, pi/2]
                self.theta =  math.degrees(math.atan2(self.resultante_y, self.resultante_x))
                
                if self.theta < 0:
                        self.theta += 360.0
                                
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
        
        def __init__(self):
                self.collider= pygame.Rect(0,0,self.radius,self.radius)
        
        def shoot(self, screen):
                if self.magnitud < self.limit:
                        self.mover_collider()

                        pygame.draw.circle(screen, (0,0, 0), self.get_position(), self.radius)
                        
                        self.magnitud += self.speed
                        
                        return True
                else:
                        return False
                
        def init_shoot(self, vector_position, player_position):
                self.h, self.k = player_position
                self.x, self.y = vector_position
                
                self.vector_respecto_al_origen()
                self.calcular_angulo()

        def deactivate_bullet(self):
                self.magnitud = self.limit + 1 


class Gun:
        bullets = []
        bullets_activate = []

        store = 3
        limit_store = 30
        ammunition = 3

        def update_gun(self, screen, player_position):
                pygame.draw.aaline(screen, (0,255,0), player_position, pygame.mouse.get_pos())
                if self.bullets:
                        for bullet in self.bullets:
                                if bullet.shoot(screen):
                                        self.bullets_activate.append(bullet)
                                        
                        self.bullets = self.bullets_activate.copy() # usamos ".copy()" para evitar la mismidad
                        self.bullets_activate = []

        def activate_gun(self, vector_position, player_position):
                if self.store > 0:
                        bullet = Bullet()
                        bullet.init_shoot(vector_position, player_position)
                        
                        self.bullets.append(bullet)

                        self.store -= 1

##        def reload_ammunition(self):
##                for i in range(self.ammunition):
##                        if self.limit_store > self.store:
##                                self.store += 1
##                        else:
##                                break
                        
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
        range_speed = [2, 5, 10, 17]
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
                
                        

        
        
                

