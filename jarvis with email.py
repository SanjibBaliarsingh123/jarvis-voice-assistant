import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import smtplib
import time

# Initialize pyttsx3 engine
engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    
    # Time-based greeting
    if hour < 12:
        speak("Good morning!")
    elif hour < 18:
        speak("Good afternoon!")
    else:
        speak("Good evening!")
    
    # Jarvis asks how you're doing
    speak("How are you?")
    
    # Wait for user's response and respond accordingly
    user_response = takeCommand().lower()

    if "good" in user_response or "fine" in user_response or "great" in user_response:
        speak("I'm glad to hear that! Let's make today even better.")
    elif "not good" in user_response or "bad" in user_response or "sad" in user_response:
        speak("I'm sorry to hear that. If you need anything, I'm here to help.")
    else:
        speak("That's interesting! Let's get started.")
    
    # Original Jarvis greeting to ask how to assist
    speak("I am Jarvis. Please tell me how may I help you.")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    for attempt in range(3):  # Retry up to 3 times
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"You said: {query}\n")
            return query.lower()  # Return lowercase for easier comparisons
        except sr.UnknownValueError:
            if attempt < 2:
                speak("I didn't catch that, please say it again.")
            else:
                speak("Sorry, I couldn't understand. Please try again later.")
                return "None"
        except Exception as e:
            speak(f"Error: {str(e)}")
            return "None"
    return "None"

def sendEmail(to, subject, body):
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()

        # Fetch email and password from environment variables
        email_user = os.getenv("sbaliarsingh7847@gmail.com")
        email_pass = os.getenv("Sanjib@123")

        if not email_user or not email_pass:
            speak("Email or password is not set in environment variables.")
            return False

        # Prepare email content
        message = f"Subject: {subject}\n\n{body}"

        server.login(email_user, email_pass)
        server.sendmail(email_user, to, message)
        server.close()
        return True
    except smtplib.SMTPAuthenticationError:
        speak("Authentication failed. Please check your email credentials.")
        return False
    except Exception as e:
        speak(f"Failed to send email. Error: {str(e)}")
        return False

def openWebsite(website):
    webbrowser.open(website)

def searchYouTubeSong(song_name):
    speak(f"Searching YouTube for the song {song_name}...")
    webbrowser.open(f"https://www.youtube.com/results?search_query={song_name} music")

def get_email_content():
    speak("Who do you want to send the email to?")
    to = takeCommand()

    speak("What is the subject of the email?")
    subject = takeCommand()

    speak("What do you want to say in the email?")
    body = takeCommand()

    return to, subject, body

if __name__ == "__main__":
    wishMe()
    last_interaction_time = time.time()

    while True:
        query = takeCommand()

        if query == "none":  # No valid input, restart loop
            continue

        last_interaction_time = time.time()  # Reset interaction timer on command
        if "wikipedia" in query:
            speak("Searching Wikipedia...")
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia:")
            print(results)
            speak(results)
        elif "open" in query:
            if "youtube" in query:
                openWebsite("youtube.com")
            elif "google" in query:
                openWebsite("google.com")
            elif "facebook" in query:
                openWebsite("facebook.com")
            elif "linkedin" in query:
                openWebsite("linkedin.com")
            elif "stackoverflow" in query:
                openWebsite("stackoverflow.com")
        elif "open code" in query:
            codePath = "C:\\Users\\sbali\\Downloads"
            os.startfile(codePath)
        elif "email" in query:
            try:
                to, subject, body = get_email_content()
                if to and subject and body:
                    if sendEmail(to, subject, body):
                        speak("Email has been sent successfully!")
                    else:
                        speak("Sorry, I couldn't send the email.")
                else:
                    speak("Email content is missing.")
            except Exception as e:
                speak(f"An error occurred: {str(e)}")
        elif "quit" in query:
            speak("Goodbye!")
            break
        elif "the time" in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {strTime}")
        elif "search" in query:
            query = query.replace("search", "")
            speak(f"Searching Google for {query}...")
            webbrowser.open(f"https://www.google.com/search?q={query}")    
        elif "how are you" in query:
            speak("I'm just a program, but thanks for asking! How can I assist you today?")
        elif "tell me about yourself" in query:
            speak("I am Jarvis, your virtual assistant. I can help you with information, send emails, and much more!")
        elif "play" in query:
            speak("What song would you like to play?")
            song_name = takeCommand()
            searchYouTubeSong(song_name)
        else:
            speak("I'm not sure how to respond to that. Can you ask me something else?")
