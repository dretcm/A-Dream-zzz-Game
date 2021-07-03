import pygame, time

pygame.init()

def load_images(paths, size=None, bg_color=None):
        images = [pygame.image.load(img) for img in paths]
        if size:
                images = [pygame.transform.scale(img, size) for img in images]
        if bg_color:
                for img in images:
                        img.set_colorkey(bg_color)
        return images

                                        

class Dialog:
        def __init__(self, color):
                self.font = pygame.font.Font(None,30)
                self.color = color
                
                self.begin = time.time()
                self.pos = 0
                self.pos_list = 0
                
                self.fast = 0.2
                self.guion = None
                
        def reset(self):
                self.begin = time.time()
                self.pos = 0
                self.pos_list += 1
                
        def text(self):
                now = time.time()
                if now - self.begin > self.fast:
                        self.pos += 1
                        self.begin = now
                if self.pos >= len(self.guion[self.pos_list]) + 3:
                        self.reset()
                msg = self.font.render(self.guion[self.pos_list][:self.pos], 1, self.color)
                return msg

        def message(self, guion):
                self.guion = guion + ['']  # limit of messages
                self.pos_list = 0

        def stream(self, screen, position):
                if self.guion[self.pos_list] != '':
                        text = self.text()
                        screen.blit(text, (position[0]-50, position[1]-50))

