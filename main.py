import os

import typer

from crawler import run_crawler
from file_processor import check_crawler_file, get_404, process_file
from graph import create_graph, get_shortest_path, get_stats_messages, plot_from_graph

app = typer.Typer()
app = typer.Typer(
    help="Script allows to run crawler, process files, "
         "get statics and run extra methods"
)


@app.command()
def crawl(
        filename: str = typer.Argument(
            "global_app_spider", help="Filename without extension"
        ),
        crawl: bool = typer.Option(
            False,
            prompt="Are you sure you want to start crawl process?",
            help="The crawl process may take some longer time",
        ),
        override_file: bool = typer.Option(
            False, help="Overrides existing crawler file"),
):
    """
    Crawl process is time consuming. Be patient.
    Logging is enabled, that you can see the process is ongoing.
    Crawler skips redirects 301,302

    :param filename: Filename without extension
    :param crawl: Extra confirmation
    :param override_file: Overrides existing file
    :return: None
    """
    if not crawl:
        raise typer.Exit()

    if not override_file:
        path = f"{filename}.csv"
        if os.path.exists(path):
            msg = typer.style(
                f"Crawler file {path} already exists!\n"
                "To override old file use option --override-file",
                fg=typer.colors.RED,
                bold=True,
            )
            typer.echo(msg)
            raise typer.Exit()

    run_crawler(filename=filename)
    msg = typer.style(
        f"Crawler finished. Do process-crawler-file next",
        fg=typer.colors.GREEN,
        bold=True,
    )
    typer.echo(msg)


@app.command()
def process_crawler_file(
        filename: str = typer.Argument(
            "global_app_spider", help="Filename without extension"
        )
):
    """
    Process the file prepared by scrapy crawler.

    :param filename: Filename without extension
    :return: None
    """
    process_file(filename)


@app.command()
def get_stats(
        filename: str = typer.Argument(
            "global_app_spider", help="Filename without extension"
        )
):
    """
    Get statistics from processed files.

    :param filename: Filename without extension
    :return: None
    """
    graph = create_graph(filename=filename)
    stats_messages = get_stats_messages(graph, filename=filename)

    for msg in stats_messages:
        typer.echo(msg)


@app.command()
def get_orphans(
        filename: str = typer.Argument(
            "global_app_spider", help="Filename without extension"
        )
):
    """
    Get orphans that is internal urls with 404 errors.
    Not checking external links.

    :param filename: Filename without extension
    :return: None
    """
    check_crawler_file(filename)
    errors = get_404(filename)
    if errors:
        for error in errors:
            typer.echo(error)
    else:
        typer.echo('Not found')


@app.command()
def shortest_path(
        from_node: str = typer.Argument(..., help="Starting url "),
        to_node: str = typer.Argument(..., help="Destination url"),
        filename: str = typer.Argument(
            "global_app_spider", help="Filename without extension"
        )
):
    """
    Shows shortest path between urls if exists.

    :param from_node: Starting url
    :param to_node: Destination url
    :param filename: Filename without extension
    :return: None
    """
    graph = create_graph(filename=filename)
    paths = get_shortest_path(graph, from_node=from_node, to_node=to_node)
    if paths:
        for path in paths:
            typer.echo(path)
    else:
        typer.echo('Not found')

@app.command()
def plot_graph(
        plot_name: str = typer.Argument(
            ..., help="Filename without extension"
        ),
        filename: str = typer.Argument(
            "global_app_spider", help="Filename without extension"
        ),
):
    """
    Get plot_name.png file from graph.
    Better plots one can create with for example cytoscape.org/cytoscape.js

    :param plot_name: Name file without extension with plot
    :param filename: Filename without extension
    :return: None
    """
    graph = create_graph(filename=filename)
    plot_from_graph(graph, plot_name=plot_name)

    msg = typer.style(
        f"File '{plot_name}' with plot successfully create",
        fg=typer.colors.GREEN,
        bold=True,
    )
    typer.echo(msg)


if __name__ == "__main__":
    app()
