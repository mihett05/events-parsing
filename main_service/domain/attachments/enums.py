from enum import Enum


class AttachmentStorageTypeEnum(Enum):
    LOCAL_STORAGE = "LOCAL_STORAGE"
    S3_STORAGE = "S3_STORAGE"


class AttachmentContentTypeEnum(Enum):
    PNG_IMAGE = "application/png"
    JPEG_IMAGE = "application/jpeg"
    PDF_FILE = "application/pdf"
    JSON_FILE = "application/json"
