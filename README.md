# LLM Script Generator API

This is a Flask API that uses OpenAI's GPT-3.5 architecture to generate Node.js scripts based on user prompts. The generated scripts can be saved to the file system and later run using the same API.

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


### `/run`
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

TBy default, the app will be running on `http://localhost:5000`.

## Usage

### Generating a Script

To generate a script, make a `POST` request to the `/generate` endpoint with a JSON payload containing the user prompt. Here's an example using `curl`:

```bash
curl -H "Content-Type: application/json" -X POST -d '{"description": "Write a function that calculates the sum of two numbers."}' http://localhost:5000/generate
```

The response will contain the ID of the generated script.

### Running a Script
To run a script, make a `POST` request to the `/run` endpoint with a JSON payload containing the `ID` of the script and any required parameters. Here's an example using curl:

```bash
curl -H "Content-Type: application/json" -X POST -d '{"script_id": 1, "parameters": [1, 2]}' http://localhost:5000/run
```
The response will contain the output of the script.



