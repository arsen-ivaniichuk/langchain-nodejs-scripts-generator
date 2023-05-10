# Flask API with LLM for Generating and Running Node.js Scripts

This is a Flask API that uses LLM/Langchain to generate Node.js scripts based on natural language descriptions provided by the user. The API also allows users to run the generated scripts by passing parameters to them.


## Requirements
- Python 3.7 or higher
- Node.js
- npm

## Endpoints
### `/generate`
**Method:** POST

**Request Body:**

- **`description`:** A string describing the task that the script should perform.

**Response:**
- **`script_id`:** A string representing the ID of the generated script.


### `/test`
**Method:** POST

**Request Body:**

- **`script_id:`** A string representing the ID of the script to run.
- **`parameters:`** A list of strings representing the parameters to pass to the script.

**Response:**

- The output of the script.

## Setup

1. Clone this repository
2. Initialize and activate a virtual environment:
```bash
python -m venv new_env
source new_env/bin/activate
```
3. Install the required packages: `pip install -r requirements.txt`
4. Set your OpenAI API key as the value of the variable `OPENAI_API_KEY` in the `constants.py` file:
```python
OPENAI_API_KEY = "..."
```
5. Run the application: `python app.py`

By default, the app will be running on `http://localhost:5000`.

## Usage
**_NOTE:_** To send `http` requests you will need to open another terminal window. You may need to activate the virtual enviroment in that terminal too.

### Generating a Script

To generate a script, make a `POST` request to the `/generate` endpoint with a JSON payload containing the user prompt. Here's an example using `curl`:

```bash
curl -H "Content-Type: application/json" -X POST -d '{"description": "Write a function that calculates the sum of two numbers."}' http://localhost:5000/generate
```

The response will contain the ID of the generated script. The script itself will be saved to `scripts` directory.

### Running a Script
To run a script, make a `POST` request to the `/test` endpoint with a JSON payload containing the `ID` of the script and any required parameters. Here's an example using curl:

```bash
curl -H "Content-Type: application/json" -X POST -d '{"script_id": "1", "parameters": [1, 2]}' http://localhost:5000/test
```
The response will contain the output of the script.

While it's not strictly required, it's best practice to pass the `parameters` as a list. If the script isn't supposed to receive any parameters, simply pass an empty list.

## More Usage Examples
### **Prompt:** Write a function that takes a string as input and returns the number of characters in the string
#### `/generate`
```bash
(new_env) arsen ~ >> curl -H "Content-Type: application/json" -X POST -d '{"description": "Write a function that takes a string as input and returns the number of characters in the string"}' http://localhost:5000/generate
"4"
```
#### `/test`
```bash
(new_env) arsen ~ >> curl -H "Content-Type: application/json" -X POST -d '{"script_id": "4", "parameters": ["aaaaa"]}' http://localhost:5000/test
"5"
```
### **Prompt:** Write a function that generates a random number between 1 and 100 and returns it
#### `/generate`
```bash
(new_env) arsen ~ >> curl -H "Content-Type: application/json" -X POST -d '{"description": "Write a function that generates a random number between 1 and 100 and returns it"}' http://localhost:5000/generate
"3"
```
#### `/test`
```bash
(new_env) arsen ~ >> curl -H "Content-Type: application/json" -X POST -d '{"script_id": "3", "parameters": []}' http://localhost:5000/test
"68"
```

