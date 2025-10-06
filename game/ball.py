import pygame
import random

class Ball:
    def __init__(self, x, y, width, height, screen_width, screen_height):
        self.original_x = x
        self.original_y = y
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.velocity_x = random.choice([-5, 5])
        self.velocity_y = random.choice([-3, 3])

    def move(self):
        self.x += self.velocity_x
        self.y += self.velocity_y

        wall_hit = False
        if self.y <= 0 or self.y + self.height >= self.screen_height:
            self.velocity_y *= -1
            wall_hit = True
            
        return wall_hit # Returns True if a wall was hit (for Task 4 sound)

    def check_collision(self, player, ai):
        """Refined collision check (Task 1)."""
        
        collision_occurred = False
        
        # Check collision with Player paddle
        if self.rect().colliderect(player.rect()):
            # Only reverse if moving towards the paddle (left)
            if self.velocity_x < 0:
                self.velocity_x *= -1
                collision_occurred = True

        # Check collision with AI paddle
        elif self.rect().colliderect(ai.rect()):
            # Only reverse if moving towards the paddle (right)
            if self.velocity_x > 0:
                self.velocity_x *= -1
                collision_occurred = True
                
        return collision_occurred # Returns True if a paddle was hit (for Task 4 sound)

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.velocity_x *= -1
        self.velocity_y = random.choice([-3, 3])

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)