import requests
from ics import Calendar, Event
from datetime import datetime
import pytz

# API endpoint
url = "https://comet.fsf.fo/data-backend/api/public/areports/run/0/25/?API_KEY=7e006067aa502e4d363ecf1ffcdc9db5e201cf40a07cccb3aaf2568eae0b3e6bdeb2778426728bc6c804cc49987cf967f5f1b404c1ce44c60be7a54563fcefe3"
response = requests.get(url)
data = response.json()

calendar = Calendar()
tz = pytz.timezone('Atlantic/Faroe')

for match in data.get('results', []):
    timestamp = match.get("matchDate")
    if not timestamp:
        continue

    description = match.get("matchDescription", "Ókend dystur")
    location = match.get("facility", "Ókend leikvøllur")
    match_status = match.get("matchStatus", "")
    round_number = match.get("round", "")
    competition = match.get("competitionType", "")

    start = datetime.fromtimestamp(timestamp / 1000, tz)

    event = Event()
    event.name = description
    event.begin = start
    event.duration = {"hours": 2}
    event.location = location
    event.description = (
        f"🏆 {competition}\n"
        f"🔁 Umfar: {round_number}\n"
        f"📊 Støða: {match_status}"
    )

    calendar.events.add(event)

with open('betri_deildin.ics', 'w', encoding='utf-8') as f:
    f.write(str(calendar))
