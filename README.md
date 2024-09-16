# CybrConsole

CybrConsole is a Python-based console application that combines workflow management with advanced text-based user interface (TUI) and command-line interface (CLI) elements.

## Features

- Workflow management system
- Advanced TUI elements for improved user interaction:
  - Progress bars with spinners
  - Select and checkbox inputs
  - Tables for displaying structured data
  - Tree views for hierarchical data
- CLI progress indicators and status messages

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/cybrconsole.git
   ```

2. Change to the project directory:
   ```
   cd cybrconsole
   ```

3. Install the project dependencies:
   - If using Poetry:
     ```
     poetry install
     ```
   - If using uv:
     ```
     uv venv
     uv pip install -r requirements.txt
     ```

## Usage

Run the main script:

- If using Poetry:
  ```
  poetry run python cybrconsole/cybrconsole.py
  ```
- If using uv:
  ```
  uv pip python cybrconsole/cybrconsole.py
  ```

This will start an example workflow and demonstrate the various TUI/CLI elements, including:
- An example workflow with progress indicators
- A select input for choosing options
- A checkbox input for selecting multiple items
- A table display of sample data
- A tree view of a project structure

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
