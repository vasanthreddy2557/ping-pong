import pygame
from game.game_engine import GameEngine

# --- Initialization ---
pygame.init()
# Initialize mixer for sound effects (Task 4)
try:
    pygame.mixer.init()
except pygame.error as e:
    print(f"Warning: Could not initialize mixer: {e}")

# Screen dimensions
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong - Pygame Version")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Fonts (For Game Over/Replay Screen)
FONT = pygame.font.Font(None, 74) # Main text (Winner)
SMALL_FONT = pygame.font.Font(None, 36) # Replay options

# Clock
clock = pygame.time.Clock()
FPS = 60

# Game State Management (Task 2 & 3)
GAME_RUNNING = 1
GAME_OVER = 2
game_state = GAME_RUNNING
SCORE_TARGET = 5 # Default winning score (Best of 5)

# Game Engine Setup
engine = GameEngine(WIDTH, HEIGHT)


def display_message(surface, text, font, color, y_offset=0):
    """Utility function to render centered text."""
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + y_offset))
    surface.blit(text_surface, text_rect)


def handle_game_over(screen):
    """Handles rendering and input for the Game Over/Replay Screen (Task 2 & 3)."""
    global game_state, SCORE_TARGET

    # 1. Determine Winner and Display Message (Task 2)
    if engine.player_score >= SCORE_TARGET:
        winner_text = "Player Wins!"
    elif engine.ai_score >= SCORE_TARGET:
        winner_text = "AI Wins!"
    else:
        return True # Should not happen

    screen.fill(BLACK)
    display_message(screen, winner_text, FONT, WHITE)

    # 2. Display Replay Options (Task 3)
    display_message(screen, "Play Best of:", SMALL_FONT, WHITE, 50)
    display_message(screen, "(3) Best of 3 | (5) Best of 5 | (7) Best of 7 | (ESC) Exit", SMALL_FONT, WHITE, 100)

    # 3. Handle Input for Replay/Exit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False # Signal main loop to quit

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # Add a small delay before closing pygame (Task 2 requirement)
                pygame.time.wait(500)
                return False # Exit
            elif event.key == pygame.K_3:
                SCORE_TARGET = 3
                engine.reset_game()
                game_state = GAME_RUNNING
            elif event.key == pygame.K_5:
                SCORE_TARGET = 5
                engine.reset_game()
                game_state = GAME_RUNNING
            elif event.key == pygame.K_7:
                SCORE_TARGET = 7
                engine.reset_game()
                game_state = GAME_RUNNING

    pygame.display.flip()
    clock.tick(FPS)
    return True # Continue the main loop


def main():
    global game_state

    running = True
    while running:
        # Check if a winner has been decided (Task 2)
        if game_state == GAME_RUNNING and (engine.player_score >= SCORE_TARGET or engine.ai_score >= SCORE_TARGET):
            # Transition to Game Over State
            game_state = GAME_OVER

        if game_state == GAME_RUNNING:
            # --- Main Game Loop Logic ---
            SCREEN.fill(BLACK)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            engine.handle_input()
            engine.update() 
            engine.render(SCREEN)
            
            pygame.display.flip()
            clock.tick(FPS)

        elif game_state == GAME_OVER:
            # --- Game Over/Replay Loop Logic (Task 2 & 3) ---
            running = handle_game_over(SCREEN)

    # The game loop has exited
    pygame.quit()


if __name__ == "__main__":
    main()