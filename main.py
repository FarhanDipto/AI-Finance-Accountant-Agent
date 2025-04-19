print("🛠️  Initializing AI Finance Agent... Please wait.")  
import os
import sys
import time
from modules.voice_input import get_voice_command
from modules.intent_parser import parse_intent
from modules.finance_api import execute_action
from modules.speech_output import speak_text

class OutputSuppressor:
    def __enter__(self):
        self._original_stdout = sys.stdout
        self._original_stderr = sys.stderr
        sys.stdout = open(os.devnull, 'w')
        sys.stderr = open(os.devnull, 'w')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout
        sys.stderr.close()
        sys.stderr = self._original_stderr

with OutputSuppressor():
    from modules.rag_engine import initialize_rag, get_rag_answer
    initialize_rag()

print("✅ Initialization complete!")

def main():
    while True:
        command = get_voice_command()
        
        if not command:
            continue
            
        intent_data = parse_intent(command)
        
        with OutputSuppressor():
            if intent_data["intent"] == "query_financial_docs":
                result = get_rag_answer(intent_data["query"])
            else:
                result = execute_action(intent_data)

        print(f"💬 Response: {result}")
        speak_text(result)

        time.sleep(1)
        print("\n🎤 Listening for next command...")
        print("\n🟡 Or, press any key to close the agent!")
        
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Shutting down AI Finance Agent. Goodbye!")