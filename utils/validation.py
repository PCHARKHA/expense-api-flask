from data.expenses import ALLOWED_CATEGORIES, ALLOWED_PAYMENT_METHODS
#HELPER FUNCTION
def validate_data(data):
     # Check required fields
    if "amount" not in data or "category" not in data or "payment_method" not in data:
        return "Amount,category and payment method are required"

    #Validate amount
    if not isinstance(data["amount"], (int, float)) or data["amount"] <= 0:
        return "Amount must be positive"
    
    #Validate category
    if data["category"] not in  ALLOWED_CATEGORIES:
        return "Category doesn't match"
    
    # Validate payment method
    if data["payment_method"] not in ALLOWED_PAYMENT_METHODS:
        return "Invalid payment method"
    
    return None
     