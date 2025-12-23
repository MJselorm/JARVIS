import speech_recognition  as sr
import datetime
import webbrowser
import subprocess
from brain import generate_response1,generate_response2
from speech import speak, conversation
from arduino_control import ArduinoController    
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
                print(f"Heard: {text}")
                
                # --- WAKE WORD LOGIC ---
                if not awake:
                    if "jarvis" in text:
                        speak("Yes sir, how can I help you?")
                        awake = True
                    continue # Skip the rest of the loop until awake
                
                    # --- ACTIVE COMMAND LOGIC ---
                if awake:
                    arduino = ArduinoController(port='COM6')
                    arduino.connect()
                    if "time" in text:
                        now = datetime.datetime.now().strftime("%I:%M %p")
                        speak(f"Sir, the time is {now}")
                    
                    
                    #jarvis tell open youtube
                    elif "open youtube" in text:
                        speak("Opening YouTube")
                        webbrowser.open("https://www.youtube.com")
                        
                        
                    #jarvis tell open vs code
                    elif "open vs code" in text or "open visual studio code" in text:
                        if "open vs code" in text:
                            speak("Opening VS Code sir")
                        if "open visual studio code" in text:
                            speak("Opening Visual Studio Code sir")
                        subprocess.Popen(r"C:\Users\USER\AppData\Local\Programs\Microsoft VS Code\Code.exe")

                    elif "close vs code" in text or "close visual studio code" in text:
                        if "close vs code" in text:
                            speak("Closing VS Code sir")
                        if "close visual studio code" in text:
                            speak("Closing Visual Studio Code sir")
                        subprocess.Popen("taskkill /IM Code.exe /F")
                    #jarvis thinking and responding
                    elif "what is " in text or "who is " in text or "tell me about " in text:
                        print("you said:",text)
                        response=generate_response1(text)
                        speak(response)
                    #jarvis go to sleep
                    elif "sleep" in text:
                        print("you said:",text)
                        speak("going to sleep sir")
                        print("jarvis: going to sleep sir")
                        awake=False
                    
                    # --- ARDUINO CONTROL ---
                    elif "turn on the light" in text or "turn on light" in text:
                        print("you said:",text)
                        speak("turning on the light sir")
                        arduino.light_on()
                    elif "turn off the light" in text or "turn off light" in text:
                        print("you said:",text)
                        speak("turning off the light sir")
                        arduino.light_off()
                        
                    # --- FALLBACK TO AI BRAIN ---
                    else:
                        # This allows him to answer anything else using your Gemini brain
                        speak(f"did u say {text}")
                        if "yes" in text or "yeah" in text or "correct" in text:
                                response = generate_response2(text)
                                print(response)
                                speak(response)
                    
            

                
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
