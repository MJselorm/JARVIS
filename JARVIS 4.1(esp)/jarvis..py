import speech_recognition  as sr
import datetime
import webbrowser
import subprocess
from brain import generate_response1
from speech import speak, conversation
from esp_control import ESPController,ESP_IP
from chatbox import  JarvisEngine  

# --- INITIALIZE ONCE ---
jarvis = JarvisEngine()
controller = ESPController(ESP_IP)

# Speech recognizer setup
r=sr.Recognizer()
r.pause_threshold=0.8
mic=sr.Microphone(device_index=1)
r.dynamic_energy_adjustment_damping=True


awake=False


with mic as source:
    conversation()

with mic as source:
    r.adjust_for_ambient_noise(source,duration=0.5)
    print("calibrated microphone")
try:
    while True:
        with mic as source:
            print("listening........")
            try:
                audio = r.listen(source, timeout=5, phrase_time_limit=4)
                text = r.recognize_google(audio).lower()
                print(f"You: {text}")
                
                # --- WAKE WORD LOGIC ---
                if not awake:
                    if "jarvis" in text or " jarvis" in text:
                        speak("Yes sir, how can I help you?")
                        awake = True
                    continue # Skip the rest of the loop until awake
                
                    # --- ACTIVE COMMAND LOGIC ---
                if awake:
                    if "time" in text :
                        now = datetime.datetime.now().strftime("%I:%M %p")
                        speak(f"Sir, the time is {now}")
                        
                    elif "date" in text:
                        today = datetime.date.today()
                        def ordinal(n):
                            if 10 <= n % 100 <= 20:
                                suffix = "th"
                            else:
                                suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
                            return str(n) + suffix
                        formatted_date = today.strftime(f"%B {ordinal(today.day)}, %Y")
                        speak(f"Sir, today's date is {formatted_date}")
                    
                    #jarvis tell open youtube
                    elif "open" in text:
                        sites={"youtube":"https://www.youtube.com",
                            "google":"https://www.google.com",
                            "facebook":"https://www.facebook.com",
                            "twitter":"https://www.twitter.com",
                            "github":"https://www.github.com"}
                        for site in sites:
                            if site in text:
                                speak(f"Opening {site}, Sir.")
                                webbrowser.open(sites[site])
                                break
                        
                        
                        
                    #jarvis tell open vs code
                    elif "visual studio code" in text or "vs code" in text:
                        if "close" in text:
                            speak("Terminating the environment, Sir.")
                            subprocess.Popen("taskkill /IM Code.exe /F", shell=True)
                        else:
                            speak("Initializing the workspace.")
                            subprocess.Popen(r"C:\Users\USER\AppData\Local\Programs\Microsoft VS Code\Code.exe")
                    
                    
                    # --- ESP control ---
                    elif "light" in text:
                        if "on" in text:
                            controller.led_on()
                            speak("turning on the light sir")
                        elif "red" in text:
                            controller.led_red()
                            speak("turning on the red light sir")
                        elif "blue" in text:
                            controller.led_blue()
                            speak("turning on the blue light sir")
                        elif "green" in text:
                            controller.led_green()
                            speak("turning on the green light sir")
                        elif "white" in text:
                            controller.led_white()
                            speak("turning on the white light sir")
                        elif "yellow" in text:
                            controller.led_yellow()
                            speak("turning on the yellow light sir")
                        else:
                            controller.led_off()
                            speak("turning off the light sir")

                    
                    #jarvis go to sleep
                    elif "sleep" in text:
                        print("you said:",text)
                        speak("going to sleep sir")
                        print("jarvis: going to sleep sir")
                        awake=False
                        
                    # --- FALLBACK TO AI BRAIN ---
                    else:
                        # This allows him to answer anything else using your Ollama brain
                        reply = jarvis.ask(text)
                        print(f"JARVIS: {reply}")
                        speak(reply)
                    
            

                
            except sr.UnknownValueError:
                pass
            except sr.WaitTimeoutError:
                pass
            except sr.RequestError:
                print("connection error")
            except Exception as e:
                print(f"Error: {e}")
except KeyboardInterrupt:
    print("shutting down jarvis.......")
    speak("Shutting down, Sir.")
