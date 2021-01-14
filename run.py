import json
import logging
import os
import sys
import argparse


from yale_alarm_scheduler.Schedule import Schedule
from yale_alarm_scheduler.YaleAutoArm import YaleAlarmScheduler

if __name__ == "__main__":
    # Instantiate the argument parser
    parser = argparse.ArgumentParser()

    parser.add_argument('-config',
                        type=str,
                        help="The email address associated with your Yale account.",
                        default="config.json")

    args = parser.parse_args()

    if not os.path.exists(args.config):
        raise Exception(f"No config file exists at path '{args.config}'.")

    # Config dict
    with open(args.config, "r") as config_file:
        config = json.loads(config_file.read())

    # Enabling logging
    if "enable_logging" in config and config["enable_logging"]:
        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    # Initialize the script
    yale_auto_arm = YaleAlarmScheduler(config["yale"]["email"],
                                       config["yale"]["password"],
                                       Schedule(
                                           config["schedule"]))

    # Optionally, if Send Grid has values, set them for email notifications
    if "send_grid" in config:
        yale_auto_arm._send_grid_api_key = config["send_grid"]["api_key"]
        yale_auto_arm._sendgrid_from_email = config["send_grid"]["email_from"]
        yale_auto_arm._sendgrid_to_email = config["send_grid"]["email_to"]

    # Enable the script
    yale_auto_arm.start()
