from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from rich.columns import Columns

def grid_layout(tasks, num_dict):
    """ Displays tasks in a grid format using rich """

    panels = []
    for task in tasks:
        ind = Text(str(num_dict[task.id]), style="bold green")
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

