# preferences_extractor.py

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv
import os
import streamlit as st

# Import your custom logger
from logger_config.logger import get_logger

# Initialize environment variables
load_dotenv()

# Initialize logger
logger = get_logger(__name__)


def get_preferences_chain():
    """
    Creates and returns a LangChain LLMChain that extracts interests from user input using an LLM.
    """
    try:
        logger.info("Initializing preference extraction chain...")

        # Define the prompt template with instructions and few-shot examples
        prompt = PromptTemplate(
            input_variables=["user_input"],
            template="""
                You are an intelligent AI assistant that helps extract a user's core interests from free-form text. 
                The user may describe their hobbies, personality traits, or passions. 
                Your task is to generalize and clean this input into a short, comma-separated list of interests.

                Guidelines:
                - Extract only meaningful interests or activities.
                - Do not include emotions or traits like "happy" or "curious" unless they relate to a domain (e.g., curiosity in science).
                - Generalize similar words (e.g., "painting, sketching, drawing" → "drawing").
                - Avoid duplicates and keep the result simple and domain-relevant.
                - Only return a valid Python list of lowercase strings (e.g., ["drawing", "animation"]).
                - No extra text, explanations, or prefixes.
                - If no valid interest is found, return an empty list: []

                Examples:

                User: I enjoy playing football and cricket, and I love watching matches.
                Interests: football, cricket, sports

                User: I like to sketch portraits, paint scenery, and illustrate comics.
                Interests: drawing, illustration, painting

                User: I'm fascinated by space and solving complex math problems.
                Interests: astronomy, mathematics

                User: I love creating digital art and 2D animations.
                Interests: digital art, animation

                User: I spend time volunteering, helping kids, and working in community projects.
                Interests: volunteering, social work, community service

                User: I'm curious and happy.
                []

                Now, extract the interests based on the user's input below.

                User: {user_input}
            """
        )
        logger.info("Prompt template created successfully.")

        # Initialize the LLM (OpenAI model with temperature setting)
        llm = ChatOpenAI(
            model_name="gpt-4o-mini", 
            temperature=0.4, 
            # openai_api_key = st.secrets["OPENAI_API_KEY"]
            api_key = os.getenv("OPENAI_API_KEY")
        )
        logger.info("LLM initialized with gpt-4o-mini.")

        # Create the chain using the prompt and model
        chain = prompt | llm
        logger.info("LLMChain created successfully.")
        return chain

    except Exception as e:
        logger.error(f"Error initializing preference extraction chain: {e}")
        raise


if __name__ == "__main__":
    try:
        logger.info("Running main execution block...")

        # Initialize the chain
        chain = get_preferences_chain()

        # Example user input
        input_text = "I am "
        logger.info(f"User input received: {input_text}")

        # Get response from the chain
        response = chain.invoke(input_text)
        logger.info(f"LLM Response: {response}")

        # Print the extracted interests
        print(response)

    except Exception as e:
        logger.error(f"Error in main execution block: {e}")
