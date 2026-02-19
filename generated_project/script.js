// Calculator logic implementation

// State variables
let currentInput = '0'; // string representation of the current number
let operator = null;    // current operator (+, -, ×, ÷)
let previousValue = null; // numeric value of the left operand

// DOM reference to the display element
const displayElement = document.getElementById('display');

// Update the calculator display
function updateDisplay() {
    displayElement.textContent = currentInput;
}

// Clear everything and reset to initial state
function clearDisplay() {
    currentInput = '0';
    operator = null;
    previousValue = null;
    updateDisplay();
}

// Remove the last character from the current input
function backspace() {
    if (currentInput.length > 1) {
        currentInput = currentInput.slice(0, -1);
    } else {
        currentInput = '0';
    }
    updateDisplay();
}

// Append a number or decimal point to the current input
function appendNumber(num) {
    if (num === '.') {
        // Prevent multiple decimal points
        if (currentInput.includes('.')) return;
        currentInput += '.';
    } else {
        // Replace leading zero unless it's a decimal point
        if (currentInput === '0') {
            currentInput = num;
        } else {
            currentInput += num;
        }
    }
    updateDisplay();
}

// Set the current operator and prepare for the next operand
function chooseOperator(op) {
    if (operator && previousValue !== null) {
        // If an operator already exists, compute intermediate result
        compute();
    }
    previousValue = parseFloat(currentInput);
    operator = op;
    currentInput = '0';
}

// Perform the calculation based on the stored operator
function compute() {
    if (!operator || previousValue === null) return;
    const currentValue = parseFloat(currentInput);
    let result;
    switch (operator) {
        case '+':
            result = previousValue + currentValue;
            break;
        case '-':
            result = previousValue - currentValue;
            break;
        case '×':
            result = previousValue * currentValue;
            break;
        case '÷':
            // Handle division by zero
            result = currentValue === 0 ? 'Infinity' : previousValue / currentValue;
            break;
        default:
            return;
    }
    // Store result back into currentInput for further operations
    currentInput = result.toString();
    // Reset operator and previous value for a new calculation chain
    operator = null;
    previousValue = null;
    updateDisplay();
}

// Attach event listeners to all buttons
const buttons = document.querySelectorAll('.buttons button');
buttons.forEach(btn => {
    const action = btn.getAttribute('data-action');
    btn.addEventListener('click', () => {
        switch (action) {
            case 'clear':
                clearDisplay();
                break;
            case 'backspace':
                backspace();
                break;
            case '=':
                compute();
                break;
            case '+':
            case '-':
            case '×':
            case '÷':
                chooseOperator(action);
                break;
            default: // numeric or decimal point
                appendNumber(action);
                break;
        }
    });
});

// Keyboard support
document.addEventListener('keydown', e => {
    const key = e.key;
    if (key >= '0' && key <= '9') {
        appendNumber(key);
    } else if (key === '.') {
        appendNumber('.');
    } else if (key === '+') {
        chooseOperator('+');
    } else if (key === '-') {
        chooseOperator('-');
    } else if (key === '*') {
        chooseOperator('×');
    } else if (key === '/') {
        chooseOperator('÷');
    } else if (key === 'Enter' || key === '=') {
        compute();
    } else if (key === 'Backspace') {
        backspace();
    } else if (key === 'c' || key === 'C' || key === 'Esc') {
        clearDisplay();
    }
});

// Initialize display
updateDisplay();
