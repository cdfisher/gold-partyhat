"""contests.py
Classes to represent both the settings for a single contest and a table of settings for all
contests for the Gold Partyhat bot.
"""


class ContestData:
    """Represents the settings for a single contest for Gold Partyhat
    """
    def __init__(self, dictionary):
        self.contest_id = dictionary['contest_id']
        self.title = dictionary['title']
        self.mode = dictionary['mode']
        self.target = dictionary['target']
        self.threshold = int(dictionary['threshold'])
        self.units = dictionary['units']
        self.group = dictionary['group']
        self.top_n = int(dictionary['top_n'])
        self.winners = int(dictionary['winners'])
        self.raffle_mode = dictionary['raffle_mode']
        self.raffle_winners = int(dictionary['raffle_winners'])
        self.silent = bool(dictionary['silent'])
        self.start = dictionary['start']
        self.end = dictionary['end']
        self.interval = int(dictionary['interval'])
        self.update_number = int(dictionary['update_number'])
        self.n_participants = int(dictionary['n_participants'])
        self.dynamic_prizes = bool(dictionary['dynamic_prizes'])
        self.datafile = dictionary['datafile']
        self.logfile = dictionary['logfile']
        self.multi_targets = dictionary['multi_targets']
        return

    def get_all_data(self):
        return (self.contest_id, self.title, self.mode, self.target, self.threshold, self.units,
                self.group, self.top_n, self.winners, self.raffle_mode, self.raffle_winners,
                self.silent, self.start, self.end, self.interval, self.update_number,
                self.n_participants, self.dynamic_prizes, self.datafile, self.logfile,
                self.multi_targets)

    def update_entry(self, entry, value):
        if not hasattr(self, entry):
            raise AttributeError(f'ContestData object {self} with contest id {self.contest_id} '
                                 f'does not have an attribute {entry}. Failed to set {entry} to'
                                 f' {value}.')
        else:
            self.__setattr__(entry, value)
        return

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self.__dict__)


class ContestTable:
    """Represents a table of contests in the form of a dictionary of
    contest_id: ContestData pairs."""
    def __init__(self, dictionary):
        self.table = dict()
        for key, value in dictionary.items():
            self.table[key] = ContestData(value)

    def get_contest(self, contest_id: str) -> ContestData:
        try:
            _contest = self.table[contest_id]
        except KeyError:
            raise KeyError(f'Contest with id {contest_id} not found.')
        return _contest

    def add_contest(self, data: ContestData) -> None:
        contest_id = data.__getattribute__('contest_id')
        self.table[contest_id] = data

    def remove_contest(self, contest_id: str) -> None:
        if contest_id in self.table:
            del self.table[contest_id]

    def __str__(self) -> str:
        return str(self.table)

    def to_file(self, filename: str):
        with open(filename + '.txt', 'w') as file:
            file.write(str(self.table))
