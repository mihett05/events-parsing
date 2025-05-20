import email
from email.header import decode_header
from email.parser import BytesParser
from email.policy import default
from email.utils import parsedate_to_datetime
from io import BytesIO
from pathlib import Path
from typing import Iterable

from aioimaplib import Response, aioimaplib
from application.mails.gateway import EmailsGateway
from domain.attachments.dtos import ParsedAttachmentInfoDto
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
        batch_size = 10
        failed_mails = []
        for i in range(0, 10, batch_size):
            batch_uids = email_ids[i : i + batch_size]

            raw_collection, failed = await self.__fetch_collection_by_batch(
                batch_uids
            )
            failed_mails.extend(failed)

            parsed_mails, failed = await self.__parse_mails(raw_collection)
            emails.extend(parsed_mails)
            failed_mails.extend(failed)

        await self.__mark_mail_as_unseen(failed_mails)
        return emails

    async def mark_mails_as_failed(self, mail_ids: list[str]):
        for mail_id in mail_ids:
            if not await self.move_mail(mail_id, "NotParsed"):
                print(f"mail {mail_id} not moved")

    async def move_mail(self, mail_id, target_folder) -> bool:
        try:
            await self.__ensure_folder_exists(target_folder)
            response = await self.client.uid("MOVE", mail_id, "NotParsed")
            return response.result == "OK"
        except Exception as e:
            print(f"Error moving mail: {e}")
            return False

    async def __ensure_folder_exists(self, folder_name: str):
        try:
            response = await self.client.list("INBOX", "*")
            folders = [
                line.decode("utf-8").split('"/"')[-1].strip('"')
                for line in response.lines
                if b'"/"' in line
            ]
            folders = [x.replace(' "', "") for x in folders]

            if folder_name not in folders:
                await self.client.create(folder_name)
        except Exception as e:
            print(f"Tunk Tunk Tunk says: {str(e)}")

    async def __fetch_collection_by_batch(
        self, batch_uuids
    ) -> tuple[list[tuple[str, Response]], list[str]]:
        batch_uuids = map(lambda uid: uid.decode("ascii"), batch_uuids)
        return await self.__fetch_collection_by_single(batch_uuids)

    async def __fetch_collection_by_single(
        self, email_ids: Iterable[str]
    ) -> tuple[list[tuple[str, Response]], list[str]]:
        collection = []
        failed = []
        for e_id in email_ids:
            try:
                collection.append((e_id, await self.__fetch_mail(e_id)))
            except FailedFetchMailError:
                await self.__mark_mail_as_unseen(e_id)
                failed.append(e_id)
        return collection, failed

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
        return ParsedMailInfoDto(
            imap_mail_uid=email_uid,
            theme=self.__decode_header(message.get("Subject", "")),
            sender=self.__decode_header(message.get("From", "")),
            raw_content=await self.__get_message_body(raw_message),
            received_date=parsedate_to_datetime(message["date"]).date()
            if "date" in message
            else None,
            attachments=await self.__get_message_attachments(message),
        )

    async def __get_message_body(self, raw_message):
        msg = BytesParser(policy=default).parsebytes(raw_message)
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                if content_type == "text/plain":
                    return part.get_payload(decode=False).encode()
        return msg.get_payload(decode=False).encode()

    async def __get_message_attachments(self, message):
        attachments = []
        if message.is_multipart():
            for part in message.walk():
                content_disposition = str(part.get("Content-Disposition", ""))
                if "attachment" in content_disposition or part.get_filename():
                    attachment = await self.__parse_attachment(part)
                    if attachment:
                        attachments.append(attachment)
        return attachments

    async def __parse_attachment(self, part) -> ParsedAttachmentInfoDto | None:
        filename = part.get_filename()
        if not filename:
            return None

        filename = self.__decode_header(filename)
        extension = Path(filename).suffix.lower()
        filename = Path(filename).stem

        payload = part.get_payload(decode=True)
        if not payload:
            return None

        content = BytesIO(payload)
        content.seek(0)

        return ParsedAttachmentInfoDto(
            filename=filename, extension=extension, content=content
        )

    async def __parse_mails(
        self, raw_messages: list[tuple[str, Response]]
    ) -> tuple[list[ParsedMailInfoDto], list[str]]:
        collection = []
        failed = []
        for email_uid, raw_msg in raw_messages:
            try:
                collection.append(await self.__parse_mail(email_uid, raw_msg))
            except FailedParseMailError:
                await self.__mark_mail_as_unseen(email_uid)
                failed.append(email_uid)
                continue
        return collection, failed

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
