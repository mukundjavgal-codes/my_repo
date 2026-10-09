import os
import time
from datetime import datetime, timezone
import requests

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
# Replace with your actual OneDrive folder path.
# Examples:
# Windows: r"C:\Users\YourName\OneDrive\F1_Tracker\index.html"
# Mac: os.path.expanduser("~/OneDrive/F1_Tracker/index.html")
ONEDRIVE_HTML_PATH = os.path.expanduser("~\OneDrive\\f1_notifier\\index.html")

VERSTAPPEN_DRIVER_NUMBER = 1
POLL_INTERVAL_SECONDS = 30  # Polling interval in seconds
OPENF1_BASE_URL = "https://api.openf1.org/v1"


# ---------------------------------------------------------------------------
# OpenF1 Helpers
# ---------------------------------------------------------------------------
def get_latest_race_session():
    """Fetches the active or most recently completed Race session."""
    url = f"{OPENF1_BASE_URL}/sessions?session_type=Race&year=2026"
    response = requests.get(url)

    if response.status_code != 200 or not response.json():
        return None

    sessions = response.json()
    now = datetime.now(timezone.utc)

    past_or_current_races = []
    for s in sessions:
        start_time = datetime.fromisoformat(
            s["date_start"].replace("Z", "+00:00")
        )
        if start_time <= now:
            past_or_current_races.append(s)

    if past_or_current_races:
        return past_or_current_races[-1]

    return None


def get_driver_map(session_key):
    """Fetches driver numbers and names for a session."""
    url = f"{OPENF1_BASE_URL}/drivers?session_key={session_key}"
    response = requests.get(url)
    drivers = {}
    if response.status_code == 200:
        for d in response.json():
            drivers[d["driver_number"]] = d.get(
                "full_name", f"Driver {d['driver_number']}"
            )
    return drivers


def get_current_standings(session_key):
    """Fetches live positions."""
    url = f"{OPENF1_BASE_URL}/position?session_key={session_key}"
    response = requests.get(url)
    if response.status_code != 200:
        return {}

    latest_positions = {}
    for pos in response.json():
        latest_positions[pos["driver_number"]] = pos["position"]
    return latest_positions


def get_race_progress(session_key):
    """Fetches current max lap number completed."""
    url = f"{OPENF1_BASE_URL}/laps?session_key={session_key}"
    response = requests.get(url)
    if response.status_code == 200 and response.json():
        laps = response.json()
        return max(l["lap_number"] for l in laps if l.get("lap_number"))
    return 0


# ---------------------------------------------------------------------------
# OneDrive HTML Writer
# ---------------------------------------------------------------------------
def update_onedrive_html(session_name, current_lap, top_5, verstappen_pos):
    """Generates a clean HTML dashboard and writes it to OneDrive."""
    top_5_rows = "".join(
        [
            f"<tr style='border-bottom: 1px solid #ddd;'><td style='padding: 10px; font-weight: bold; color: #e10600;'>P{pos}</td><td style='padding: 10px;'>{name}</td></tr>"
            for pos, name in top_5
        ]
    )

    verstappen_str = (
        f"P{verstappen_pos}" if verstappen_pos else "Not Ranked / DNF"
    )
    last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>F1 Live Dashboard</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background-color: #121212; color: #ffffff; padding: 20px; margin: 0; }}
        .card {{ background-color: #1e1e1e; border-radius: 12px; padding: 20px; max-width: 450px; margin: 0 auto; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }}
        .header {{ border-bottom: 2px solid #e10600; padding-bottom: 10px; margin-bottom: 15px; }}
        .title {{ color: #e10600; margin: 0; font-size: 22px; text-transform: uppercase; }}
        .subtitle {{ color: #aaa; margin-top: 5px; font-size: 14px; }}
        .stat-box {{ background-color: #2a2a2a; border-left: 4px solid #007bff; padding: 12px; border-radius: 6px; margin: 15px 0; }}
        .max-box {{ background-color: #2a2a2a; border-left: 4px solid #f39c12; padding: 12px; border-radius: 6px; margin: 15px 0; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
        .footer {{ font-size: 11px; color: #666; text-align: center; margin-top: 20px; }}
    </style>
</head>
<body>
    <div class="card">
        <div class="header">
            <h2 class="title">🏎️ {session_name}</h2>
            <div class="subtitle">Live OpenF1 Telemetry Dashboard</div>
        </div>

        <div class="stat-box">
            <strong>Race Progress:</strong> Lap {current_lap}
        </div>

        <h3>📊 Top 5 Standings</h3>
        <table>
            {top_5_rows}
        </table>

        <div class="max-box">
            <strong>🦁 Max Verstappen Position:</strong> <span style="font-size: 18px; font-weight: bold; color: #f39c12;">{verstappen_str}</span>
        </div>

        <div class="footer">
            Last Synced: {last_updated}<br>
            Auto-generated by Python OpenF1 Tracker
        </div>
    </div>
</body>
</html>
"""

    # Ensure output directory exists before writing
    os.makedirs(os.path.dirname(ONEDRIVE_HTML_PATH), exist_ok=True)

    with open(ONEDRIVE_HTML_PATH, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"[{last_updated}] Updated HTML file in OneDrive.")


# ---------------------------------------------------------------------------
# Main Execution Loop
# ---------------------------------------------------------------------------
def run_race_monitor():
    print("Starting F1 OneDrive Tracker...")

    session = get_latest_race_session()
    if not session:
        print("No past or active race session found.")
        return

    session_key = session["session_key"]
    session_name = f"{session['location']} GP {session['year']}"
    print(f"Tracking Session: {session_name} (Key: {session_key})")

    driver_map = get_driver_map(session_key)

    while True:
        positions = get_current_standings(session_key)
        current_lap = get_race_progress(session_key)

        if positions:
            sorted_positions = sorted(positions.items(), key=lambda x: x[1])

            top_5 = [
                (pos, driver_map.get(num, f"Driver #{num}"))
                for num, pos in sorted_positions[:5]
            ]
            verstappen_pos = positions.get(VERSTAPPEN_DRIVER_NUMBER, None)

            # Re-write the HTML file every cycle
            update_onedrive_html(
                session_name, current_lap, top_5, verstappen_pos
            )

        time.sleep(POLL_INTERVAL_SECONDS)


if __name__ == "__main__":
    run_race_monitor()