import requests
from datetime import datetime, timedelta, timezone
from dateutil import parser
from typing import List, Tuple, Dict


API_URL = "https://openapi.samsung.net/pims/calendar/api/v2.0/schedules"
SYSTEM_ID = "KCC10REST03311"
ACCESS_TOKEN = "be3200c6-3215-3063-909b-e788ed8daedd"

HEADERS = {
    "System-ID": SYSTEM_ID,
    "Authorization": f"Bearer {ACCESS_TOKEN}"
}

TIMEZONE = timezone(timedelta(hours=9))  # KST
DEFAULT_START_HOUR = 8
DEFAULT_END_HOUR = 18
DEFAULT_DURATION = timedelta(minutes=30)

class Scheduler:
    def fetch_user_schedules(self, user_id: str, epid: str, start_at: str, end_at: str) -> List[Dict]:
        params = {
            "userId": user_id,
            "targetId": epid,
            "startAt": start_at,
            "endAt": end_at
        }

        try:
            response = requests.get(API_URL, headers=HEADERS, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"[ERROR] {user_id}의 일정 조회 실패: {e}")
            return []

    def parse_schedules(self, schedules: List[Dict]) -> List[Tuple[datetime, datetime]]:
        events = []
        for schedule in schedules:
            try:
                start = parser.isoparse(schedule['startTime']['dateTime'])
                end = parser.isoparse(schedule['endTime']['dateTime'])
                events.append((start, end))
            except Exception as e:
                continue

        return events

    def find_common_free_time(self, users: List[List[Tuple[datetime, datetime]]], day_start: datetime, day_end: datetime, min_duration: timedelta = DEFAULT_DURATION) -> List[Tuple[datetime, datetime]]:
        all_events = [slot for user in users for slot in user]

        merged = self.merge_events(all_events)

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

    def merge_events(self, all_events: List[Tuple[datetime, datetime]]) -> List[Tuple[datetime, datetime]]:
        all_events.sort()
        merged = []
        for start, end in all_events:
            if not merged or start > merged[-1][1]:
                merged.append((start, end))
            else:
                merged[-1] = (merged[-1][0], max(merged[-1][1], end))
        return merged

    def input_users(self) -> List[Tuple[str, str]]:
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

    def input_date(self, prompt: str, default_date: datetime) -> datetime:
        while True:
            user_input = input(f"{prompt} (yyyy-mm-dd) [기본값: {default_date.strftime('%Y-%m-%d')}]: ").strip()
            if not user_input:
                return default_date
            try:
                return datetime.strptime(user_input, "%Y-%m-%d").replace(tzinfo=timezone(timedelta(hours=9)))
            except ValueError:
                print("날짜 형식이 올바르지 않습니다. 다시 입력해주세요.")

    def execute(self):
        users = self.input_users()

        today = datetime.now(TIMEZONE).replace(hour=0, minute=0, second=0, microsecond=0)
        start_date = self.input_date("일정 조회 시작일", today)
        end_date = self.input_date("일정 조회 종료일", today + timedelta(days=7))

        current_date = start_date
        while current_date <= end_date:
            if current_date.weekday() < 5:  # 주말은 건너뜀
                self.show_common_free_time_for_day(current_date, users)
            current_date += timedelta(days=1)

    def show_common_free_time_for_day(self, current_date: datetime, users: List[Tuple[str, str]]):
        day_start = current_date.replace(hour=DEFAULT_START_HOUR, minute=0, second=0, microsecond=0)
        day_end = current_date.replace(hour=DEFAULT_END_HOUR, minute=0, second=0, microsecond=0)

        all_users_events = []
        for login_id, epid in users:
            schedules = self.fetch_user_schedules(login_id, epid, day_start.isoformat(), day_end.isoformat())
            events = self.parse_schedules(schedules)
            all_users_events.append(events)

        common_free_times = self.find_common_free_time(all_users_events, day_start, day_end)

        print(f"\n{current_date.date()} 공통 빈 시간대:")
        if not common_free_times:
            print(" - 없음")
        for start, end in common_free_times:
            print(f" - {start.time()} ~ {end.time()}")
