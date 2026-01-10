import pygame
import random
import sys
import asyncio

# Global constants (Safe to define before init)
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
GROUND_HEIGHT = 100
PIPE_WIDTH = 70
PIPE_GAP = 200
BIRD_SIZE = 45   # Increased size for better Angry Bird look
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SKY_BLUE = (135, 206, 235)
PIPE_GREEN = (34, 177, 76)
PIPE_DARK_GREEN = (14, 100, 35)
BIRD_RED = (200, 0, 0)       # Angry Bird Red
BIRD_BELLY = (222, 184, 135) # Light shade for belly
BIRD_BEAK = (255, 165, 0)    # Orange beak
GROUND_BROWN = (222, 184, 135)
GROUND_LINE = (139, 69, 19)

class Bird:
    def __init__(self):
        self.x = 80
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0
        self.gravity = 0.5
        self.jump_strength = -8
        self.size = BIRD_SIZE
        self.rotation = 0
        
    def update(self):
        self.velocity += self.gravity
        self.y += self.velocity
        
        # Rotation based on velocity
        if self.velocity < 0:
            self.rotation = 25
        else:
            self.rotation = max(-90, self.rotation - 3)
        
        if self.y < 0:
            self.y = 0
            self.velocity = 0
        elif self.y > SCREEN_HEIGHT - GROUND_HEIGHT - self.size:
            self.y = SCREEN_HEIGHT - GROUND_HEIGHT - self.size
    
    def jump(self):
        self.velocity = self.jump_strength
        self.rotation = 45
    
    def get_rect(self):
        # Slightly broken hitbox for gameplay forgiveness
        # Hitbox is smaller than the visual bird
        return pygame.Rect(self.x + 8, self.y + 8, self.size - 16, self.size - 16)
    
    def draw(self, screen):
        center_x = int(self.x + self.size//2)
        center_y = int(self.y + self.size//2)
        radius = self.size // 2

        # Tail Feathers (Black) - Drawn first so they are behind body
        pygame.draw.polygon(screen, BLACK, [
            (center_x - radius + 5, center_y),
            (center_x - radius - 12, center_y - 10),
            (center_x - radius - 12, center_y + 10)
        ])

        # Body (Red)
        pygame.draw.circle(screen, BIRD_RED, (center_x, center_y), radius)
        # Outline
        pygame.draw.circle(screen, BLACK, (center_x, center_y), radius, 3)

        # Belly (Light patch at bottom)
        pygame.draw.circle(screen, BIRD_BELLY, (center_x, center_y + 10), radius - 8)

        # Eyes (White with Black pupils)
        eye_radius = 10
        left_eye_pos = (center_x + 2, center_y - 12)
        right_eye_pos = (center_x + 18, center_y - 12)
        
        # Left Eye
        pygame.draw.circle(screen, WHITE, left_eye_pos, eye_radius)
        pygame.draw.circle(screen, BLACK, left_eye_pos, eye_radius, 2) # Outline
        pygame.draw.circle(screen, BLACK, (left_eye_pos[0] + 3, left_eye_pos[1]), 4) # Pupil
        
        # Right Eye
        pygame.draw.circle(screen, WHITE, right_eye_pos, eye_radius)
        pygame.draw.circle(screen, BLACK, right_eye_pos, eye_radius, 2) # Outline
        pygame.draw.circle(screen, BLACK, (right_eye_pos[0] + 3, right_eye_pos[1]), 4) # Pupil

        # Eyebrows (The angry look - clear V shape)
        eyebrow_thick = 4 
        # V shape meeting in middle
        pygame.draw.line(screen, BLACK, (center_x - 6, center_y - 20), (center_x + 10, center_y - 6), eyebrow_thick)
        pygame.draw.line(screen, BLACK, (center_x + 10, center_y - 6), (center_x + 26, center_y - 20), eyebrow_thick)

        # Beak (Yellow/Orange Triangle)
        beak_points = [
            (center_x + 10, center_y + 2),   # Top center
            (center_x + 28, center_y + 10),  # Tip
            (center_x + 10, center_y + 18)   # Bottom center
        ]
        pygame.draw.polygon(screen, BIRD_BEAK, beak_points)
        pygame.draw.polygon(screen, BLACK, beak_points, 2)

class Pipe:
    def __init__(self, x):
        self.x = x
        self.height = random.randint(50, SCREEN_HEIGHT - GROUND_HEIGHT - PIPE_GAP - 50)
        self.top_rect = pygame.Rect(x, 0, PIPE_WIDTH, self.height)
        self.bottom_rect = pygame.Rect(x, self.height + PIPE_GAP, PIPE_WIDTH, SCREEN_HEIGHT - self.height - PIPE_GAP - GROUND_HEIGHT)
        self.passed = False
        
    def update(self, speed):
        self.x -= speed
        self.top_rect.x = self.x
        self.bottom_rect.x = self.x
        
    def draw(self, screen):
        # Top Pipe with 3D effect
        pygame.draw.rect(screen, PIPE_GREEN, self.top_rect)
        pygame.draw.rect(screen, PIPE_DARK_GREEN, self.top_rect, 2)
        
        cap_height = 25
        # Top Cap
        pygame.draw.rect(screen, PIPE_GREEN, (self.x - 4, self.height - cap_height, PIPE_WIDTH + 8, cap_height))
        pygame.draw.rect(screen, PIPE_DARK_GREEN, (self.x - 4, self.height - cap_height, PIPE_WIDTH + 8, cap_height), 2)

        # Bottom Pipe
        pygame.draw.rect(screen, PIPE_GREEN, self.bottom_rect)
        pygame.draw.rect(screen, PIPE_DARK_GREEN, self.bottom_rect, 2)
        
        # Bottom Cap
        pygame.draw.rect(screen, PIPE_GREEN, (self.x - 4, self.height + PIPE_GAP, PIPE_WIDTH + 8, cap_height))
        pygame.draw.rect(screen, PIPE_DARK_GREEN, (self.x - 4, self.height + PIPE_GAP, PIPE_WIDTH + 8, cap_height), 2)
        
        # Highlights
        pygame.draw.line(screen, (100, 200, 100), (self.x + 10, 0), (self.x + 10, self.height - cap_height), 3)
        pygame.draw.line(screen, (100, 200, 100), (self.x + 10, self.height + PIPE_GAP + cap_height), (self.x + 10, SCREEN_HEIGHT), 3)

    def collides_with(self, bird):
        bird_rect = bird.get_rect()
        return bird_rect.colliderect(self.top_rect) or bird_rect.colliderect(self.bottom_rect)

class Game:
    def __init__(self):
        # Initialize Pygame here, not globally, to be safer for headless builds
        try:
            pygame.init()
            pygame.font.init()
        except:
            pass # Handle potential headless issues gracefully
            
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Flappy Bird - By Yuvraj Chopra")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 40)
        self.score_font = pygame.font.Font(None, 60)
        
        self.clouds = []
        for i in range(5):
             self.clouds.append({
                 'x': random.randint(0, SCREEN_WIDTH),
                 'y': random.randint(20, 200),
                 'speed': random.uniform(0.5, 1.5)
             })
             
        self.reset_game()
        
    def reset_game(self):
        self.bird = Bird()
        self.pipes = []
        self.pipe_timer = 0
        self.score = 0
        self.game_over = False
        self.game_started = False
        
    def create_pipe(self):
        return Pipe(SCREEN_WIDTH)
    
    def update_pipes(self):
        pipe_speed = 3
        
        self.pipe_timer += 1
        if self.pipe_timer > 100: 
            self.pipes.append(self.create_pipe())
            self.pipe_timer = 0
            
        for pipe in self.pipes[:]:
            pipe.update(pipe_speed)
            
            if pipe.x + PIPE_WIDTH < 0:
                self.pipes.remove(pipe)
                
            if not pipe.passed and pipe.x + PIPE_WIDTH < self.bird.x:
                pipe.passed = True
                self.score += 1
                
            if pipe.collides_with(self.bird):
                self.game_over = True

    def draw_clouds(self):
        for cloud in self.clouds:
            cloud['x'] -= cloud['speed']
            if cloud['x'] < -100:
                cloud['x'] = SCREEN_WIDTH + 100
                cloud['y'] = random.randint(20, 200)
            
            # Simple cloud drawing
            pygame.draw.circle(self.screen, WHITE, (int(cloud['x']), int(cloud['y'])), 30)
            pygame.draw.circle(self.screen, WHITE, (int(cloud['x'] - 20), int(cloud['y'] + 10)), 25)
            pygame.draw.circle(self.screen, WHITE, (int(cloud['x'] + 20), int(cloud['y'] + 10)), 25)

    def draw_background(self):
        self.screen.fill(SKY_BLUE)
        self.draw_clouds()
        
        # Ground
        ground_rect = pygame.Rect(0, SCREEN_HEIGHT - GROUND_HEIGHT, SCREEN_WIDTH, GROUND_HEIGHT)
        pygame.draw.rect(self.screen, GROUND_BROWN, ground_rect)
        
        # Ground decoration
        pygame.draw.line(self.screen, (100, 200, 100), (0, SCREEN_HEIGHT - GROUND_HEIGHT), (SCREEN_WIDTH, SCREEN_HEIGHT - GROUND_HEIGHT), 10)
        
        # Moving ground
        offset = -(pygame.time.get_ticks() // 5) % 20
        for i in range(offset, SCREEN_WIDTH, 20):
             pygame.draw.line(self.screen, GROUND_LINE, (i, SCREEN_HEIGHT - GROUND_HEIGHT), (i - 10, SCREEN_HEIGHT), 2)

    def draw_ui(self):
        if self.game_started:
             score_text = self.score_font.render(str(self.score), True, WHITE)
             score_shadow = self.score_font.render(str(self.score), True, (0,0,0, 50))
             self.screen.blit(score_shadow, (SCREEN_WIDTH//2 - 18, 52))
             self.screen.blit(score_text, (SCREEN_WIDTH//2 - 20, 50))
        
        if not self.game_started and not self.game_over:
            title_text = self.font.render("FLAPPY BIRD", True, BIRD_RED)
            start_text = self.font.render("Press SPACE", True, WHITE)
            
            title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
            start_rect = start_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 20))
            
            self.screen.blit(title_text, title_rect)
            self.screen.blit(start_text, start_rect)
        
        if self.game_over:
            box_rect = pygame.Rect(50, 200, 300, 200)
            pygame.draw.rect(self.screen, GROUND_BROWN, box_rect, border_radius=10)
            pygame.draw.rect(self.screen, WHITE, box_rect, 3, border_radius=10)
            
            game_over_text = self.font.render("GAME OVER", True, WHITE)
            score_text = self.font.render(f"Score: {self.score}", True, BLACK)
            restart_text = self.font.render("Press R to Restart", True, WHITE)
            
            self.screen.blit(game_over_text, (box_rect.centerx - game_over_text.get_width()//2, box_rect.y + 30))
            self.screen.blit(score_text, (box_rect.centerx - score_text.get_width()//2, box_rect.y + 80))
            self.screen.blit(restart_text, (box_rect.centerx - restart_text.get_width()//2, box_rect.y + 140))
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not self.game_started and not self.game_over:
                        self.game_started = True
                        self.bird.jump()
                    elif not self.game_over:
                        self.bird.jump()
                        
                elif event.key == pygame.K_r and self.game_over:
                    self.reset_game()
            
            # Mouse click and touch support for mobile
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not self.game_started and not self.game_over:
                    self.game_started = True
                    self.bird.jump()
                elif not self.game_over:
                    self.bird.jump()
                elif self.game_over:
                   self.reset_game()
            
            # Touch support for mobile devices (via pygame events)
            if event.type == pygame.FINGERDOWN:
                if not self.game_started and not self.game_over:
                    self.game_started = True
                    self.bird.jump()
                elif not self.game_over:
                    self.bird.jump()
                elif self.game_over:
                   self.reset_game()

        return True
    
    async def run(self):
        running = True
        
        while running:
            running = self.handle_events()
            
            if self.game_started and not self.game_over:
                self.bird.update()
                self.update_pipes()
                
                if (self.bird.y <= 0 or 
                    self.bird.y >= SCREEN_HEIGHT - GROUND_HEIGHT - self.bird.size):
                    self.game_over = True
            
            self.draw_background()
            
            for pipe in self.pipes:
                pipe.draw(self.screen)
            
            self.bird.draw(self.screen)
            
            self.draw_ui()
            
            pygame.display.flip()
            self.clock.tick(FPS)
            await asyncio.sleep(0)  # Critical for web compatibility
        
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    asyncio.run(game.run())
