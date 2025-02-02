import pygame
import sys
import numpy as np
from typing import Tuple, Optional
import random
import math

# Initialize Pygame
pygame.init()

# Constants
WINDOW_SIZE = 800
BOARD_SIZE = 600
CELL_SIZE = BOARD_SIZE // 3

# Colors
BACKGROUND = (78, 29, 112)  # Deep purple
MENU_BG = (144, 58, 168)    # Bright purple
GRID_COLOR = (255, 214, 10)  # Bright yellow
PLAYER_X_COLOR = (255, 89, 94)  # Coral pink
PLAYER_O_COLOR = (10, 255, 157)  # Bright mint
HOVER_COLOR = (255, 214, 10, 100)  # Semi-transparent yellow
TEXT_COLOR = (255, 255, 255)  # Pure white
TEXT_SHADOW_COLOR = (40, 10, 60)  # Dark purple for text shadow
STATUS_TEXT_COLOR = (255, 236, 179)  # Light yellow for status text
BUTTON_COLOR = (255, 122, 89)  # Coral
BUTTON_HOVER_COLOR = (255, 157, 89)  # Light coral
WINNER_LINE_COLOR = (255, 214, 10)  # Bright yellow
STATUS_GLOW_COLOR = (144, 58, 168)  # Purple glow for better contrast
PARTICLE_COLORS = [(255, 89, 94), (10, 255, 157), (255, 214, 10), (255, 122, 89)]  # Vibrant colors

class AnimatedValue:
    def __init__(self, start=0, end=0, duration=20):
        self.start = start
        self.end = end
        self.duration = duration
        self.current = start
        self.progress = 0
        self.is_animating = False

    def animate_to(self, end):
        self.start = self.current
        self.end = end
        self.progress = 0
        self.is_animating = True

    def update(self):
        if self.is_animating:
            self.progress += 1
            progress_ratio = min(1, self.progress / self.duration)
            # Use ease-out cubic function for smooth animation
            t = 1 - (1 - progress_ratio) ** 3
            self.current = self.start + (self.end - self.start) * t
            if self.progress >= self.duration:
                self.is_animating = False
                self.current = self.end

class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.is_hovered = False
        self.scale = AnimatedValue(1.0, 1.0)
        self.alpha = AnimatedValue(255, 255)
        self.bounce_offset = 0
        self.bounce_speed = random.uniform(0.02, 0.03)  # Much slower bounce
        self.time_offset = random.uniform(0, 2 * math.pi)
        self.hover_glow = AnimatedValue(0, 0, duration=15)  # Smooth hover transition

    def draw(self, surface):
        self.scale.update()
        self.alpha.update()
        self.hover_glow.update()
        
        # Add a very subtle bounce effect
        self.bounce_offset = math.sin(pygame.time.get_ticks() * self.bounce_speed + self.time_offset) * 2
        
        # Create a scaled rect for hover effect
        scaled_width = int(self.rect.width * self.scale.current)
        scaled_height = int(self.rect.height * self.scale.current)
        scaled_x = self.rect.centerx - scaled_width // 2
        scaled_y = self.rect.centery - scaled_height // 2 + self.bounce_offset
        scaled_rect = pygame.Rect(scaled_x, scaled_y, scaled_width, scaled_height)

        # Create button surface with alpha
        button_surface = pygame.Surface((scaled_width, scaled_height), pygame.SRCALPHA)
        color = BUTTON_HOVER_COLOR if self.is_hovered else BUTTON_COLOR
        
        # Draw a more playful button shape with rounded corners
        pygame.draw.rect(button_surface, (*color, int(self.alpha.current)), 
                        button_surface.get_rect(), border_radius=25)
        
        # Add a fun border
        if self.is_hovered:
            border_color = (*GRID_COLOR, int(self.alpha.current))
            pygame.draw.rect(button_surface, border_color,
                           button_surface.get_rect(), border_radius=25, width=3)
        
        # Add a glow effect when hovered with smooth transition
        glow_alpha = int(self.hover_glow.current)
        if self.is_hovered and glow_alpha > 0:
            glow_surface = pygame.Surface((scaled_width + 40, scaled_height + 40), pygame.SRCALPHA)
            for i in range(20, 0, -2):
                alpha = int((30 - (i * 1.5)) * glow_alpha / 255)
                pygame.draw.rect(glow_surface, (*GRID_COLOR, alpha),
                               pygame.Rect(20-i, 20-i, scaled_width+i*2, scaled_height+i*2),
                               border_radius=25+i)
            surface.blit(glow_surface, (scaled_x-20, scaled_y-20))

        surface.blit(button_surface, (scaled_x, scaled_y))
        
        # Draw text with shadow
        font_size = 32
        text_font = pygame.font.Font(None, font_size)
        
        # Draw shadow
        shadow_surface = text_font.render(self.text, True, (0, 0, 0))
        shadow_rect = shadow_surface.get_rect(center=(scaled_rect.centerx + 2, scaled_rect.centery + 2))
        shadow_surface.set_alpha(100)
        surface.blit(shadow_surface, shadow_rect)
        
        # Draw main text
        text_surface = text_font.render(self.text, True, TEXT_COLOR)
        text_rect = text_surface.get_rect(center=scaled_rect.center)
        surface.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovered:
                return True
        return False

