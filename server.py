import hashlib
import os
import psycopg2
import schedule
import threading
import base64
import time
from dotenv import load_dotenv
from flask import Flask, request, session
from flask_cors import CORS
from werkzeug.utils import redirect


#################################### Flask #####################################

app = Flask(__name__)
app.secret_key = os.urandom(16)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

############################## Connect to Databse ##############################

# Load environment variables from a .env file
# This is just for testing, not for production
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


# Function to wipe the rows but preserve the table
def wipe_database():
    with conn.cursor() as cur:
        cur.execute("DELETE FROM hacktheearth.logs")
        conn.commit()


# Schedule weekly task
schedule.every().sunday.at("23:59").do(wipe_database)
# Start the background thread
stop_run_continuously = run_continuously(1)

################################ Authentication ################################

base_url = os.environ["CLIENT_URL"]
success_url = base_url + "data_visualization/"


@app.route("/auth/create_user", methods=["POST"])
def create_user():
    # Get request data
    data = request.get_json()
    address = data["address"]
    password = data["password"]

    # Check to see that address doesn't already have account
    with conn.cursor() as cur:
        cur.execute(
            "CREATE TABLE IF NOT EXISTS hacktheearth.users (address STRING PRIMARY KEY, salt STRING, password STRING)"
        )
        conn.commit()
        cur.execute(
            "SELECT * FROM hacktheearth.users WHERE address = %s", (address,))
        already_created = cur.fetchall()
        if already_created:
            return "Address already associated with account", 400

    # Generate salt
    salt = base64.b64encode(os.urandom(16)).decode("ascii")

    # Salt and hash password
    salted_password = password + salt
    hashed_password = hashlib.sha256(
        salted_password.encode("utf-8")).hexdigest()

    # Add user to database
    with conn.cursor() as cur:
        cur.execute("UPSERT INTO hacktheearth.users (address, salt, password) VALUES (%s, %s, %s)",
                    (address, salt, hashed_password,))
        conn.commit()

    return "Account successfully created"


@app.route("/auth/login", methods=["POST"])
def login():
    # Get request data
    # TODO: use request.form
    data = request.get_json()
    address = data["address"]
    password = data["password"]

    # Query database and decode response
    with conn.cursor() as cur:
        # Create the table so we don't get an error if it doesn't exist
        cur.execute(
            "CREATE TABLE IF NOT EXISTS hacktheearth.users (address STRING PRIMARY KEY, salt STRING, password STRING)"
        )
        conn.commit()

        # Find the user with the given address
        cur.execute(
            "SELECT * FROM hacktheearth.users WHERE address = %s", (address,))

        # Decode response
        (stored_address, salt, old_hash) = cur.fetchall()[0]

        # If we don't get a response, it means that there is no user with that
        # address yet.
        if not stored_address:
            return "This address does not have an account associated with it yet", 400

    # Hash the password that the person trying to login provided
    salted_password = password + salt
    new_hash = hashlib.sha256(salted_password.encode("utf-8")).hexdigest()

    # Compare the hashes to see if they gave the correct password or not
    if new_hash == old_hash:
        # Store session cookie then redirect to success url
        session["username"] = stored_address
        return redirect(success_url)
    else:
        return "Incorrect password", 400


@app.route("/auth/logout", methods=["POST"])
def logout():
    # Remove session cookie then go to home page
    # TODO: Confirm this works
    session.pop("username", None)
    return redirect(base_url)

########################### Data Querying and Updating #########################


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
        cur.execute("UPSERT INTO hacktheearth.logs (id) VALUES (2)")
        conn.commit()
    return "Add entry"


@app.route("/api/get_general_data", methods=["GET"])
def get_general_data():

    # TODO: If "username" in session:

    # Get data from database
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM hacktheearth.logs ORDER BY id DESC")
        posts = cur.fetchall()
    return str(posts)


if __name__ == "__main__":
    app.run()
    stop_run_continuously.set()
    conn.close()
