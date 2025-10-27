# pyditor
[![PyPI version](https://img.shields.io/pypi/v/pyditor)](https://pypi.org/project/pyditor/)
[![Python versions](https://img.shields.io/pypi/pyversions/pyditor)](https://pypi.org/project/pyditor/)
[![License](https://img.shields.io/pypi/l/pyditor)](https://github.com/sshu2017/pyditor/blob/main/LICENSE)

## A minimalist Python runner

Pyditor is a lightweight, standalone Python code editor and runner built with Tkinter. It provides a simple interface for writing and executing Python code with syntax highlighting and real-time output display. Perfect for coding interviews, quick prototyping, and learning Python.

<p align="center">
    <img src="assets/screenshot.gif" width="50%" alt="Pyditor Demo">
</p>

## Features

- **Clean UI**: Minimalist interface with syntax highlighting for Python code
- **Instant Execution**: Run Python code with a single click
- **Real-time Output**: Displays stdout, stderr, and execution status
- **Syntax Highlighting**: Color-coded keywords, strings, comments, numbers, and built-in functions
- **Multi-monitor Support**: Automatically centers window on the active monitor (Linux/xrandr)
- **File Operations**: Save code snippets for later use
- **Timeout Protection**: Automatic timeout after 5 seconds to prevent infinite loops

## Installation

### Prerequisites
- Python 3.6 or higher
- Tkinter (usually included with Python)

 - Note: While Tkinter is part of Python's standard library, many Linux distributions separate GUI components like Tkinter into their own packages. Run this if Tkiniter is missing:
```bash
sudo apt update
sudo apt install python3-tk
```


### Setup

```bash
pip install pyditor
```

### Run
Run ```pyditor``` in termianl (MacOS and Linux) or in powershell (Windows).


## Keyboard Shortcuts

The application uses standard Tkinter text widget shortcuts:
- **Ctrl+A**: Select all
- **Ctrl+C**: Copy
- **Ctrl+V**: Paste
- **Ctrl+X**: Cut
- **Ctrl+Z**: Undo


## License

MIT License - see [LICENSE](LICENSE) for details

## Use Cases

- Coding interviews and technical assessments
- Quick Python prototyping and testing
- Learning Python syntax and features
- Code snippet testing without IDE overhead
- Teaching Python programming basics

## Contributing

This is a minimalist tool by design. If you find bugs or have suggestions, feel free to open an issue or submit a pull request.
