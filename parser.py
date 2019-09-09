#!/usr/bin/env python3.7

import click
import gitlab

GITLAB_SERVER = 'https://gitlab.codethink.co.uk'


@click.command()
@click.option('-n', '--project_id', type=int, nargs=1, required=True)
@click.option('-t', '--token', type=str, nargs=1, required=True)
@click.option('-s', '--server', type=str, nargs=1, default=GITLAB_SERVER)
@click.option('-f', '--content',
              type=click.Path(file_okay=True,
                              readable=True,
                              resolve_path=True),
              nargs=1,
              required=True)
def main(project_id, token, content, server):
    server = gitlab.Gitlab(server, private_token=token)
    project = server.projects.get(project_id)
    print(project.wikis.list())


if __name__ == '__main__':
    main()
