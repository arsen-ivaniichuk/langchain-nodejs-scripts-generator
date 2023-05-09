import os
import re
import json
from langchain.llms import OpenAI
from langchain.prompts import StringPromptTemplate
from pydantic import BaseModel, validator
from constants import OPENAI_API_KEY
from utils import ValidationError, save_script

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY


class GenerateScriptPromptTemplate(StringPromptTemplate, BaseModel):
    """
    Prompt generator
    """
    @validator("input_variables")
    def validate_input(cls, variables):
        """
        Input validator
        """
        if not variables or "description" not in variables:
            raise ValueError("Inconsistent input variables!")

        return variables

    def format(self, **kwargs) -> str:
        prompt = f"""Write a Node.js script, which will satisfy the following conditions:
        1. Script must contain a function or a set of functions, which must fulfill the task given
        in the description;
        2. If the task is to perform arithmetical calculations, ensure converting input variables  
        to numeric data type;
        3. Script must contain one more function named 'test', which will accept 
        any given parameters and will run the previously described functions with 
        those parameters. The result must be logged in console;
        4. The script must contain nothing, but the comments and functions, described above.
        Do not generate any examples of usage 

        Description: {kwargs["description"]}
        """

        return prompt

    @property
    def _prompt_type(self) -> str:
        return "script-generator"


class ValidateScriptPromptTemplate(StringPromptTemplate, BaseModel):
    """
    Prompt generator for script validation
    """
    @validator("input_variables")
    def validate_input(cls, variables):
        """
        Input validator
        """
        if not variables or "script" not in variables:
            raise ValueError("Inconsistent input variables!")

        return variables

    def format(self, **kwargs) -> str:
        prompt = f"""Given a Node.js script and a desscription, make a conclusion
                whether the script correctly performs the task geiven in the description.
                Follow the instructions below:
                1. Your conclusion must be '1' if the script works as expected and '0' if not;
                2. Your response must be fromatted as a valid JSON with the "answer" key and your conclusion.
                3. Use double quoting;
                4. Anything except the JSON described above must not be included in your response;
                Description: {kwargs["description"]};
                Script: {kwargs["script"]}
                """

        return prompt

    @property
    def _prompt_type(self) -> str:
        return "script-validator"


class ScriptGenerator:
    """
    A class for generating and validating Node.js scripts that fulfill given tasks.

    This class uses the OpenAI GPT language model to generate code based on user-provided prompts. The generated code
    is then validated using the same language model to ensure that it meets the requirements of the prompt.

    To use this class, instantiate it with the appropriate OpenAI API credentials, then call the `run` method with a
    user-provided prompt to generate and validate a script. The resulting script is saved to the file system and the
    ID of the saved script is returned.

    Attributes:
        llm: An instance of the OpenAI Language model used for generating and validating code.
        generator_prompt_formatter: A string formatter for generating the prompt used to generate code.
        validator_prompt_formatter: A string formatter for generating the prompt used to validate generated code.
    """
    def __init__(self):
        self.llm = OpenAI(temperature=0)
        self.generator_prompt_formatter = GenerateScriptPromptTemplate(input_variables=["description"])
        self.validator_prompt_formatter = ValidateScriptPromptTemplate(input_variables=["description", "script"])

    def generate_response(self, **kwargs) -> str:
        """
        Generates a node.js script that fulfills the task described in the prompt.

        :param kwargs: a dictionary of keyword arguments including:
            - description (str): the prompt description
        :return: a string containing the generated node.js script
        """
        prompt = self.generator_prompt_formatter.format(description=kwargs["description"])
        response = self.llm(prompt)

        return response

    def validate_response(self, **kwargs) -> str:
        """
        Validates the previously generated node.js script using the LLM.

        :param kwargs: a dictionary of keyword arguments including:
            - description (str): the prompt description
            - script (str): the generated node.js script to validate
        :return: a string containing the validation conclusion in JSON format
        """
        prompt = self.validator_prompt_formatter.format(description=kwargs["description"], script=kwargs["script"])
        response = self.llm(prompt)
        conclusion = re.search("(\{.+})", response).group(1)

        return conclusion

    def run(self, user_prompt: str) -> str:
        """
        Generates a Node.js script that fulfills the task described in the prompt,
        validates the script, saves it to the file system, and returns the ID of the script.

        :param user_prompt: the prompt for the task
        :return: the ID of the generated script
        """
        script = self.generate_response(description=user_prompt)
        validator_conclusion = self.validate_response(description=user_prompt, script=script)
        validator_conclusion = json.loads(validator_conclusion)

        if not validator_conclusion["answer"]:
            raise ValidationError(user_prompt)

        # Save the script to the file system
        script_id = save_script(script)

        return script_id
