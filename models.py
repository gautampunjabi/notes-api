from sqlalchemy.orm import Mapped, mapped_column
from database import Base

class NoteModel(Base):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    content: Mapped[str]