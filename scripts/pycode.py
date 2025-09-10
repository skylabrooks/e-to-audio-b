import os
import base64
import mimetypes

from google import genai
from google.genai import types
import logging


def save_binary_file(file_path: str, data: bytes) -> None:
    """
    Save binary data to a file using context manager for safe resource handling.

    Args:
        file_path: Path to the file to save data to.
        data: Binary data to write to the file.
    """
    try:
        with open(file_path, "wb") as f:
            f.write(data)
        logging.info(f"File saved to {file_path}")
    except IOError as e:
        logging.error(f"Error saving file {file_path}: {e}")


def generate(input_text: str, api_key: str) -> None:
    """
    Generate content using Google Gemini API with txt2image capabilities.

    Args:
        input_text (str): Input text for the model.
        api_key (str): API key for authentication.

    Raises:
        ValueError: If api_key is None or empty.
        Exception: For API initialization or processing errors.
    """
    if not api_key:
        raise ValueError("API key must be provided")
    try:
        client = genai.Client(api_key=api_key)
    except Exception as e:
        logging.error(f"Failed to initialize Gemini client: {e}")
        raise

    model = "gemini-2.5-flash-image-preview"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=input_text),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        response_modalities=[
            "IMAGE",
            "TEXT",
        ],
    )

    file_index = 0
    try:
        for chunk in client.models.generate_content_stream(
            model=model,
            contents=contents,
            config=generate_content_config,
        ):
            if (
                chunk.candidates is None
                or chunk.candidates[0].content is None
                or chunk.candidates[0].content.parts is None
            ):
                continue
            part = chunk.candidates[0].content.parts[0]
            if hasattr(part, 'inline_data') and part.inline_data and part.inline_data.data:
                inline_data = part.inline_data
                # Decode base64-encoded data to bytes
                try:
                    data_buffer = base64.b64decode(inline_data.data)
                except ValueError as e:
                    logging.error(f"Error decoding base64 data: {e}")
                    continue
                # Guess file extension from MIME type
                mime_type = inline_data.mime_type or 'application/octet-stream'
                file_extension = mimetypes.guess_extension(mime_type) or '.bin'
                # Use sequential naming for uniqueness
                prefix = "diesel_demon"
                prefix = "gemini_output"
                file_name = f"{prefix}_{file_index}{file_extension}"
                file_index += 1
                save_binary_file(file_name, data_buffer)
            elif hasattr(part, 'text') and part.text:
                logging.info(part.text)
            else:
                logging.warning("Received unsupported response part")
    except Exception as e:
        logging.error(f"Error during API call or processing: {e}")
        raise


if __name__ == "__main__":
    input_text = os.environ.get("INPUT_TEXT", "Default input text for generation")
    api_key = os.environ.get("GOOGLE_API_KEY")
    if api_key:
        try:
            generate(input_text, api_key)
        except Exception as e:
            logging.error(f"Generation failed: {e}")
    else:
        logging.error("GOOGLE_API_KEY nvironment variable not set")
