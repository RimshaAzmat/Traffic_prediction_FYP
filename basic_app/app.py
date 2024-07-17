from flask import Flask, render_template, redirect, url_for, send_from_directory, make_response
import os
import subprocess
import logging
from datetime import datetime

app = Flask(__name__)

# Directory paths
BASE_DIR = os.path.join("C:", os.sep, "Users", "hsarw", "OneDrive", "Desktop", "Others", "FYP", "basic_app")

# Configure logging
logging.basicConfig(level=logging.DEBUG)

def start_sumo_simulation(config_file_path):
    """
    Start the SUMO simulation.

    Args:
        config_file_path (str): Path to the SUMO configuration file.
    """
    sumo_executable = os.path.join(BASE_DIR, "sumo", "bin", "sumo-gui.exe")
    logging.debug(f"Starting SUMO simulation with config: {config_file_path}")
    subprocess.Popen([sumo_executable, "-c", config_file_path])

def find_latest_file(directory, file_name):
    """
    Find the latest file with the specified name in the given directory.

    Args:
        directory (str): Directory to search for the file.
        file_name (str): Name of the file to search for.

    Returns:
        str: Path to the latest file, or None if not found.
    """
    latest_file = None
    latest_time = 0
    logging.debug(f"Searching for {file_name} in {directory}")
    for root, _, files in os.walk(directory):
        for file in files:
            if file == file_name:
                file_path = os.path.join(root, file)
                try:
                    modified_time = os.path.getmtime(file_path)
                except FileNotFoundError:
                    logging.debug(f"File {file_path} not found, skipping.")
                    continue
                logging.debug(f"Found file {file_path} with modified time {datetime.fromtimestamp(modified_time)}")
                if modified_time > latest_time:
                    latest_file = file_path
                    latest_time = modified_time
    logging.debug(f"Latest file: {latest_file}")
    return latest_file

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/open_osm_wizard')
def open_osm_wizard():
    osm_web_wizard_script = os.path.join(BASE_DIR, "sumo", "tools", "osmWebWizard.py")
    logging.debug(f"Opening OSM Web Wizard: {osm_web_wizard_script}")
    subprocess.Popen(["python", osm_web_wizard_script])
    return redirect(url_for('run_simulation'))

@app.route('/run_simulation')
def run_simulation():
    config_path = os.path.join(BASE_DIR, "config", "simulation.sumocfg")
    start_sumo_simulation(config_path)
    return redirect(url_for('home'))

@app.route('/show_passenger_trips')
def show_passenger_trips():
    logging.debug("Request to show passenger trips file")
    latest_passenger_trips_file = find_latest_file(BASE_DIR, "osm.passenger.trips.xml")
    if latest_passenger_trips_file:
        logging.debug(f"Sending file: {latest_passenger_trips_file}")
        response = make_response(send_from_directory(os.path.dirname(latest_passenger_trips_file), os.path.basename(latest_passenger_trips_file)))
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response
    else:
        logging.debug("Passenger trips file not found")
        return "Passenger trips file not found."

@app.route('/show_data')
def show_simulation_data():
    logging.debug("Request to show simulation data")
    latest_passenger_trips_file = find_latest_file(BASE_DIR, "osm.passenger.trips.xml")
    if latest_passenger_trips_file:
        with open(latest_passenger_trips_file, 'r') as file:
            file_content = file.read()
        logging.debug(f"Displaying data from file: {latest_passenger_trips_file}")
        response = make_response(render_template('data.html', file_content=file_content))
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response
    else:
        logging.debug("Passenger trips file not found")
        return "Passenger trips file not found."

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
