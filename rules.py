def apply_rules(context: dict):
    allowed_methods = ["upi", "card", "wallet"]

    amount = context["transaction"]["amount_inr"]

    # Example rule: wallet not allowed for high amount
    if amount > 5000 and "wallet" in allowed_methods:
        allowed_methods.remove("wallet")

    return allowed_methods
