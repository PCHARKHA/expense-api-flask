from pydantic import BaseModel,Field,field_validator
from data.expenses import ALLOWED_CATEGORIES,ALLOWED_PAYMENT_METHODS
class Expense(BaseModel):
    amount: float = Field(gt=0,le=100000)
    category: str = Field(min_length=2,max_length=30)
    payment_method: str = Field(min_length=2,max_length=30)
    note: str | None = Field(default=None,max_length=200)

    # @field_validator("amount")
    # @classmethod
    # def validate_amount(cls, value):
    #     if value <= 0:
    #         raise ValueError("Amount must be greater than 0")
    #     return value

    @field_validator("category")
    @classmethod
    def validate_category(cls, value):
        if value not in ALLOWED_CATEGORIES:
            raise ValueError("Invalid category")
        return value
    
    @field_validator("payment_method")
    @classmethod
    def validate_payment_method(cls, value):
        if value not in ALLOWED_PAYMENT_METHODS:
            raise ValueError("Invalid payment method")
        return value

    @field_validator("note")
    @classmethod
    def validate_note(cls, value):
        if value is not None and not value.strip():
            raise ValueError("Note cannot contain only spaces")
        return value
    

