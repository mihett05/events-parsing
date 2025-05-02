import asyncio
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import aiosmtplib
from aiosmtplib import SMTP

from domain.attachments.dtos import ParsedAttachmentInfoDto
from domain.notifications.entities import Notification
from domain.users.entities import User


class NotificationEmailGateway:
    def __init__(self, smtp_server, smtp_host, imap_username, imap_password):
        self.smtp_server = smtp_server
        self.smtp_host = smtp_host
        self.smtp_username = imap_username
        self.smtp_password = imap_password

    async def __aenter__(self):
        self.smtp_client = SMTP(hostname=self.smtp_server, port=self.smtp_host)
        await self.smtp_client.connect()
        response = await self.smtp_client.login(self.smtp_username, self.smtp_password)
        print(response)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.smtp_client.quit()

    async def send(self, notification, recipient):
        try:
            msg = MIMEMultipart()
            msg["From"] = "events-parsing@mail.ru"
            msg["To"] = recipient.email
            msg["Subject"] = "Уведомление"
            msg.attach(MIMEText(notification.text, "plain"))
            await self.smtp_client.send_message(msg)
        except Exception as e:
            print(f"Ошибка отправки сообщения: {str(e)}")


class NotificationWithAttachmentsEmailGateway:
    async def send_with_attachments(
        self,
        notification: Notification,
        recipient: User,
        attachments: list[ParsedAttachmentInfoDto],
    ):
        try:
            msg = MIMEMultipart()
            msg["From"] = "events-parsing@mail.ru"
            msg["To"] = recipient.email
            msg["Subject"] = "Уведомление"
            msg.attach(MIMEText(notification.text, "plain"))
            for attachment in attachments:
                file_content = attachment.content.read()
                part = MIMEApplication(file_content, Name=attachment.filename)
                part["Content-Disposition"] = (
                    f'attachment; filename="{attachment.filename}"'
                )
                msg.attach(part)
                attachment.content.seek(0)
        except Exception as e:
            print(f"Ошибка отправки сообщения: {str(e)}")
