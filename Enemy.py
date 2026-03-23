import pygame

class Enemy:
    def __init__(self, delay_ms=500):
        self.frames = []
        for i in range(1, 11):
            img = pygame.image.load(f"assets/enemy/cop{i}.png").convert_alpha()
            img = pygame.transform.scale(img, (60, 60))  # ajusta tamaño
            self.frames.append(img)

        self.current_frame = 0
        self.animation_speed = 0.2  # controla velocidad

        self.speed = 6
        self.delay_ms = delay_ms

        self.spawn_time = pygame.time.get_ticks()
        self.active = False

        # Físicas simples
        self.vel_y = 0
        self.gravity = 1
        self.jump_force = -15
        self.on_ground = True

    def update(self, player_rect, obstacles):
        current_time = pygame.time.get_ticks()
        
        # Animación
        self.current_frame += self.animation_speed
        if self.current_frame >= len(self.frames):
            self.current_frame = 0  

        # Spawn delay
        if not self.active:
            if current_time - self.spawn_time >= self.delay_ms:
                self.active = True
                self.rect.midleft = (0, player_rect.centery)
            else:
                return False

        # Movimiento constante
        self.rect.x += self.speed

        # Seguir altura del jugador 
        self.rect.y += (player_rect.y - self.rect.y) * 0.1

        # DETECTAR obstáculo enfrente
        look_ahead = self.rect.copy()
        look_ahead.x += 60  # distancia de reacción

        for obstacle in obstacles:
            if look_ahead.colliderect(obstacle.rect):
                if self.on_ground:
                    self.vel_y = self.jump_force
                    self.on_ground = False

        # Aplicar gravedad
        self.vel_y += self.gravity
        self.rect.y += self.vel_y

        # Colisión con suelo (ajustar)
        ground_y = 300
        if self.rect.bottom >= ground_y:
            self.rect.bottom = ground_y
            self.vel_y = 0
            self.on_ground = True

        # Matar jugador
        if self.rect.colliderect(player_rect):
            return True

        return False
    
        

    def draw(self, screen):
        if self.active:
            frame = self.frames[int(self.current_frame)]
            screen.blit(frame, self.rect)