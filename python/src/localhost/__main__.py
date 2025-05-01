import typer
from pathlib import Path
from .config import load_config
from .ssr_server import run_ssr_server
from .ssg_server import run_ssg_server

app = typer.Typer()

@app.command()
def serve(
    host: str = typer.Option(None, help="Server host (default from config or CLI)"),
    port: int = typer.Option(None, help="Server port (default from config or CLI)"),
    public_dir: Path = typer.Option(None, help="Directory of static files"),
    ssr_dir: Path = typer.Option(None, help="Directory for SSR dynamic functions"),
    ssr_provider: str = typer.Option(None, help="SSR provider (only 'default' is supported)"),
    config: Path = typer.Option(None, help="Optional config file path")
):
    if ssr_provider and ssr_provider.lower() not in ['default', '']:
        raise typer.Exit("Error: --ssr-provider is not supported in Python version.")

    # load_config parameters order: host, port, ssr_dir, ssg_dir, ssr_provider, cli_config
    cfg = load_config(host, port, ssr_dir, public_dir, ssr_provider, config)
    if ssr_dir:
        run_ssr_server(cfg)
    else:
        run_ssg_server(cfg)

if __name__ == "__main__":
    app()
