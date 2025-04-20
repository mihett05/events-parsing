import asyncio
import email
from email.header import decode_header
from email.utils import parsedate_to_datetime
from typing import Iterable

from aioimaplib import aioimaplib, Response

from application.mails.gateway import EmailsGateway
from domain.mails.dtos import ParsedMailInfoDto
from domain.mails.exceptions import FailedFetchMailError, FailedParseMailError


class ImapEmailsGateway(EmailsGateway):
    async def __aenter__(self, imap_server, username, password):
        self.client = aioimaplib.IMAP4_SSL(host=imap_server)
        await self.client.wait_hello_from_server()
        await self.client.login(username, password)
        await self.client.select("INBOX")
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.logout()

    async def receive_mails(self) -> list[ParsedMailInfoDto]:
        response = await self.client.search("UNSEEN")
        emails = []
        email_ids = response.lines[0].split()
        batch_size = 200

        for i in range(0, len(email_ids), batch_size):
            batch_uids = email_ids[i : i + batch_size]
            raw_mail_collection = await self.__fetch_collection_by_batch(
                batch_uids
            )
            async for raw_mail in self.__parse_mails(raw_mail_collection):
                emails.append(raw_mail)

        return emails

    async def __fetch_collection_by_batch(self, batch_uuids) -> list[Response]:
        batch_uuids = ",".join(uid.decode('ascii') for uid in batch_uuids)
        fetch_response = await self.client.uid(
            "FETCH", ",".join(batch_uuids), "(RFC822 FLAGS)"
        )

        if fetch_response.result != "OK":
            return await self.__fetch_collection_by_single(batch_uuids)

        collection = []
        raw_messages = [
            line
            for line in fetch_response.lines
            if line.startswith(b"UID") and b"RFC822" in line
        ]

        for j in range(0, len(raw_messages), 2):
            uid = batch_uuids[j // 2]
            try:
                collection.append(raw_messages[j + 1])
                await self.__mark_mail_as_seen(raw_messages[j + 1])
            except IndexError:
                await self.__mark_mail_as_unseen(uid)
                continue

    async def __fetch_collection_by_single(self, email_ids) -> list[Response]:
        collection = []
        for e_id in email_ids:
            try:
                collection.append(await self.__fetch_mail(e_id))
                await self.__mark_mail_as_seen(e_id)
            except FailedFetchMailError:
                await self.__mark_mail_as_unseen(e_id)
        return collection

    async def __fetch_mail(self, e_id) -> Response:
        fetch_response = await self.client.fetch(e_id, "(RFC822)")
        if fetch_response.result != "OK":
            raise FailedFetchMailError
        return fetch_response

    async def __mark_mail_as_seen(self, e_id):
        await self.client.uid("STORE", e_id, "+FLAGS", "\\Seen")

    async def __mark_mail_as_unseen(self, e_id):
        await self.client.uid("STORE", e_id, "-FLAGS", "\\Seen")

    async def __parse_mail(self, raw_msg) -> ParsedMailInfoDto:
        raw_msg = raw_msg.lines[1]
        msg = email.message_from_bytes(raw_msg)
        theme = self.__decode_header(msg.get("Subject", ""))
        sender = self.__decode_header(msg.get("From", ""))
        try:
            return ParsedMailInfoDto(
                theme=theme,
                sender=sender,
                raw_content=raw_msg,
                received_date=parsedate_to_datetime(msg["date"]).date()
                if "date" in msg
                else None,
            )
        except IndexError:
            raise FailedParseMailError()

    async def __parse_mails(self, raw_messages) -> Iterable[ParsedMailInfoDto]:
        for raw_msg in raw_messages:
            try:
                yield await self.__parse_mail(raw_msg)
            except FailedParseMailError:
                continue

    @staticmethod
    def __decode_payload(payload, charset=None):
        encodings_to_try = [
            charset,
            'utf-8',
        ]
        encodings_to_try = list(dict.fromkeys([e for e in encodings_to_try if e]))
        for encoding in encodings_to_try:
            try:
                return payload.decode(encoding, errors='replace')
            except (UnicodeDecodeError, LookupError):
                continue

    @staticmethod
    def __decode_header(header):
        decoded_parts = []
        for part, encoding in decode_header(header):
            if isinstance(part, bytes):
                decoded_parts.append(ImapEmailsGateway.__decode_payload(part, encoding))
            else:
                decoded_parts.append(str(part))
        return "".join(decoded_parts)


async def main():
    gate = ImapEmailsGateway()
    print(gate)
    async with gate('imap.gmail.com', 'your@gmail.com', "your_password") as g:
        data = await g.receive_mails()
        for email in data:
            print(f"From: {email.sender}")
            print(f"Subject: {email.theme}")
            print(f"Date: {email.received_date}")

if __name__ == '__main__':
    asyncio.run(main())
