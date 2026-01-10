import pygame
import random
import sys
import asyncio

pygame.init()

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
GROUND_HEIGHT = 100
PIPE_WIDTH = 70  # Slightly thinner pipes
PIPE_GAP = 200   # Wider gap for easier gameplay
BIRD_SIZE = 34   # Slightly smaller bird
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SKY_BLUE = (135, 206, 235)
PIPE_GREEN = (34, 177, 76)
PIPE_DARK_GREEN = (14, 100, 35)
BIRD_YELLOW = (255, 215, 0)
BIRD_ORANGE = (255, 140, 0)
GROUND_BROWN = (222, 184, 135)
GROUND_LINE = (139, 69, 19)

class Bird:
    def __init__(self):
        self.x = 80
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0
        self.gravity = 0.5  # Reduced gravity for easier control
        self.jump_strength = -8 # Reduced jump strength to match gravity
        self.size = BIRD_SIZE
        self.rotation = 0
        
    def update(self):
        self.velocity += self.gravity
        self.y += self.velocity
        
        # Rotation logic
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
        # forgiving collision box (smaller than visual)
        return pygame.Rect(self.x + 5, self.y + 5, self.size - 10, self.size - 10)
    
    def draw(self, screen):
        # Draw Body
        center = (int(self.x + self.size//2), int(self.y + self.size//2))
        pygame.draw.circle(screen, BIRD_YELLOW, center, self.size//2)
        pygame.draw.circle(screen, BIRD_ORANGE, center, self.size//2, 2) # Outline
        
        # Draw Eye
        eye_pos = (int(self.x + self.size//2 + 8), int(self.y + self.size//2 - 8))
        pygame.draw.circle(screen, WHITE, eye_pos, 8)
        pygame.draw.circle(screen, BLACK, (eye_pos[0] + 2, eye_pos[1]), 3)
        
        # Draw Wing
        wing_rect = (self.x + 5, self.y + 20, 18, 12)
        pygame.draw.ellipse(screen, WHITE, wing_rect)
        pygame.draw.ellipse(screen, BLACK, wing_rect, 1)

        # Draw Beak
        beak_points = [(self.x + self.size - 5, self.y + 15), 
                       (self.x + self.size + 5, self.y + 20), 
                       (self.x + self.size - 5, self.y + 25)]
        pygame.draw.polygon(screen, BIRD_ORANGE, beak_points)
        pygame.draw.polygon(screen, BLACK, beak_points, 1)

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
        # Top Pipe
        pygame.draw.rect(screen, PIPE_GREEN, self.top_rect)
        pygame.draw.rect(screen, PIPE_DARK_GREEN, self.top_rect, 2)
        # Top Pipe Cap
        cap_height = 25
        pygame.draw.rect(screen, PIPE_GREEN, (self.x - 4, self.height - cap_height, PIPE_WIDTH + 8, cap_height))
        pygame.draw.rect(screen, PIPE_DARK_GREEN, (self.x - 4, self.height - cap_height, PIPE_WIDTH + 8, cap_height), 2)

        # Bottom Pipe
        pygame.draw.rect(screen, PIPE_GREEN, self.bottom_rect)
        pygame.draw.rect(screen, PIPE_DARK_GREEN, self.bottom_rect, 2)
        # Bottom Pipe Cap
        pygame.draw.rect(screen, PIPE_GREEN, (self.x - 4, self.height + PIPE_GAP, PIPE_WIDTH + 8, cap_height))
        pygame.draw.rect(screen, PIPE_DARK_GREEN, (self.x - 4, self.height + PIPE_GAP, PIPE_WIDTH + 8, cap_height), 2)
        
        # Highlights for 3D effect
        pygame.draw.line(screen, (100, 200, 100), (self.x + 10, 0), (self.x + 10, self.height - cap_height), 3)
        pygame.draw.line(screen, (100, 200, 100), (self.x + 10, self.height + PIPE_GAP + cap_height), (self.x + 10, SCREEN_HEIGHT), 3)

    def collides_with(self, bird):
        bird_rect = bird.get_rect()
        return bird_rect.colliderect(self.top_rect) or bird_rect.colliderect(self.bottom_rect)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Flappy Bird - By Yuvraj Chopra")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 40)
        self.score_font = pygame.font.Font(None, 60)
        
        # Cloud data for background
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
        if self.pipe_timer > 100: # Slower pipe generation
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
            
            # Simple cloud drawing (3 circles)
            pygame.draw.circle(self.screen, WHITE, (int(cloud['x']), int(cloud['y'])), 30)
            pygame.draw.circle(self.screen, WHITE, (int(cloud['x'] - 20), int(cloud['y'] + 10)), 25)
            pygame.draw.circle(self.screen, WHITE, (int(cloud['x'] + 20), int(cloud['y'] + 10)), 25)

    def draw_background(self):
        self.screen.fill(SKY_BLUE)
        self.draw_clouds()
        
        # Ground
        ground_rect = pygame.Rect(0, SCREEN_HEIGHT - GROUND_HEIGHT, SCREEN_WIDTH, GROUND_HEIGHT)
        pygame.draw.rect(self.screen, GROUND_BROWN, ground_rect)
        
        # Decoration on ground (Grass line)
        pygame.draw.line(self.screen, (100, 200, 100), (0, SCREEN_HEIGHT - GROUND_HEIGHT), (SCREEN_WIDTH, SCREEN_HEIGHT - GROUND_HEIGHT), 10)
        
        # Moving ground effect
        offset = -(pygame.time.get_ticks() // 5) % 20
        for i in range(offset, SCREEN_WIDTH, 20):
             pygame.draw.line(self.screen, GROUND_LINE, (i, SCREEN_HEIGHT - GROUND_HEIGHT), (i - 10, SCREEN_HEIGHT), 2)

    def draw_ui(self):
        if self.game_started:
             score_text = self.score_font.render(str(self.score), True, WHITE)
             # Shadow
             score_shadow = self.score_font.render(str(self.score), True, (0,0,0, 50))
             self.screen.blit(score_shadow, (SCREEN_WIDTH//2 - 18, 52))
             self.screen.blit(score_text, (SCREEN_WIDTH//2 - 20, 50))
        
        if not self.game_started and not self.game_over:
            # Title Screen
            title_text = self.font.render("FLAPPY BIRD", True, BIRD_ORANGE)
            start_text = self.font.render("Press SPACE", True, WHITE)
            
            title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
            start_rect = start_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 20))
            
            self.screen.blit(title_text, title_rect)
            self.screen.blit(start_text, start_rect)
        
        if self.game_over:
            # Game Over Box
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
             
            # Mouse support for web
            if event.type == pygame.MOUSEBUTTONDOWN:
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
