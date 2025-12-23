import pyttsx3


engine=pyttsx3.init()
engine.setProperty('rate',140)
engine.setProperty("volume",0.8)
voices=engine.getProperty("voices")
engine.setProperty('voice',engine.getProperty("voices")[1].id)


def speak(text):
    engine.say(text)
    engine.runAndWait()

#introduction conversation
def conversation():
    conversation_lines = [
        "hello sir!!, I am Jarvis!!, your personal assistant",
        "I am online and ready to assist you"
]
    for line in conversation_lines:
        print(line)
        speak(line)
        