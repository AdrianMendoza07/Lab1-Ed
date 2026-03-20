import pygame

class Button:
    def __init__(self, text, width, height, pos, font):
        self.text = text
        self.width = width
        self.height = height
        self.font = font

        # Rect
        self.rect = pygame.Rect(0, 0, width, height)
        self.rect.center = pos

        # Colores 
        self.baseColor  = (20, 20, 50, 160)   # translucent dark blue
        self.hoverColor = (60, 20, 90)        # neon purple
        self.clickColor = (0, 255, 200)       # neon cyan
        self.textColor  = (220, 240, 255)

        # Colores glow
        self.glowHover = (160, 80, 255)
        self.glowClick = (0, 255, 200)

        # Estado
        self.currentColor = self.baseColor
        self.is_pressed = False
        self.press_time = 0
        self.delay = 75  # ms

    # Manejo de clicks
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.is_pressed = True
                self.press_time = pygame.time.get_ticks()
                self.currentColor = self.clickColor
                return True
        return False

    # Update
    def update(self, mouse_pos):
        if not self.is_pressed:
            if self.rect.collidepoint(mouse_pos):
                self.currentColor = self.hoverColor
            else:
                self.currentColor = self.baseColor

    # Click termina
    def is_ready(self):
        if self.is_pressed:
            now = pygame.time.get_ticks()
            if now - self.press_time >= self.delay:
                self.is_pressed = False
                return True
        return False

    # Draw
    def draw(self, screen):
        # transparente 
        button_surf = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)

        # Draw base
        pygame.draw.rect(
            button_surf,
            self.currentColor,
            (0, 0, self.rect.width, self.rect.height),
            border_radius=12
        )

        # Glow effect
        if self.currentColor == self.hoverColor:
            self.draw_glow(screen, self.glowHover)
        elif self.currentColor == self.clickColor:
            self.draw_glow(screen, self.glowClick)

        
        screen.blit(button_surf, self.rect.topleft)

        # Borde
        pygame.draw.rect(
            screen,
            (160, 80, 255),
            self.rect,
            2,
            border_radius=12
        )

        # Texto
        text_surface = self.font.render(self.text, True, self.textColor)
        text_rect = text_surface.get_rect(center=self.rect.center)

        # texto glow
        glow = self.font.render(self.text, True, (0, 255, 200))
        screen.blit(glow, (text_rect.x - 1, text_rect.y))

        screen.blit(text_surface, text_rect)

    # Efecto de glow
    def draw_glow(self, screen, color):
        for i in range(8, 0, -2):
            glow_rect = self.rect.inflate(i * 4, i * 4)
            glow_surf = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)

            pygame.draw.rect(
                glow_surf,
                (*color, 30),  # alpha glow
                glow_surf.get_rect(),
                border_radius=14
            )

            screen.blit(glow_surf, glow_rect.topleft)