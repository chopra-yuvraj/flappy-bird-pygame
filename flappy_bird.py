import pygame
import random
import sys

pygame.init()

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
GROUND_HEIGHT = 100
PIPE_WIDTH = 80
PIPE_GAP = 150
BIRD_SIZE = 40
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 128, 0)
BLUE = (135, 206, 250)
YELLOW = (255, 255, 0)
BROWN = (139, 69, 19)

class Bird:
    def __init__(self):
        self.x = 80
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0
        self.gravity = 0.8
        self.jump_strength = -12
        self.size = BIRD_SIZE
        
    def update(self):
        self.velocity += self.gravity
        self.y += self.velocity
        
        if self.y < 0:
            self.y = 0
            self.velocity = 0
        elif self.y > SCREEN_HEIGHT - GROUND_HEIGHT - self.size:
            self.y = SCREEN_HEIGHT - GROUND_HEIGHT - self.size
    
    def jump(self):
        self.velocity = self.jump_strength
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.size, self.size)
    
    def draw(self, screen):
        pygame.draw.circle(screen, YELLOW, (int(self.x + self.size//2), int(self.y + self.size//2)), self.size//2)
        pygame.draw.circle(screen, BLACK, (int(self.x + self.size//2 + 10), int(self.y + self.size//2 - 5)), 3)

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
        pygame.draw.rect(screen, GREEN, self.top_rect)
        pygame.draw.rect(screen, GREEN, self.bottom_rect)
        pygame.draw.rect(screen, GREEN, (self.x - 5, self.height - 20, PIPE_WIDTH + 10, 20))
        pygame.draw.rect(screen, GREEN, (self.x - 5, self.height + PIPE_GAP, PIPE_WIDTH + 10, 20))
    
    def collides_with(self, bird):
        bird_rect = bird.get_rect()
        return bird_rect.colliderect(self.top_rect) or bird_rect.colliderect(self.bottom_rect)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Flappy Bird - By Yuvraj Chopra")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
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
        if self.pipe_timer > 90: 
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
    
    def draw_background(self):
        self.screen.fill(BLUE)
        
        ground_rect = pygame.Rect(0, SCREEN_HEIGHT - GROUND_HEIGHT, SCREEN_WIDTH, GROUND_HEIGHT)
        pygame.draw.rect(self.screen, BROWN, ground_rect)
        
        for i in range(0, SCREEN_WIDTH, 20):
            pygame.draw.rect(self.screen, (100, 50, 0), (i, SCREEN_HEIGHT - GROUND_HEIGHT, 10, 10))
    
    def draw_ui(self):
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        if not self.game_started and not self.game_over:
            start_text = self.font.render("Press SPACE to start!", True, WHITE)
            text_rect = start_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            self.screen.blit(start_text, text_rect)
        
        if self.game_over:
            game_over_text = self.font.render("Game Over!", True, WHITE)
            restart_text = self.font.render("Press R to restart", True, WHITE)
            
            game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 20))
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 20))
            
            self.screen.blit(game_over_text, game_over_rect)
            self.screen.blit(restart_text, restart_rect)
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not self.game_started and not self.game_over:
                        self.game_started = True
                    elif not self.game_over:
                        self.bird.jump()
                        
                elif event.key == pygame.K_r and self.game_over:
                    self.reset_game()
                    
        return True
    
    def run(self):
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
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    print("Starting Flappy Bird...")
    print("Controls:")
    print("- SPACE: Jump/Start game")
    print("- R: Restart after game over")
    print("- Close window: Quit game")
    
    game = Game()
    game.run()