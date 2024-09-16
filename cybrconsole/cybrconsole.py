from dataclasses import dataclass, field
from typing import Callable, List, Dict, Any
import time
import random

@dataclass
class Action:
    name: str
    func: Callable
    args: Dict[str, Any] = field(default_factory=dict)
    status: str = 'pending'

    def run(self):
        self.func(**self.args)
        self.status = 'completed'

@dataclass
class Phase:
    title: str
    actions: List[Action] = field(default_factory=list)
    status: str = 'pending'

    def add(self, name: str, func: Callable, **kwargs):
        self.actions.append(Action(name, func, kwargs))
        return self

    def run(self):
        for action in self.actions:
            action.run()
        self.status = 'completed'

class Workflow:
    def __init__(self, name: str):
        self.name = name
        self.phases: List[Phase] = []

    def phase(self, title: str) -> Phase:
        phase = Phase(title)
        self.phases.append(phase)
        return phase

    def run(self):
        for phase in self.phases:
            print(f"Running phase: {phase.title}")
            phase.run()

class WorkflowManager:
    def __init__(self):
        self.workflows: Dict[str, Workflow] = {}

    def create(self, name: str) -> Workflow:
        workflow = Workflow(name)
        self.workflows[name] = workflow
        return workflow

    def run(self, name: str):
        if name in self.workflows:
            self.workflows[name].run()
        else:
            raise ValueError(f"Workflow '{name}' not found")

class CybrConsole:
    def __init__(self):
        self.workflow_manager = WorkflowManager()
        self.console = None
        self.progress = None
        self.questionary = None

    def setup_dependencies(self):
        from rich.console import Console
        from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
        import questionary
        self.console = Console()
        self.progress = Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%")
        )
        self.questionary = questionary

    def handle_wait(self, message: str, total: int = 100):
        with self.progress:
            task = self.progress.add_task(f"[cyan]{message}", total=total)
            while not self.progress.finished:
                self.progress.update(task, advance=random.uniform(0, 5))
                time.sleep(0.1)

    def handle_success(self, message: str):
        self.console.print(f"[bold green]✔ {message}[/bold green]")

    def handle_error(self, message: str):
        self.console.print(f"[bold red]✖ {message}[/bold red]")

    def handle_text_area_input(self, prompt: str) -> str:
        return self.questionary.text(prompt, multiline=True).ask()

    def handle_select(self, prompt: str, choices: List[str]) -> str:
        return self.questionary.select(prompt, choices=choices).ask()

    def handle_checkbox(self, prompt: str, choices: List[str]) -> List[str]:
        return self.questionary.checkbox(prompt, choices=choices).ask()

    def display_banner(self, text: str):
        from rich.panel import Panel
        from rich import box
        self.console.print(Panel(text, style="bold magenta", expand=False, box=box.ROUNDED))

    def display_table(self, title: str, data: List[Dict[str, Any]]):
        from rich.table import Table
        table = Table(title=title)
        if data:
            for key in data[0].keys():
                table.add_column(key, style="cyan")
            for row in data:
                table.add_row(*[str(value) for value in row.values()])
            self.console.print(table)
        else:
            self.console.print("[yellow]No data to display[/yellow]")

    def display_tree(self, title: str, data: Dict[str, Any]):
        from rich.tree import Tree
        tree = Tree(f"[bold]{title}")
        self._add_tree_nodes(tree, data)
        self.console.print(tree)

    def _add_tree_nodes(self, tree, data):
        if isinstance(data, dict):
            for key, value in data.items():
                node = tree.add(f"[cyan]{key}")
                self._add_tree_nodes(node, value)
        elif isinstance(data, list):
            for item in data:
                self._add_tree_nodes(tree, item)
        else:
            tree.add(f"[green]{data}")

    def run_example_workflow(self):
        workflow = self.workflow_manager.create("Example Workflow")

        workflow.phase("Initialization") \
            .add("Setup environment", self.setup_env) \
            .add("Create directories", self.create_dirs, path="/tmp/example")

        workflow.phase("Processing") \
            .add("Process data", self.process_data, input_file="data.csv") \
            .add("Generate report", self.generate_report)

        workflow.phase("Finalization") \
            .add("Cleanup", self.cleanup) \
            .add("Send notification", self.send_notification, email="user@example.com")

        self.workflow_manager.run("Example Workflow")

    # Example functions
    def setup_env(self):
        self.handle_wait("Setting up environment...", total=50)
        time.sleep(1)
        self.handle_success("Environment setup complete")

    def create_dirs(self, path: str):
        self.handle_wait(f"Creating directory at {path}...", total=30)
        time.sleep(1)
        self.handle_success(f"Directory created at {path}")

    def process_data(self, input_file: str):
        self.handle_wait(f"Processing data from {input_file}...", total=100)
        time.sleep(2)
        self.handle_success(f"Data processed from {input_file}")

    def generate_report(self):
        self.handle_wait("Generating report...", total=75)
        time.sleep(1.5)
        self.handle_success("Report generated")

    def cleanup(self):
        self.handle_wait("Cleaning up...", total=40)
        time.sleep(1)
        self.handle_success("Cleanup complete")

    def send_notification(self, email: str):
        self.handle_wait(f"Sending notification to {email}...", total=25)
        time.sleep(1)
        self.handle_success(f"Notification sent to {email}")

def main():
    cybr_console = CybrConsole()
    cybr_console.setup_dependencies()
    cybr_console.display_banner("Welcome to CybrConsole")
    cybr_console.run_example_workflow()

    # Example usage of new TUI elements
    selected_option = cybr_console.handle_select("Choose an option:", ["Option 1", "Option 2", "Option 3"])
    cybr_console.console.print(f"You selected: {selected_option}")

    selected_items = cybr_console.handle_checkbox("Select items:", ["Item 1", "Item 2", "Item 3", "Item 4"])
    cybr_console.console.print(f"You selected: {', '.join(selected_items)}")

    cybr_console.display_table("Sample Data", [
        {"Name": "Alice", "Age": 30, "City": "New York"},
        {"Name": "Bob", "Age": 25, "City": "Los Angeles"},
        {"Name": "Charlie", "Age": 35, "City": "Chicago"}
    ])

    cybr_console.display_tree("Project Structure", {
        "src": {
            "main.py": None,
            "utils": ["helper.py", "config.py"]
        },
        "tests": ["test_main.py", "test_utils.py"],
        "docs": ["README.md", "CONTRIBUTING.md"]
    })

    user_input = cybr_console.handle_text_area_input("Enter your thoughts on CybrConsole: ")
    cybr_console.console.print(f"\nYour input: {user_input}")

if __name__ == "__main__":
    main()
