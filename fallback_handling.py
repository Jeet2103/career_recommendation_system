# fallback_handling.py

from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
import streamlit as st

# Import your custom logger
from logger_config.logger import get_logger

# Load environment variables
load_dotenv()

# Initialize logger
logger = get_logger(__name__)


def get_fallback_chain():
    """
    Returns a composed prompt | llm chain using LangChain's pipe syntax.
    """
    try:
        logger.info("Creating fallback prompt and LLM chain using | pipe...")

        prompt = PromptTemplate(
            input_variables=["context"],
            template="""
            The user input was unclear or ambiguous: "{context}".
            Ask a follow-up question to get a clearer understanding of the user's interests.
            Keep it short, polite, and specific.
            """
        )

        llm = ChatOpenAI(
            model_name="gpt-4o-mini",
            temperature=0.5,
            # openai_api_key=os.getenv("OPENAI_API_KEY")  # or st.secrets["OPENAI_API_KEY"]
            openai_api_key = st.secrets["OPENAI_API_KEY"]
        )

        chain = prompt | llm
        logger.info("Prompt | LLM chain created successfully.")
        return chain

    except Exception as e:
        logger.error(f"Error in creating fallback pipe chain: {e}")
        raise


def check_for_fallback(interests, original_input):
    """
    Checks if fallback is needed (i.e., no valid interests).
    If so, generates a polite follow-up question using prompt | llm chain.

    Args:
        interests (List[str] or str): Extracted interests
        original_input (str): Original user input

    Returns:
        Tuple[bool, str or None]: (True, question) if fallback needed, else (False, None)
    """
    try:
        logger.info(f"Checking fallback condition... Extracted interests: {interests}")

        # Normalize input
        if isinstance(interests, str):
            interests = interests.strip()
            if interests in ["[]", "['[]']", "['uncertain']", "uncertain"]:
                interests = []
            else:
                try:
                    interests = eval(interests)
                except:
                    interests = []

        # Fallback Conditions
        if not interests or \
           (len(interests) == 1 and str(interests[0]).strip().lower() in ["uncertain", "[]"]):
            logger.warning("Fallback triggered due to no valid interests.")

            # Get fallback chain and invoke
            fallback_chain = get_fallback_chain()
            response = fallback_chain.invoke({"context": original_input})

            # Extract the response text
            follow_up = response.content.strip() if hasattr(response, "content") else str(response).strip()

            logger.info(f"Generated fallback question: {follow_up}")
            return True, follow_up

        logger.info("Valid interests found — fallback not needed.")
        return False, None

    except Exception as e:
        logger.error(f"Fallback check failed: {e}")
        return True, "Could you please clarify your interests a bit more?"
