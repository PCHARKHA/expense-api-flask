from data.expenses import ALLOWED_CATEGORIES
#HELPER FUNCTION
def validate_data(data):
     # Check required fields
    if "amount" not in data or "category" not in data:
        return "Amount and category are required"

    #Validate amount
    if not isinstance(data["amount"], (int, float)) or data["amount"] <= 0:
        return "Amount must be positive"
    
    #Validate category
    if data["category"] not in  ALLOWED_CATEGORIES:
        return "Category doesn't match"
    
    return None
     