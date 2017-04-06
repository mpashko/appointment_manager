def parse_dates(date_string):
    return [date for date in date_string.split(',')]


def parse_time_ranges(time_list):
    return [item.split(',') for item in time_list]


def parse_time(time):
    parsed_string = time.split(',')
    return [time[2:4] for time in parsed_string]


class Environment:
    def __init__(self):
        self.appointments = []
        self.users = set()

    def add_appointment(self, appointment):
        self.appointments.append(appointment)

    def add_user(self, user_name):
        self.users.add(user_name)

    @staticmethod
    def create_appointment(**kwargs):
        return Appointment.create_appointment(**kwargs)

    def get_appointment(self, id):
        for appointment in self.appointments:
            if appointment.get_id() == int(id):
                return appointment

    def update_appointment(self, id, participant):
        appointment = self.get_appointment(id)
        appointment.add_participant(participant)

    def add_participant(self, appointment_id, data):
        participant = Participant.create_participant(**data)
        appointment = self.get_appointment(appointment_id)
        appointment.append_participant(participant)


class Appointment:
    counter = 0

    def __init__(self, initiator, subject, description, additional_info, dates, time):
        Appointment.counter += 1
        self.id = self.counter
        self.initiator = initiator
        self.subject = subject
        self.description = description
        self.additional_info = additional_info
        self.dates = dates
        self.time = time
        self.participants = []

    @staticmethod
    def create_appointment(**kwargs):
        initiator = kwargs.get('initiator')
        subject = kwargs.get('subject')
        description = kwargs.get('description')
        additional_info = kwargs.get('additional_info')
        dates = kwargs.get('dates')
        time = kwargs.get('time')
        return Appointment(initiator, subject, description, additional_info, dates, time)

    def get_id(self):
        return self.id

    def append_participant(self, participant):
        self.participants.append(participant)


class Participant:
    def __init__(self, full_name, email, date, time):
        self.full_name = full_name
        self.email = email
        self.date = date
        self.time = time

    @staticmethod
    def create_participant(**kwargs):
        full_name = kwargs.get('full_name')
        email = kwargs.get('email')
        date = kwargs.get('date')
        time = kwargs.get('time')
        return Participant(full_name, email, date, time)