class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.size = random.randint(4, 12)  # Bigger particles
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(3, 8)  # Faster particles
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.life = 1.0
        self.decay = random.uniform(0.01, 0.03)  # Slower decay for longer-lasting particles

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.2  # Stronger gravity effect
        self.size = max(1, self.size * 0.99)  # Gradually shrink
        self.life -= self.decay
        return self.life > 0

    def draw(self, surface):
        alpha = int(self.life * 255)
        size = int(self.size)
        # Draw a more playful particle (small star-like shape)
        points = []
        for i in range(8):
            angle = i * math.pi / 4
            if i % 2 == 0:
                radius = size
            else:
                radius = size / 2
            points.append((
                self.x + math.cos(angle) * radius,
                self.y + math.sin(angle) * radius
            ))
        if len(points) >= 3:  # Need at least 3 points to draw a polygon
            pygame.draw.polygon(surface, (*self.color, alpha), points)

class Game:
    def __init__(self):
        self.state = "menu"
        self.board = np.zeros((3, 3))
        self.current_player = 1
        self.winner = None
        self.game_mode = None
        self.ai_difficulty = "medium"
        self.hover_cell = None
        self.animations = []
        self.winning_line = None
        self.particles = []
        
        # Initialize fonts
        self.font = pygame.font.Font(None, 40)
        self.large_font = pygame.font.Font(None, 80)
        
        # Create menu buttons
        button_width = 300
        button_height = 60
        center_x = WINDOW_SIZE // 2 - button_width // 2
        
        self.menu_buttons = [
            Button(center_x, 250, button_width, button_height, "Player vs Player"),
            Button(center_x, 350, button_width, button_height, "Player vs AI (Easy)"),
            Button(center_x, 450, button_width, button_height, "Player vs AI (Hard)")
        ]

        # Create back to menu and reset buttons
        self.back_button = Button(20, 20, 200, 50, "Back to Menu")
        self.reset_button = Button(WINDOW_SIZE - 220, 20, 200, 50, "Reset Game")
        
        # Animation properties
        self.cell_alphas = [[AnimatedValue(0, 0) for _ in range(3)] for _ in range(3)]
        self.cell_scales = [[AnimatedValue(0.5, 1.0) for _ in range(3)] for _ in range(3)]
        self.board_rotation = AnimatedValue(0, 0, duration=40)
        self.board_scale = AnimatedValue(1, 1, duration=30)
        self.status_alpha = AnimatedValue(255, 255, duration=30)  # Start fully visible

    def add_particles(self, x, y, color):
        for _ in range(20):
            self.particles.append(Particle(x, y, color))

    def update_particles(self):
        self.particles = [p for p in self.particles if p.update()]

    def draw_particles(self):
        particle_surface = pygame.Surface((WINDOW_SIZE, WINDOW_SIZE), pygame.SRCALPHA)
        for particle in self.particles:
            particle.draw(particle_surface)
        screen.blit(particle_surface, (0, 0))

    def draw_menu(self):
        # Create sophisticated gradient background with animated waves
        t = pygame.time.get_ticks() / 1000
        for y in range(WINDOW_SIZE):
            progress = y / WINDOW_SIZE
            color = tuple(int(a + (b - a) * progress) for a, b in zip(BACKGROUND, MENU_BG))
            # Add multiple wave effects
            wave1 = math.sin(y / 30 + t) * 8
            wave2 = math.cos(y / 20 + t * 0.7) * 5
            wave = wave1 + wave2
            pygame.draw.line(screen, color, (max(0, wave), y), 
                           (WINDOW_SIZE + min(0, wave), y))

        # Draw title with improved shadow and glow
        title_text = "Tic Tac Toe!"
        title_surface = self.large_font.render(title_text, True, TEXT_COLOR)
        title_rect = title_surface.get_rect(center=(WINDOW_SIZE//2, 120))
        
        # Draw multiple shadows for depth
        shadow_offsets = [(4, 4), (3, 3), (2, 2)]
        for offset_x, offset_y in shadow_offsets:
            shadow_surface = self.large_font.render(title_text, True, TEXT_SHADOW_COLOR)
            shadow_rect = shadow_surface.get_rect(center=(WINDOW_SIZE//2 + offset_x, 120 + offset_y))
            screen.blit(shadow_surface, shadow_rect)
        
        # Draw main title
        screen.blit(title_surface, title_rect)
        
        # Add random particles for fun
        if random.random() < 0.1:
            x = random.randint(0, WINDOW_SIZE)
            y = random.randint(0, WINDOW_SIZE)
            self.add_particles(x, y, random.choice(PARTICLE_COLORS))
        
        # Draw buttons
        for button in self.menu_buttons:
            button.draw(screen)
        
        # Draw particles
        self.update_particles()
        self.draw_particles()

    def draw_board(self):
        # Update animations
        self.board_rotation.update()
        self.board_scale.update()
        self.status_alpha.update()
        
        # Create gradient background with wave effect
        for y in range(WINDOW_SIZE):
            progress = y / WINDOW_SIZE
            color = tuple(int(a + (b - a) * progress) for a, b in zip(BACKGROUND, MENU_BG))
            wave = math.sin(y / 40 + pygame.time.get_ticks() / 1500) * 3
            pygame.draw.line(screen, color, (max(0, wave), y), 
                           (WINDOW_SIZE + min(0, wave), y))

        offset = (WINDOW_SIZE - BOARD_SIZE) // 2

        # Create a surface for the board
        board_surface = pygame.Surface((BOARD_SIZE + 100, BOARD_SIZE + 100), pygame.SRCALPHA)
        board_rect = board_surface.get_rect(center=(WINDOW_SIZE//2, WINDOW_SIZE//2))

        # Draw grid with enhanced glow effect
        for i in range(1, 3):
            for thickness in range(6, 0, -1):
                alpha = 60 if thickness == 6 else 25
                pulse = (math.sin(pygame.time.get_ticks() / 1000 + i) + 1) / 2
                alpha = int(alpha * (0.7 + pulse * 0.3))
                
                # Vertical lines
                pygame.draw.line(board_surface, (*GRID_COLOR, alpha),
                               (50 + i * CELL_SIZE, 50),
                               (50 + i * CELL_SIZE, BOARD_SIZE + 50), thickness)
                # Horizontal lines
                pygame.draw.line(board_surface, (*GRID_COLOR, alpha),
                               (50, 50 + i * CELL_SIZE),
                               (BOARD_SIZE + 50, 50 + i * CELL_SIZE), thickness)

        # Draw hover effect with pulsing animation
        if self.hover_cell and self.winner is None:
            row, col = self.hover_cell
            if self.board[row][col] == 0:
                pulse = (math.sin(pygame.time.get_ticks() / 500) + 1) / 2
                hover_alpha = int(100 * (0.7 + pulse * 0.3))
                rect = pygame.Rect(50 + col * CELL_SIZE, 50 + row * CELL_SIZE,
                                 CELL_SIZE, CELL_SIZE)
                hover_surface = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
                pygame.draw.rect(hover_surface, (*HOVER_COLOR[:3], hover_alpha), 
                               hover_surface.get_rect(), border_radius=10)
                board_surface.blit(hover_surface, rect)

        # Draw X's and O's with enhanced animations
        for row in range(3):
            for col in range(3):
                cell_value = self.board[row][col]
                if cell_value != 0:
                    self.cell_alphas[row][col].update()
                    self.cell_scales[row][col].update()
                    
                    center_x = 50 + col * CELL_SIZE + CELL_SIZE // 2
                    center_y = 50 + row * CELL_SIZE + CELL_SIZE // 2
                    scale = self.cell_scales[row][col].current
                    alpha = int(self.cell_alphas[row][col].current)
                    
                    if cell_value == 1:  # X
                        color = (*PLAYER_X_COLOR, alpha)
                        size = int(CELL_SIZE * 0.3 * scale)
                        thickness = max(1, int(15 * scale))
                        
                        # Draw X with glow effect
                        for i in range(3):
                            glow_alpha = alpha // (i + 2)
                            glow_thickness = thickness + i * 2
                            pygame.draw.line(board_surface, (*PLAYER_X_COLOR, glow_alpha),
                                           (center_x - size - i, center_y - size - i),
                                           (center_x + size + i, center_y + size + i),
                                           glow_thickness)
                            pygame.draw.line(board_surface, (*PLAYER_X_COLOR, glow_alpha),
                                           (center_x + size + i, center_y - size - i),
                                           (center_x - size - i, center_y + size + i),
                                           glow_thickness)
                        
                    else:  # O
                        color = (*PLAYER_O_COLOR, alpha)
                        radius = int(CELL_SIZE * 0.3 * scale)
                        thickness = max(1, int(15 * scale))
                        
                        # Draw O with glow effect
                        for i in range(3):
                            glow_alpha = alpha // (i + 2)
                            glow_thickness = thickness + i * 2
                            pygame.draw.circle(board_surface, (*PLAYER_O_COLOR, glow_alpha),
                                            (center_x, center_y), radius + i, glow_thickness)

        # Draw winning line with particle effects
        if self.winning_line:
            start_pos, end_pos = self.winning_line
            start_x = 50 + start_pos[1] * CELL_SIZE + CELL_SIZE // 2
            start_y = 50 + start_pos[0] * CELL_SIZE + CELL_SIZE // 2
            end_x = 50 + end_pos[1] * CELL_SIZE + CELL_SIZE // 2
            end_y = 50 + end_pos[0] * CELL_SIZE + CELL_SIZE // 2
            
            # Draw line with glow effect
            for thickness in range(12, 0, -2):
                alpha = 150 if thickness == 12 else 60
                pygame.draw.line(board_surface, (*WINNER_LINE_COLOR, alpha),
                               (start_x, start_y), (end_x, end_y), thickness)
            
            # Add particles along the winning line
            if random.random() < 0.2:
                progress = random.random()
                particle_x = start_x + (end_x - start_x) * progress
                particle_y = start_y + (end_y - start_y) * progress
                self.add_particles(particle_x, particle_y, random.choice(PARTICLE_COLORS))

        # Apply board rotation and scale
        rotated_surface = pygame.transform.rotozoom(board_surface, 
                                                  self.board_rotation.current,
                                                  self.board_scale.current)
        rotated_rect = rotated_surface.get_rect(center=(WINDOW_SIZE//2, WINDOW_SIZE//2))
        screen.blit(rotated_surface, rotated_rect)

        # Draw back to menu and reset buttons
        self.back_button.draw(screen)
        self.reset_button.draw(screen)

        # Draw game status with improved visibility
        if self.winner is not None:
            if self.winner == 0:
                status = "It's a Tie!"
                status_color = STATUS_TEXT_COLOR
            else:
                winner_symbol = 'X' if self.winner == 1 else 'O'
                winner_color = PLAYER_X_COLOR if self.winner == 1 else PLAYER_O_COLOR
                status = f"Player {winner_symbol} wins!"
                status_color = winner_color
        else:
            current_symbol = 'X' if self.current_player == 1 else 'O'
            current_color = PLAYER_X_COLOR if self.current_player == 1 else PLAYER_O_COLOR
            status = f"Player {current_symbol}'s turn"
            status_color = current_color

        # Draw status text with improved shadow
        shadow_offsets = [(3, 3), (2, 2), (1, 1)]
        for offset_x, offset_y in shadow_offsets:
            shadow_surface = self.font.render(status, True, TEXT_SHADOW_COLOR)
            shadow_rect = shadow_surface.get_rect(center=(WINDOW_SIZE//2 + offset_x, 50 + offset_y))
            shadow_surface.set_alpha(int(self.status_alpha.current * 0.7))
            screen.blit(shadow_surface, shadow_rect)

        # Draw main status text
        status_surface = self.font.render(status, True, status_color)
        status_rect = status_surface.get_rect(center=(WINDOW_SIZE//2, 50))
        status_surface.set_alpha(int(self.status_alpha.current))
        screen.blit(status_surface, status_rect)

        # Draw particles
        self.update_particles()
        self.draw_particles()

    def handle_click(self, pos):
        if self.state == "menu":
            for i, button in enumerate(self.menu_buttons):
                if button.handle_event(pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': pos})):
                    self.state = "game"
                    self.reset()
                    if i == 0:
                        self.game_mode = "pvp"
                    else:
                        self.game_mode = "ai"
                        self.ai_difficulty = "easy" if i == 1 else "hard"
                    # Ensure status is visible immediately
                    self.status_alpha.current = 255
                    self.status_alpha.end = 255
                    return
        elif self.state == "game":
            # Handle back button click
            if self.back_button.handle_event(pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': pos})):
                self.state = "menu"
                self.reset()
                return
            
            # Handle reset button click
            if self.reset_button.handle_event(pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': pos})):
                self.reset()
                return

            # Handle game board clicks
            if self.winner is None:  # Only allow moves if game is not over
                offset = (WINDOW_SIZE - BOARD_SIZE) // 2
                if offset <= pos[0] <= offset + BOARD_SIZE and offset <= pos[1] <= offset + BOARD_SIZE:
                    row = (pos[1] - offset) // CELL_SIZE
                    col = (pos[0] - offset) // CELL_SIZE
                    if 0 <= row < 3 and 0 <= col < 3:
                        if self.board[row][col] == 0:  # Only make move if cell is empty
                            self.make_move(row, col)
                            if self.game_mode == "ai" and self.winner is None:
                                self.ai_move()

    def make_move(self, row, col):
        if self.board[row][col] == 0 and self.winner is None:
            self.board[row][col] = self.current_player
            
            # Add particle effect on move
            center_x = (WINDOW_SIZE - BOARD_SIZE) // 2 + col * CELL_SIZE + CELL_SIZE // 2
            center_y = (WINDOW_SIZE - BOARD_SIZE) // 2 + row * CELL_SIZE + CELL_SIZE // 2
            color = PLAYER_X_COLOR if self.current_player == 1 else PLAYER_O_COLOR
            self.add_particles(center_x, center_y, color)
            
            # Animate the cell
            self.cell_alphas[row][col].animate_to(255)
            self.cell_scales[row][col].animate_to(1.0)
            
            # Add board effects
            self.board_rotation.animate_to(random.uniform(-2, 2))
            self.board_scale.animate_to(1.05)
            
            # Check for winner or tie
            winner = self.check_winner()
            if winner is not None:  # This includes both win (1 or 2) and tie (0)
                self.winner = winner
                if winner != 0:  # Only set winning line if it's not a tie
                    self.winning_line = self.get_winning_line()
                self.status_alpha.animate_to(255)  # Fade in the winner/tie status
                # Add victory particles
                for _ in range(50):
                    x = random.randint(0, WINDOW_SIZE)
                    y = random.randint(0, WINDOW_SIZE)
                    self.add_particles(x, y, random.choice(PARTICLE_COLORS))
            else:
                self.current_player = 3 - self.current_player
                self.status_alpha.animate_to(255)  # Fade in the new player's turn status

    def reset(self):
        self.board = np.zeros((3, 3))
        self.current_player = 1
        self.winner = None
        self.winning_line = None
        for row in range(3):
            for col in range(3):
                self.cell_alphas[row][col].current = 0
                self.cell_scales[row][col].current = 0.5

    def ai_move(self):
        if self.ai_difficulty == "easy":
            # Random empty cell with some basic strategy
            empty_cells = [(r, c) for r in range(3) for c in range(3) if self.board[r][c] == 0]
            if empty_cells:
                # Check if AI can win in one move
                for row, col in empty_cells:
                    self.board[row][col] = 2
                    if self.check_winner() == 2:
                        self.board[row][col] = 0
                        self.make_move(row, col)
                        return
                    self.board[row][col] = 0
                
                # Check if player can win in one move and block
                for row, col in empty_cells:
                    self.board[row][col] = 1
                    if self.check_winner() == 1:
                        self.board[row][col] = 0
                        self.make_move(row, col)
                        return
                    self.board[row][col] = 0
                
                # Otherwise make a random move with preference for center and corners
                weights = []
                for row, col in empty_cells:
                    if row == 1 and col == 1:  # Center
                        weight = 3
                    elif (row, col) in [(0,0), (0,2), (2,0), (2,2)]:  # Corners
                        weight = 2
                    else:  # Edges
                        weight = 1
                    weights.append(weight)
                
                total_weight = sum(weights)
                choice = random.uniform(0, total_weight)
                cumulative_weight = 0
                for i, weight in enumerate(weights):
                    cumulative_weight += weight
                    if choice <= cumulative_weight:
                        row, col = empty_cells[i]
                        self.make_move(row, col)
                        break
        else:
            # Advanced AI with Minimax and Alpha-Beta pruning
            best_score = float('-inf')
            best_move = None
            alpha = float('-inf')
            beta = float('inf')
            
            # First check for immediate winning moves or blocking moves
            empty_cells = [(r, c) for r in range(3) for c in range(3) if self.board[r][c] == 0]
            
            # Try to win in one move
            for row, col in empty_cells:
                self.board[row][col] = 2
                if self.check_winner() == 2:
                    self.board[row][col] = 0
                    self.make_move(row, col)
                    return
                self.board[row][col] = 0
            
            # Block opponent's winning move
            for row, col in empty_cells:
                self.board[row][col] = 1
                if self.check_winner() == 1:
                    self.board[row][col] = 0
                    self.make_move(row, col)
                    return
                self.board[row][col] = 0
            
            # If no immediate winning/blocking moves, use minimax with positional heuristics
            for row in range(3):
                for col in range(3):
                    if self.board[row][col] == 0:
                        self.board[row][col] = 2
                        score = self.minimax(0, False, alpha, beta)
                        self.board[row][col] = 0
                        
                        if score > best_score:
                            best_score = score
                            best_move = (row, col)
                        
                        alpha = max(alpha, best_score)
                        if beta <= alpha:
                            break
            
            if best_move:
                self.make_move(best_move[0], best_move[1])

    def evaluate_position(self):
        # Evaluate the current board state with positional heuristics
        if self.check_winner() == 2:
            return 100  # AI wins
        elif self.check_winner() == 1:
            return -100  # Player wins
        elif self.check_winner() == 0:
            return 0  # Tie
        
        score = 0
        
        # Prefer center position
        if self.board[1][1] == 2:
            score += 3
        elif self.board[1][1] == 1:
            score -= 3
        
        # Prefer corners
        corners = [(0,0), (0,2), (2,0), (2,2)]
        for row, col in corners:
            if self.board[row][col] == 2:
                score += 2
            elif self.board[row][col] == 1:
                score -= 2
        
        # Check for two-in-a-row opportunities
        for i in range(3):
            # Rows
            row = self.board[i]
            if np.sum(row == 2) == 2 and np.sum(row == 0) == 1:
                score += 5
            if np.sum(row == 1) == 2 and np.sum(row == 0) == 1:
                score -= 5
            
            # Columns
            col = self.board[:, i]
            if np.sum(col == 2) == 2 and np.sum(col == 0) == 1:
                score += 5
            if np.sum(col == 1) == 2 and np.sum(col == 0) == 1:
                score -= 5
        
        # Check diagonals
        diag = np.diag(self.board)
        if np.sum(diag == 2) == 2 and np.sum(diag == 0) == 1:
            score += 5
        if np.sum(diag == 1) == 2 and np.sum(diag == 0) == 1:
            score -= 5
        
        anti_diag = np.diag(np.fliplr(self.board))
        if np.sum(anti_diag == 2) == 2 and np.sum(anti_diag == 0) == 1:
            score += 5
        if np.sum(anti_diag == 1) == 2 and np.sum(anti_diag == 0) == 1:
            score -= 5
        
        return score

    def minimax(self, depth, is_maximizing, alpha, beta):
        result = self.check_winner()
        if result is not None:
            return self.evaluate_position()
        
        if depth >= 5:  # Limit search depth for better performance
            return self.evaluate_position()
        
        if is_maximizing:
            best_score = float('-inf')
            for row in range(3):
                for col in range(3):
                    if self.board[row][col] == 0:
                        self.board[row][col] = 2
                        score = self.minimax(depth + 1, False, alpha, beta)
                        self.board[row][col] = 0
                        best_score = max(score, best_score)
                        alpha = max(alpha, best_score)
                        if beta <= alpha:
                            break
            return best_score
        else:
            best_score = float('inf')
            for row in range(3):
                for col in range(3):
                    if self.board[row][col] == 0:
                        self.board[row][col] = 1
                        score = self.minimax(depth + 1, True, alpha, beta)
                        self.board[row][col] = 0
                        best_score = min(score, best_score)
                        beta = min(beta, best_score)
                        if beta <= alpha:
                            break
            return best_score

    def check_winner(self) -> Optional[int]:
        # Check rows, columns and diagonals
        for player in [1, 2]:
            # Rows and columns
            for i in range(3):
                if all(self.board[i, :] == player) or all(self.board[:, i] == player):
                    return player
            # Diagonals
            if all(np.diag(self.board) == player) or all(np.diag(np.fliplr(self.board)) == player):
                return player
        
        # Check for tie (board is full)
        if np.all(self.board != 0):
            return 0
            
        return None

    def get_winning_line(self):
        # Check rows
        for i in range(3):
            if all(self.board[i, :] == self.winner):
                start_x = (WINDOW_SIZE - BOARD_SIZE) // 2 + CELL_SIZE // 2
                end_x = (WINDOW_SIZE - BOARD_SIZE) // 2 + BOARD_SIZE - CELL_SIZE // 2
                y = (WINDOW_SIZE - BOARD_SIZE) // 2 + i * CELL_SIZE + CELL_SIZE // 2
                return ((start_x, y), (end_x, y))
        
        # Check columns
        for i in range(3):
            if all(self.board[:, i] == self.winner):
                x = (WINDOW_SIZE - BOARD_SIZE) // 2 + i * CELL_SIZE + CELL_SIZE // 2
                start_y = (WINDOW_SIZE - BOARD_SIZE) // 2 + CELL_SIZE // 2
                end_y = (WINDOW_SIZE - BOARD_SIZE) // 2 + BOARD_SIZE - CELL_SIZE // 2
                return ((x, start_y), (x, end_y))
        
        # Check diagonals
        if all(np.diag(self.board) == self.winner):
            start_x = (WINDOW_SIZE - BOARD_SIZE) // 2 + CELL_SIZE // 2
            start_y = (WINDOW_SIZE - BOARD_SIZE) // 2 + CELL_SIZE // 2
            end_x = (WINDOW_SIZE - BOARD_SIZE) // 2 + BOARD_SIZE - CELL_SIZE // 2
            end_y = (WINDOW_SIZE - BOARD_SIZE) // 2 + BOARD_SIZE - CELL_SIZE // 2
            return ((start_x, start_y), (end_x, end_y))
        elif all(np.diag(np.fliplr(self.board)) == self.winner):
            start_x = (WINDOW_SIZE - BOARD_SIZE) // 2 + BOARD_SIZE - CELL_SIZE // 2
            start_y = (WINDOW_SIZE - BOARD_SIZE) // 2 + CELL_SIZE // 2
            end_x = (WINDOW_SIZE - BOARD_SIZE) // 2 + CELL_SIZE // 2
            end_y = (WINDOW_SIZE - BOARD_SIZE) // 2 + BOARD_SIZE - CELL_SIZE // 2
            return ((start_x, start_y), (end_x, end_y))

    def run(self):
        clock = pygame.time.Clock()
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.state == "game":
                            self.state = "menu"
                            self.reset()
                elif event.type == pygame.MOUSEMOTION:
                    # Update button hover states
                    mouse_pos = event.pos
                    if self.state == "menu":
                        for button in self.menu_buttons:
                            was_hovered = button.is_hovered
                            button.is_hovered = button.rect.collidepoint(mouse_pos)
                            if button.is_hovered != was_hovered:
                                if button.is_hovered:
                                    button.scale.animate_to(1.1)
                                    button.hover_glow.animate_to(255)  # Fade in glow
                                    # Add particles on hover
                                    self.add_particles(button.rect.centerx, button.rect.centery, GRID_COLOR)
                                else:
                                    button.scale.animate_to(1.0)
                                    button.hover_glow.animate_to(0)  # Fade out glow
                    elif self.state == "game":
                        # Update back and reset button hover states
                        for button in [self.back_button, self.reset_button]:
                            was_hovered = button.is_hovered
                            button.is_hovered = button.rect.collidepoint(mouse_pos)
                            if button.is_hovered != was_hovered:
                                if button.is_hovered:
                                    button.scale.animate_to(1.1)
                                    button.hover_glow.animate_to(255)  # Fade in glow
                                    self.add_particles(button.rect.centerx, button.rect.centery, GRID_COLOR)
                                else:
                                    button.scale.animate_to(1.0)
                                    button.hover_glow.animate_to(0)  # Fade out glow
                        
                        # Update board hover state
                        offset = (WINDOW_SIZE - BOARD_SIZE) // 2
                        if offset <= mouse_pos[0] <= offset + BOARD_SIZE and offset <= mouse_pos[1] <= offset + BOARD_SIZE:
                            row = (mouse_pos[1] - offset) // CELL_SIZE
                            col = (mouse_pos[0] - offset) // CELL_SIZE
                            if 0 <= row < 3 and 0 <= col < 3:
                                self.hover_cell = (row, col)
                                if random.random() < 0.1:  # Occasionally add particles on hover
                                    center_x = offset + col * CELL_SIZE + CELL_SIZE // 2
                                    center_y = offset + row * CELL_SIZE + CELL_SIZE // 2
                                    self.add_particles(center_x, center_y, GRID_COLOR)
                        else:
                            self.hover_cell = None
            
            # Clear screen
            screen.fill(BACKGROUND)
            
            # Draw current state
            if self.state == "menu":
                self.draw_menu()
            else:
                self.draw_board()
            
            # Update display
            pygame.display.flip()
            clock.tick(60)

if __name__ == "__main__":
    pygame.init()
    global screen
    screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
    pygame.display.set_caption("Tic Tac Toe!")
    game = Game()
    game.run()
