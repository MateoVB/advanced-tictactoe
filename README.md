# Advanced Tic Tac Toe

A modern implementation of the classic Tic Tac Toe game with advanced features:
- Beautiful UI with modern colors and animations
- Play against another player or AI
- Multiple difficulty levels for AI
- Interactive menu system
- Particle effects and smooth animations
- Smart AI with strategic decision making

## Development Information

### Contributor
**Mateo Velarde**

### Project Timeline
- Total Development Time: 30 min
- Completed: February 1, 2025

### Key Contributions
1. **Core Game Implementation**
   - Developed game logic and state management
   - Created interactive UI with modern design
   - Implemented smooth animations and particle effects

2. **AI Development**
   - Designed and implemented two AI difficulty levels
   - Created Minimax algorithm with Alpha-Beta pruning
   - Added strategic position evaluation

3. **Testing and Documentation**
   - Developed comprehensive test suite
   - Created detailed documentation
   - Added installation and usage instructions

### Technical Challenges
1. **UI/UX Improvements**
   - Initial challenge with text visibility against bright backgrounds
   - Resolved by implementing better contrast and shadow effects
   - Added smooth transitions for better user experience

2. **Button Interaction**
   - Initial issues with button jitter and stability
   - Fixed by optimizing animation parameters
   - Improved hover effects and click detection

3. **AI Implementation**
   - Balancing AI difficulty levels
   - Optimizing Minimax algorithm performance
   - Creating engaging gameplay for both difficulty modes

### Future Improvements
1. Game enhancements:
   - Add sound effects
   - Implement game statistics tracking
   - Create additional AI difficulty levels

2. Technical improvements:
   - Add configuration options
   - Implement save/load game state
   - Create replay functionality

## Features

### Visual Effects
- Vibrant color scheme with dynamic backgrounds
- Smooth animations for moves and transitions
- Particle effects for interactions
- Modern button designs with hover effects
- Clear game status display

### Game Modes
1. **Player vs Player**: Classic two-player mode
2. **Player vs AI (Easy)**: AI with basic strategy
   - Blocks winning moves
   - Prefers center and corners
   - Makes some random moves
3. **Player vs AI (Hard)**: Advanced AI using Minimax algorithm
   - Perfect play with Alpha-Beta pruning
   - Strategic position evaluation
   - Looks ahead multiple moves

## Installation

1. Ensure you have Python 3.8+ installed

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Run the game:
```bash
python main.py
```

## How to Play
1. **Main Menu**
   - Choose your game mode
   - Click on buttons to navigate
   - Hover for interactive effects

2. **During Game**
   - Click on any empty cell to make a move
   - Current player is shown at the top
   - Winner is announced when game ends
   - Press ESC or click "Back to Menu" to return

3. **Controls**
   - Use mouse to interact with the game
   - Left-click to make moves
   - ESC key returns to main menu

## AI Implementation

### Easy Mode
- Implements basic strategy
- Prioritizes:
  1. Winning moves
  2. Blocking opponent's winning moves
  3. Center position
  4. Corner positions
  5. Random available moves

### Hard Mode
- Uses Minimax algorithm with Alpha-Beta pruning
- Evaluates positions based on:
  - Winning positions (±100 points)
  - Center control (±3 points)
  - Corner control (±2 points)
  - Two-in-a-row opportunities (±5 points)
- Looks ahead up to 5 moves
- Optimized for quick responses

## Testing

The game includes a comprehensive test suite covering all major functionality:

1. Run all tests:
```bash
python -m unittest test_game.py -v
```

2. Test coverage includes:
   - Basic game logic
   - Move validation
   - Win detection
   - AI decision making
   - UI component initialization
   - Animation system
   - Game state management

3. Test Categories:
   - `test_initial_state`: Verifies correct game initialization
   - `test_make_move`: Tests valid and invalid move handling
   - `test_check_winner`: Tests win detection for rows, columns, diagonals
   - `test_ai_move_easy`: Verifies easy AI behavior
   - `test_ai_move_hard`: Tests advanced AI decision making
   - `test_evaluate_position`: Checks position evaluation
   - `test_reset`: Verifies game reset functionality
   - `test_animated_value`: Tests animation system
   - `test_button_initialization`: Tests UI components

## Contributing
Feel free to submit issues and enhancement requests!
