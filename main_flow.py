# Import core pipeline components
from extract_preferences import get_preferences_chain
from map_to_career import map_interest_to_career
from explain_recommendation import get_explanation_chain
from fallback_handling import check_for_fallback

# Import your logger class
from logger_config.logger import get_logger

# Initialize logger
logger = get_logger(__name__)

def run_pipeline(user_input):
    """
    Full pipeline to process user input:
    1. Extract preferences
    2. Map interests to careers
    3. Generate career explanations
    4. Handle fallback if input is unclear
    """
    try:
        logger.info("Pipeline started with user input: %s", user_input)

        # Step 1: Extract preferences using LLM
        extract_chain = get_preferences_chain()
        logger.info("Preference extraction chain initialized.")

        raw_response = extract_chain.invoke(user_input)
        logger.info("Raw response from preference extraction: %s", raw_response)

        # Ensure we get clean string content from the response
        response_content = raw_response.content.strip() if hasattr(raw_response, "content") else str(raw_response).strip()
        interests = [x.strip() for x in response_content.split(',') if x.strip()]
        logger.info("Extracted interests: %s", interests)

        # Step 2: Check if fallback is needed due to uncertain mapping
        fallback_needed, fallback_prompt = check_for_fallback(interests, user_input)
        if fallback_needed:
            logger.warning("Fallback triggered due to ambiguous interests.")
            return f"Clarification Needed:\n{fallback_prompt}"

        # Step 3: Map extracted interests to career fields
        career_fields = map_interest_to_career(interests)
        logger.info("Mapped career fields: %s", career_fields)

        # Step 4: Generate explanations for each career path
        explanation_chain = get_explanation_chain()
        logger.info("Explanation chain initialized.")

        results = []

        for career in career_fields:
            prompt_vars = {
                "interest": ", ".join(interests),
                "career": career
            }

            logger.info("Generating explanation for: %s", prompt_vars)

            explanation_response = explanation_chain.invoke(prompt_vars)
            explanation_text = explanation_response.content.strip() if hasattr(explanation_response, "content") else str(explanation_response).strip()

            logger.info("Generated explanation: %s", explanation_text)

            results.append(f"Career Path: {career}\nExplanation: {explanation_text}\n")

        logger.info("Pipeline completed successfully.")
        return "\n".join(results)

    except Exception as e:
        logger.error("Error in pipeline execution: %s", e)
        return "An unexpected error occurred while processing your request. Please try again later."


# CLI entry point for standalone execution
if __name__ == "__main__":
    try:
        logger.info("Starting CLI execution of career recommendation pipeline.")
        user_text = input("Describe your interests: ")
        output = run_pipeline(user_text)

        print("\nRecommendations:\n")
        print(output)
        logger.info("CLI execution completed successfully.")

    except Exception as e:
        logger.error("Error in CLI execution: %s", e)
        print("An error occurred during execution. Check logs for details.")
