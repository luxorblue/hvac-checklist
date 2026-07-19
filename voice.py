"""
Voice handling for Rex HVAC System
Handles speech recognition via Bluetooth mic and text-to-speech output
"""

import subprocess
import sys

class VoiceHandler:
    """Manages voice input and output for HVAC checklist"""
    
    def __init__(self):
        self.recognizer = None
        self.mic = None
        self.init_speech_recognition()
    
    def init_speech_recognition(self):
        """Initialize speech recognition library"""
        try:
            import speech_recognition as sr
            self.recognizer = sr.Recognizer()
            # List available microphones
            try:
                self.mic = sr.Microphone()
            except Exception as e:
                print(f"Warning: Microphone not available: {e}")
                self.mic = None
        except ImportError:
            print("speech_recognition not installed. Install with: pip install SpeechRecognition")
            self.recognizer = None
    
    def listen(self, timeout=5):
        """
        Listen for voice input from Bluetooth mic
        Returns transcribed text or None if no speech detected
        """
        if not self.recognizer or not self.mic:
            return None
        
        try:
            import speech_recognition as sr
            
            with self.mic as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=timeout)
            
            # Try Google Speech Recognition
            try:
                text = self.recognizer.recognize_google(audio)
                print(f"Heard: {text}")
                return text.lower()
            except sr.UnknownValueError:
                print("Could not understand audio")
                return None
            except sr.RequestError as e:
                print(f"Speech recognition error: {e}")
                return None
        
        except Exception as e:
            print(f"Error during listening: {e}")
            return None
    
    def speak(self, text, rate=150):
        """
        Speak text using text-to-speech
        Uses espeak via Bluetooth earbuds
        """
        try:
            # Use espeak for TTS (lightweight, works on Pi)
            subprocess.run(
                ['espeak', '-s', str(rate), text],
                check=False,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        except FileNotFoundError:
            print("espeak not installed. Install with: sudo apt-get install espeak")
        except Exception as e:
            print(f"Error during speech: {e}")
    
    def confirm_reading(self, reading_name, value):
        """Speak a confirmation of a reading"""
        text = f"Confirming {reading_name}: {value}"
        self.speak(text)
    
    def prompt_for_reading(self, reading_name):
        """Prompt user to provide a reading value"""
        text = f"Please provide {reading_name}"
        self.speak(text)
    
    def voice_command(self, command):
        """
        Process a voice command
        Returns action and value if applicable
        """
        command = command.lower().strip()
        
        # Common commands
        if "exit" in command or "quit" in command or "done" in command:
            return ("exit", None)
        elif "save" in command:
            return ("save", None)
        elif "back" in command or "menu" in command:
            return ("back", None)
        elif "next" in command or "skip" in command:
            return ("next", None)
        elif "repeat" in command:
            return ("repeat", None)
        else:
            return ("value", command)
    
    def test_mic(self):
        """Test microphone connectivity"""
        if not self.recognizer or not self.mic:
            return False
        
        try:
            print("Testing microphone...")
            self.speak("Microphone test")
            return True
        except Exception as e:
            print(f"Microphone test failed: {e}")
            return False

# Test
if __name__ == "__main__":
    print("voice.py loaded successfully")
