import speech_recognition  as sr
import datetime
import webbrowser
import subprocess
from brain import generate_response1
from speech import speak, conversation
from arduino_control import ArduinoController  
from chatbox import  JarvisEngine  

# --- INITIALIZE ONCE ---
jarvis = JarvisEngine()
arduino = ArduinoController(port='COM6')
# Try to connect once at startup
try:
    arduino.connect()
except:
    print("Warning: Arduino not found on COM6")

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
                    if "jarvis" in text:
                        speak("Yes sir, how can I help you?")
                        awake = True
                    continue # Skip the rest of the loop until awake
                
                    # --- ACTIVE COMMAND LOGIC ---
                if awake:
                    if "time" in text:
                        now = datetime.datetime.now().strftime("%I:%M %p")
                        speak(f"Sir, the time is {now}")
                        

                    
                    #jarvis tell open youtube
                    elif "open youtube" in text:
                        speak("Opening YouTube")
                        webbrowser.open("https://www.youtube.com")
                        
                        
                    #jarvis tell open vs code
                    elif "visual studio code" in text or "vs code" in text:
                        if "close" in text:
                            speak("Terminating the environment, Sir.")
                            subprocess.Popen("taskkill /IM Code.exe /F", shell=True)
                        else:
                            speak("Initializing the workspace.")
                            subprocess.Popen(r"C:\Users\USER\AppData\Local\Programs\Microsoft VS Code\Code.exe")
                    
                    
                    # --- ARDUINO CONTROL ---
                    elif "light" in text:
                        if "on" in text:
                            arduino.light_on()
                            speak("turning on the light sir")
                        else:
                            arduino.light_off()
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
    arduino.close()
    print("shutting down jarvis.......")
    speak("Shutting down, Sir.")
