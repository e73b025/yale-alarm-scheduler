from datetime import datetime

from yalesmartalarmclient.client import YALE_STATE_ARM_FULL, YALE_STATE_ARM_PARTIAL, YALE_STATE_DISARM


class Schedule:
    def __init__(self, json_serialized_schedule: str):
        """
        Constructor.
        :param json_serialized_schedule:
        """
        self.schedule = dict()

        if json_serialized_schedule:
            self.load_from_dict(json_serialized_schedule)

    def add_time(self, time: str, mode: str):
        """
        Add a new time/mode to the schedule.
        :param time:
        :param mode:
        :return:
        """
        try:
            # Catch exception, provide more useful feedback (to user)
            datetime.strptime(time, "%H:%M")
        except Exception as e:
            raise Exception(
                f"Invalid schedule time {time}, please provide a valid time in format HH:MM.")

        if mode not in [YALE_STATE_ARM_FULL, YALE_STATE_ARM_PARTIAL, YALE_STATE_DISARM]:
            raise Exception(
                f"Invalid schedule mode found for time {time}, please provide either 'disarm' or 'arm'.")

        self.schedule[time] = mode

    def is_set(self) -> bool:
        """
        Check if the schedule has at least one value.
        :return:
        """
        return len(self.schedule) != 0

    def items(self):
        """
        Get items, wrapper.
        :return:
        """
        return self.schedule.items()

    def load_from_dict(self, serialized_schedule: dict):
        """
        Attempt to parse a JSON serialized schedule that the script will use to arm and disarm the alarm system.
        :param serialized_schedule:
        :return:
        """
        for schedule_time, schedule_mode in serialized_schedule.items():
            self.add_time(schedule_time, schedule_mode)
