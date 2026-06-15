from pydantic import BaseModel, Field, field_validator


class BookBase(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    author: str = Field(min_length=2)
    price: float = Field(gt=0)
    pages: int = Field(gt=0)
    description: str | None = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        cleaned_value = value.strip()
        if len(cleaned_value) < 3:
            raise ValueError("Title too short")
        return cleaned_value


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=3, max_length=100)
    author: str | None = Field(default=None, min_length=2)
    price: float | None = Field(default=None, gt=0)
    pages: int | None = Field(default=None, gt=0)
    description: str | None = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str | None) -> str | None:
        if value is None:
            return value

        cleaned_value = value.strip()
        if len(cleaned_value) < 3:
            raise ValueError("Title too short")
        return cleaned_value


class BookResponse(BookBase):
    id: int