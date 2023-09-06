#!/usr/bin/env python
import os
import sys
import coverage
from django.core.management import execute_from_command_line

# Set the path to your Django project settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "trade_core.settings")

def run_tests():
    cov = coverage.Coverage()
    cov.start()

    execute_from_command_line(sys.argv)

    cov.stop()
    cov.save()

if __name__ == "__main__":
    run_tests()
