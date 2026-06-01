#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ia_project.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        user_site = os.path.expanduser('~/.local/lib/python3.12/site-packages')
        if os.path.isdir(user_site) and user_site not in sys.path:
            sys.path.insert(0, user_site)
        from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
