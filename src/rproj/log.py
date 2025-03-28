from rich import print

ERR_PFX = "[red]ERR:[/red]"
INFO_PFX = "[green]INFO:[/green]"
WARN_PFX = "[yellow]WARN:[/yellow]"


def err(msg, *args, **kwargs):
    print(f"{ERR_PFX} {msg}", *args, **kwargs)

def info(msg, *args, **kwargs):
    print(f"{INFO_PFX} {msg}", *args, **kwargs)

def warn(msg, *args, **kwargs):
    print(f"{WARN_PFX} {msg}", *args, **kwargs)
