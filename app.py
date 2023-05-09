import os
import subprocess
from flask import Flask
from flask_restful import Resource, Api, reqparse

from models.llm import ScriptGenerator
from constants import SCRIPTS_PATH

app = Flask(__name__)
api = Api(app)

# Request parser for script generator
generator_parser = reqparse.RequestParser()
generator_parser.add_argument("description", type=str, required=True, help="Enter the prompt!")

# Request parser for script runner
runner_parser = reqparse.RequestParser()
runner_parser.add_argument("script_id", type=str, required=True, help="Provide a script id to run the script")
runner_parser.add_argument("parameters", required=True, help="Provide parameters for the script", action="append")


class GeneratorBot(Resource):
    """
    This class represents an API endpoint for generating and saving node.js scripts based on the prompt
    received in a POST request. It uses the ScriptGenerator object to generate and validate the script.
    """
    def __init__(self):
        self.generator: ScriptGenerator = ScriptGenerator()

    @staticmethod
    def get():
        return "Opposite to great success, use POST instead"

    def post(self):
        """
        Generates and saves node.js scripts based on the prompt received in the POST request. Uses the
        ScriptGenerator object to generate and validate the script. Returns the script ID.
        :return: The script ID.
        """
        args = generator_parser.parse_args()
        script_id = self.generator.run(args["description"])
        return script_id


class ScriptRunner(Resource):
    """
    A Flask resource that runs a script with given parameters using Node.js.
    """
    @staticmethod
    def get():
        return "Opposite to great success, use POST instead"

    @staticmethod
    def post():
        """
        Runs a script with given parameters using Node.js.
        :return: The output of the script as a string
        """
        args = runner_parser.parse_args()
        sub = subprocess.run(
            ["node", os.path.join(SCRIPTS_PATH, f"script_{args['script_id']}.js")] + args["parameters"],
            capture_output=True
        )
        return sub.stdout.decode("utf-8").strip()


api.add_resource(GeneratorBot, "/generate")
api.add_resource(ScriptRunner, "/test")


if __name__ == '__main__':
    app.run()

