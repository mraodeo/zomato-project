# AI-Powered Restaurant Recommendation System (Zomato Use Case)

This project is a phase-wise implementation of a restaurant recommendation engine based on a Hugging Face Zomato dataset. It leverages LLMs for intelligent ranking and explanations based on user preferences.

## Prerequisites
- Python 3.10+
- An API key for your chosen LLM provider (Groq)

## Setup

1. **Clone the repository** (if not already done)
2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Configure environment**:
   Copy `.env.example` to `.env` and fill in your API key and preferred model.
   ```bash
   cp .env.example .env
   ```

## Running the Application

To smoke-test the Phase 1 setup, run:
```bash
python -m src.main
```

## Dataset Note
The application uses the `ManikaSaini/zomato-restaurant-recommendation` dataset from Hugging Face. The data will be downloaded and cached on the first run of the ingestion phase (Phase 2).
