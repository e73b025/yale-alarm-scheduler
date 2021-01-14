import logging
import time
import schedule

from threading import Thread

from yalesmartalarmclient.client import YaleSmartAlarmClient
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from yale_alarm_scheduler.Schedule import Schedule


class YaleAlarmScheduler(Thread):
    def __init__(self,
                 yale_email: str,
                 yale_password: str,
                 arm_schedule: Schedule):
        """
        Constructor
        :param yale_email:
        :param yale_password:
        :param arm_schedule:
        """
        Thread.__init__(self)

        self._schedule = arm_schedule

        self._send_grid_api_key = None
        self._sendgrid_from_email = None
        self._sendgrid_to_email = None

        self._yale_client = YaleSmartAlarmClient(yale_email, yale_password)

        self.__print_log(f"Using Yale account: {yale_email}.")

    def arm(self, partial=True):
        """
        Arm the alarm system and send notification.
        :param partial:
        :return:
        """
        if partial:
            self._yale_client.arm_partial()
        else:
            self._yale_client.arm_full()

        self.__print_log("Alarm has been armed.")

        self.__send_notification("House Alarm Armed",
                                 "yale_alarm_scheduler has armed your house alarm.")

    def is_send_grid_active(self) -> bool:
        """
        Check if Send Grid is properly initialized
        :return:
        """
        return True if self._send_grid_api_key and self._sendgrid_from_email and self._sendgrid_to_email else False

    def disarm(self):
        """
        Disarm the alarm system and send notification.
        :return:
        """
        self._yale_client.disarm()
        self.__print_log("Alarm has been disarmed.")
        self.__send_notification("House Alarm Disarmed",
                                 "yale_alarm_scheduler has disarmed your house alarm.")

    def run(self):
        """
        Working thread that will handle the arming and disarming.
        :return:
        """
        for schedule_time, schedule_mode in self._schedule.items():
            self.__print_log(f"Alarm state will be set to '{schedule_mode}' at '{schedule_time}'.")

            if schedule_mode == 'arm':
                schedule.every().day.at(schedule_time).do(lambda: self.arm(False))
            elif schedule_mode == 'home':
                schedule.every().day.at(schedule_time).do(lambda: self.arm(True))
            elif schedule_mode == 'disarm':
                schedule.every().day.at(schedule_time).do(lambda: self.arm())

        self.__print_log("Ready and waiting.")

        while True:
            schedule.run_pending()
            time.sleep(60)

    @staticmethod
    def __print_log(message):
        """
        Simple function to print a log message.
        :param message:
        :return:
        """
        log = logging.getLogger("yale_alarm_scheduler")
        log.info(message)

    def __send_notification(self, subject, message):
        """
        Send a notification using the SendGrid API.
        :param subject:
        :param message:
        :return:
        """
        if not self.is_send_grid_active():
            return

        mail_message = Mail(
            from_email=self._sendgrid_from_email,
            to_emails=self._sendgrid_to_email,
            subject=subject,
            html_content=message)

        sg = SendGridAPIClient(self._send_grid_api_key)
        sg.send(mail_message)
