const accentPalette = [
    '#5ef8ff',
    '#ff7be5',
    '#70ffb5',
    '#ffd166',
    '#8fa2ff',
    '#ff6f91',
    '#6efacc',
    '#f0a6ff',
    '#74fce6',
    '#f8a0ff',
    '#ffe066',
    '#9ad0ff'
];

function hexToRgba(hex, alpha = 1) {
    if (typeof hex !== 'string') {
        return hex;
    }

    let sanitized = hex.replace('#', '');

    if (sanitized.length === 3) {
        sanitized = sanitized
            .split('')
            .map((char) => char + char)
            .join('');
    }

    if (sanitized.length !== 6) {
        return hex;
    }

    const numeric = Number.parseInt(sanitized, 16);

    if (Number.isNaN(numeric)) {
        return hex;
    }

    const r = (numeric >> 16) & 255;
    const g = (numeric >> 8) & 255;
    const b = numeric & 255;

    return `rgba(${r}, ${g}, ${b}, ${alpha})`;
}

function readSoundboardConfig() {
    const configElement = document.getElementById('soundboard-config');

    if (!configElement) {
        return { layout: [0, 0], buttons: [] };
    }

    try {
        const parsed = JSON.parse(configElement.textContent);

        if (!Array.isArray(parsed.layout) && parsed.layout) {
            const { rows = 0, cols = 0 } = parsed.layout;
            parsed.layout = [rows, cols];
        }

        if (!Array.isArray(parsed.layout)) {
            parsed.layout = [0, 0];
        }

        if (!Array.isArray(parsed.buttons)) {
            parsed.buttons = [];
        }

        return parsed;
    } catch (error) {
        console.error('Unable to parse soundboard configuration.', error);
        return { layout: [0, 0], buttons: [] };
    }
}

const config = readSoundboardConfig();
const playingSounds = new Set();

function createSoundboard() {
    const grid = document.getElementById('soundboard');
    if (!grid) {
        return;
    }

    grid.innerHTML = '';
    const [rows, cols] = config.layout;

    const buttonMap = new Map();
    config.buttons.forEach((button, index) => {
        const key = `${button.row}_${button.col}`;
        if (!buttonMap.has(key)) {
            buttonMap.set(key, { ...button, _order: index });
        }
    });

    for (let row = 1; row <= rows; row += 1) {
        for (let col = 1; col <= cols; col += 1) {
            const key = `${row}_${col}`;
            const button = buttonMap.get(key);

            if (button) {
                grid.appendChild(createSoundButton(button));
            } else {
                grid.appendChild(createEmptySlot(row, col));
            }
        }
    }
}

function createSoundButton(button) {
    const element = document.createElement('button');
    element.className = 'sound-button';
    element.dataset.buttonId = button.id;
    element.setAttribute(
        'aria-label',
        button.label ? `Play ${button.label}` : `Play pad ${button.row} ${button.col}`
    );

    const accentColor = accentPalette[button._order % accentPalette.length] || accentPalette[0];
    element.style.setProperty('--accent', accentColor);
    element.style.setProperty('--accent-soft', hexToRgba(accentColor, 0.3));
    element.style.setProperty('--accent-strong', hexToRgba(accentColor, 0.82));

    const padShell = document.createElement('div');
    padShell.className = 'pad-shell';

    const padSurface = document.createElement('div');
    padSurface.className = 'pad-surface';
    padShell.appendChild(padSurface);

    const padMeta = document.createElement('div');
    padMeta.className = 'pad-meta';

    const labelText = document.createElement('span');
    labelText.className = 'pad-label';
    labelText.textContent = button.label || `Pad ${button.row},${button.col}`;

    const positionText = document.createElement('span');
    positionText.className = 'pad-position';
    positionText.textContent = `R${button.row} · C${button.col}`;

    padMeta.appendChild(labelText);
    padMeta.appendChild(positionText);

    element.appendChild(padShell);
    element.appendChild(padMeta);

    element.addEventListener('click', () => playSound(button.id, element));

    return element;
}

function createEmptySlot(row, col) {
    const element = document.createElement('div');
    element.className = 'empty-slot';
    element.textContent = `R${row} · C${col}`;
    return element;
}

async function playSound(buttonId, buttonElement) {
    try {
        const response = await fetch(`/api/play/${buttonId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        const result = await response.json();

        if (result.success) {
            buttonElement.classList.add('playing');
            playingSounds.add(buttonId);

            const labelNode = buttonElement.querySelector('.pad-label');
            const labelText = labelNode ? labelNode.textContent : 'Sound';
            showStatus(`Playing ${labelText}`, 'success');

            setTimeout(() => {
                if (!playingSounds.has(buttonId)) {
                    return;
                }
                buttonElement.classList.remove('playing');
                playingSounds.delete(buttonId);
            }, 10000);
        } else {
            showStatus('Failed to play sound', 'error');
        }
    } catch (error) {
        console.error('Error playing sound:', error);
        showStatus('Network error', 'error');
    }
}

async function stopSound(buttonId) {
    try {
        const response = await fetch(`/api/stop/${buttonId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        const result = await response.json();

        if (result.success) {
            const buttonElement = document.querySelector(`[data-button-id="${buttonId}"]`);
            if (buttonElement) {
                buttonElement.classList.remove('playing');
            }
            playingSounds.delete(buttonId);
        }
    } catch (error) {
        console.error('Error stopping sound:', error);
    }
}

async function stopAllSounds() {
    try {
        const response = await fetch('/api/stop-all', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        const result = await response.json();

        if (result.success) {
            document.querySelectorAll('.sound-button.playing').forEach((button) => {
                button.classList.remove('playing');
            });
            playingSounds.clear();
            showStatus('All sounds stopped', 'success');
        } else {
            showStatus('Failed to stop sounds', 'error');
        }
    } catch (error) {
        console.error('Error stopping all sounds:', error);
        showStatus('Network error', 'error');
    }
}

function showStatus(message, type) {
    const indicator = document.getElementById('status-indicator');
    if (!indicator) {
        return;
    }

    indicator.textContent = message;
    indicator.className = `status-indicator status-${type}`;
    indicator.style.display = 'block';

    setTimeout(() => {
        indicator.style.display = 'none';
    }, 2800);
}

document.addEventListener('keydown', (event) => {
    if (event.code === 'Space' || event.code === 'Escape') {
        event.preventDefault();
        stopAllSounds();
    }
});

document.addEventListener('DOMContentLoaded', () => {
    createSoundboard();
});

window.stopAllSounds = stopAllSounds;
window.stopSound = stopSound;
