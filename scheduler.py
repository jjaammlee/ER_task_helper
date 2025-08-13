import requests
from datetime import datetime, timedelta, timezone
from dateutil import parser
from typing import List, Tuple

API_URL = "https://openapi.samsung.net/pims/calendar/api/v2.0/schedules"
SYSTEM_ID = "KCC10REST03311"
ACCESS_TOKEN = "be3200c6-3215-3063-909b-e788ed8daedd"

HEADERS = {
    "System-ID": SYSTEM_ID,
    "Authorization": f"Bearer {ACCESS_TOKEN}"
}
def fetch_user_schedules(user_login_id, epid, start_at, end_at):
    params = {
        "userId": user_login_id,
        "targetId": epid,
        "startAt": start_at,
        "endAt": end_at
    }
    response = requests.get(API_URL, headers=HEADERS, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch for {user_login_id}: {response.status_code}")
        return []


def parse_schedules(schedules):
    events = []
    for schedule in schedules:
        try:
            start = parser.isoparse(schedule['startTime']['dateTime'])
            end = parser.isoparse(schedule['endTime']['dateTime'])
            events.append((start, end))
        except Exception as e:
            continue
    return events

def find_common_free_time(users, day_start, day_end, min_duration = timedelta(minutes=30)):
    all_events = [slot for user in users for slot in user]
    all_events.sort()
    merged = []
    for start, end in all_events:
        if not merged or start > merged[-1][1]:
            merged.append((start, end))
        else:
            merged[-1] = (merged[-1][0], max(merged[-1][1], end))

    free_slots = []
    current = day_start
    for start, end in merged:
        if current < start:
            gap = (current, start)
            if (gap[1] - gap[0]) >= min_duration:
                free_slots.append(gap)
        current = max(current, end)

    if current < day_end and (day_end - current) >= min_duration:
        free_slots.append((current, day_end))

    return free_slots