from data.expenses import ALLOWED_CATEGORIES, ALLOWED_PAYMENT_METHODS
# HELPER FUNCTION
def validate_data(data):
    errors = {}

    # Required fields
    if "amount" not in data:
        errors["amount"] = "Amount is required"

    if "category" not in data:
        errors["category"] = "Category is required"

    if "payment_method" not in data:
        errors["payment_method"] = "Payment method is required"

    # Data type validation
    if "amount" in data:
        if not isinstance(data["amount"], (int, float)) or isinstance(data["amount"], bool):
            errors["amount"] = "Amount must be a number"

    if "category" in data:
        if not isinstance(data["category"], str):
            errors["category"] = "Category must be a string"

    if "payment_method" in data:
        if not isinstance(data["payment_method"], str):
            errors["payment_method"] = "Payment method must be a string"

    # Amount validation
    if "amount" in data and isinstance(data["amount"], (int, float)) and not isinstance(data["amount"], bool):
        if data["amount"] <= 0:
            errors["amount"] = "Amount must be greater than 0"

    # Category validation
    if "category" in data and isinstance(data["category"], str):
        if data["category"] not in ALLOWED_CATEGORIES:
            errors["category"] = "Invalid category"

    # Payment method validation
    if "payment_method" in data and isinstance(data["payment_method"], str):
        if data["payment_method"] not in ALLOWED_PAYMENT_METHODS:
            errors["payment_method"] = "Invalid payment method"

    # Optional note validation
    if "note" in data and data["note"] is not None:
        if not isinstance(data["note"], str):
            errors["note"] = "Note must be a string"
        elif len(data["note"]) > 200:
            errors["note"] = "Note must be 200 characters or less"

    return errors