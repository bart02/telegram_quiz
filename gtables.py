import gspread
from oauth2client.service_account import ServiceAccountCredentials
from cached_property import cached_property_with_ttl as mwt
from collections import defaultdict


class Parser(gspread.Client):
    def __init__(self, credentials_file):
        creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"])
        super().__init__(creds)
    
    @mwt(100)
    def groups(self):
        return {file['name']: Group(file['name'], self.open(file['name'])) for file in self.list_spreadsheet_files()}


class Group:
    def __init__(self, name, file):
        self.file = file
        self.name = name

    
    @mwt(100)
    def users(self):
        logging = self.file.worksheet("Logging")
        users = list(zip(logging.col_values(1)[1:], logging.col_values(2)[1:]))
        return {user[0]: User(self, *user) for user in users}

    
    @mwt(100)
    def themes(self):
        sheets = []
        for sheet in self.file.worksheets():
            if sheet.title != "Logging":
                sheets.append(Theme(sheet, self))
        # sheets.pop("Logging")
        return sheets


class User:
    tg_id = -1
    q_now = None
    def __init__(self, group, id, name):
        self.id = id
        self.name = name
        self.group = group
        self.queue = []
        self.answered = defaultdict(int)

    def add_task(self, task):
        self.queue.append(task)

    def __eq__(self, other):
        return self.id == other.id

    def __repr__(self):
        return '<User: {}, {}>'.format(self.id, self.name)


class Theme:
    def __init__(self, sheet, group):
        self.name = sheet.title
        self.all_values = sheet.get_all_values()
        self.group = group

    def __eq__(self, other):
        return self.name == other.name

    @mwt(100)
    def params(self):
        return {'link': self.all_values[0][1],
                'repetitions_per_week': self.all_values[0][3],
                'number_of_repetitions': self.all_values[0][5],
                'wrong_answer_pop': self.all_values[0][7]
                }

    
    @mwt(100)
    def questions(self):
        ret = []
        for row in self.all_values[2:]:
            question_type = row[0]
            repetition = row[1]
            question_text = row[2]
            right_answer = row[3]
            remain_answers = row[4:]
            if question_type == "Open":
                ret.append(OpenQuestion(repetition, question_text, right_answer, self))
            elif question_type == "Multiple choice":
                ret.append(MultipleQuestion(repetition, question_text, right_answer, remain_answers, self))
        return ret


class Question:
    pass


class MultipleQuestion(Question):
    def __init__(self, repetition, question_text, right_answer, remain_answers, theme):
        self.repetition = int(repetition)
        self.question_text = question_text
        self.right_answer = right_answer
        self.remain_answers = remain_answers
        self.theme = theme

    def __repr__(self):
        return '<MultipleQuestion: {}; Answers {}; Right {}>'.format(self.question_text, self.remain_answers, self.right_answer)


class OpenQuestion(Question):
    def __init__(self, repetition, question_text, right_answer, theme):
        self.repetition = int(repetition)
        self.question_text = question_text
        self.right_answer = right_answer
        self.theme = theme


# client = Parser("creds.json")
# q = (list(client.groups["SE"].themes[0].questions))
# print(q)
