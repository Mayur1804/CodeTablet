# Calculator Project

## Overview

This is a simple, responsive web‑based calculator built with vanilla HTML, CSS, and JavaScript. It supports the four basic arithmetic operations (addition, subtraction, multiplication, division), a clear button, backspace, and equals. The UI is minimal yet fully functional on both desktop and mobile browsers.

The project is split into three files:

- **index.html** – Defines the calculator layout and button elements.
- **styles.css** – Provides styling and responsive behavior.
- **script.js** – Implements all calculator logic and event handling.


## Features

| Feature | Description |
|---------|-------------|
| Basic Arithmetic | `+`, `-`, `×`, `÷` operations |
| Clear & Backspace | Reset or delete last digit |
| Keyboard Support | Full keyboard mapping (see Usage) |
| Responsive Design | Works on mobile and desktop |
| Modifiable Code | Easy to extend with new functions |


## Setup

No build step is required. Simply open `index.html` in your browser:

```bash
# From the project root
open index.html   # macOS
start index.html  # Windows
xdg-open index.html  # Linux
```

The calculator will load automatically and is ready for use.


## Usage

### Button Functions
| Button | Action |
|--------|--------|
| `0`–`9` | Append digit |
| `.` | Append decimal point |
| `+` `-` `×` `÷` | Set current operator and prepare for next operand |
| `=` | Compute the current expression |
| `C` | Clear the display and reset state |
| `⌫` | Delete the last character |

### Keyboard Shortcuts
| Key | Action |
|-----|--------|
| `0`–`9` | Append digit |
| `.` | Append decimal point |
| `+` `-` `*` `/` | Corresponding operator (`*` → `×`, `/` → `÷`) |
| `Enter` or `=` | Compute |
| `Backspace` | Delete last character |
| `c`, `C`, or `Esc` | Clear display |

The mapping is implemented in `script.js` inside the `keydown` event listener.


## Customization

### Styling
All visual aspects are defined in **styles.css**. To change the calculator’s look:

1. Edit color values, font sizes, or spacing.
2. Add new CSS rules targeting `.calculator`, `.display`, or `.buttons button`.
3. Use media queries to adjust layout for different screen sizes.

Example – change button background:

```css
.buttons button {
    background: #f0f8ff; /* light blue */
}
```

### Extending Functionality
The logic resides in **script.js**. To add a new operation (e.g., exponentiation `^`):

1. Add a button in `index.html`:
   ```html
   <button id="btn-exponent" data-action="^">^</button>
   ```
2. In `script.js`, extend the `chooseOperator` and `compute` functions:
   ```js
   function chooseOperator(op) {
       if (operator && previousValue !== null) {
           compute();
       }
       previousValue = parseFloat(currentInput);
       operator = op;
       currentInput = '0';
   }
   
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
               result = currentValue === 0 ? 'Infinity' : previousValue / currentValue;
               break;
           case '^':
               result = Math.pow(previousValue, currentValue);
               break;
           default:
               return;
       }
       currentInput = result.toString();
       operator = null;
       previousValue = null;
       updateDisplay();
   }
   ```
3. Update the keyboard mapping in the `keydown` listener if desired.

Feel free to add more advanced math functions (sin, cos, etc.) following the same pattern.


## Key Functions (excerpt from `script.js`)

```js
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

// Append a number or decimal point to the current input
function appendNumber(num) {
    if (num === '.') {
        if (currentInput.includes('.')) return;
        currentInput += '.';
    } else {
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
            result = currentValue === 0 ? 'Infinity' : previousValue / currentValue;
            break;
        default:
            return;
    }
    currentInput = result.toString();
    operator = null;
    previousValue = null;
    updateDisplay();
}
```

These functions form the core of the calculator’s behaviour. All button events and keyboard interactions are wired to them.


## License

This project is released under the MIT License.
