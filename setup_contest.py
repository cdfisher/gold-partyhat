"""setup_contest.py
Script for adding a new Gold Partyhat contest to the contest-table file.
Default values for optional arguments are set in gph_config.py

@:arg target: str in hs.SKILLS, hs.ACTIVITIES, hs.BOSSES, or 'multi' (NYI) denoting the specific target to track.
@:arg title: str The name of the contest.
@:arg start: str representation of a datetime object in the form '[DD MM YYYY - HH:MM]' to mark the start of the
contest. Included for future use by a planned feature to automatically create cronjobs. Not yet used.
@:arg end: str representation of a datetime object in the form '[DD MM YYYY - HH:MM]' to mark the end of the
contest. Included for future use by a planned feature to automatically create cronjobs. Not yet used.
@:arg group: str The name of the text file listing group members to track, excluding the file extension.
@:arg --force_id: str Manually sets contest_id to a given value. Otherwise defaults to generating an ID value.
@:arg --threshold: int The minimum increase in score a user needs to gain during the contest in order to be
considered a participant at the end. Default value: 100
@:arg --top_n: int The number of top participants to list when running updates. Default value: 5
@:arg --winners: int The number of contest winners. Default value: 3
@:arg --raffle_winners: int The number of participation prizes available. Default value: 3
@:arg --raffle_mode: str in {'classic', 'top_participants'}. Optional flag defaulting to 'top_participants' used
to set how the end of contest raffle works.
@:arg --participants: int The number of top participants to include in the end of contest raffle
if raffle_mode = 'top_participants'.
@:arg --datafile: str. Optional flag to set the name of the file where contest data is stored, not including a file
extension.  Defaults to title.lower.replace(' ', '-'), with any other special characters removed.
@:arg --logfile: str. Optional flag to set the name of the file where log messages are stored, not including a file
extension.  Defaults to (title.lower.replace(' ', '-') + '-log'), with any other special characters removed.
@:arg --interval: int Optional argument to set the interval at which the contest updates, in hours. Defaults to 6.
Included for future use by a planned feature to automatically create cronjobs. Not yet used.
@:arg --silent, -s: bool Optional argument to disable sending of messages to Discord when running contest
scripts for the duration of the contest. Defaults to False
@:arg --quiet, -q: bool Runs script without sending messages to Discord, but does not stop other updates run for
this contest from sending messages. Defaults to False

Example call for a contest:

"python setup_contest.py 'hitpoints' 'My Hitpoints Contest' '[01 12 2022 - 19:00]' '[08 12 2022 - 19:00]' 'group'
--threshold 50000"

"""

import os.path
import re
import argparse
from hashlib import sha1
from contests import *
from gph_utils.gph_config import *
from gph_utils.gph_logging import log_message
import hs_wrapper as hs

parser = argparse.ArgumentParser()
parser.add_argument('target', type=str, help='The goal to track with this contest.')
parser.add_argument('title', type=str, help='Title of the contest.')
parser.add_argument('start', type=str, help='Timestamp marking the start of the contest, '
                                            'in the form "[DD MM YYYY - HH:MM]."')
parser.add_argument('end', type=str, help='Timestamp marking the end of the contest, '
                                          'in the form "[DD MM YYYY - HH:MM]."')
parser.add_argument('group', type=str, help='Name of the text file where group members are listed, excluding the'
                                            'file extension.')
parser.add_argument('--force_id', nargs='?', default='', type=str, help='Set the contest ID to be a specific value '
                                                                        'instead of an automatically generated one.')
parser.add_argument('--threshold', nargs='?', default=THRESHOLD, type=int, help='The amount of XP, KC, or score needed '
                                                                                'to be counted as a participant.')
parser.add_argument('--top_n', nargs='?', default=TOP_N, type=int, help='The number of top participants to list when '
                                                                        'updating the contest.')
parser.add_argument('--winners', nargs='?', default=WINNERS, type=int, help='The number of contest winners.')
parser.add_argument('--raffle_winners', nargs='?', default=3, type=int, help='The number of participation prizes'
                                                                             ' available.')
parser.add_argument('--participants', nargs='?', default=N_PARTICIPANTS, type=int, help='The number of participants to '
                                                                                        'include in the end of contest '
                                                                                        'raffle if raffle_mode = '
                                                                                        '"top_participants"')
parser.add_argument('--raffle_mode', type=str, choices=['classic', 'top_participants'], default='top_participants',
                    help='The mode to use at the end of the contest to draw participation prizes.')
