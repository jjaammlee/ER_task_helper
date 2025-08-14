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

def input_users():
    users = []
    print("사용자 정보를 입력하세요. (형식: login_id epid)")
    print("입력을 마치려면 빈 줄을 입력하세요.")
    while True:
        line = input(">> ").strip()
        if not line:
            break
        try:
            login_id, epid = line.split()
            users.append((login_id, epid))
        except ValueError:
            print("형식이 올바르지 않습니다. 예: jjaamm.lee P190317230718C100223")
    return users

def input_date(prompt, default_date):
    while True:
        user_input = input(f"{prompt} (yyyy-mm-dd) [기본값: {default_date.strftime('%Y-%m-%d')}]: ").strip()
        if not user_input:
            return default_date
        try:
            return datetime.strptime(user_input, "%Y-%m-%d").replace(tzinfo=timezone(timedelta(hours=9)))
        except ValueError:
            print("날짜 형식이 올바르지 않습니다. 다시 입력해주세요.")

if __name__ == "__main__":
    users = input_users()

    TIMEZONE = timezone(timedelta(hours=9))  # KST
    today = datetime.now(TIMEZONE).replace(hour=0, minute=0, second=0, microsecond=0)
    default_start = today
    default_end = today + timedelta(days=7)

    start_date = input_date("일정 조회 시작일", default_start)
    end_date = input_date("일정 조회 종료일", default_end)

    current_date = start_date
    while current_date <= end_date:
        if current_date.weekday() < 5:  # 주말은 건너뜀
            day_start = current_date.replace(hour=8, minute=0, second=0, microsecond=0)
            day_end = current_date.replace(hour=18, minute=0, second=0, microsecond=0)
            start_at = day_start.isoformat()
            end_at = day_end.isoformat()

            all_users_events = []
            for login_id, epid in users:
                schedules = fetch_user_schedules(login_id, epid, start_at, end_at)
                events = parse_schedules(schedules)
                all_users_events.append(events)

            common_free_times = find_common_free_time(all_users_events, day_start, day_end)

            print(f"\n{current_date.date()} 공통 빈 시간대:")
            if not common_free_times:
                print(" - 없음")
            for start, end in common_free_times:
                print(f" - {start.time()} ~ {end.time()}")

        current_date += timedelta(days=1)