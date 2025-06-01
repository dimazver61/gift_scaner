from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


# --- Вспомогательные модели ---
class File(BaseModel):
    id: int
    expected_size: int
    size: int
    local: Dict[str, Any]
    remote: Dict[str, Any]


class ThumbnailFormat(BaseModel):
    type: str = "thumbnailFormatWebp"  # Пример: {"@type": "thumbnailFormatWebp"}


class Thumbnail(BaseModel):
    file: File
    height: int
    width: int
    format: ThumbnailFormat


class StickerFormat(BaseModel):
    type: str = "stickerFormatTgs"  # Пример: {"@type": "stickerFormatTgs"}


class StickerFullType(BaseModel):
    type: str = "stickerFullTypeCustomEmoji"  # Пример: {"@type": "stickerFullTypeCustomEmoji"}
    custom_emoji_id: str
    needs_repainting: bool


class Sticker(BaseModel):
    id: str
    emoji: str
    width: int
    height: int
    format: StickerFormat
    full_type: StickerFullType
    sticker: File
    thumbnail: Thumbnail
    set_id: str


# --- Основная модель Gift ---
class Gift(BaseModel):
    type: str = Field(alias="@type")  # Маппинг "@type" -> "type"
    id: str
    star_count: int
    default_sell_star_count: int
    sticker: Sticker
    remaining_count: int = 0
    upgrade_star_count: int = 0
    total_count: int = 0
    is_for_birthday: bool = False
    first_send_date: int = 0
    last_send_date: int = 0