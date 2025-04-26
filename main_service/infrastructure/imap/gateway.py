import asyncio
import email
import os
from email.header import decode_header
from email.utils import parsedate_to_datetime
from io import BytesIO
from typing import Iterable
from domain.attachments.dtos import ParsedAttachmentInfoDto
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
        await self.client.login(self.imap_username, self.imap_password)
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

    async def mark_mails_as_failed(self, mail_ids: list[str]): ...

    """async def move_mail(self, mail_id, target_folder) -> bool:
        try:
            await self.__ensure_folder_exists(target_folder)

            # Копируем письмо
            copy_response = await self.client.uid('COPY', mail_id, target_folder)
            if copy_response.result != 'OK':
                return False

            # Помечаем исходное письмо как удалённое
            store_response = await self.client.uid('STORE', mail_id, '+FLAGS', '\\Deleted')
            if store_response.result != 'OK':
                return False

            return True
        except Exception as e:
            print(f"Error moving mail: {e}")
            return False"""

    """async def __ensure_folder_exists(self, folder_name: str):
        try:
            response = await self.client.list('INBOX', '*')
            folders = [
                line.decode('utf-8').split('"/"')[-1].strip('"')
                for line in response.lines
                if b'"/"' in line
            ]
            folders = [x.replace(' "', '') for x in folders]

            if folder_name not in folders:
                await self.client.create(folder_name)
        except Exception as e:
            print(f"Tunk Tunk Tunk says: {str(e)}")"""

    async def __fetch_collection_by_batch(
        self, batch_uuids
    ) -> list[tuple[str, Response]]:
        batch_uuids = map(lambda uid: uid.decode("ascii"), batch_uuids)
        return await self.__fetch_collection_by_single(batch_uuids)

    async def __fetch_collection_by_single(
        self, email_ids: Iterable[str]
    ) -> list[tuple[str, Response]]:
        collection = []
        for e_id in email_ids:
            try:
                collection.append((e_id, await self.__fetch_mail(e_id)))
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

    async def __parse_mail(
        self, email_uid: str, raw_message: Response
    ) -> ParsedMailInfoDto:
        raw_message = raw_message.lines[1]
        message = email.message_from_bytes(raw_message)
        attachments = []
        if message.is_multipart():
            for part in message.walk():
                content_disposition = str(part.get("Content-Disposition", ""))
                if "attachment" in content_disposition or part.get_filename():
                    attachment = await self.__parse_attachment(part)
                    if attachment:
                        attachments.append(attachment)

        return ParsedMailInfoDto(
            imap_mail_uid=email_uid,
            theme=self.__decode_header(message.get("Subject", "")),
            sender=self.__decode_header(message.get("From", "")),
            raw_content=raw_message,
            received_date=parsedate_to_datetime(message["date"]).date()
            if "date" in message
            else None,
            attachments=attachments
        )

    async def __parse_attachment(self, part) -> ParsedAttachmentInfoDto | None:
        filename = part.get_filename()
        if not filename:
            return None

        filename = self.__decode_header(filename)

        _, extension = os.path.splitext(filename)
        extension = extension.lower().lstrip('.') if extension else ''

        payload = part.get_payload(decode=True)
        if not payload:
            return None

        content = BytesIO(payload)
        content.seek(0)

        return ParsedAttachmentInfoDto(
            filename=filename,
            extension=extension,
            content=content
        )

    async def __parse_mails(
        self, raw_messages: list[tuple[str, Response]]
    ) -> list[ParsedMailInfoDto]:
        collection = []
        for email_uid, raw_msg in raw_messages:
            try:
                collection.append(await self.__parse_mail(email_uid, raw_msg))
            except FailedParseMailError:
                await self.__mark_mail_as_unseen(email_uid)
                continue
        return collection

    @staticmethod
    def __decode_payload(payload, charset=None):
        encodings_to_try = [charset, "utf-8"]
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