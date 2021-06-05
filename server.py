import threading
import time
import schedule
from flask import Flask
from flask_cors import CORS


############################ Wipe Database Weekly ##############################

def run_continuously(interval):
    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):
        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                schedule.run_pending()
                time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.start()
    return cease_continuous_run


def wipe_databse():
    # TODO: Implement database wiping
    print("Interval")


schedule.every().tuesday.at("23:59").do(wipe_databse)
# Start the background thread
stop_run_continuously = run_continuously(300)

################################################################################

app = Flask(__name__)
CORS(app)


@app.route("/api/add_entry", methods=["POST"])
def add_entry():
    # Database should have a table of public keys
    # The person collecting trash/recycling will sign with their private key
    # The server should then check that using the public key from the database
    # If that passes, add the entry to the database
    # A security alternative is to use a password sent with the POST request
    return "Add entry"


@app.route("/api/get_general_data", methods=["GET"])
def get_general_data():
    return "Data"


if __name__ == "__main__":
    app.run()
