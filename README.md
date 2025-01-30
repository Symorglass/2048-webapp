# 2048
A web-based implementation of the popular 2048 game built with Flask for the backend and JavaScript for the frontend. Includes Prometheus monitoring for tracking game metrics.

![2048 game image](image/2048_example.png)

# Getting Started
## Clone the Repository
```
git clone https://github.com/yourusername/2048-webapp.git
cd 2048-webapp
```
## Install Dependencies
```
pip install -r requirements.txt
```

## Run the game
```
python -m app
```
## Access the game
```
http://127.0.0.1:5000
```
## How to Restart a New Game
Click the "New Game" button in the UI or send a POST request:
```
curl -X POST http://127.0.0.1:5000/new_game
```

# Monitoring with Prometheus
This project includes Prometheus metrics to track game moves, scores, and session durations.
## Access Metrics
You can access Prometheus metrics at:

- Standalone Prometheus Server:
```
http://localhost:8000/metrics
```
or 

- Flask Metrics Route:
```
http://127.0.0.1:5000/metrics
```

# Running Tests
```
pytest tests/
```

# Architecture
The overview of the architecture is as follows:
```mermaid
flowchart TD
    subgraph Frontend
        UI[Browser Interface]
        Game_JS[game.js]
        UI <--> Game_JS
        style UI fill:#f9f,stroke:#333
        style Game_JS fill:#f9f,stroke:#333
    end

    subgraph Backend
        Flask[Flask App]
        Controller[Game Controller]
        Board[Board Logic]
        
        Flask <--> Controller
        Controller <--> Board
        
        style Flask fill:#bbf,stroke:#333
        style Controller fill:#bbf,stroke:#333
        style Board fill:#bbf,stroke:#333
    end

    subgraph Monitoring
        Metrics[Prometheus Metrics]
        Logs[Game Logs]
        style Metrics fill:#bfb,stroke:#333
        style Logs fill:#bfb,stroke:#333
    end

    %% Main Flow
    Game_JS <-->|HTTP Requests/Responses| Flask
    Board -->|Game Events| Metrics
    Board -->|Debug Info| Logs

    %% External Access
    Monitor[External Monitoring] -.->|Access| Metrics

    %% Key Actions
    UI -->|Arrow Keys| Game_JS
    UI -->|New Game Button| Game_JS
```

# License

This project is open-source and licensed under the MIT License.

