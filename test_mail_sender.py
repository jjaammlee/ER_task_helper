import pytest
from mail_sender import MailSender
from unittest.mock import MagicMock


@pytest.fixture
def mail_sender():
    return MailSender()


def test_send_mail(mocker, mail_sender):
    mock_post = mocker.patch('mail_sender.requests.post')
    mock_post.return_value.json.return_value = {"result": "success"}

    recipients = [{'emailAddress': 'test@samsung.com', 'recipientType': 'TO'}]

    mail_sender.newFilePath = ''
    mail_sender.send_mail(recipients)

    mock_post.assert_called_once()

def test_send_mail_with_attachment(mocker, mail_sender):
    mock_post = mocker.patch('mail_sender.requests.post')
    mock_post.return_value.json.return_value = {"result": "success"}

    mail_sender.newFilePath = 'C:\\Users\\jjaamm.lee.SECDS\\Desktop\\ER업무dummy_path.xlsx'

    # open 함수도 mock (실제 파일 읽지 않게)
    mocker.patch('builtins.open', mocker.mock_open(read_data='filedata'))

    recipients = [{'emailAddress': 'test@samsung.com', 'recipientType': 'TO'}]
    mail_sender.send_mail(recipients)

    assert mock_post.called
    mock_post.assert_called_once()


def test_execute(mocker, mail_sender):
    mocker.patch.object(mail_sender, 'get_recipients_from_excel')
    mocker.patch.object(mail_sender, 'remove_columns_and_save')
    mocker.patch.object(mail_sender, 'send_mail')

    mock_dispatch = mocker.patch('mail_sender.win32.DispatchEx')
    mock_excel = mocker.Mock()
    mock_dispatch.return_value = mock_excel

    mock_sheet = MagicMock()
    mock_workbook = MagicMock()
    mock_excel.Workbooks.Open.return_value = mock_workbook
    mock_workbook.Sheets.__getitem__.return_value = mock_sheet

    mocker.patch('builtins.input', side_effect=[
        'C:\\Users\\Dummy\\Desktop',       # baseDir
        'source.xlsx',                     # source
        'modified.xlsx'                    # new_filename
    ])

    mail_sender.execute()

    mail_sender.get_recipients_from_excel.assert_called_once()
    mail_sender.remove_columns_and_save.assert_called_once()
    mail_sender.send_mail.assert_called_once()
