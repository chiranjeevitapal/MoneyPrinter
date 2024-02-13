import g4f
import json
import re
from termcolor import colored
from typing import Tuple, List


def generate_script(video_subject: str, max_video_duration: int) -> str:
    """
    Generate a script for a short video about parallel universes.

    Args:
        video_subject (str): The subject of the video.

    Returns:
        str: The script for the video.
    """

    # Build prompt
    prompt = f"""
    Generate a script for a short video about {video_subject} that could be read within {max_video_duration} minute.
    Provide engaging content exploring the topic concisely.
    
    YOU MUST ONLY RETURN A SINGLE PARAGRAPH WITHOUT ANY SPECIAL CHARACTERS or UNWANTED SPACES.

    Ensure the script is in a continuous paragraph style without any scene descriptions, character actions, or dialogue tags.
    """

    # Generate script with a maximum length for 1 minute duration
    max_words_per_minute = 150  # Assuming an average speaking rate of 150 words per minute
    max_script_length = max_words_per_minute  # Maximum words for 1 minute
    response = g4f.ChatCompletion.create(
        model=g4f.models.gpt_35_turbo_16k_0613,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_script_length  # Maximum tokens for GPT to generate
    )

    # Return the generated script
    if response:
        response = clean_script(response)
        print(colored(f"\nScript: {response}", "green"))
        return response
    print(colored("[-] GPT returned an empty response.", "red"))
    return None


def clean_script(script: str) -> str:
    """
    Clean the generated script by removing markdown syntax, special characters,
    and unwanted spaces between sentences.

    Args:
        script (str): The generated script.

    Returns:
        str: The cleaned script.
    """
    # Remove markdown syntax
    script = re.sub(r'\[.*?\]', '', script)
    script = re.sub(r'\(.*?\)', '', script)
    # Remove special characters and unwanted spaces between sentences
    script = re.sub(r'\s+', ' ', script)
    return script.strip()



def get_search_terms(video_subject: str, amount: int, script: str) -> List[str]:
    """
    Generate a JSON-Array of search terms for stock videos,
    depending on the subject and script of a video.

    Args:
        video_subject (str): The subject of the video.
        amount (int): The amount of search terms to generate.
        script (str): The script of the video.

    Returns:
        List[str]: The search terms for the video subject and script.
    """

    # Build prompt including the video subject and script
    prompt = f"""
    Generate {amount} search terms for stock videos,
    based on the subject and script of a 1-minute short video about {video_subject}.
    
    Script:
    {script}
    
    Each search term should consist of 1-3 words,
    always adding the main subject of the video.
    
    YOU MUST ONLY RETURN THE JSON-ARRAY OF STRINGS.
    YOU MUST NOT RETURN ANYTHING ELSE. 
    
    The search terms must be related to the subject and content of the video script.
    """

    # Generate search terms
    response = g4f.ChatCompletion.create(
        model=g4f.models.gpt_35_turbo_16k_0613,
        messages=[{"role": "user", "content": prompt}],
    )

    # Load response into JSON-Array
    try:
        search_terms = json.loads(response)
    except Exception:
        print(colored("[*] GPT returned an unformatted response. Attempting to clean...", "yellow"))

        # Use Regex to extract the array from the markdown
        search_terms = re.findall(r'\[.*\]', str(response))

        if not search_terms:
            print(colored("[-] Could not parse response.", "red"))

        # Load the array into a JSON-Array
        search_terms = json.loads(search_terms[0])

    # Let user know
    print(colored(f"\nGenerated {amount} search terms: {', '.join(search_terms)}", "cyan"))

    # Return search terms
    return search_terms


def generate_metadata(video_subject: str, script: str) -> Tuple[str, str, List[str]]:
    """
    Generate metadata for a YouTube video, including the title, description, and keywords.

    Args:
        video_subject (str): The subject of the video.
        script (str): The script of the video.

    Returns:
        Tuple[str, str, List[str]]: The title, description, and keywords for the video.
    """

    # Build prompt for title
    title_prompt = f"""  
    Generate a catchy and SEO-friendly title for a YouTube shorts video about {video_subject}.  
    """

    # Generate title
    title_response = g4f.ChatCompletion.create(
        model=g4f.models.gpt_35_turbo_16k_0613,
        messages=[{"role": "user", "content": title_prompt}],
    )

    # Extract title from response
    title = title_response.strip()  # Assuming title_response is a string

    # Build prompt for description
    description_prompt = f"""  
    Write a brief and engaging description for a YouTube shorts video about {video_subject}.  
    The video is based on the following script:  
    {script}  
    """

    # Generate description
    description_response = g4f.ChatCompletion.create(
        model=g4f.models.gpt_35_turbo_16k_0613,
        messages=[{"role": "user", "content": description_prompt}],
    )

    # Extract description from response
    description = description_response.strip()  # Assuming description_response is a string

    # Generate keywords
    keywords = get_search_terms(video_subject, 6, script)  # Assuming you want 6 keywords

    return title, description, keywords