parser.add_argument('--dynamic_prizes', help='Determine the number of raffle prizes given out when using raffle_mode'
                                             'classic based on number of participants using '
                                             'n = 3 + floor(participants / 10)', action='store_true')
parser.add_argument('--datafile', type=str, help='File name of where to save contest data, excluding the extension.')
parser.add_argument('--logfile', type=str, help='File name of where the logs will be saved, excluding the extension.')
parser.add_argument('--interval', type=int, default=6, help='The number of hours between updates.')
parser.add_argument('-s', '--silent', help='Runs script without sending messages to Discord,'
                                           ' and persists for the whole contest.', action='store_true')

#TODO Multi_targets NYI
#parser.add_argument('-m', '--multi_targets', type=str, default='{}', help='String representation of a dictionary of '
#                                                                          'targets and weights to use in conjunction '
#                                                                          'with the flag -target \'multi\'.')

# Assign variables from args and use defaults if no value given
settings = dict()
args = parser.parse_args()
settings['contest_id'] = args.force_id
settings['title'] = args.title
settings['target'] = args.target
settings['threshold'] = int(args.threshold)
settings['group'] = args.group + '.txt'
settings['top_n'] = int(args.top_n)
settings['winners'] = int(args.winners)
settings['raffle_mode'] = args.raffle_mode
settings['raffle_winners'] = int(args.raffle_winners)
settings['silent'] = bool(args.silent)
settings['start'] = args.start
settings['end'] = args.end
settings['interval'] = int(args.interval)
settings['update_number'] = 0
settings['n_participants'] = int(args.participants)
settings['dynamic_prizes'] = bool(args.dynamic_prizes)
ftitle = args.title
ftitle = re.sub(' ', '-', ftitle)
ftitle = re.sub('[!@#$%^&*()+=,/<>?|]', '', ftitle)
if args.datafile is None:
    datafile = ftitle.lower() + '.csv'
else:
    datafile = args.datafile + '.csv'
settings['datafile'] = datafile
if args.logfile is None:
    logfile = ftitle.lower() + '-log.txt'
else:
    logfile = args.logfile + '.txt'
settings['logfile'] = logfile

# TODO Temporary workaround, multi_targets NYI
#settings['multi_targets'] = args.multi_targets
settings['multi_targets'] = {}

if not settings['multi_targets'] and settings['target'] == 'multi':
    log_message('Target value of \'multi\' requires a non-empty dictionary to be passed to the --multi_targets'
                'flag.', log=logfile)
    raise ValueError('Target value of \'multi\' requires a non-empty dictionary to be passed to the --multi_targets'
                     'flag.')

if settings['multi_targets'] and settings['target'] != 'multi':
    print(f'Target not set to \'multi\', ignoring multi_targets value: {settings["multi_targets"]}')
    log_message(f'Target not set to \'multi\', ignoring multi_targets value: {settings["multi_targets"]}', log=logfile)


# TODO this selection can be cleaned up with dict membership
target = settings['target']
mode = ''
units = ''
if target in hs.SKILLS:
    mode = 'skill'
    units = 'XP'
elif target in hs.BOSSES:
    mode = 'boss'
    units = 'KC'
elif target in hs.ACTIVITIES:
    mode = 'activity'
    if target == 'league_points' or 'bounty_hunter' in target:
        units = 'points'
    elif 'clue' in target:
        units = 'caskets'
    elif 'rank' in target:
        units = 'rank'
    elif target == 'soul_wars_zeal':
        units = 'zeal'
    elif target == 'rifts_closed':
        units = 'rifts closed'
    else:
        log_message(f'Activity "{target}" not recognized, unable to set contest units.', log=logfile)
else:
    log_message(f'Target \'{target}\' not found, unable to set contest mode.', log=logfile)

settings['mode'] = mode
settings['units'] = units

# If contest ID is not manually set with --force_id, generate an 8 character code as a contest
# identifier.
if not settings['contest_id']:
    contest_id = str(sha1((settings['mode'] + settings['target'] +
                           settings['title'] + settings['start']
                           + settings['end']).encode('utf-8')).hexdigest())[-9:-1]
    settings['contest_id'] = contest_id

# TODO implement multi_targets
# TODO add argument verification for mode/units/multi_targets/etc

contest = ContestData(settings)

if os.path.exists('contest-table.txt'):
    with open('contest-table.txt', 'rb') as infile:
        file_input = infile.read()

    file_input = eval(file_input)
    contest_table = ContestTable(file_input)
else:
    contest_table = ContestTable({})

contest_table.add_contest(contest)

contest_table.to_file('contest-table')

print(f'Contest with ID {settings["contest_id"]} added to contest table.')

# TODO add python-crontab integration
