import time
import sys
import threading
import queue

class TTSEngineTest:
    def __init__(self):
        self.q = queue.Queue()
        self.thread = threading.Thread(target=self._tts_worker, daemon=True)
        self.thread.start()

    def _tts_worker(self):
        try:
            import pythoncom
            pythoncom.CoInitialize()
        except ImportError:
            pass
        
        import pyttsx3
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 170)
        self.engine.setProperty('volume', 1.0)
        
        voices = self.engine.getProperty('voices')
        for voice in voices:
            if "zira" in voice.name.lower() or "female" in voice.name.lower():
                self.engine.setProperty('voice', voice.id)
                break
                
        while True:
            text = self.q.get()
            if text is None:
                self.q.task_done()
                break
            print(f"Speaking: {text}")
            self.engine.say(text)
            self.engine.runAndWait()
            self.q.task_done()

    def speak(self, text):
        self.q.put(text)
        self.q.join()

if __name__ == '__main__':
    tts = TTSEngineTest()
    tts.speak("Testing daemon thread speech.")
    time.sleep(1)
