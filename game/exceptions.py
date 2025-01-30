class InvalidMoveError(Exception):
    """Exception raised when an invalid move is attempted in the game.
    
    Attributes:
        message -- explanation of why the move is invalid
    """
    
    def __init__(self, message="Invalid move attempted"):
        self.message = message
        super().__init__(self.message)
        
class GameOverError(Exception):
    """Exception raised when a move is attempted after the game is over."""
    
    def __init__(self, message="Game is already over"):
        self.message = message
        super().__init__(self.message)

class ConfigError(Exception):
    """Exception raised when there's an issue with game configuration."""
    
    def __init__(self, message="Invalid game configuration"):
        self.message = message
        super().__init__(self.message)