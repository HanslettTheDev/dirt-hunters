from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from dirt_hunters import db


class Reviews(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    rating: Mapped[int]
    review_title: Mapped[str]
    review_content: Mapped[str]
    date_created: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now((timezone.utc))
    )


class CustomerRequests(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str]
    email: Mapped[str]
    phone_number: Mapped[int] = mapped_column(default=0)
    service_type: Mapped[str]
    message: Mapped[str]
    is_email_sent: Mapped[bool] = mapped_column(default=False)
    date_created: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now((timezone.utc))
    )

    def __str__(self):
        return f"Customer Request: {self.full_name}"
