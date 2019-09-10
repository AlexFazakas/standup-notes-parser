#!/usr/bin/env python3.7

import click
import gitlab
import datetime
import sys
import os

from jinja2 import Environment, FileSystemLoader

GITLAB_SERVER = 'https://gitlab.codethink.co.uk'
ERROR = 1


@click.command()
@click.option('-n', '--project_id', type=int, nargs=1, required=True)
@click.option('-t', '--token', type=str, nargs=1, required=True)
@click.option('-s', '--server', type=str, nargs=1, default=GITLAB_SERVER)
@click.option('-f', '--content_file',
              type=click.Path(file_okay=True,
                              readable=True,
                              resolve_path=True,
                              exists=True),
              nargs=1,
              required=True)
def main(project_id, token, content_file, server):
    server = gitlab.Gitlab(server, private_token=token)
    project = server.projects.get(project_id)
    standups_page = project.wikis.get('Standups')
    page_content = get_page_content(content_file)
    current_date = datetime.datetime.now()
    page_slug = current_date.isoformat()[:10]
    page_title = f'{current_date.day}/{current_date.month}/{current_date.year}'
    project.wikis.create({'title': page_slug.replace('/', ' '),
                          'content': page_content})
    print('Created page with title {} and slug {}'.format(page_title, page_slug))
    standups_page.content = get_updated_standups_page(standups_page,
                                                      page_title,
                                                      page_slug)
    standups_page.save()
    print('Updated standups page!')

def get_updated_standups_page(standups_page, page_title, page_slug):
    return standups_page.content + f'\n\n[{page_title}]({page_slug})'

def get_page_content(content_file):
    with open(content_file, 'r') as f:
        lines = iter(f.readlines())

    participants_lines = []
    discussion_lines = []
    for line in lines:
        participants_lines.append(line.split('> ')[1].rstrip())
        if line.find('# Discussion') >= 0:
            break
    for line in lines:
        discussion_lines.append(line.rstrip())

    file_loader = FileSystemLoader(os.getcwd())
    env = Environment(loader=file_loader)
    template = env.get_template('standup_notes.j2')
    new_content = template.render(participants_lines=participants_lines,
                                  discussion_lines=discussion_lines)
    return new_content


if __name__ == '__main__':
    main()
