document.addEventListener('DOMContentLoaded', () => {
    initializeGrid();
    document.addEventListener('keydown', handleKeyPress);
});

function initializeGrid() {
    const grid = document.getElementById('grid');
    for (let i = 0; i < 16; i++) {
        const cell = document.createElement('div');
        cell.className = 'cell';
        cell.setAttribute('data-value', '');
        grid.appendChild(cell);
    }
    updateGrid();
}

function updateGrid() {
    fetch('/move', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ direction: 'none' })
    })
    .then(response => response.json())
    .then(data => {
        renderGrid(data.grid);
        updateScore(data.score);
        if (data.gameOver) {
            showGameOver();
        }
    });
}

function renderGrid(gridData) {
    const cells = document.querySelectorAll('.cell');
    let cellIndex = 0;
    for (let i = 0; i < gridData.length; i++) {
        for (let j = 0; j < gridData[0].length; j++) {
            const value = gridData[i][j];
            cells[cellIndex].setAttribute('data-value', value || '');
            cells[cellIndex].textContent = value || '';
            cellIndex++;
        }
    }
}

function updateScore(score) {
    document.getElementById('score').textContent = score;
}

function handleKeyPress(event) {
    const keyToDirection = {
        'ArrowUp': 'up',
        'ArrowDown': 'down',
        'ArrowLeft': 'left',
        'ArrowRight': 'right'
    };

    const direction = keyToDirection[event.key];
    if (direction) {
        event.preventDefault();
        makeMove(direction);
    }
}

function makeMove(direction) {
    fetch('/move', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ direction })
    })
    .then(response => response.json())
    .then(data => {
        if (data.validMove) {
            renderGrid(data.grid);
            updateScore(data.score);
            if (data.gameOver) {
                showGameOver();
            }
        }
    });
}

function startNewGame() {
    fetch('/new_game', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        renderGrid(data.grid);
        updateScore(data.score);
        hideGameOver();
    });
}

function showGameOver() {
    document.getElementById('gameOver').classList.add('active');
}

function hideGameOver() {
    document.getElementById('gameOver').classList.remove('active');
}