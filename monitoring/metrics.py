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
        # moves_counter.labels(direction="up").inc() → increases the move count for "up".

    def record_score(self, score: int):
        self.score_gauge.set(score)  # set is to set a new value 
        
    def record_error(self, error_type: str):
        self.errors_counter.labels(type=error_type).inc()
        # errors_counter.labels(type="move_error").inc() → increases the count of "move_error".
        # self.metrics.record_error("move_error")  # Called when an error happens


'''
1. Overview of Prometheus Metrics
Metric Type	                                 Purpose	                                                     Example Use Case
Counter:	    Increases over time (never decreases). Used for counting occurrences.	                    Number of moves made in the game.
Gauge:   	    Can increase and decrease (like a variable). Used for tracking current values.	            Current game score.
Histogram:	    Tracks the distribution of values (e.g., response times). Used to measure performance.	    Duration of a game session.
'''


'''
How Histogram Buckets Work
By default, Prometheus automatically creates buckets:

Histogram('game_duration_seconds', 'Game duration in seconds')
will generate default buckets:

[0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0, +Inf]
Example of How Values Are Stored
If observe(2.5) is called:

The count of the bucket ≤2.5 seconds increases.
The count of all higher buckets also increases.
Bucket	Count
≤ 0.005	0
≤ 0.01	0
≤ 0.025	0
≤ 0.05	0
≤ 0.1	0
≤ 0.25	0
≤ 0.5	0
≤ 1.0	0
≤ 2.5	1 (our observation)
≤ 5.0	1
≤ 10.0	1
+Inf	1

'''



'''
6. How to View Prometheus Metrics?
Run a Prometheus Server and scrape metrics from your app.
Expose metrics via HTTP using prometheus_client:

from prometheus_client import start_http_server
start_http_server(8000)  # Starts a server at localhost:8000/metrics
Visit http://localhost:8000/metrics to see:

# HELP game_moves_total Total number of moves
# TYPE game_moves_total counter
game_moves_total{direction="left"} 5.0
game_moves_total{direction="right"} 3.0

# HELP game_score Current game score
# TYPE game_score gauge
game_score 150

# HELP game_duration_seconds Game duration in seconds
# TYPE game_duration_seconds histogram
game_duration_seconds_bucket{le="1"} 0
game_duration_seconds_bucket{le="2"} 1

'''