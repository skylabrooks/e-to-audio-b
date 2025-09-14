#!/usr/bin/env python3
"""
MCP server for OpenAI Text-to-Speech.
"""
import base64
import os

from fastmcp import FastMCP  # type: ignore
from openai import OpenAI  # type: ignore

# Initialize OpenAI client
api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable not set")
client = OpenAI(api_key=api_key)

# Create FastMCP server
mcp = FastMCP("OpenAI TTS")


@mcp.tool()
def synthesize_speech(
    text: str, voice: str = "alloy", model: str = "tts-1"
) -> str:
    """Synthesizes speech from text using the OpenAI TTS API.

    Args:
        text: The text to synthesize.
        voice: The voice to use for the synthesis.
        model: The TTS model to use.

    Returns:
        A string containing the path to the generated audio file.
    """
    Convert text to speech using OpenAI TTS API.

    Args:
        text: The text to synthesize.
        voice: The voice to use for the synthesis.
        model: The TTS model to use.

    Returns:
        A base64-encoded string of the audio content.
    """
    try:
        response = client.audio.speech.create(
            model=model, voice=voice, input=text
        )
        return base64.b64encode(response.content).decode("utf-8")
    except Exception as e:
        return f"Error synthesizing speech: {e}"


@mcp.tool()
def list_voices() -> list[str]:
    """
    List available OpenAI TTS voices.

    Returns:
        A list of available voice names.
    return [
        "alloy", "echo", "fable", "onyx", "nova", "shimmer"
    ]


if __name__ == "__main__":
    mcp.run()
