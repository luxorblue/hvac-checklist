"""
Local offline LLM client for Raspberry Pi 5 using Ollama.
"""

import json
import urllib.request
import urllib.error


class LocalLLM:
    """Simple local chat client for Ollama running on localhost."""

    def __init__(self, host="127.0.0.1", port=11434, model="phi3:mini", timeout=60):
        self.host = host
        self.port = port
        self.model = model
        self.timeout = timeout
        self.base_url = f"http://{self.host}:{self.port}"

    def is_available(self):
        """Return True if Ollama server is reachable."""
        try:
            with urllib.request.urlopen(f"{self.base_url}/api/tags", timeout=3) as response:
                return response.status == 200
        except Exception:
            return False

    def chat(self, messages):
        """
        Send chat messages to local model.

        messages format:
        [
          {"role": "system", "content": "..."},
          {"role": "user", "content": "..."}
        ]
        """
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False,
        }

        req = urllib.request.Request(
            url=f"{self.base_url}/api/chat",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as response:
                data = json.loads(response.read().decode("utf-8"))
                # Expected: {"message": {"role": "assistant", "content": "..."}, ...}
                return data.get("message", {}).get("content", "")
        except urllib.error.HTTPError as e:
            return f"LLM HTTP error: {e.code}"
        except urllib.error.URLError as e:
            return f"LLM connection error: {e.reason}"
        except Exception as e:
            return f"LLM error: {e}"

