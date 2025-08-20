class MailSender:
    def __init__(self, baseDir='', source='', new_filename=''):
        self.baseDir = baseDir
        self.source = source
        self.new_filename = new_filename
        self.newFilePath = ''

    def get_recipients_from_excel(self, sheet, pickUpCol):
        pass

    def remove_columns_and_save(self, sheet, workbook, removeCols):
        pass

    def send_mail(self, recipientList):
        pass

    def execute(self):
        pass
