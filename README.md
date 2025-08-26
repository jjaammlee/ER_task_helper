# [소개]
이 프로젝트는 ER(인사/인력 운영)업무 중 반복적이고 단순한 작업들을 보다 효율적으로 처리하기 위해 제작하였습니다.
일정 조율, 멘토링 메일 발송과 같은 기능들을 자동화함으로써 업무 효율을 높이고 보다 중요한 인사 업무에 집중할 수 있도록 돕습니다.

# [주요 기능]
* 스케줄링 자동화
  - scheduler.py를 통해 여러 사용자의 일정 정보를 API로 불러오기
  - 주어진 시간 범위 안에서 모든 사용자에게 공통으로 비어있는 시간대를 탐색 및 반환
  - 회의나 멘토링 등 다자간 스케줄 조율에 활용 가능
  - 사용 예시
  - 
    <img width="482" height="597" alt="image" src="https://github.com/user-attachments/assets/ebbc22ff-e56d-4972-b559-f4ba4d4cf460" />


* 멘토링 안내 메일 자동화
  - mail_profiles.py에서 정의한 메일 유형에 따라 메일 수신자 목록과 메일 본문을 자동으로 구성
  - excel파일을 읽어 지정된 조건 (특정 부서/ 팀 필터)에 맞는 수신자 이메일 주소 추출
  - 불필요한 열을 삭제하고 추가 정보 열을 삽입하여 메일 발송용 excel파일 재가공
  - win32com.client기반 excel자동화 지원 (Windows환경 필요)
  - 사용 예시
  - <img width="570" height="133" alt="image" src="https://github.com/user-attachments/assets/e6d8197a-638e-4ffe-8986-89c3c4739217" />
  
# [환경]
- python 3.x
- Windows환경 (메일 발송 시 win32com.client를 통한 excel자동화 필요)
- 외부 라이브러리
  - requests
  - python-dateutil
  - pywin32
- 사내 Knox API사용 권한 필수
  - 메일/스케줄러 기능은 내부 Knox API연동을 통해 동작합니다.
  - 사용자는 Knox API사용을 위한 사내 결재/승인 절차를 완료해야 합니다.
  - 승인된 API Key/Token이 있어야만 정상적으로 실행 가능합니다.
