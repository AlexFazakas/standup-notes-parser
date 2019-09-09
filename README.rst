===================
standup-notes-parser
===================
A simple python script to parse standup notes and automatically post them to the GitLab wiki.

.. code:: bash

$ Usage: parser.py [OPTIONS]

$ Options:
  $ -n, --project_id INTEGER  [required]
  $ -t, --token TEXT          [required]
  $ -s, --server TEXT
  $ -f, --content_file PATH   [required]
