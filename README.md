# Yale Alarm Scheduler

## Overview

![graph](https://user-images.githubusercontent.com/60853824/104706444-fff1da00-5712-11eb-98f7-634d56822719.png)

A super simple package/script that will allow you to easily arm and disarm your Yale alarm system using a provided 
schedule. The schedule along with the configuration details are stored in config file.

Run it directly via your favourite Python interpreter, use provided Dockerfile or run the shell script.

## Prerequisites

* Python3 
* Yale Alarm System (Yale Smart Living WIFI Enabled)
* [SendGrid](https://sendgrid.com) (if you wish to get email notifications)

## Python Packages

* [yale-smart-alarm-client](https://github.com/domwillcode/yale-smart-alarm-client)
* [sendgrid])(https://github.com/sendgrid/sendgrid-python)
* backoff
* schedule

## Schedule (in config.json file)

```
 "schedule": {
    "23:00": "arm",
    "06:00": "disarm"
  }
```
Allowed values for state are: ```arm```, ```disarm``` and ```home``` (for partial arm).

## Setup

You can run the script directly via a Python interpreter or, alternatively, use docker.

**Before Starting**: Please modify the ```config.json``` file and provide all the values that are present in the 
provided template config.json file.

If you wish to use SendGrid to receive email notifications on arm/disarm events, provide your SendGrip API key. 
SendGrid is free for a specific amount of emails per month and is a fast and reliable service.

### Python Interpreter

1. Install dependencies:
   ```
    pip install -r requirements.txt
    ```
2. Run the following:
    ```
    python run.py -config "path/to/config.json"
    ```
3. Done. System is now running.

### Docker

Assuming you have Docker installed, follow the below steps:

1. Modify the ```config.json``` file and provide all the required values.

2. Build a docker image using Dockerfile:
    ```
    docker build -t yale-alarm-scheduler .
    ```
3. Create and run the image as a new container:
   ```
   docker run --rm yale-alarm-scheduler
   ```
