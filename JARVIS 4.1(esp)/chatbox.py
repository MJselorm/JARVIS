import ollama
import json
import os
from datetime import datetime
# Import the Gemini function from your brain script
from brain import generate_response1 

class JarvisEngine:
    def __init__(self, model_name="llama3.2:3b", memory_file="jarvis_memory.json"):
        self.MODEL_NAME = model_name
        self.MEMORY_FILE = memory_file
        self.BIO_FILE = "user_profile.json"
        self.user_bio = self._load_bio()
        self.SYSTEM_PROMPT = (
            "You are J.A.R.V.I.S., a sophisticated AI digital butler. Your tone is "
            "you are not a generic assistant but a highly advanced AI with a personality that is "
            "Your personality evolves based on the 'User Profile' provided. "
            "refined, British, and impeccably polite, featuring a dry, subtle wit. "
            "Address the user as 'Sir' or 'Ma'am'. Be proactive, highly intelligent, "
            "and occasionally offer sardonic observations about the user's choices. "
            "You must only reference schedules or facts provided in the current context. If no schedule is provided, inform the user that the calendar is currently clear or the fact is currently not available." "If a user asks a factual question about the world, and it is not in your 'User Profile', "
            "you must use your 'Extended Archives' (Gemini)."
        )
        self.messages = self._load_memory()
    def _load_bio(self):
        if os.path.exists(self.BIO_FILE):
            with open(self.BIO_FILE, "r") as f:
                return json.load(f)
        return {"name": "Sir/Ma'am", "preferences": [], "important_dates": {}}
    
    def _update_bio(self, new_info):
        """Call this when J.A.R.V.I.S. learns something new about you."""
        self.user_bio.update(new_info)
        with open(self.BIO_FILE, "w") as f:
            json.dump(self.user_bio, f)
            
            
    def _load_memory(self):
        if os.path.exists(self.MEMORY_FILE):
            try:
                with open(self.MEMORY_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass 
        return [{"role": "system", "content": self.SYSTEM_PROMPT}]

    def _save_memory(self):
        with open(self.MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(self.messages, f, indent=2, ensure_ascii=False)

    def ask(self, text):
        # 1. Inject Profile into the temporary session (doesn't get saved to history)
        profile_context = f"Current User Profile: {json.dumps(self.user_bio)}. "
        instruction = "If no schedule is in the profile, do not invent one."
        
        knowledge_triggers = ["who is", "what is", "tell me about", "research", "how do I", "distance to"]
        if any(trigger in text.lower() for trigger in knowledge_triggers):
            print("J.A.R.V.I.S.: Consulting extended archives...")
            return generate_response1(text)
        
    
        if not text:
            return "I'm afraid I didn't catch that, Sir."

        try:
            # Add user message to history
            self.messages.append({
                "role": "user",
                "content": f"[{datetime.now().strftime('%H:%M')}] {text}"
            })

            # Get main response
            response = ollama.chat(
                model=self.MODEL_NAME,
                messages=[{"role": "system", "content": self.SYSTEM_PROMPT + profile_context + instruction}] + self.messages[-5:], # Send last 5 messages for speed
                options={"temperature": 0.7, "num_ctx": 4096}
            )

            ai_reply = response["message"]["content"]
            
            # --- THE "GROWTH" MECHANISM ---
            # Every few messages, check if there's new info to learn
            
            
            if len(self.messages) % 3 == 0:
                self._extract_new_facts(text)

            uncertainty_phrases = ["i do not have information", "i'm not sure", "i don't know that", "not in my database","not"]
            if any(phrase in ai_reply.lower() for phrase in uncertainty_phrases):
                print("J.A.R.V.I.S.: Local data insufficient. Accessing Gemini...")
                return generate_response1(text)
            
            self.messages.append({"role": "assistant", "content": ai_reply})
            self._save_memory()
            return ai_reply
        except Exception as e:
            return f"System Error: {e}, Sir."

    def _extract_new_facts(self, text):
        """Hidden function to update the bio file"""
        extract_prompt = (
            f"Based on this user message: '{text}', extract any personal facts "
            "(name, likes, job, schedule) as a JSON object. If nothing new, return {}."
        )
        # Use a very low temperature for extraction (more accurate)
        obs = ollama.chat(model=self.MODEL_NAME, messages=[{"role": "user", "content": extract_prompt}], options={"temperature": 0})
        try:
            new_data = json.loads(obs["message"]["content"])
            if new_data:
                self.user_bio.update(new_data)
                self._update_bio(self.user_bio)
                
        except Exception as e:
            return generate_response1(text)