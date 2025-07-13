from datetime import datetime
from typing import Optional
from enum import Enum
from pydantic import BaseModel, Field

class TransferStatus(str, Enum):
    """
    Перечисление для статусов трансфера.
    """
    SCHEDULED = "scheduled"
    COMPLETED = "completed"
    CANCELED = "canceled"

class TransferBase(BaseModel):
    """
    Базовая схема с общими полями для трансфера.
    """
    guest_name: str = Field(..., min_length=1, description="Имя гостя")
    room_number: str = Field(..., description="Номер комнаты")
    phone_number: str = Field(..., description="Контактный номер телефона")
    transfer_date: datetime = Field(..., description="Дата и время трансфера")
    passengers: int = Field(..., gt=0, description="Количество пассажиров")
    pickup_location: str = Field(..., description="Место подачи машины")
    destination: str = Field(..., description="Пункт назначения")
    flight_number: Optional[str] = Field(None, description="Номер рейса (опционально)")
    comments: Optional[str] = Field(None, description="Комментарии к заказу (опционально)")

class TransferCreate(TransferBase):
    """
    Схема для создания нового трансфера (данные от API).
    """
    pass

class TransferInDBBase(TransferBase):
    """
    Базовая схема для трансфера, хранящегося в БД.
    """
    id: str = Field(..., alias="_id", description="Уникальный идентификатор трансфера в MongoDB")
    status: TransferStatus = Field(default=TransferStatus.SCHEDULED, description="Текущий статус трансфера")

class TransferPublic(TransferInDBBase):
    """
    Публичная схема, возвращаемая через API.
    """
    pass

class TransferUpdate(BaseModel):
    """
    Схема для частичного обновления трансфера.
    Все поля опциональны.
    """
    guest_name: Optional[str] = None
    room_number: Optional[str] = None
    phone_number: Optional[str] = None
    transfer_date: Optional[datetime] = None
    passengers: Optional[int] = None
    pickup_location: Optional[str] = None
    destination: Optional[str] = None
    flight_number: Optional[str] = None
    comments: Optional[str] = None
    status: Optional[TransferStatus] = None 