import click
import json
from .common import loader


def read_data(file_path: str = None) -> dict:
    """
    read JSON data file.
    """
    if file_path is None:
        return {}

    with open(file_path, "r+", encoding="utf-8") as json_file:
        req_data = json.load(json_file)
        return req_data


@click.command()
@click.option('-h', '--hook', help='hook function file.')
@click.option('-q', '--request', help='request data file.')
@click.option('-s', '--response', help='response data file.')
def main(hook, request, response):
    """Copycat CLI."""
    
    if hook:
        req_data = read_data(request)
        resp_data = read_data(response)
        # check hook function
        resp = loader(file_name=hook, request=req_data, response=resp_data)
        click.echo(f"response:\n {resp}")


if __name__ == '__main__':
    main()
