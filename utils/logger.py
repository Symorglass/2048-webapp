import logging
import sys

def setup_logger():
    """Configure and setup application logging"""
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('game.log')
        ]
    )
    
    # Return a logger instance for the caller to use
    return logging.getLogger(__name__)

# Create a default logger instance
logger = setup_logger()