import time
from dataclasses import dataclass
from typing import Dict
from prometheus_client import Counter, Gauge, Histogram

@dataclass
class GameMetrics:
    # Count the number of moves, labeled by direction (up, down, left, right)
    moves_counter = Counter('game_moves_total', 'Total number of moves', ['direction'])  
    # Store the current game score (can increase or decrease), Purpose: Stores a value that can increase or decrease (e.g., the current score). Unlike a Counter, it can be reset or changed.
    score_gauge = Gauge('game_score', 'Current game score')
    # Record the duration of a game (distribution metric)
    game_duration = Histogram('game_duration_seconds', 'Game duration in seconds')
    # Count the number of errors, categorized by type
    errors_counter = Counter('game_errors_total', 'Total number of errors', ['type'])
    
    def __init__(self):
        self.start_time = None
        
    def record_game_start(self):
        self.start_time = time.time()
        
    def record_game_end(self, result: str):
        if self.start_time:
            duration = time.time() - self.start_time
            self.game_duration.observe(duration)
            
    def record_move(self, direction: str):
        self.moves_counter.labels(direction=direction).inc()

    def record_score(self, score: int):
        self.score_gauge.set(score)  # set is to set a new value 
        
    def record_error(self, error_type: str):
        self.errors_counter.labels(type=error_type).inc()