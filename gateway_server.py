import threading
import time
import datetime
import json
import requests
import pandas as pd
import io
from flask import Flask, render_template, request, jsonify, send_file

app = Flask(__name__, template_folder='../src_iot/templates', static_folder='../src_iot/static')

# Shared Concurrency Protection Lock
data_lock = threading.Lock()

# Central Database Memory Structure (Expanded for Arrays)
live_system_data = {
    "team_1": {
        "checked_in": 0, 
        "total_runners": 0, 
        "attendees": []
    },
    "team_2": {
        "leader_time": "00:00:00", 
        "runners": []
    },
    "team_3": {
        "sos_triggered": False, 
        "temp": 0.0
    },
    "team_4": {
        "water_level_percent": 100
    }
}

# OS Mechanism: File Management for logging
def log_to_file(payload):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("system_logs.txt", "a") as log_file:
        log_file.write(f"[{timestamp}] {json.dumps(payload)}\n")

# Thread 1: Continuous Firebase Sync (Team 2 Timing)
# 1. Update your Firebase Thread to safely handle clean copy lists
def poll_team2_firebase():
    firebase_url = "https://runner-system-default-rtdb.firebaseio.com/tracking.json"
    while True:
        try:
            response = requests.get(firebase_url, timeout=5)
            tracking_data = response.json()
            if tracking_data:
                runners_list = list(tracking_data.values())
                
                # Sort runners by fastest completion time safely
                runners_list.sort(key=lambda x: x.get('raw_time', 0))
                
                with data_lock:
                    if runners_list:
                        live_system_data["team_2"]["leader_time"] = runners_list[0].get("recorded_time", "00:00:00")
                    # Store a direct clean copy of the array for dashboard.js
                    live_system_data["team_2"]["runners"] = runners_list
            else:
                with data_lock:
                    live_system_data["team_2"]["runners"] = []
        except Exception as e:
            print(f"Firebase Worker Sync Error: {e}")
        time.sleep(2)


# Thread 2: Continuous Google Sheet Responses Sync (Team 1 Registration)
# Thread 2: Continuous Google Sheet Responses Sync (Team 1 Registration)
def poll_registration_sheet():
    spreadsheet_id = "1YDd6K_a2gRIBid9uWObZNOIeOFZ0INAUmowUD9n8LV8"
    csv_url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export?format=csv"
    
    while True:
        try:
            df = pd.read_csv(csv_url)
            total_runners = len(df)
            
            # Filter rows where registration status equals "Hadir"
            # We use fillna("") so blank rows don't crash the program with 'NaN'
            checked_in_df = df[df['Status kehadiran'].fillna("").str.lower() == 'hadir']
            checked_in_count = len(checked_in_df)
            
            # CRITICAL FIX: Add .fillna("") here so invalid data isn't sent to the browser
            attendees = checked_in_df[['NAMA PENUH', 'NO MATRIK']].fillna("").to_dict(orient='records')
            
            with data_lock:
                live_system_data["team_1"]["total_runners"] = total_runners
                live_system_data["team_1"]["checked_in"] = checked_in_count
                live_system_data["team_1"]["attendees"] = attendees
                
        except Exception as e:
            print(f"Registration Sheet Sync Error: {e}")
            
        time.sleep(30)
        
@app.route('/')
def serve_dashboard():
    return render_template('index.html')

# Endpoint for IoT Devices (ESP32, Sensors) to push data updates
@app.route('/api/update', methods=['POST'])
def update_data():
    payload = request.json
    team_id = payload.get('team_id')
    log_to_file(payload)
    
    with data_lock: # Critical Section Protection
        if team_id == 1:
            live_system_data["team_1"]["checked_in"] = payload.get('checked_in', 0)
        elif team_id == 3:
            live_system_data["team_3"]["sos_triggered"] = payload.get('sos_triggered', False)
            live_system_data["team_3"]["temp"] = payload.get('temperature_celsius', 0.0)
        elif team_id == 4:
            live_system_data["team_4"]["water_level_percent"] = payload.get('water_level_percent', 100)
            
    return jsonify({"status": "success"}), 200

# UI Polling Endpoint
@app.route('/api/live_data', methods=['GET'])
def get_live_data():
    with data_lock: # Thread-safe snapshot read
        return jsonify(live_system_data)

# 2. Update your Export Route to completely clean dataframes before saving
@app.route('/api/export_excel', methods=['GET'])
def export_excel():
    with data_lock:
        # Fill all missing or empty fields with blank text strings so Excel doesn't fail
        runners_df = pd.DataFrame(live_system_data["team_2"]["runners"]).fillna("")
        attendees_df = pd.DataFrame(live_system_data["team_1"]["attendees"]).fillna("")
        
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        if not attendees_df.empty:
            attendees_df.to_excel(writer, sheet_name='Attendance_Registration', index=False)
        if not runners_df.empty:
            runners_df.to_excel(writer, sheet_name='Race_Leaderboard', index=False)
            
    output.seek(0)
    return send_file(output, download_name="Smart_Fun_Run_Official_Report.xlsx", as_attachment=True)

if __name__ == '__main__':
    # Initializing Concurrent OS Workers
    t2 = threading.Thread(target=poll_team2_firebase, daemon=True)
    t1 = threading.Thread(target=poll_registration_sheet, daemon=True)
    
    t2.start()
    t1.start()
    
    app.run(debug=True, port=5000)
