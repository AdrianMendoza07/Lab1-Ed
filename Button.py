import pygame

class Button:
    def __init__(self, text, width, height, pos, font):
        self.text = text
        self.width = width
        self.height = height
        self.pos = pos # (x,y)
        self.font = font
        
        self.rect = pygame.Rect(0, 0, width, height)
        self.rect.center = pos
        
        self.baseColor=(20, 20, 40)
        self.hoverColor=(0, 255, 180)
        self.textColor=(225, 225, 225)
        self.clickedColor=(255,50,200)
        
        self.currentColor = self.baseColor
        
    def draw(self, screen):
        # Efecto visual en Hover
        if self.currentColor == self.hoverColor:
            for i in range(8, 0, -2):
                glow_rect = self.rect.inflate(i*2, i*2)
                glow_surf = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
                pygame.draw.rect(glow_surf, (*self.hoverColor, 10), glow_surf.get_rect(), border_radius=10)
                screen.blit(glow_surf, glow_rect.topleft)
        
        #Draw boton
        pygame.draw.rect(screen, self.currentColor, self.rect, border_radius = 10)
        
        #Render texto
        text_surface = self.font.render(self.text, True, self.textColor)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
    
    def update(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                self.currentColor = self.clickedColor
                
            else:
                self.currentColor = self.hoverColor
        else:
            self.currentColor = self.baseColor
            
    def isClicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.rect.collidepoint(event.pos):
                    return True                    
        
        return False
            

