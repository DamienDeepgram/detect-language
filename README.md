# Language Detection using OpenAI's Whisper API

This project detects the language of an audio file using OpenAI's Whisper API. The script, `main.py`, can be run as a standalone tool or a Flask API server.

---

## Features

- **Language Detection**: Processes an audio file (WAV format) to detect its language.
- **Audio Trimming**: Automatically trims the input audio to the first 15 seconds if it is longer.
- **Dual Mode**: Run as a command-line tool or a Flask API server.
- **Easy Integration**: API endpoint for uploading files and receiving language detection results.

---

## Prerequisites

1. **Python Version**: Python 3.7 or later.
2. **Dependencies**:
   - Flask
   - OpenAI Python Library

   Install dependencies with:
   ```
   pip install flask openai
   ```

3. **OpenAI API Key**: Ensure you have access to OpenAI's API and configure the `OpenAI` client with your credentials.

---

## Usage

### 1. **Command-Line Mode**

Detect the language of a WAV file directly from the command line:

```
python main.py path/to/audio.wav
```

**Example**:
```
python main.py ./sample.wav
```

### 2. **Flask API Mode**

Run the script as a Flask API server:

```
python main.py --serve
```

Once the server is running, you can send a `POST` request to the `/detect-language` endpoint with an audio file:

```
curl -X POST -F "file=@path/to/audio.wav" http://localhost:5000/detect-language
```

**Response**:
```
{
  "detected_language": "english"
}
```

---

## Code Structure

### `main.py`

The main script includes the following components:
- **Audio Trimming**: Ensures the WAV file is no longer than 15 seconds.
- **Language Detection**: Uses OpenAI's Whisper API to determine the language.
- **Flask API**: A RESTful endpoint for language detection.

---

## Error Handling

- **Missing File**: If no file is provided in API mode or the file path is invalid in command-line mode, an appropriate error message is returned.
- **API Issues**: Errors during API communication are handled and logged.

---

## Running Tests

Test the functionality locally using example WAV files. Ensure the OpenAI API key is valid and properly configured before running the script.

---

## License

This project is licensed under the MIT License.
