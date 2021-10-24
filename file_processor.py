import csv
import os

import typer
from statistics import mean

def _eliminate_duplicates(filename: str) -> bool:
    file_with_duplicates = f"{filename}.csv"
    file_without_duplicates = f"{filename}_unique.csv"

    with open(file_with_duplicates, "r") as in_file, open(
        file_without_duplicates, "w"
    ) as out_file:
        seen = set()
        for line in in_file:
            if line in seen:
                continue

            seen.add(line)
            out_file.write(line)

    # remove old file and rename to old name
    os.remove(file_with_duplicates)
    os.rename(file_without_duplicates, file_with_duplicates)
    return True


def process_file(filename: str):
    path = f"{filename}.csv"
    check_crawler_file(path)

    _eliminate_duplicates(filename=filename)

    in_file_name = f"{filename}.csv"
    node_file_name = f"{filename}_nodes.csv"
    edge_file_name = f"{filename}_edges.csv"

    with open(in_file_name, "r") as in_file, open(
        node_file_name, "w"
    ) as node_file, open(edge_file_name, "w") as edge_file:
        reader = csv.DictReader(in_file)
        node_file_writer = csv.writer(node_file)
        edge_file_writer = csv.writer(edge_file)

        node_headers = [
            "url",
            "len_next_urls",
            "len_foreign_urls",
            "body_size",
        ]
        edge_headers = ["url", "next_url"]
        node_file_writer.writerow(node_headers)
        edge_file_writer.writerow(edge_headers)

        nodes_values = set()
        edge_values = set()
        for line in reader:
            nodes_values.add(tuple(line[value] for value in node_headers))
            edge_values.add(tuple(line[value] for value in edge_headers))

        node_file_writer.writerows(nodes_values)
        edge_file_writer.writerows(edge_values)

    msg = typer.style(
        f"Successfully prepared 3 files.\n"
        f"crawler file without duplicates:'{in_file_name}'\n"
        f"node file:'{node_file_name}'\n"
        f"egde file:'{edge_file_name}'",
        fg=typer.colors.GREEN,
        bold=True,
    )
    typer.echo(msg)


def get_mean_values_from_file(filename):
    internal = []
    external = []
    size = []
    with open(filename, "r") as file:
        reader = csv.DictReader(file)
        for line in reader:
            internal.append(int(line['len_next_urls']))
            external.append(int(line['len_foreign_urls']))
            size.append(int(line['body_size']))

    mean_internal = mean(internal or [0])
    mean_external = mean(external or [0])
    mean_size = mean(size or [0])
    return mean_internal, mean_external, mean_size


def check_crawler_file(filename):
    if not os.path.exists(filename):
        msg = typer.style(
            f"File {filename} does not exists!\n"
            "Perhaps you should run crawl first or check name filename again!",
            fg=typer.colors.RED,
            bold=True,
        )
        typer.echo(msg)
        raise typer.Exit()


def get_404(filename):
    with open(f"{filename}.csv", "r") as file:
        reader = csv.DictReader(file)
        errors = []
        for line in reader:
            if line['request_status'] != '200':
                errors.append(line['url'])
        return errors
