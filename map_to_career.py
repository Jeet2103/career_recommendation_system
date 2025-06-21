from typing import List, Dict
import os
import faiss
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from openai import OpenAI as OpenAIClient
from dotenv import load_dotenv
from logger_config.logger import get_logger
import ast  # for safe parsing of GPT responses
import streamlit as st

# Load environment variables and NLTK resources
load_dotenv()
nltk.download('wordnet')

# Initialize components
logger = get_logger(__name__)
lemmatizer = WordNetLemmatizer()
# openai_client = OpenAIClient(api_key=st.secrets["OPENAI_API_KEY"])
openai_client = OpenAIClient(api_key=os.getenv("OPENAI_API_KEY"))

# Define base interest-to-career mapping
base_mapping = {
    "coding": "Software Engineering",
    "programming": "Software Engineering",
    "robots": "Robotics Engineering",
    "robotics": "Robotics Engineering",
    "math": "Data Science",
    "statistics": "Data Science",
    "drawing": "Graphic Design",
    "painting": "Fine Arts",
    "sketching": "Fine Arts",
    "art": "Fine Arts",
    "animations": "Animation & VFX",
    "animation": "Animation & VFX",
    "cartoons": "Animation & VFX",
    "sports": "Athletics",
    "fitness": "Athletics",
    "teamwork": "Human Resources",
    "communication": "Public Relations",
    "helping": "Social Work",
    "volunteering": "Social Work",
    "writing": "Content Writing",
    "storytelling": "Screenwriting",
    "creative writing": "Creative Writing",
    "business": "Entrepreneurship",
    "entrepreneur": "Entrepreneurship",
    "nature": "Environmental Science",
    "environment": "Environmental Science",
    "machines": "Mechanical Engineering",
    "engineering": "Mechanical Engineering",
    "teaching": "Education",
    "mentoring": "Education",
    "Dancing": "Dancer",
    "music": "Music Production",
    "singing": "Music Production",
    "photography": "Photography",
    "videography": "Film Making",
    "fashion": "Fashion Design",
    "style": "Fashion Design",
    "history": "Archaeology",
    "past": "Archaeology",
    "animals": "Veterinary Science",
    "pets": "Veterinary Science",
    "cooking" : "Chef"
}

def get_embedding(text: str) -> np.ndarray:
    """Get text embedding using OpenAI."""
    try:
        response = openai_client.embeddings.create(
            model="text-embedding-3-small",
            input=[text]
        )
        return np.array(response.data[0].embedding, dtype=np.float32)
    except Exception as e:
        logger.error(f"Embedding generation failed for '{text}': {e}")
        return np.zeros(1536, dtype=np.float32)

def prepare_faiss_index(mapping: Dict[str, str]):
    """Build FAISS index from base mapping."""
    try:
        logger.info("Preparing FAISS index...")
        keys = list(mapping.keys())
        embeddings = [get_embedding(k) for k in keys]
        dimension = len(embeddings[0])
        index = faiss.IndexFlatL2(dimension)
        index.add(np.array(embeddings))
        logger.info("FAISS index built successfully.")
        return index, keys
    except Exception as e:
        logger.error(f"Failed to prepare FAISS index: {e}")
        raise

def expand_synonyms_with_gpt(keyword: str) -> List[str]:
    prompt = f"List 5 synonyms or related words for '{keyword}' in Python list format. Only return the list."

    try:
        logger.info(f"Requesting synonyms from GPT for: {keyword}")
        completion = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        raw = completion.choices[0].message.content.strip()

        # Clean the response
        if raw.startswith("```"):
            raw = raw.strip("`")  # remove ```python or ``` blocks
        if "=" in raw:
            raw = raw.split("=", 1)[-1].strip()  # get only the right-hand side list
        if raw.startswith("[") and raw.endswith("]"):
            synonyms = ast.literal_eval(raw)
            if isinstance(synonyms, list):
                return [str(s).strip() for s in synonyms]

        logger.warning(f"GPT response was not a valid list: {raw}")
        return []

    except Exception as e:
        logger.warning(f"Failed to fetch synonyms for '{keyword}': {e}")
        return []


def map_interest_to_career(interests: List[str]) -> List[str]:
    """Map user interests to career fields using FAISS and optional synonym expansion."""
    try:
        logger.info(f"Mapping user interests: {interests}")
        matched = set()

        for interest in interests:
            lemmatized = lemmatizer.lemmatize(interest.lower())
            logger.info(f"Interest '{interest}' lemmatized to '{lemmatized}'")

            emb = get_embedding(lemmatized)
            D, I = faiss_index.search(np.array([emb]), k=1)
            closest_keyword = faiss_keys[I[0][0]]
            logger.info(f"Best FAISS match for '{lemmatized}': {closest_keyword} -> {base_mapping[closest_keyword]}")
            matched.add(base_mapping[closest_keyword])

            for synonym in expand_synonyms_with_gpt(lemmatized):
                syn_lem = lemmatizer.lemmatize(synonym.lower())
                if syn_lem in base_mapping:
                    logger.info(f"Synonym '{syn_lem}' matched to {base_mapping[syn_lem]}")
                    matched.add(base_mapping[syn_lem])

        result = list(matched) if matched else ["Uncertain"]
        logger.info(f"Final mapped careers: {result}")
        return result

    except Exception as e:
        logger.error(f"Error during interest mapping: {e}")
        return ["Uncertain"]

# Build FAISS index once at startup
faiss_index, faiss_keys = prepare_faiss_index(base_mapping)

# Optional testing block
if __name__ == "__main__":
    sample_input = ["sketching", "math", "helping", "Drawing"]
    print("User Interests:", sample_input)
    careers = map_interest_to_career(sample_input)
    print("Mapped Careers:", careers)
