"""remove_contest.py
Utility script to remove contest settings from the contest table file.

@:arg contest_id: str identifier of the contest to remove.
"""

import os.path
import argparse
from contests import *
from gph_logging import log_message

parser = argparse.ArgumentParser()
parser.add_argument('contest_id', type=str, help='Unique contest identifier.')

args = parser.parse_args()
contest_id = args.contest_id

if not os.path.exists('contest-table.txt'):
    log_message('Contest table file not found!')
    raise FileNotFoundError('Contest table file not found!')
else:
    # Load contest table from file
    with open('contest-table.txt', 'rb') as infile:
        indata = infile.read()

    indata = eval(indata)
    contest_table = ContestTable(indata)

# Print settings and remove contest
print(f'Removing contest {contest_id} with settings: \n'
      f'{pprint.pformat(contest_table.get_contest(contest_id))}')

contest_table.remove_contest(contest_id)
contest_table.to_file('contest-table')
