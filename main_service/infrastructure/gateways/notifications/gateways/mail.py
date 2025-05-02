import asyncio
from email.mime.application import MIMEApplication
from domain.attachments.dtos import ParsedAttachmentInfoDto
from domain.notifications.entities import Notification
from domain.users.entities import User


from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import aiosmtplib


class NotificationEmailGateway:
    async def send(self, notification, recipient):
        try:
            msg = MIMEMultipart()
            msg['From'] = "events-parsing@mail.ru"
            msg['To'] = recipient.email
            msg['Subject'] = "Уведомление"
            msg.attach(MIMEText(notification.text, 'plain'))
            await aiosmtplib.send(
                msg,
                hostname="smtp.mail.ru",
                port=587,
                username="events-parsing@mail.ru",
                password="NYPjKvmsvPpynkLCcgWi"
            )
        except Exception as e:
            print(f"Ошибка отправки сообщения: {str(e)}")


class NotificationWithAttachmentsEmailGateway:
    async def send_with_attachments(self,
                                    notification: Notification,
                                    recipient: User,
                                    attachments: list[ParsedAttachmentInfoDto]):
        try:
            msg = MIMEMultipart()
            msg['From'] = "events-parsing@mail.ru"
            msg['To'] = recipient.email
            msg['Subject'] = "Уведомление"
            msg.attach(MIMEText(notification.text, 'plain'))
            for attachment in attachments:
                file_content = attachment.content.read()
                part = MIMEApplication(
                    file_content,
                    Name=attachment.filename
                )
                part['Content-Disposition'] = f'attachment; filename="{attachment.filename}"'
                msg.attach(part)
                attachment.content.seek(0)

            await aiosmtplib.send(
                msg,
                hostname="smtp.mail.ru",
                port=587,
                username="events-parsing@mail.ru",
                password="NYPjKvmsvPpynkLCcgWi"
            )
        except Exception as e:
            print(f"Ошибка отправки сообщения: {str(e)}")


async def main():
    gateway = NotificationEmailGateway()
    await gateway.send(
        notification=Notification(text="Тестовое сообщение"),
        recipient=User(email="events-parsing@mail.ru", fullname="Nick")
    )


if __name__ == "__main__":
    asyncio.run(main())
