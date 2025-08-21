import json
import requests
import os
import win32com.client as win32
import warnings

warnings.filterwarnings('ignore')

# API 정보
baseUrl = "https://openapi.stage.samsung.net/mail/api/v2.0"
url = baseUrl + "/mails/send?userId=jjaamm.lee"
token = "b6b7e0da-138f-32f9-8c6d-8a07b2efa53f"
accountID = "KCC10REST03311"
header = {
    'Authorization': 'Bearer ' + token,
    'System-ID': accountID,
}


class MailSender:
    def get_recipients_from_excel(self, sheet, pickUpCol):
        used_range = sheet.UsedRange
        row_count = used_range.Rows.Count

        recipientList = []
        for i in range(1, row_count + 1):
            if sheet.Cells(i, 3).Value != '01 AI개발실':
                continue
            for col in pickUpCol:
                email = sheet.Cells(i, col).Value
                if email:
                    recipientList.append({"emailAddress": email + '@samsung.com', "recipientType": "TO"})
        return recipientList

    def remove_columns_and_save(self, sheet, workbook, removeCols):
        used_range = sheet.UsedRange
        row_count = used_range.Rows.Count

        for i in range(row_count, 2, -1):
            cell_value = sheet.Cells(i, 3).Value
            if not cell_value or 'AI개발실' not in str(cell_value):
                sheet.Rows(i).Delete()

        for col in sorted(removeCols, reverse=True):
            sheet.Columns(col).Delete()

        used_range = sheet.UsedRange
        row_count = used_range.Rows.Count
        col_count = used_range.Columns.Count

        header_row = 1
        new_cols = [col_count + 1, col_count + 2, col_count + 3]
        headers = ['경비 사용 멘토 이름', '실 사용 금액', '비고']
        yellow_color = 6

        for col, header in zip(new_cols, headers):
            cell = sheet.Cells(header_row, col)
            cell.Value = header
            cell.Interior.ColorIndex = yellow_color
            cell.Font.Bold = True

            borders = cell.Borders
            borders(7).LineStyle = 1
            borders(10).LineStyle = 1
            borders(8).LineStyle = 1
            borders(9).LineStyle = 1

        data_range = sheet.Range(sheet.Cells(1, 1), sheet.Cells(row_count, col_count + 3))
        borders = data_range.Borders
        for edge in [7, 8, 9, 10, 11, 12]:
            borders(edge).LineStyle = 1
        workbook.SaveAs(self.newFilePath)

    def send_mail(self, recipientList):
        body = {
            "subject": "[테스트] 경력입사자 멘토링 실시",
            "contents": f"""
                <p><span style="font-family:맑은 고딕; font-size:13.3333px;">
                    안녕하세요, AI개발실 ER 이재원입니다.<br><br>
                    멘토링 자동화 테스트 메일입니다.<br>
                    아래 링크를 통해 관련 내용을 확인하실 수 있습니다.<br><br>
                    ▶ <a href="http://edm2.sec.samsung.net/cc/link/verLink/175497174727804373/12" target="_blank">
                    멘토링 안내 바로가기</a><br><br>
                    감사합니다.<br>
                </span></p>
            """,
            "contentType": "HTML",
            "docSecuType": "PERSONAL",
            "sender": {
                "emailAddress": "jjaamm.lee@stage.samsung.com"
            },
            "recipients": recipientList
        }

        try:
            if self.newFilePath:
                result = requests.post(
                    url, headers=header, data=[('mail', (None, json.dumps(body)))],
                    files=[('attachments', (open(self.newFilePath, 'rb')))], verify=False
                )
            else:
                result = requests.post(url, headers=header, data=[('mail', (None, json.dumps(body)))], verify=False)
            sendResult = result.json()

            if sendResult.get('errorCode'):
                print(f"[ERROR] {sendResult['errorCode']} - {sendResult.get('errorMessage', 'No error message')}")
            else:
                print(f"[OK] result: {sendResult.get('result')}")
        except Exception as e:
            print(f"[ERROR] 메일 전송 실패: {e}")

    def input_directory(self, prompt):
        user_input = input(f"{prompt}: ").strip()
        return user_input

    def execute(self):
        # Excel 열기
        excel = win32.DispatchEx('Excel.Application')
        excel.Visible = False

        self.baseDir = self.input_directory("파일 경로를 입력해주세요")
        self.source = self.input_directory("멘토링 파일 이름을 입력해주세요")
        self.new_filename = self.input_directory("새롭게 생성할 파일 이름을 입력해주세요")
        self.sourceFile = os.path.join(self.baseDir, self.source)
        self.newFilePath = os.path.join(self.baseDir, self.new_filename)

        workbook = excel.Workbooks.Open(self.sourceFile)
        sheet = workbook.Sheets(2)
        pick_cols = [13, 16]
        recipientList = self.get_recipients_from_excel(sheet, pick_cols)

        self.remove_columns_and_save(sheet, workbook, [2, 5, 6, 14])
        self.send_mail(recipientList)

        # 엑셀 파일 닫기 및 종료
        workbook.Close(SaveChanges=0)
        excel.Quit()

        del sheet
        del workbook
        del excel
