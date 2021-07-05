import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class MailSenderService:

    TAG = "$$TOKEN_REF$$"

    def __init__(self, config_path: str, template_path: str):
        with open(config_path) as json_config:
            config = json.load(json_config)
        self.server = config['server']
        self.port = config['port']
        self.mail = config['email']
        self.pwd = config['password']

        with open(template_path) as template:
            self.template = template.read()


    def send_verification_email(self, url: str):
        server = smtplib.SMTP_SSL(self.server, self.port)

        server.connect(self.server, self.port)
        server.login(self.mail, self.pwd)

        msg = MIMEMultipart('alternative')
        msg['subject'] = u'Подтверждение регистрации для StdQueue'
        attach = MIMEText(self.template.replace(MailSenderService.TAG, url), 'html', 'utf-8')
        msg.attach(attach)

        server.sendmail(self.mail, ["gipermonk@bk.ru"], msg.as_string())

        server.quit()
