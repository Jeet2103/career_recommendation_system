"""
# Brainwonders Assignment - Career Recommendation via LLMs

## Objective:
Extract user preferences, map them to career domains, and generate dynamic explanations using LLMs.

## Codebase Structure 

```
brainwonders_assignment/
├── extract_preferences.py     # Prompt template + LLM Chain
├── map_to_career.py           # LLM based mapping
├── explain_recommendation.py  # LLM prompt for explanations
├── fallback_handling.py       # Clarification prompts
├── main_flow.py               # Complete integrated pipeline
├── requirements.txt           # List OpenAI, LangChain, FAISS, etc.

```

## Tech Stack:
- Python
- OpenAI (GPT-4o Mini)
- LangChain
- FAISS (Vector similarity)
- NLTK (Stemming/Lemmatization)

## Features:
- Dynamic extraction of interests
- FAISS-based fuzzy matching for interest-to-career mapping
- Synonym expansion using GPT
- Personalized career explanations
- AI-generated fallback questions for ambiguous input

## Instructions:
1. Add your API key in a `.env` file:
   ```
   OPENAI_API_KEY=your-key-here
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run:
   ```bash
   python main_flow.py
   ```
4. Type your interests when prompted.
"""