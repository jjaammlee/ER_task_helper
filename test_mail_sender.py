import pytest
from mail_sender import MailSender


@pytest.fixture
def mail_sender():
    return MailSender(baseDir='dummy_dir', source='source.xlsx', new_filename='modified.xlsx')


def test_send_mail(mocker, mail_sender):
    mock_post = mocker.patch('mail_sender.requests.post')
    mock_post.return_value.json.return_value = {"result": "success"}

    recipients = [{'emailAddress': 'test@samsung.com', 'recipientType': 'TO'}]

    mail_sender.newFilePath = ''
    mail_sender.send_mail(recipients)

    mock_post.assert_called_once()


def test_execute(mocker, mail_sender):
    mocker.patch.object(mail_sender, 'get_recipients_from_excel')
    mocker.patch.object(mail_sender, 'remove_columns_and_save')
    mocker.patch.object(mail_sender, 'send_mail')

    mock_dispatch = mocker.patch('mail_sender.win32.Dispatch')
    mock_excel = mocker.Mock()
    mock_dispatch.return_value = mock_excel
    mock_excel.Workbooks.Open.return_value = mocker.Mock(Sheets={2: mocker.Mock()})

    mail_sender.execute()

    assert mail_sender.get_recipients_from_excel.called
    assert mail_sender.remove_columns_and_save.called
    assert mail_sender.send_mail.called
