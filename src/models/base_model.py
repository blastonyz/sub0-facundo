from datetime import datetime

import sqlalchemy as sa
from sqlmodel import SQLModel, Field, TIMESTAMP

class BaseTable(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime | None = Field(
        default=None,
        sa_type=sa.DateTime(timezone=True),
        sa_column_kwargs={"server_default": sa.func.now()},
        nullable=False,
    )
    updated_at: datetime | None = Field(
      default_factory=lambda: datetime.now(),
      nullable=False,
      sa_column_kwargs={
          "onupdate": lambda: datetime.now(),
      },
      sa_type=TIMESTAMP(timezone=True),
  )