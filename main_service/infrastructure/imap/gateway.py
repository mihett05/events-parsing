import email
from email.header import decode_header
from email.utils import parsedate_to_datetime

from aioimaplib import Response, aioimaplib

from application.mails.gateway import EmailsGateway
from domain.mails.dtos import ParsedMailInfoDto
from domain.mails.exceptions import FailedFetchMailError, FailedParseMailError


class ImapEmailsGateway(EmailsGateway):
    def __init__(self, imap_server, imap_username, imap_password):
        self.imap_server = imap_server
        self.imap_username = imap_username
        self.imap_password = imap_password

    async def __aenter__(self):
        self.client = aioimaplib.IMAP4_SSL(host=self.imap_server)
        await self.client.wait_hello_from_server()
        res = await self.client.login(self.imap_username, self.imap_password)
        print(res.lines)  # посмотри, что вернул сервер
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
            emails.extend(await self.__parse_mails(raw_mail_collection))

        return emails

    async def __fetch_collection_by_batch(self, batch_uuids) -> list[Response]:
        batch_uuids = ",".join(uid.decode("ascii") for uid in batch_uuids)
        return await self.__fetch_collection_by_single(batch_uuids)

    async def __fetch_collection_by_single(self, email_ids) -> list[Response]:
        collection = []
        for e_id in email_ids:
            try:
                collection.append(await self.__fetch_mail(e_id.decode()))
                await self.__mark_mail_as_seen(e_id)
            except FailedFetchMailError:
                await self.__mark_mail_as_unseen(e_id)
        return collection

    async def __fetch_mail(self, e_id: str) -> Response:
        fetch_response = await self.client.fetch(e_id, "(RFC822)")
        if fetch_response.result != "OK":
            raise FailedFetchMailError
        return fetch_response

    async def __mark_mail_as_seen(self, e_id):
        await self.client.uid("STORE", e_id, "+FLAGS", "\\Seen")

    async def __mark_mail_as_unseen(self, e_id):
        await self.client.uid("STORE", e_id, "-FLAGS", "\\Seen")

    async def __parse_mail(self, raw_message) -> ParsedMailInfoDto:
        raw_message = raw_message.lines[1]
        message = email.message_from_bytes(raw_message)

        return ParsedMailInfoDto(
            theme=self.__decode_header(message.get("Subject", "")),
            sender=self.__decode_header(message.get("From", "")),
            raw_content=raw_message,
            received_date=parsedate_to_datetime(message["date"]).date()
            if "date" in message
            else None,
        )

    async def __parse_mails(self, raw_messages) -> list[ParsedMailInfoDto]:
        collection = []
        for raw_msg in raw_messages:
            try:
                collection.append(await self.__parse_mail(raw_msg))
            except FailedParseMailError:
                continue
        return collection

    @staticmethod
    def __decode_payload(payload, charset=None):
        encodings_to_try = [
            charset,
            "utf-8",
        ]
        encodings_to_try = list(
            dict.fromkeys([e for e in encodings_to_try if e])
        )
        for encoding in encodings_to_try:
            try:
                return payload.decode(encoding, errors="replace")
            except (UnicodeDecodeError, LookupError):
                continue

    @staticmethod
    def __decode_header(header):
        decoded_parts = []
        for part, encoding in decode_header(header):
            if isinstance(part, bytes):
                decoded_parts.append(
                    ImapEmailsGateway.__decode_payload(part, encoding)
                )
            else:
                decoded_parts.append(str(part))
        return "".join(decoded_parts)
