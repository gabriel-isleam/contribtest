#!/usr/bin/python3
# generate site from static pages, loosely inspired by Jekyll
# run like this:
#   ./generate.py test/source output
# the generated `output` should be the same as `test/expected_output`

import os
import logging
import jinja2
import sys
from jinja2 import FileSystemLoader
import json

log = logging.getLogger(__name__)

# checks all files in the folder_path and yields
# the path only for the files with extension .rst
def list_files(folder_path):
    for name in os.listdir(folder_path):
        base, ext = os.path.splitext(name)
        if ext != '.rst':
            continue
        yield os.path.join(folder_path, name)

# returns the content of the file as a tuple of a
# dictionary and a string -> (metadata, content)
def read_file(file_path):
    with open(file_path, 'rb') as f:
        raw_metadata = ""
        for line in f:
            decoded_line = line.decode("utf-8").strip()
            if decoded_line == '---':
                break
            raw_metadata += decoded_line
        content = ""
        for line in f:
            decoded_line = line.decode("utf-8").strip()
            content += decoded_line
    return json.loads(raw_metadata), content

# write the html code to the 'name' file from output_folder
def write_output(output_folder, name, html):
    if not os.path.exists(output_folder):
    	os.makedirs(output_folder)
    with open(os.path.join(output_folder, name+'.html'), "wt") as f:
        f.write(html)

def generate_site(folder_path, output_folder):
    log.info("Generating site from %r", folder_path)
    # create an environment to store the configuration and
    # global variables, but also helps to load templates
    jinja_env = jinja2.Environment(loader=FileSystemLoader(folder_path + '/layout'))
    for file_path in list_files(folder_path):
        metadata, content = read_file(file_path)
        template_name = metadata['layout']
        # loads a template from the environment
        #print(template_name)
        template = jinja_env.get_template(template_name)
        data = dict(metadata, content=content)
        # render the template with the variables from data
        html = template.render(**data)
        # take the file_name from the path
        path, file_name = os.path.split(file_path)
        # remove extension from the file_name
        name, ext = os.path.splitext(file_name)
        write_output(output_folder, name, html)
        log.info("Writing %r with template %r", name, template_name)


def main():
    generate_site(sys.argv[1], sys.argv[2])


if __name__ == '__main__':
    logging.basicConfig()
    main()
