from email.header import decode_header
from email.utils import parsedate_to_datetime

from aioimaplib import aioimaplib
import email
from domain.mails.dtos import ParsedMailInfoDto
from application.mails.gateway import EmailsGateway
from domain.mails.exceptions import FailedParseMailError


class ImapEmailsGateway(EmailsGateway):

    async def __aenter__(self, imap_server, username, password):
        self.client = aioimaplib.IMAP4_SSL(host=imap_server)
        await self.client.wait_hello_from_server()
        await self.client.login(username, password)
        await self.client.select("INBOX")

    async def __aexit__(self):
        await self.client.logout()

    async def receive_emails(self) -> list[ParsedMailInfoDto]:
        response = await self.client.search("UNSEEN")
        email_ids = response.lines[0].split()
        emails = []
        for e_id in email_ids:
            try:
                emails.append(await self.__fetch_mails(e_id))
                await self.__mark_mail_as_seen(e_id)
            except FailedParseMailError:
                await self.__mark_mail_as_unseen(e_id)
        return emails

    async def __fetch_mails(self, e_id):
        fetch_response = await self.client.fetch(e_id, "(RFC822)")
        if fetch_response.result != "OK":
            raise FailedParseMailError
        return await self.__parse_mail(fetch_response)

    async def __mark_mail_as_seen(self, e_id):
        await self.client.uid('STORE', e_id, '+FLAGS', '\\Seen')

    async def __mark_mail_as_unseen(self, e_id):
        await self.client.uid('STORE', e_id, '-FLAGS', '\\Seen')

    async def __parse_mail(self, raw_msg) -> ParsedMailInfoDto:
        msg = email.message_from_bytes(raw_msg)

        return ParsedMailInfoDto(
            theme=self.__parse_mail_header(decode_header(msg.get("Subject", ""))[0][0]),
            sender=self.__parse_mail_header(decode_header(msg.get("From", ""))[0][0]),
            raw_content=raw_msg,
            received_date=parsedate_to_datetime(msg["date"]).date() if "date" in msg else None
        )

    def __parse_mail_header(self, entity):
        return entity.decode('utf-8', errors='replace') if isinstance(entity, bytes) else str(entity)
