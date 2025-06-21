# Import necessary libraries for prompt chaining and environment setup
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
import streamlit as st

# Import your custom logger class from the logger_config folder
from logger_config.logger import get_logger

# Load environment variables from the .env file
load_dotenv()

# Initialize logger
logger = get_logger(__name__)

def get_explanation_chain():
    """
    Creates a LangChain chain that explains why a particular career is suitable
    based on a given interest using an OpenAI LLM.
    """
    try:
        logger.info("Initializing PromptTemplate for career explanation...")

        # Define the prompt template that accepts 'interest' and 'career' as inputs
        prompt = PromptTemplate(
            input_variables=["interest", "career"],
            template="""
            The user has shown interest in {interest}.
            Explain in 2-3 lines why a career in {career} is a suitable path for someone interested in {interest}.
            Only use information relevant to the given interest and career. 
            Do not reference any other unrelated interests.
            """
        )
        logger.info("PromptTemplate created successfully.")

        # Instantiate the OpenAI language model with desired parameters
        llm = ChatOpenAI(
            model_name="gpt-4o-mini",           # Using GPT-4o mini model
            temperature=0.6,                    # Medium creativity for variation in explanations
            openai_api_key=os.getenv("OPENAI_API_KEY")  # Load API key from environment
            # openai_api_key = st.secrets["OPENAI_API_KEY"]
        )
        logger.info("ChatOpenAI LLM initialized with model gpt-4o-mini.")

        # Pipe the prompt template to the LLM to create a chain
        chain = prompt | llm
        logger.info("Prompt successfully chained with LLM.")

        return chain

    except Exception as e:
        logger.error(f"Error while creating explanation chain: {e}")
        raise  # Re-raise exception for higher-level handling if needed


# Optional main block for testing
if __name__ == "__main__":
    try:
        logger.info("Testing explanation chain with sample input...")

        chain = get_explanation_chain()

        # Example input
        input_data = {
            "interest": "drawing",
            "career": "Graphic Design"
        }

        # Run the chain with input
        response = chain.invoke(input_data)

        # Print and log result
        print("Explanation:", response.content.strip())
        logger.info(f"Generated Explanation: {response.content.strip()}")

    except Exception as e:
        logger.error(f"Error in main test block: {e}")
