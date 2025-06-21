# Career Recommendation via LLMs

## Objective:
This project leverages Large Language Models (LLMs) to analyze a user’s interests and recommend relevant career paths with intelligent, personalized explanations. It combines prompt engineering, fuzzy semantic matching, and fallback clarification to handle ambiguity and guide users towards fulfilling career decisions through AI-driven insights.

---

## Live Demo

[Try the Live App on Streamlit Cloud](https://careerrecommendationsystem1.streamlit.app/) 

---


## Tech Stack

| Component                | Technology Used                     |
|--------------------------|-------------------------------------|
| LLM Backend              | OpenAI GPT-4o-mini                  |
| LLM Framework            | LangChain                           |
| Backend Language         | Python 3.10+                        |
| Environment Management   | Conda / venv + `.env` for secrets   |
| Logging                  | Custom logger via `logger_config`   |
| Frontend UI              | Streamlit                           |

---

## Approach

### 1. **Interest Extraction with GPT-4o**
- Extracts clean, generalized interests from unstructured user input.
- Uses few-shot learning with carefully crafted prompts.
- Normalizes similar expressions (e.g., “painting, sketching” → “drawing”).

### 2. **Interest-to-Career Mapping**
- Maps user interests to specific career domains using FAISS similarity + GPT prompting.
- Handles synonyms, ambiguity, and missing cases using LLM flexibility.
- Returns `"Uncertain"` when no confident match is found.

### 3. **Fallback Clarification for Ambiguity**
- If interests can't be determined or input is vague (e.g., "I’m good at things"), the system generates a clarifying follow-up question using GPT.
- Prevents poor mappings due to unclear user input.

### 4. **Career Explanation Generation**
- For each matched career path, GPT generates a customized explanation specific to the user’s interests.
- Eliminates repetition and aligns content to that interest (e.g., drawing → “graphic design” without discussing unrelated fields).

### 5. **Streamlit-Based Interactive UI**
- Users enter their interests into a text box with a sleek, dark-themed UI.
- Recommendations appear as modern, bordered cards with personalized feedback.
- Includes fallback messaging directly in the UI if needed.
- Background image and theme enhance user experience.

---
## Codebase Structure 

```
career_recommendation_system/
├── app.py                          # Streamlit front-end UI
├── main_flow.py                    # Main pipeline execution logic
├── extract_preferences.py          # Interest extraction using GPT
├── map_to_career.py                # Maps interests to career domains
├── explain_recommendation.py       # Career explanation generator
├── fallback_handling.py            # Fallback questions via GPT
├── logger_config/
│ └── logger.py                     # Custom logging utility
├── requirements.txt                # Project dependencies
├── .env                            # API key and secrets
└── README.md                       # Project documentation



```

---

## Setup Instructions:

###  Step 1: Clone the Repository
```
git clone  https://github.com/Jeet2103/Brainwonders_assignment.git
cd Brainwonders_assignment

```

### Step 2: Create a Virtual Environment
You can use either  `venv` or `conda`.

- Using Python `venv` (recommended for simplicity)
```
python -m venv env
source env/bin/activate      # For Linux/macOS
env\Scripts\activate         # For Windows

```
- Using `conda`
```
conda create -n brainwonders_env python=3.10 -y
conda activate brainwonders_env

```

### Step 3: Install Dependencies
```
pip install -r requirements.txt

```

###  Step 4: Configure Environment Variables
Create a   `.env` file in the root directory and add your OpenAI key:
```
OPENAI_API_KEY=your-openai-api-key-here

```

###  Step 5: Run the Application

```
python main_flow.py

```
You'll be prompted to enter your interests like:
```
Describe your interests: I love sketching, playing cricket and solving math puzzles.

```

- The system will:

    - Extract interests

    - Trigger fallback questions if input is unclear

    - Map interests to careers

    - Generate personalized explanations

### Step 6: Run the Streamlit App (Recommended)
To launch the interactive UI:
```
streamlit run app.py

```

- This will open a browser where you can:

    - Enter your interests in natural language

    - View personalized career recommendations with detailed insights

    - Get follow-up questions if input is unclear

---

Maintained by **Jeet Nandigrami**  
- GitHub: [Jeet2103](https://github.com/Jeet2103)  
- LinkedIn: [Jeet Nandigrami](https://www.linkedin.com/in/jeet-nandigrami/)
- Resume : [RESUME](https://drive.google.com/file/d/1Zvm0yAK--t_K-lNBpLnDFA2Lz41ZBqvX/view?usp=sharing)
