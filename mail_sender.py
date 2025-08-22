import json
import requests
import os
import win32com.client as win32
import warnings
from api_config import MAIL_API_CONFIG, build_headers
from mail_profiles import MAIL_PROFILES

warnings.filterwarnings('ignore')

BASE_URL = MAIL_API_CONFIG["BASE_URL"]
USER_ID = MAIL_API_CONFIG["USER_ID"]
URL = f"{BASE_URL}/mails/send?userId={USER_ID}"
HEADERS = build_headers(stage=True)


class MailSender:
    def __init__(self, profile_key):
        if profile_key not in MAIL_PROFILES:
            raise ValueError(f"'{profile_key}' is not a valid mail profile.")
        self.profile = MAIL_PROFILES[profile_key]

    def get_recipients_from_excel(self, sheet):
        used_range = sheet.UsedRange
        row_count = used_range.Rows.Count

        recipients = []
        filter_col = self.profile["filter_column"]
        filter_val = self.profile["filter_value"]

        for i in range(1, row_count + 1):
            if sheet.Cells(i, filter_col).Value != filter_val:
                continue
            for col in self.profile["recipient_columns"]:
                email = sheet.Cells(i, col).Value
                if email:
                    recipients.append({
                        "emailAddress": email + '@samsung.com',
                        "recipientType": "TO"
                    })
        return recipients

    def remove_columns_and_save(self, sheet, workbook):
        used_range = sheet.UsedRange
        row_count = used_range.Rows.Count

        filter_col = self.profile["filter_column"]
        filter_val = self.profile["filter_value"]

        for i in range(row_count, 2, -1):
            cell_value = sheet.Cells(i, filter_col).Value
            if not cell_value or filter_val not in str(cell_value):
                sheet.Rows(i).Delete()

        for col in sorted(self.profile.get("remove_columns", []), reverse=True):
            sheet.Columns(col).Delete()

        used_range = sheet.UsedRange
        row_count = used_range.Rows.Count
        col_count = used_range.Columns.Count

        additional_cols = self.profile.get("additional_columns", [])
        header_row = 1
        start_col = col_count + 1

        for offset, col_info in enumerate(additional_cols):
            col_index = start_col + offset
            cell = sheet.Cells(header_row, col_index)
            cell.Value = col_info["name"]
            cell.Interior.ColorIndex = col_info.get("color", 6)
            cell.Font.Bold = True

            borders = cell.Borders
            borders(7).LineStyle = 1  # xlEdgeLeft
            borders(8).LineStyle = 1  # xlEdgeTop
            borders(9).LineStyle = 1  # xlEdgeBottom
            borders(10).LineStyle = 1  # xlEdgeRight

        last_col = col_count + len(additional_cols)
        data_range = sheet.Range(sheet.Cells(1, 1), sheet.Cells(row_count, last_col))
        borders = data_range.Borders
        for edge in [7, 8, 9, 10, 11, 12]:  # xlEdgeLeft to xlInsideVertical
            borders(edge).LineStyle = 1

        workbook.SaveAs(self.newFilePath)

    def send_mail(self, recipientList):
        body = {
            "subject": self.profile["mail_subject"],
            "contents": self.profile["mail_body"],
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
                    URL, headers=HEADERS, data=[('mail', (None, json.dumps(body)))],
                    files=[('attachments', (open(self.newFilePath, 'rb')))], verify=False
                )
            else:
                result = requests.post(URL, headers=HEADERS, data=[('mail', (None, json.dumps(body)))], verify=False)

            sendResult = result.json()
            if sendResult.get('errorCode'):
                print(f"[ERROR] {sendResult['errorCode']} - {sendResult.get('errorMessage', 'No error message')}")
            else:
                print(f"[{sendResult.get('result')}]: 메일 전송 성공")
        except Exception as e:
            print(f"[ERROR] 메일 전송 실패: {e}")

    def input_directory(self, prompt):
        return input(f"{prompt}: ").strip()

    def execute(self):
        excel = win32.DispatchEx('Excel.Application')
        excel.Visible = False

        self.baseDir = self.input_directory("파일 경로를 입력해주세요")
        self.source = self.input_directory("멘토링 파일 이름을 입력해주세요")
        self.new_filename = self.input_directory("새롭게 생성할 파일 이름을 입력해주세요")
        self.sourceFile = os.path.join(self.baseDir, self.source)
        self.newFilePath = os.path.join(self.baseDir, self.new_filename)

        workbook = excel.Workbooks.Open(self.sourceFile)
        sheet_index = self.profile.get("sheet_index", 1)
        sheet = workbook.Sheets(sheet_index)

        recipients = self.get_recipients_from_excel(sheet)
        self.remove_columns_and_save(sheet, workbook)
        self.send_mail(recipients)

        workbook.Close(SaveChanges=0)
        excel.Quit()

        del sheet
        del workbook
        del excel
