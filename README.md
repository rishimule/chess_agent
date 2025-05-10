# Chess Agent

A Python-based chess engine and game implementation with a minimax AI.

## Overview

This project implements a chess game with a minimax-based AI engine. It supports standard chess rules, including special moves like castling, en passant, and pawn promotion. The AI uses the minimax algorithm with alpha-beta pruning to evaluate positions and make decisions.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/rishimule/chess_agent.git
   cd chess_agent
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the package in development mode:
   ```bash
   pip install -e .
   ```

4. Install test dependencies:
   ```bash
   pip install -r tests/requirements.txt
   ```

## Usage

Run the main game:
```bash
python src/main.py
```

Run the tests:
```bash
PYTHONPATH=src python -m pytest tests/ -v
```

## Project Structure

```
chess_agent/
├── src/
│   ├── chess/
│   │   ├── __init__.py
│   │   ├── board.py
│   │   ├── engines/
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   └── minimax.py
│   │   └── pieces/
│   │       ├── __init__.py
│   │       ├── bishop.py
│   │       ├── king.py
│   │       ├── knight.py
│   │       ├── pawn.py
│   │       ├── queen.py
│   │       └── rook.py
│   └── main.py
├── tests/
│   ├── __init__.py
│   ├── engines/
│   │   ├── __init__.py
│   │   ├── test_base.py
│   │   └── test_minimax.py
│   ├── pieces/
│   │   ├── __init__.py
│   │   ├── test_bishop.py
│   │   ├── test_king.py
│   │   ├── test_knight.py
│   │   ├── test_pawn.py
│   │   ├── test_queen.py
│   │   └── test_rook.py
│   ├── test_board.py
│   └── requirements.txt
├── .gitignore
├── README.md
├── requirements.txt
└── setup.py
```

## Features

- **Chess Rules**: Implements standard chess rules, including special moves.
- **Minimax AI**: Uses the minimax algorithm with alpha-beta pruning for AI decision-making.
- **Comprehensive Tests**: Extensive test coverage for all components.

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
 