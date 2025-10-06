import pygame
import os
from .paddle import Paddle
from .ball import Ball

# Game Engine

WHITE = (255, 255, 255)

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100

        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height)

        self.player_score = 0
        self.ai_score = 0
        self.font = pygame.font.SysFont("Arial", 30)

        # --- Task 4: Load Sounds ---
        # Resolve assets directory relative to project root (sibling to this file's directory)
        try:
            project_root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            assets_dir = os.path.join(project_root_dir, 'assets')

            paddle_hit_path = os.path.join(assets_dir, 'paddle_hit.wav')
            wall_bounce_path = os.path.join(assets_dir, 'wall_bounce.wav')
            score_path = os.path.join(assets_dir, 'score.wav')

            # Debug info in case assets are missing/running from unexpected CWD
            if not os.path.isdir(assets_dir):
                print(f"Warning: assets directory not found at: {assets_dir}")
            else:
                print(f"Assets directory: {assets_dir}")
                print(f"paddle_hit.wav exists: {os.path.isfile(paddle_hit_path)}")
                print(f"wall_bounce.wav exists: {os.path.isfile(wall_bounce_path)}")
                print(f"score.wav exists: {os.path.isfile(score_path)}")

            self.paddle_hit_sound = pygame.mixer.Sound(paddle_hit_path)
            self.wall_bounce_sound = pygame.mixer.Sound(wall_bounce_path)
            self.score_sound = pygame.mixer.Sound(score_path)
        except (pygame.error, FileNotFoundError) as e:
            print(f"Error loading sound files. Ensure files exist in 'assets/'. Error: {e}")
            self.paddle_hit_sound = None
            self.wall_bounce_sound = None
            self.score_sound = None


    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move(-10, self.height)
        if keys[pygame.K_s]:
            self.player.move(10, self.height)

    def update(self):
        # 1. Wall Bounce (Plays sound if move returns True)
        wall_hit = self.ball.move()
        if wall_hit and self.wall_bounce_sound:
            self.wall_bounce_sound.play()
            
        # 2. Paddle Hit (Plays sound if check_collision returns True)
        paddle_hit = self.ball.check_collision(self.player, self.ai) 
        if paddle_hit and self.paddle_hit_sound:
            self.paddle_hit_sound.play()

        # 3. Scoring (Plays sound and resets ball)
        scored = False
        if self.ball.x <= 0:
            self.ai_score += 1
            self.ball.reset()
            scored = True
        elif self.ball.x >= self.width:
            self.player_score += 1
            self.ball.reset()
            scored = True
            
        if scored and self.score_sound:
            self.score_sound.play()

        self.ai.auto_track(self.ball, self.height)
        
    def reset_game(self):
        """Resets scores and the ball position for a new game (Task 3)."""
        self.player_score = 0
        self.ai_score = 0
        self.ball.reset()

    def render(self, screen):
        # Draw paddles and ball
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())
        pygame.draw.aaline(screen, WHITE, (self.width//2, 0), (self.width//2, self.height))

        # Draw score
        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width//4, 20))
        screen.blit(ai_text, (self.width * 3//4, 20))