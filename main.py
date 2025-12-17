import json
from agent import PaymentMethodAgent
from evaluator import evaluate
from memory import update_memory, load_memory

def run_demo():
    agent = PaymentMethodAgent()

    # Sample transaction context
    transaction_context = {
        "user": {
            "location": "India",
            "bank": "HDFC",
            "device": "Android"
        },
        "transaction": {
            "amount_inr": 1200,
            "currency": "INR",
            "time_of_day": "Evening"
        },
        "history": {
            "upi": {"success": 3, "failure": 0},
            "card": {"success": 1, "failure": 1},
            "wallet": {"success": 0, "failure": 0}
        }
    }

    print("\n=== Running Payment Method Recommendation ===\n")

    recommendation = agent.recommend(transaction_context)

    print("Agent Recommendation:")
    print(json.dumps(recommendation, indent=2))

    # ---- Simulate real outcome ----
    actual_payment_method = "upi"      # simulate user choice
    transaction_success = True          # simulate success/failure

    print("\n=== Simulating Payment Outcome ===\n")
    print(f"Actual Method Used: {actual_payment_method}")
    print(f"Transaction Success: {transaction_success}")

    # Update memory
    update_memory(actual_payment_method, transaction_success)

    # Evaluate prediction
    evaluation = evaluate(
        predicted=recommendation["primary_method"],
        actual=actual_payment_method
    )

    print("\n=== Evaluation Result ===\n")
    print(json.dumps(evaluation, indent=2))

    print("\n=== Updated Agent Memory ===\n")
    print(json.dumps(load_memory(), indent=2))


if __name__ == "__main__":
    run_demo()
