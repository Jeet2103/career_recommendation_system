# Import required libraries
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
import os
# from dotenv import load_dotenv
import streamlit as st

# Import your custom logger
from logger_config.logger import get_logger

# Load environment variables from .env file
# load_dotenv()

# Initialize logger
logger = get_logger(__name__)


def get_fallback_chain():
    """
    Returns an LLMChain that generates a follow-up question when user input is ambiguous or unclear.
    """
    try:
        logger.info("Creating fallback prompt template...")

        # Define a polite and short follow-up question prompt
        prompt = PromptTemplate(
            input_variables=["context"],
            template="""
            The user input was unclear or ambiguous: "{context}".
            Ask a follow-up question to get a clearer understanding of the user's interests.
            Keep it short, polite, and specific.
            """
        )
        logger.info("PromptTemplate for fallback question created successfully.")

        # Initialize ChatOpenAI LLM with gpt-4o-mini
        llm = ChatOpenAI(
            model_name="gpt-4o-mini",
            temperature=0.5,
            # openai_api_key=os.getenv("OPENAI_API_KEY")
            openai_api_key = st.secrets["OPENAI_API_KEY"]
        )
        logger.info("ChatOpenAI LLM initialized for fallback chain.")

        # Create and return the LLMChain
        chain = LLMChain(llm=llm, prompt=prompt)
        logger.info("Fallback LLMChain created successfully.")
        return chain

    except Exception as e:
        logger.error(f"Error in creating fallback chain: {e}")
        raise


def check_for_fallback(interests, original_input):
    """
    Checks if a fallback is needed (i.e., interest mapping failed),
    and if so, generates a clarifying follow-up question using the fallback chain.
    
    Args:
        interests (List[str]): List of mapped career fields or ["Uncertain"]
        original_input (str): Original user text input
    
    Returns:
        Tuple[bool, str or None]: (True, question) if fallback needed, else (False, None)
    """
    try:
        logger.info(f"Checking for fallback condition with interests: {interests}")

        # If interests are empty or just "Uncertain", trigger fallback
        if not interests or interests == ["Uncertain"]:
            logger.info("Fallback required. Generating follow-up question...")

            # Get the fallback chain and run it
            chain = get_fallback_chain()
            question = chain.run({"context": original_input})

            logger.info(f"Generated follow-up question: {question.strip()}")
            return True, question.strip()

        # No fallback needed
        logger.info("Fallback not required. Interest mapping seems valid.")
        return False, None

    except Exception as e:
        logger.error(f"Error during fallback check: {e}")
        return True, "Could you please clarify your interests a bit more?"
