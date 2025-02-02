import unittest
import numpy as np
import pygame
from main import Game, AnimatedValue, Button

class TestTicTacToe(unittest.TestCase):
    def setUp(self):
        """Initialize pygame and create a new game instance before each test."""
        pygame.init()
        pygame.display.set_mode((800, 800))
        self.game = Game()

    def test_initial_state(self):
        """Test the initial game state."""
        self.assertEqual(self.game.state, "menu")
        self.assertEqual(self.game.current_player, 1)
        self.assertIsNone(self.game.winner)
        self.assertTrue(np.array_equal(self.game.board, np.zeros((3, 3))))

    def test_make_move(self):
        """Test making valid and invalid moves."""
        # Test valid move
        self.game.make_move(0, 0)
        self.assertEqual(self.game.board[0, 0], 1)
        self.assertEqual(self.game.current_player, 2)

        # Test invalid move (occupied cell)
        self.game.make_move(0, 0)
        self.assertEqual(self.game.board[0, 0], 1)  # Should remain unchanged
        self.assertEqual(self.game.current_player, 2)  # Should remain unchanged

    def test_check_winner(self):
        """Test win detection in various scenarios."""
        # Test row win
        self.game.board = np.array([
            [1, 1, 1],
            [0, 2, 2],
            [0, 0, 0]
        ])
        self.assertEqual(self.game.check_winner(), 1)

        # Test column win
        self.game.board = np.array([
            [2, 1, 0],
            [2, 1, 0],
            [2, 0, 0]
        ])
        self.assertEqual(self.game.check_winner(), 2)

        # Test diagonal win
        self.game.board = np.array([
            [1, 2, 0],
            [2, 1, 0],
            [0, 0, 1]
        ])
        self.assertEqual(self.game.check_winner(), 1)

        # Test tie
        self.game.board = np.array([
            [1, 2, 1],
            [1, 2, 2],
            [2, 1, 1]
        ])
        self.assertEqual(self.game.check_winner(), 0)

        # Test game in progress
        self.game.board = np.array([
            [1, 2, 0],
            [0, 0, 0],
            [0, 0, 0]
        ])
        self.assertIsNone(self.game.check_winner())

    def test_ai_move_easy(self):
        """Test AI behavior in easy mode."""
        self.game.state = "game"
        self.game.game_mode = "ai"
        self.game.ai_difficulty = "easy"
        
        # Test AI blocks winning move
        self.game.board = np.array([
            [1, 1, 0],
            [0, 2, 0],
            [0, 0, 0]
        ])
        self.game.current_player = 2
        self.game.ai_move()
        self.assertEqual(self.game.board[0, 2], 2)  # AI should block at (0,2)

    def test_ai_move_hard(self):
        """Test AI behavior in hard mode."""
        self.game.state = "game"
        self.game.game_mode = "ai"
        self.game.ai_difficulty = "hard"
        
        # Test AI takes winning move
        self.game.board = np.array([
            [2, 2, 0],
            [1, 1, 0],
            [0, 0, 0]
        ])
        self.game.current_player = 2
        self.game.ai_move()
        self.assertEqual(self.game.board[0, 2], 2)  # AI should win at (0,2)

    def test_evaluate_position(self):
        """Test the position evaluation function."""
        # Test winning position
        self.game.board = np.array([
            [2, 2, 2],
            [1, 1, 0],
            [0, 0, 0]
        ])
        self.assertEqual(self.game.evaluate_position(), 100)

        # Test losing position
        self.game.board = np.array([
            [1, 1, 1],
            [2, 2, 0],
            [0, 0, 0]
        ])
        self.assertEqual(self.game.evaluate_position(), -100)

        # Test center control
        self.game.board = np.array([
            [0, 0, 0],
            [0, 2, 0],
            [0, 0, 0]
        ])
        self.assertEqual(self.game.evaluate_position(), 3)

    def test_reset(self):
        """Test game reset functionality."""
        # Make some moves
        self.game.make_move(0, 0)
        self.game.make_move(1, 1)
        
        # Reset game
        self.game.reset()
        
        # Verify reset state
        self.assertEqual(self.game.current_player, 1)
        self.assertIsNone(self.game.winner)
        self.assertTrue(np.array_equal(self.game.board, np.zeros((3, 3))))

    def test_animated_value(self):
        """Test AnimatedValue behavior."""
        anim = AnimatedValue(0, 10, duration=20)
        
        # Test initial state
        self.assertEqual(anim.current, 0)
        self.assertEqual(anim.end, 10)
        
        # Test animation
        anim.animate_to(5)
        self.assertTrue(anim.is_animating)
        
        # Update a few times
        for _ in range(10):
            anim.update()
        
        self.assertGreater(anim.current, 0)

    def test_button_initialization(self):
        """Test Button initialization and properties."""
        button = Button(100, 100, 200, 50, "Test Button")
        self.assertEqual(button.text, "Test Button")
        self.assertEqual(button.rect.width, 200)
        self.assertEqual(button.rect.height, 50)
        self.assertFalse(button.is_hovered)

if __name__ == '__main__':
    unittest.main()
