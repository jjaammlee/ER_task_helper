MAIL_PROFILES = {
    "mentoring": {
        "filter_column": 3,
        "filter_value": "01 AI개발실",
        "recipient_columns": [13, 16],
        "remove_columns": [2, 5, 6, 14],
        "sheet_index": 2,
        "additional_columns": [
            {"name": "경비 사용 멘토 이름", "color": 6},
            {"name": "실 사용 금액", "color": 6},
            {"name": "비고", "color": 6}
        ],
        "mail_subject": "[테스트] 경력입사자 멘토링 실시",
        "mail_body": """
            <p><span style="font-family:맑은 고딕; font-size:13.3333px;">
                안녕하세요, AI개발실 ER 이재원입니다.<br><br>
                멘토링 자동화 테스트 메일입니다.<br>
                아래 링크를 통해 관련 내용을 확인하실 수 있습니다.<br><br>
                ▶ <a href="http://edm2.sec.samsung.net/cc/link/verLink/175497174727804373/12" target="_blank">
                멘토링 안내 바로가기</a><br><br>
                감사합니다.<br>
            </span></p>
        """,
    }
}
