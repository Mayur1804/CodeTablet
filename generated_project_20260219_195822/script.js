// Declare core variables for time tracking
let workDuration = 25; // in minutes
let breakDuration = 5; // in minutes
let remainingTime = workDuration * 60; // time converted to seconds
let timer;
let isRunning = false;

// Array to store mindful suggestions
const suggestions = [
    'Take a deep breath and relax.',
    'Stretch your arms and legs.',
    'Reflect on a positive moment.'
];

// Function to update the display
function updateDisplay() {
    const minutes = Math.floor(remainingTime / 60);
    const seconds = remainingTime % 60;
    document.getElementById('timer-display').textContent = 
        `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    document.getElementById('timer-display').className = 
        isRunning ? 'work' : 'break'; // Highlight based on mode
}

// Function to start the timer
function startTimer() {
    const workInput = parseInt(document.getElementById('work-duration').value, 10);
    const breakInput = parseInt(document.getElementById('break-duration').value, 10);

    if (!isNaN(workInput)) {
        workDuration = workInput;
    } else {
        workDuration = 25;
    }

    if (!isNaN(breakInput)) {
        breakDuration = breakInput;
    } else {
        breakDuration = 5;
    }

    remainingTime = workDuration * 60;

    if (!isRunning) {
        isRunning = true;
        updateDisplay(); // Update display to show work mode
        timer = setInterval(() => {
            if (remainingTime > 0) {
                remainingTime--;
                updateDisplay();
            } else {
                clearInterval(timer);
                isRunning = false;
                alert('Time is up!');
                
                // When the timer ends (beginning of a break)
                const randomSuggestion = suggestions[Math.floor(Math.random() * suggestions.length)];
                document.getElementById('mindful-suggestions').textContent = randomSuggestion;
                updateDisplay(); // Update to show break mode (color change)
            }
        }, 1000);
    }
}

// Function to pause the timer
function pauseTimer() {
    if (isRunning) {
        clearInterval(timer);
        isRunning = false;
        updateDisplay(); // Update to show break mode (color change)
    }
}

// Function to reset the timer
function resetTimer() {
    clearInterval(timer);
    isRunning = false;
    remainingTime = workDuration * 60;
    updateDisplay();
}

// Function to update timer settings based on input fields
function updateTimerSettings(event) {
    const value = parseInt(event.target.value, 10);
    if (!isNaN(value)) {
        if (event.target.id === 'work-duration') {
            workDuration = value;
        } else if (event.target.id === 'break-duration') {
            breakDuration = value;
        }
    } else {
        if (event.target.id === 'work-duration') {
            workDuration = 25;
        } else if (event.target.id === 'break-duration') {
            breakDuration = 5;
        }
    }
    remainingTime = workDuration * 60;
    updateDisplay();
}

// Add event listeners for input fields
document.getElementById('work-duration').addEventListener('focusout', updateTimerSettings);
document.getElementById('break-duration').addEventListener('focusout', updateTimerSettings);

// Set initial display
updateDisplay();

// Add event listeners for buttons
document.getElementById('start-btn').addEventListener('click', startTimer);
document.getElementById('pause-btn').addEventListener('click', pauseTimer);
document.getElementById('reset-btn').addEventListener('click', resetTimer);
