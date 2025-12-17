# Payment Method Recommendation Agent 🤖💳

An intelligent AI-powered agent that recommends the optimal payment method (UPI, Card, or Wallet) for transactions based on context, historical success rates, and multi-agent debate reasoning using Large Language Models.

## 🌟 Features

- **AI-Powered Recommendations**: Uses Groq's Llama 3.3 70B model for intelligent decision-making
- **Multi-Agent Debate System**: Debate agents advocate for different payment methods (UPI, Card, Wallet)
- **Adaptive Learning**: Learns from transaction outcomes and updates its memory
- **Rule-Based Filtering**: Applies business rules to ensure recommended methods are appropriate
- **Context-Aware**: Considers user location, device, amount, time, and historical patterns
- **REST API**: FastAPI-based API for easy integration
- **Evaluation System**: Tracks prediction accuracy and learning progress
- **Persistent Memory**: Stores success/failure rates to improve future recommendations

## 🏗️ Architecture

```
┌─────────────┐
│   Client    │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────┐
│         FastAPI Server              │
│  ┌─────────────────────────────┐   │
│  │  PaymentMethodAgent         │   │
│  │                             │   │
│  │  ┌──────────────────────┐  │   │
│  │  │  Rules Engine        │  │   │
│  │  └──────────────────────┘  │   │
│  │                             │   │
│  │  ┌──────────────────────┐  │   │
│  │  │  Debate Agents       │  │   │
│  │  │  • UPI Agent         │  │   │
│  │  │  • Card Agent        │  │   │
│  │  │  • Wallet Agent      │  │   │
│  │  └──────────────────────┘  │   │
│  │                             │   │
│  │  ┌──────────────────────┐  │   │
│  │  │  Groq LLM            │  │   │
│  │  │  (Llama 3.3 70B)     │  │   │
│  │  └──────────────────────┘  │   │
│  │                             │   │
│  │  ┌──────────────────────┐  │   │
│  │  │  Memory System       │  │   │
│  │  └──────────────────────┘  │   │
│  └─────────────────────────────┘   │
└─────────────────────────────────────┘
```

## 📋 Prerequisites

- Python 3.8+
- Groq API Key ([Get one here](https://console.groq.com))

## 🚀 Installation

1. **Clone the repository**:
```bash
git clone <repository-url>
cd payment-method-agent
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**:
Create a `.env` file in the project root:
```env
GROQ_API_KEY=your_groq_api_key_here
```

## 💻 Usage

### Running the Demo

Run the demo script to see the agent in action:

```bash
python main.py
```

This will:
1. Create a sample transaction context
2. Get a payment method recommendation
3. Simulate a payment outcome
4. Evaluate the prediction
5. Update the agent's memory

### Starting the API Server

Launch the FastAPI server:

```bash
uvicorn api:app --reload
```

The API will be available at `http://localhost:8000`

Visit `http://localhost:8000/docs` for interactive API documentation.

## 📡 API Endpoints

### POST /recommend

Get a payment method recommendation.

**Request Body**:
```json
{
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
```

**Response**:
```json
{
  "primary_method": "upi",
  "fallback_method": "card",
  "confidence": 0.85,
  "explanation": "UPI has highest success rate for this amount range and device type..."
}
```

### POST /feedback

Provide feedback on transaction outcome to improve the agent's learning.

**Request Body**:
```json
{
  "method": "upi",
  "success": true
}
```

**Response**:
```json
{
  "status": "memory updated"
}
```

## 📁 Project Structure

```
payment-method-agent/
├── agent.py              # Main payment recommendation agent
├── api.py                # FastAPI REST API
├── config.py             # Configuration and environment variables
├── debate_agents.py      # Multi-agent debate system
├── evaluator.py          # Prediction evaluation logic
├── main.py               # Demo/testing script
├── memory.py             # Persistent memory management
├── rules.py              # Business rules engine
├── tools.py              # Utility functions (success rates, etc.)
├── requirements.txt      # Python dependencies
├── agent_memory.json     # Persistent memory storage (auto-generated)
└── README.md            # This file
```

## 🧠 How It Works

1. **Context Collection**: The agent receives transaction context including user details, transaction amount, device, location, and historical data.

2. **Rule Application**: Business rules are applied to filter out inappropriate payment methods (e.g., wallets for high-value transactions).

3. **Debate Phase**: Each payment method agent (UPI, Card, Wallet) provides arguments for their method.

4. **LLM Decision**: The main agent uses Groq's Llama 3.3 70B model to analyze:
   - Global success rates
   - User's historical performance
   - Debate arguments
   - Transaction context
   - Applied rules

5. **Recommendation**: Returns a primary method, fallback method, confidence score, and explanation.

6. **Learning**: After transaction completion, feedback updates the agent's memory for future improvements.

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GROQ_API_KEY` | Your Groq API key | Required |

### Model Configuration

Edit [`config.py`](config.py:7) to change the LLM model:

```python
MODEL_NAME = "llama-3.3-70b-versatile"  # Default
```

### Business Rules

Customize rules in [`rules.py`](rules.py:1) to match your business logic:

```python
def apply_rules(context: dict):
    allowed_methods = ["upi", "card", "wallet"]
    amount = context["transaction"]["amount_inr"]
    
    # Example: wallet not allowed for amounts > 5000 INR
    if amount > 5000 and "wallet" in allowed_methods:
        allowed_methods.remove("wallet")
    
    return allowed_methods
```

### Global Success Rates

Update success rates in [`tools.py`](tools.py:1):

```python
def get_global_success_rates():
    return {
        "upi": 0.92,
        "card": 0.85,
        "wallet": 0.78
    }
```

## 📊 Example Scenarios

### High-Value Transaction
```python
context = {
    "transaction": {"amount_inr": 15000},
    # ... other fields
}
# Likely recommends: Card (wallet excluded by rules)
```

### Low-Value with Good UPI History
```python
context = {
    "transaction": {"amount_inr": 500},
    "history": {
        "upi": {"success": 10, "failure": 0}
    }
}
# Likely recommends: UPI
```

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 📧 Contact

For questions or feedback, please open an issue on GitHub.

---

**Made with ❤️ for better payment experiences**
