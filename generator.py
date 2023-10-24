import os 
import openai
import json
from dotenv import load_dotenv
from error import AppError


load_dotenv()
config = json.load(open('config.json'))

# getting api_key
if os.getenv("OPENAI_API_KEY"):
    openai.api_key = os.getenv("OPENAI_API_KEY")
else:
    openai.api_key = config["api_key"]


def generate_dictionary(words):


    prompt = f"""Given this list of words below, return a json containing words as keys and single line definitions as values.
    Make sure to wrap all elements inside JSON with double quotes. 
    If there is a typo, replace the word with closest candidate and give definition of replaced word. 
    If a word is not recognizable at all, give a definition of 'Unknown':\n{words}"""
    
    print("getting response from openai...")
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0,
        max_tokens=config['max_tokens'],
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.0,)
    
    print(response.usage)

    # convert json to dictionary containing word-definition pairs
    json_dict = response.choices[0].text
    dictionary = json.loads(json_dict)
    print("successfully got a response!!")

    return dictionary

