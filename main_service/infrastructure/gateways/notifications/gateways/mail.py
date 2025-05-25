from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from aiosmtplib import SMTP
from application.notifications.gateway import NotificationGateway
from domain.attachments.dtos import ParsedAttachmentInfoDto
from domain.notifications.entities import Notification
from domain.users.entities import User


class NotificationEmailGateway(NotificationGateway):
    def __init__(self, smtp_server, smtp_port, imap_username, imap_password):
        self.smtp_server = smtp_server
        self.smtp_host = smtp_port
        self.smtp_username = imap_username
        self.smtp_password = imap_password

    async def __aenter__(self):
        self.smtp_client = SMTP(hostname=self.smtp_server, port=self.smtp_host)
        await self.smtp_client.connect()
        await self.smtp_client.login(self.smtp_username, self.smtp_password)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.smtp_client.quit()

    async def send(
        self,
        notification: Notification,
        recipient: User,
        attachments: list[ParsedAttachmentInfoDto] = None,
    ):
        try:
            msg = MIMEMultipart()
            msg["From"] = self.smtp_username
            msg["To"] = recipient.email
            msg["Subject"] = "Уведомление"
            msg.attach(MIMEText(notification.text, "plain"))
            if attachments:
                msg = self.__add_attachments(msg, attachments)
            await self.smtp_client.send_message(msg)
        except Exception as e:
            print(f"Ошибка отправки сообщения: {str(e)}")

    def __add_attachments(self, msg, attachments):
        for attachment in attachments:
            file_content = attachment.content.read()
            part = MIMEApplication(file_content, Name=attachment.file_path)
            part["Content-Disposition"] = (
                f'attachment; filename="{attachment.filename}"'
            )
            msg.attach(part)
            attachment.content.seek(0)
        return msg
