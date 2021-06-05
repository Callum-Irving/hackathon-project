import os
import psycopg2
import schedule
import threading
import time
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS


############################## Connect to Databse ##############################

# Load environment variables from a .env file
load_dotenv()

# Establish connection to CockroachDB database
conn = psycopg2.connect(
    database=os.environ['DB_DATABASE'],
    user=os.environ['DB_USER'],
    password=os.environ['DB_PASSWD'],
    sslmode='require',
    port=26257,
    host=os.environ['DB_HOST'],
    options=os.environ['DB_OPTIONS']
)

############################# Wipe Database Weekly #############################


# Run the thread in the background
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

################################ Flask Routes ##################################

app = Flask(__name__)
CORS(app)


@app.route("/api/add_entry", methods=["POST"])
def add_entry():
    # Database should have a table of public keys
    # The person collecting trash/recycling will sign with their private key
    # The server should then check that using the public key from the database
    # If that passes, add the entry to the database
    # A security alternative is to use a password sent with the POST request
    with conn.cursor() as cur:
        cur.execute(
            "CREATE TABLE IF NOT EXISTS hacktheearth.logs (id INT PRIMARY KEY)"
        )
        cur.execute("UPSERT INTO hacktheearth.logs (id) VALUES (1)")
        conn.commit()
    return "Add entry"


@app.route("/api/get_general_data", methods=["GET"])
def get_general_data():
    return "Data"


if __name__ == "__main__":
    app.run()
    stop_run_continuously.set()
    conn.close()
