import os
from typing import List, Dict
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableLambda

# Import your custom logger
from logger_config.logger import get_logger

# Load environment variables
load_dotenv()

# Initialize the logger
logger = get_logger(__name__)

# Base interest-to-career mapping dictionary
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
    "music": "Music Production",
    "singing": "Music Production",
    "photography": "Photography",
    "videography": "Film Making",
    "fashion": "Fashion Design",
    "style": "Fashion Design",
    "history": "Archaeology",
    "past": "Archaeology",
    "animals": "Veterinary Science",
    "pets": "Veterinary Science"
}


def format_mapping(mapping: Dict[str, str]) -> str:
    """
    Reverses the mapping from interest-to-career to career-to-interests for prompt formatting.
    """
    logger.info("Formatting career field mapping from base dictionary...")
    reverse = {}
    try:
        for k, v in mapping.items():
            reverse.setdefault(v, []).append(k)
        formatted = "\n".join(f"- {v}: {', '.join(list(set(ks)))}" for v, ks in reverse.items())
        logger.info("Mapping formatted successfully.")
        return formatted
    except Exception as e:
        logger.error(f"Error formatting mapping: {e}")
        raise


# Define the prompt template used by the LLM
prompt_template = PromptTemplate.from_template("""
You are a career mapping assistant.

Given a list of interests, map each to one or more career fields using the predefined mappings below.

Rules:
- Resolve synonyms (e.g., "sketching" → "drawing" → "Fine Arts")
- Use the closest career field from the list.
- Avoid duplicates.
- If unsure, use "Uncertain".

Career Field Mapping:
{career_mapping}

Examples:
User Interests: ["drawing", "painting", "coding"]
Career Fields: ["Graphic Design", "Fine Arts", "Software Engineering"]

User Interests: ["volunteering", "helping", "teamwork"]
Career Fields: ["Social Work", "Human Resources"]

User Interests: ["robots", "math", "programming"]
Career Fields: ["Robotics Engineering", "Data Science", "Software Engineering"]

Now map the following:
User Interests: {user_interests}
Career Fields:
""")


def map_interests_with_llm(interests: List[str]) -> List[str]:
    """
    Uses an LLM to map user interests to career fields based on predefined mappings.
    """
    logger.info(f"Received user interests: {interests}")
    try:
        formatted_map = format_mapping(base_mapping)

        # Initialize the LLM with chosen model
        llm = ChatOpenAI(
            model="gpt-4o",
            temperature=0.2,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        logger.info("ChatOpenAI model initialized.")

        # Chain the prompt with the LLM
        chain = prompt_template | llm
        logger.info("Prompt chained with LLM.")

        # Generate response
        response = chain.invoke({"career_mapping": formatted_map, "user_interests": interests})
        logger.info(f"LLM response received: {response.content.strip()}")

        # Try to extract from structured list format
        text = response.content.strip()
        if "[" in text and "]" in text:
            try:
                extracted = eval(text[text.index("["):text.index("]")+1])
                result = [item.strip(' "\'') for item in extracted]
                logger.info(f"Extracted structured career fields: {result}")
                return result
            except Exception as e:
                logger.warning(f"Fallback to manual parsing due to eval error: {e}")

        # Fallback: manually extract lines if structured format fails
        fields = []
        for line in text.splitlines():
            if ":" not in line and line.strip():  # Skip mappings or empty lines
                fields.extend([field.strip(' "\'') for field in line.split(",") if field.strip()])

        result = fields if fields else ["Uncertain"]
        logger.info(f"Final mapped career fields (fallback): {result}")
        return result

    except Exception as e:
        logger.error(f"Error during LLM mapping: {e}")
        return ["Uncertain"]


if __name__ == "__main__":
    try:
        logger.info("Running test cases for career mapping...")

        # Example user interest test cases
        test_cases = [
            ["drawing", "painting", "coding"],
            ["volunteering", "helping", "teamwork"],
            ["robots", "math", "programming"],
            ["fashion", "style", "photography"],
            ["unknown", "skydiving"]
        ]

        for i, interests in enumerate(test_cases):
            print(f"\nTest Case {i+1}")
            print("User Interests:", interests)
            logger.info(f"Test Case {i+1}: {interests}")
            careers = map_interests_with_llm(interests)
            print("Mapped Careers:", careers)
            logger.info(f"Mapped Careers: {careers}")

    except Exception as e:
        logger.error(f"Fatal error in main block: {e}")
