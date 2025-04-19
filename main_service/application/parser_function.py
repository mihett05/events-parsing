import asyncio
import imaplib
import email
from typing import List
from email.utils import parsedate_to_datetime

from domain.mails.dtos import CreateMailDto
from domain.mails.enums import MailStateEnum



#Нужны тесты на почте!


async def parse_unread_emails(
        imap_server: str,
        username: str,
        password: str,
) -> List[CreateMailDto]:

    def _sync_imap_fetch():
        imap = imaplib.IMAP4_SSL(imap_server)
        imap.login(username, password)
        imap.select("INBOX")

        status, messages = imap.search(None, "UNSEEN")
        if status != "OK" or not messages[0]:
            return []

        email_ids = messages[0].split()
        emails_data = []

        for e_id in email_ids:
            try:
                status, msg_data = imap.fetch(e_id, "(RFC822)")
                if status != "OK":
                    raise Exception(f"Не удалось получить письмо {e_id}")

                raw_email = msg_data[0][1]
                msg = email.message_from_bytes(raw_email)

                theme = msg["subject"] or None
                sender = msg["from"] or None
                received_date = parsedate_to_datetime(msg["date"]).date() if "date" in msg else None

                raw_content = raw_email

                email_dto = CreateMailDto(
                    theme=theme,
                    sender=sender,
                    raw_content=raw_content,
                    received_date=received_date,
                    state=MailStateEnum.PROCESSED
                )
                emails_data.append(email_dto)

            except Exception as ex:
                print(f"Ошибка парсинга письма {e_id}: {ex}")
                imap.store(e_id, "-FLAGS", "\\Seen")
                continue

        imap.close()
        imap.logout()
        return emails_data

    loop = asyncio.get_running_loop()
    emails = await loop.run_in_executor(None, _sync_imap_fetch)
    return emails
