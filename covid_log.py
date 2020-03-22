from datetime import datetime
import sys
my_logger = None
handler = None


task = ""


def set_task(name):
    global task
    task = name


def log(message):
    try:
        s = "{} - [{}] - {}".format(datetime.utcnow(), task, message)
        print(s)
        fn = "/var/log/covid.log"
        try:
            with open(fn, 'a') as the_file:
                the_file.write(s + '\n')
        except Exception as e:
            if sys.platform != "darwin":
                print("WTF? LOG - {}".format(e))
    except Exception as e:
        print(str(e))
