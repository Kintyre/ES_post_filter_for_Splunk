# Developing es_post_filter_for_Splunk

## Development

Setup a local virtual environment in the top level of the package to install the necessary build and runtime requirements.

    python -m virtualenv venv
    . venv/bin/activate
    python -m pip install -U -r requirements-dev.txt

Setup pre-commit

    pre-commit install --install-hooks

## Building

You can build ES Post-filter for Splunk using the following steps:

    ./build.py && "$SPLUNK_HOME/bin/splunk" install app "$(<.release_path)" -update 1

The above command will build and (re)install the app into a running Splunk development instance.

## Tools

 * [Cookiecutter](https://github.com/audreyr/cookiecutter) is use to kickstart the development of new addons.
 * [bump2version](https://pypi.org/project/bump2version/) Version bump your addon with a single command!
 * [ksconf](https://ksconf.readthedocs.io/) Kintyre Splunk CONF tool
 * [pre-commit](https://pre-commit.com/) a framework for managing and maintaining pre-commit hooks for git.
