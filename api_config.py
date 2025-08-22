TOKEN = "be3200c6-3215-3063-909b-e788ed8daedd"
ACCOUNT_ID = "KCC10REST03311"

STAGE_TOKEN = "b6b7e0da-138f-32f9-8c6d-8a07b2efa53f"
STAGE_ACCOUNT_ID = "KCC10REST03311"

def build_headers(stage=False):
    token = STAGE_TOKEN if stage else TOKEN
    account_id = STAGE_ACCOUNT_ID if stage else ACCOUNT_ID
    return {
        "Authorization": f"Bearer {token}",
        "System-ID": account_id
    }


MAIL_API_CONFIG = {
    "BASE_URL": "https://openapi.stage.samsung.net/mail/api/v2.0",
    "USER_ID": "jjaamm.lee",
}

SCHEDULER_API_CONFIG = {
    "BASE_URL": "https://openapi.samsung.net/pims/calendar/api/v2.0",
}
