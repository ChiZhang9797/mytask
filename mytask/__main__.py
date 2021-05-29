import click
import sys
from .models import Tasks, Base
from .database import Session, engine
from .layouts import grid_layout

Base.metadata.create_all(engine)

session = Session()

def map_num_to_id(tasks):
    id_dict = dict()
    for i, row in enumerate(tasks):
        id_dict.update({i + 1: row.id})
    return id_dict


def parse_indices(task_numbers):
    inds = []
    for num in task_numbers:
        try:
            ind = int(num)
        except ValueError:
            click.echo(f"Fail to parse the argument: {num}")
            continue
        inds.append(ind)
    return inds


@click.group()
def cli():
    pass

@click.command(help="Adds a task to your task list")
@click.argument("task", nargs=-1)
@click.option(
    "--detail", 
    "-d",
    prompt="Detail about this task",
    prompt_required=False,
    help="Adds detail about this task"
)
def add(task, detail):
    task_str = " ".join(task)
    if detail:
        new_task = Tasks(name=task_str, detail=detail)
    else:        
        new_task = Tasks(name=task_str)
    try:
        session.add(new_task)
        session.commit()
    except:
        click.echo(f"Something went wrong: {sys.exc_info()[0]}")
        return

    click.echo(f"Added \"{task_str}\" to your task list")
    

@click.command(help="Marks a task as complete")
@click.argument("task_numbers", nargs=-1)
def do(task_numbers):
    inds = parse_indices(task_numbers)

    tasks = session.query(Tasks).all();
    id_dict = map_num_to_id(tasks)

    for ind in inds:
        if ind <= 0 or ind > len(tasks):
            click.echo(f"Invalid task number: {ind}")
            continue
        
        task = session.query(Tasks).filter(Tasks.id==id_dict[ind])
        if task.first().completed:
            click.echo(f"task #{ind} is already completed")
        else: 
            try:
                task.update({Tasks.completed: True})
                session.commit()
            except:
                click.echo(
                    f"Failed to mark task #{ind} as complete: " 
                    + f"{sys.exc_info()[0]}"
                )
                continue

            click.echo(f"Marked task #{ind} as complete. ✔️")


@click.command(help="Deletes a task")
@click.argument("task_numbers", nargs=-1)
def delete(task_numbers):
    inds = parse_indices(task_numbers)
            
    tasks = session.query(Tasks).all()
    id_dict = map_num_to_id(tasks)

    for ind in inds:
        if ind <= 0 or ind > len(tasks):
            click.echo(f"Invalid task number: {ind}")
            continue
        
        task = session.query(Tasks).filter(Tasks.id==id_dict[ind])
        try:
            task.delete(synchronize_session=False)
            session.commit()
        except:
            click.echo(
                f"Failed to delete task #{ind}: {sys.exc_info()[0]}"
            )
            continue

        click.echo(f"Deleted task #{ind} 🗑️")


@click.command(name="list", help="Displays all tasks")
def lis():
    try:
        tasks = session.query(Tasks).all()
    except:
        sys.exit(f"Something went wrong. {sys.exc_info()[0]}")

    if len(tasks) == 0:
        click.echo("You have no tasks, take a vacation!🏖️")
        return

    click.echo("You have the following tasks:")
    grid_layout(tasks)


cli.add_command(add)
cli.add_command(do)
cli.add_command(delete)
cli.add_command(lis)

if __name__ == "__main__":
    cli()