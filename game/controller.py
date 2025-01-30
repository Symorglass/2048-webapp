import logging
from typing import Optional
from game.board import Board
from utils.config import GameConfig
from monitoring.metrics import GameMetrics

logger = logging.getLogger(__name__)

class GameController:
    def __init__(self, config: GameConfig):
        self.config = config
        self.board = Board(config.board_size)
        self.metrics = GameMetrics()
        logger.info("Game controller initialized")
        
    def start_game(self):
        """Initializes and starts a new game."""
        self.board.add_new_tile()
        self.board.add_new_tile()
        self.metrics.record_game_start()
        
    def handle_move(self, direction: str) -> bool:
        """Handles a move in the specified direction."""
        try:
            if self.board.move(direction):
                self.board.add_new_tile()
                self.metrics.record_score(self.board.score)
                
                if self.board.is_game_over():
                    self.metrics.record_game_end("loss")
                    logger.info("Game over!")
                    return False
                    
                return True
            return True
        except Exception as e:
            logger.error(f"Error handling move: {e}")
            self.metrics.record_error("move_error")
            raise
