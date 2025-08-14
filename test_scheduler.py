import pytest
from datetime import datetime, timedelta, timezone
from scheduler import parse_schedules, find_common_free_time


def test_parse_schedule():
    schedules = [
        {
            "startTime": {"dateTime": "2025-08-11T10:00:00+09:00"},
            "endTime": {"dateTime": "2025-08-11T11:00:00+09:00"},
        },
        {
            "startTime": {"dateTime": "2025-08-11T13:00:00+09:00"},
            "endTime": {"dateTime": "2025-08-11T14:00:00+09:00"},
        },
    ]
    event= parse_schedules(schedules)
    assert len(event) == 2

def test_find_common_free_time():
    tz = timezone(timedelta(hours=9))
    day_start = datetime(2025, 8, 11, 9, 0, tzinfo=tz)
    day_end = datetime(2025, 8, 11, 18, 0, tzinfo=tz)

    user1= [
        (datetime(2025, 8, 11, 10, 0, tzinfo=tz), datetime(2025, 8, 11, 11, 0, tzinfo=tz)),
        (datetime(2025, 8, 11, 13, 0, tzinfo=tz), datetime(2025, 8, 11, 14, 0, tzinfo=tz)),
    ]

    user2= [
        (datetime(2025, 8, 11, 11, 0, tzinfo=tz), datetime(2025, 8, 11, 12, 0, tzinfo=tz)),
        (datetime(2025, 8, 11, 15, 0, tzinfo=tz), datetime(2025, 8, 11, 16, 0, tzinfo=tz)),
    ]

    result = find_common_free_time([user1, user2], day_start, day_end, timedelta(minutes=30))

    expected = [
        (datetime(2025, 8, 11, 9, 0, tzinfo=tz), datetime(2025, 8, 11, 10, 0, tzinfo=tz)),
        (datetime(2025, 8, 11, 12, 0, tzinfo=tz), datetime(2025, 8, 11, 13, 0, tzinfo=tz)),
        (datetime(2025, 8, 11, 14, 0, tzinfo=tz), datetime(2025, 8, 11, 15, 0, tzinfo=tz)),
        (datetime(2025, 8, 11, 16, 0, tzinfo=tz), datetime(2025, 8, 11, 18, 0, tzinfo=tz)),
    ]

    assert result == expected
