from email.header import decode_header
from email.utils import parsedate_to_datetime

from aioimaplib import aioimaplib
import email
from domain.mails.dtos import ReadMailDto
from application.mails.gateway import EmailsGateway
from domain.mails.exceptions import FailedParseMailError


class EmailsGateway(EmailsGateway):

    async def __aenter__(self, imap_server, username, password):
        self.client = aioimaplib.IMAP4_SSL(host=imap_server)
        await self.client.wait_hello_from_server()
        await self.client.login(username, password)
        await self.client.select("INBOX")

    async def __aexit__(self):
        await self.client.logout()

    async def receive_emails(self) -> list[ReadMailDto]:
        response = await self.client.search("UNSEEN")
        email_ids = response.lines[0].split()
        emails = []
        for e_id in email_ids:
            try:
                fetch_response = await self.client.fetch(e_id, "(RFC822)")
                if fetch_response.result != "OK":
                    raise FailedParseMailError
                emails.append(await self.__parse_mail(fetch_response))
                await self.__mark_mail_as_seen(e_id)
            except FailedParseMailError:
                await self.__mark_mail_as_unseen(e_id)
        return emails

    async def __mark_mail_as_seen(self, e_id):
        await self.client.uid('STORE', e_id, '+FLAGS', '\\Seen')

    async def __mark_mail_as_unseen(self, e_id):
        await self.client.uid('STORE', e_id, '-FLAGS', '\\Seen')

    async def __parse_mail(self, fetch_response) -> ReadMailDto:
        msg = email.message_from_bytes(fetch_response.lines[1])

        return ReadMailDto(theme="".join(
            part.decode(enc) if isinstance(part, bytes) else str(part)
            for part, enc in decode_header(msg.get("Subject", ""))),
            sender="".join(
                part.decode(enc) if isinstance(part, bytes) else str(part)
                for part, enc in decode_header(msg.get("From", ""))),
            raw_content=fetch_response.lines[1],
            received_date=parsedate_to_datetime(msg["date"]).date() if "date" in msg else None
        )
