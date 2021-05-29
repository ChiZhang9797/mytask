from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from rich.columns import Columns

def grid_layout(tasks):
    """ Displays tasks in a grid format using rich """

    panels = []
    for i, task in enumerate(tasks):
        ind = Text(str(i + 1), style="bold green")
        name = Text(task.name, style="blue")
        created_date = Text(
            task.created_date.strftime("%d/%m/%Y %H:%M"), 
            style="italic magenta"
        )
        detail = Text(task.detail, style="gray") \
            if task.detail else "None"
        
        completed = Text("(completed) ", style="green") \
            if task.completed else ""

        task_summary = Text.assemble(
            ind, 
            ". ", 
            completed,
            name,
            "\nCreated at: ",
            created_date,
            "\nDetail: ",
            detail,
        )

        panels.append(Panel(task_summary, expand=True))

    console = Console()
    console.print((Columns(panels, width=30, expand=True)))

