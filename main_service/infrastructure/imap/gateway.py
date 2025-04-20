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

    async def __aexit__(self):
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
            emails.extend(self.__parse_mails(raw_mail_collection))

        return emails

    async def __fetch_collection_by_batch(self, batch_uuids) -> list[Response]:
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
            uid = raw_messages[j].decode()
            try:
                uid = uid.split()[1]
                collection.append(raw_messages[j + 1])
                await self.__mark_mail_as_seen(raw_messages[j + 1])
            except IndexError:
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
        msg = email.message_from_bytes(raw_msg)

        try:
            return ParsedMailInfoDto(
                theme=self.__parse_mail_header(
                    decode_header(msg.get("Subject", ""))[0][0]
                ),
                sender=self.__parse_mail_header(
                    decode_header(msg.get("From", ""))[0][0]
                ),
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
    def __parse_mail_header(entity):
        return (
            entity.decode("utf-8", errors="replace")
            if isinstance(entity, bytes)
            else str(entity)
        )
