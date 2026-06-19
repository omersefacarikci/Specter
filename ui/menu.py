from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Confirm, Prompt
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich import box
from rich.text import Text
from rich.columns import Columns

console = Console()

BANNER = """
[bold red]
 ███████╗██████╗ ███████╗ ██████╗████████╗███████╗██████╗ 
 ██╔════╝██╔══██╗██╔════╝██╔════╝╚══██╔══╝██╔════╝██╔══██╗
 ███████╗██████╔╝█████╗  ██║        ██║   █████╗  ██████╔╝
 ╚════██║██╔═══╝ ██╔══╝  ██║        ██║   ██╔══╝  ██╔══██╗
 ███████║██║     ███████╗╚██████╗   ██║   ███████╗██║  ██║
 ╚══════╝╚═╝     ╚══════╝ ╚═════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝
[/bold red]
[dim]Ghost follower hunter — GitHub Bot Cleaner[/dim]
"""

def show_banner():
    console.print(BANNER)

def show_menu() -> str:
    console.print(Panel(
        "[1] Detect and block bot followers\n"
        "[2] Unfollow users who don't follow you back\n"
        "[3] Star my own repositories\n"
        "[4] Generate report only (safe)\n"
        "[5] Exit",
        title="[bold]What do you want to do?[/bold]",
        border_style="red",
        padding=(1, 2)
    ))
    return Prompt.ask("[bold red]Choice[/bold red]", choices=["1", "2", "3", "4", "5"])

def show_bot_table(bots: list):
    if not bots:
        console.print("[green]✓ No bots detected![/green]")
        return
    
    table = Table(
        title=f"[red] {len(bots)} Bot/Spam accounts detected![/red]",
        box=box.ROUNDED,
        border_style="red",
        show_lines=True
    )
    table.add_column("User", style="bold white", min_width=20)
    table.add_column("Reason", style="dim", min_width=40)
    table.add_column("Profile", style="cyan")
    
    for bot in bots:
        table.add_row(
            bot["login"],
            bot["reason"][:60] + ("..." if len(bot["reason"]) > 60 else ""),
            f"github.com/{bot['login']}"
        )
    console.print(table)

def show_unfollow_table(users: list):
    if not users:
        console.print("[green]✓ No users found who don't follow you![/green]")
        return

    table = Table(
        title=f"[yellow] {len(users)} Users who don't follow you back[/yellow]",
        box=box.ROUNDED,
        border_style="yellow",
        show_lines=True
    )
    table.add_column("User", style="bold white", min_width=20)
    table.add_column("Profile", style="cyan")

    for u in users:
        table.add_row(u["login"], f"github.com/{u['login']}")
    console.print(table)

def show_repos_table(repos: list):
    table = Table(
        title=f"[cyan] {len(repos)} repos to be starred[/cyan]",
        box=box.ROUNDED,
        border_style="cyan"
    )
    table.add_column("Repo", style="bold white")
    table.add_column("Star count", style="yellow", justify="right")
    for r in repos:
        table.add_row(r["full_name"], str(r.get("stargazers_count", 0)))
    console.print(table)

def confirm(msg: str) -> bool:
    return Confirm.ask(f"[bold yellow]{msg}[/bold yellow]")

def spinner(msg: str):
    return Progress(
        SpinnerColumn(),
        TextColumn(f"[cyan]{msg}[/cyan]"),
        transient=True
    )

def success(msg: str):
    console.print(f"[bold green]✓[/bold green] {msg}")

def error(msg: str):
    console.print(f"[bold red]✗[/bold red] {msg}")

def info(msg: str):
    console.print(f"[bold red]→[/bold red] {msg}")
