# Career Recommendation via LLMs

## Objective:
This project leverages Large Language Models (LLMs) to analyze a user’s interests and recommend relevant career paths with intelligent, personalized explanations. It combines prompt engineering, fuzzy semantic matching, and fallback clarification to handle ambiguity and guide users towards fulfilling career decisions through AI-driven insights.


## Tech Stack:
- LLMs & API(`GPT-4o-mini`)
- LLM Framework	(`LangChain`)
- Environment	(`Python 3.10+`, `Conda`, `.env` for secrets)
- Logging	(Custom `get_logger` class (in `logger_config/logger.py`))

## Features:

- **Interest Extraction via LLMs:**

    - Uses few-shot prompting with GPT-4o Mini to extract generalized interests from free-form user input.
    - Automatically normalizes niche activities into broader terms
    (e.g., "`sketching portraits`" → "`drawing`").

- **Interest-to-Career Mapping via LLMs:**
    - Maps each extracted interest to a relevant career domain using LLM-driven logic and predefined mapping.
    - Utilizes a carefully crafted prompt template with examples and rules (e.g., duplication, synonym resolution, fallback to "`Uncertain`").
    - Supports one-to-one or one-to-many mappings with natural language understanding rather than keyword-only rules.

- **Career Explanation Generation:**

    - Dynamically generates individual career explanations for each matched interest using LLM.
    - Descriptions are contextual and personalized, avoiding repetition or overlap between different career paths.
    - E.g., a "drawing" explanation will focus solely on art-related fields without referencing "math" or other unrelated areas.

- **Fallback Questioning for Uncertainty:**

    - For ambiguous, unclear, or very short inputs, a clarification question is generated using GPT.
    - This fallback mechanism ensures meaningful user input before initiating the mapping process.
    - Enhances recommendation accuracy and reduces LLM misfires.

## Codebase Structure 

```
brainwonders_assignment/
├── extract_preferences.py     # Extract structured interests using GPT
├── map_to_career.py           # Interest-to-career mapping (LLM + FAISS)
├── explain_recommendation.py  # Career explanation generator (per interest)
├── fallback_handling.py       # GPT fallback questions for ambiguous input
├── main_flow.py               # Main execution pipeline
├── logger_config/logger.py    # Contains get_logger class
├── requirements.txt           # Python dependencies
├── .env                       # API keys and secrets



```


## Setup Instructions:

###  Step 1: Clone the Repository
```
git clone  https://github.com/Jeet2103/career_recommendation_system.git
cd career_recommendation_system

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

    - Extract structured interests.

    - Fallback Message system.

    - Map them to suitable career paths.

    - Provide individual explanations per career.

Maintained by **Jeet Nandigrami**  
- GitHub: [Jeet2103](https://github.com/Jeet2103)  
- LinkedIn: [Jeet Nandigrami](https://www.linkedin.com/in/jeet-nandigrami/)
- Resume : [RESUME](https://drive.google.com/file/d/1Zvm0yAK--t_K-lNBpLnDFA2Lz41ZBqvX/view?usp=sharing)
