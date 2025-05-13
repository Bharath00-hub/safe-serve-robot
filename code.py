import RPi.GPIO as GPIO
import subprocess
import time
import socket
import os
import pygame
from gtts import gTTS
import speech_recognition as sr
import random
from datetime import datetime

# Motor Control Setup
GPIO.setmode(GPIO.BCM)

# Define GPIO pins for the motors
# Left side motors
IN1 = 17  # Forward input for left motor
IN2 = 27  # Backward input for left motor

# Right side motors
IN3 = 22  # Forward input for right motor
IN4 = 23  # Backward input for right motor

# Set up the GPIO pins as output
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)

# Motor Functions
def move_forward(duration):
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    time.sleep(duration)
    stop_motors()

def move_backward(duration):
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    time.sleep(duration)
    stop_motors()

def turn_left(duration):
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    time.sleep(duration)
    stop_motors()

def turn_right(duration):
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    time.sleep(duration)
    stop_motors()

def stop_motors():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)


def get_time_period():
    """Determine the time period based on the current time."""
    current_hour = datetime.now().hour
    if current_hour < 12:
        return "morning"
    elif current_hour < 18:
        return "afternoon"
    else:
        return "evening"

# Voice Interaction Functions
def play_audio(filename):
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.music.stop()
    pygame.mixer.quit()

def speak(text):
    tts = gTTS(text=text, lang="en")
    filename = "voice.mp3"
    tts.save(filename)
    try:
        play_audio(filename)
    finally:
        if os.path.exists(filename):
            os.remove(filename)


# Function to record and recognize audio
def get_audio():
    """Record audio using ALSA and process with SpeechRecognition."""
    try:
        print("Listening... Speak now.")
        # Record audio using arecord
        filename = "input.wav"
        command = ["arecord", "-D", "hw:0,0", "-f", "cd", "-c", "1", "-t", "wav", "-d", "5", filename]
        subprocess.run(command, check=True)

        # Use SpeechRecognition to process the audio
        r = sr.Recognizer()
        with sr.AudioFile(filename) as source:
            audio_data = r.record(source)
            text = r.recognize_google(audio_data)
            print(f"You said: {text}")
            os.remove(filename)  # Clean up recorded file
            return text.lower()
    except sr.UnknownValueError:
        print("Could not understand the audio.")
        return ""
    except sr.RequestError as e:
        print(f"Error with the recognition service: {e}")
        return ""
    except Exception as e:
        print(f"Error during audio recording: {e}")
        return ""

def notify_display_order():
    """Notify the system/server that the customer wants to order via the display."""
    HOST = '192.168.232.192'  # Replace with the IP of the server/machine you're notifying
    PORT = 12345  # Port number to use for communication

    try:
        # Set up the client socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((HOST, PORT))
        
        # Send a notification/message
        message = "display_order"
        client_socket.sendall(message.encode())
        print("Notification sent to server for display order.")
        
        # Close the connection
        client_socket.close()
    except Exception as e:
        print(f"Error while sending notification: {e}")


def navigate_to_customer():
    """Navigate the robot to the customer."""
    speak("customer arrived, going to take order from customer.")
    move_forward(5)  # Move forward for 5 seconds
    turn_right(1.6)
    move_forward(4)
    turn_left(1)
        # Turn left
  # Move forward again

def navigate_to_kitchen():
    """Return the robot to the base."""
    speak("order ready, going to kitchen.") # Move backward for 5 seconds
    turn_left(2)     # Turn right
    move_forward(3)
    turn_left(1)
    move_forward(2)  # Move backward to the 
    speak("please give food in tray, i'll go and serve to customer.")
    stop_motors()
    time.sleep(15)
    
def kitchen_to_customer():
    turn_right(4.5)
    move_forward(4)
    speak("Take Your order.")
    stop_motors()
    time.sleep(10)
    
def greeting_at_end():
    speak("Thank You for visiting our restaurant,Have a Wonderful day.")
    stop_motors()
    time.sleep(3)
    
def after_end():
    turn_right(4)     # Turn right
    move_forward(5)  # Move backward to the
    stop_motors()
    time.sleep(15)
    
        

    
# Interaction Logic
def trivia_game():
    """Ask a trivia question to entertain the customer."""
    questions = {
        "What is the most expensive spice in the world?": "saffron",
        "Which fruit is known as the king of fruits?": "mango",
        "What is the national dish of Italy?": "pizza",
        "Which beverage is known as the world's most popular drink after water?": "tea"
    }
    question, answer = random.choice(list(questions.items()))
    speak(f"Here's a trivia question: {question}")
    response = get_audio()
    if answer in response:
        speak("Correct! You know your stuff!")
    else:
        speak(f"Nice try! The correct answer is {answer}.")

# Fun Facts Function
def fun_facts():
    """Share a fun fact with the customer."""
    facts = [
        "Did you know that octopuses have three hearts?",
        "Honey never spoils. Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old!",
        "Bananas are berries, but strawberries aren't!"
    ]
    fact = random.choice(facts)
    speak(f"Here's a fun fact: {fact}")

# Personalized Greeting Function
def personalized_greeting():
    """Provide personalized greetings based on the time of day."""
    current_hour = datetime.now().hour
    if current_hour < 12:
        speak("Good morning! I hope you're having a great start to your day!")
    elif current_hour < 18:
        speak("Good afternoon! I hope you're enjoying your day!")
    else:
        speak("Good evening! I hope you're having a relaxing time!")

# Main waiter bot function
def interact_with_customer():
    """Main function to interact with the customer."""
    time_period = get_time_period()
    greet_message = f"Good {time_period}! Welcome to our restaurant!"
    meal_suggestion = "breakfast" if time_period == "morning" else "lunch" if time_period == "afternoon" else "dinner"

    speak(greet_message)
    speak("Would you like to order food through voice commands or on the display?")
    input_mode = get_audio()

    if "voice" in input_mode:
        speak(f"Great! Let's proceed with the voice command option.")
    elif "display" in input_mode:
        speak("Sure! Please use the display to browse our menu and place your order.")

        notify_display_order()

        return  # End interaction for display mode
    else:
        speak("I did not understand that. let's proceed with the voice command option")

    # Voice order handling starts here
    order = ""
    order_complete = False
    while not order_complete:
        speak(f"Would you like to explore our {meal_suggestion} options, beverages, or desserts?")
        category = get_audio()

        if not category:
            speak("I didn't catch that. Please repeat.")
            continue
        if "exit" in category:
            speak("Thank you for visiting. Have a wonderful day!")
            break

        if "breakfast" in category or "lunch" in category or "dinner" in category:
            speak(f"Our {meal_suggestion} specials include:")
            if meal_suggestion == "breakfast":
                speak("Idli Sambar, Aloo Paratha, Puri-Saagu, Set Dosa, and Masala Dosa,")
            elif meal_suggestion == "lunch":
                speak("Paneer Butter Masala, Chicken Biryani, Mutton Biryani, Mushroom Kebab, and Dal Tadka.")
            elif meal_suggestion == "dinner":
                speak("Tandoori Roti with Butter Chicken, Mutton Curry with Naan, Roti-Curry, Khichdi with Ghee, Rice-Daal, Rajma-Rice, and Veg Pulao.")

        elif "beverages" in category:
            speak("We have Fresh Orange Juice, Mango Shake, Whiskey, and Beer available.")
        elif "desserts" in category:
            speak("Our desserts include Vanilla Ice Cream, Chocolate Brownie, and Gulab Jamun.")
        elif "trivia" in category:
            trivia_game()
        elif "facts" in category:
            fun_facts()
        else:
            speak("I didn't understand that. Please choose between breakfast, lunch, dinner, beverages, or desserts.")
            continue

        # Finalize order
        speak("Please let me know your order.")
        final_order = get_audio()
        if not final_order:
            speak("I didn't hear your order. Please say it again.")
            continue

        # Clean up common prefixes in the order input
        final_order = final_order.replace("your order is", "").strip()
        order += final_order
        speak(f"You have ordered: {final_order}.")

        speak("Would you like to add anything else like dessert, ice cream, or alcohol to your order?")
        additional_items = get_audio()

        if not additional_items or additional_items.strip() == "":
            speak("I didn't catch that. Would you like to add anything else?")
            additional_items = get_audio()

        if "alcohol" in additional_items.lower():
            speak("Are you traveling alone or with family?")
            travel_response = get_audio()

            if "alone" in travel_response:
                speak("Sorry, we cannot serve alcohol for safety reasons, especially if you're alone.")
            elif "family" in travel_response:
                speak("Proceeding with the addition of alcohol to your order.")
                order += ", alcohol"
            else:
                speak("I didn't understand your response. Please specify if you are traveling alone or with family.")
                continue

        elif "yes" in additional_items.lower():
            speak("Please let me know what you would like to add.")
            extra_order = get_audio()
            order += f", {extra_order}"
            speak(f"Got it! You have ordered: {order}.")
        elif "no" in additional_items.lower():
            speak("No problem. Proceeding with your current order.")
        else:
            speak("I didn't catch that. Proceeding with your current order.")

        speak("Your order will be ready shortly. Thank you for your order!")

        # Wait Time: Trivia, Facts, or Game
        speak("While your order is being prepared, let's have some fun!")
        action = random.choice(["trivia", "facts", "game"])

        if action == "trivia":
            trivia_game()
        elif action == "facts":
            fun_facts()
        elif action == "game":
            speak("Let's play a quick game of 'Guess the number!' Think of a number between 1 and 10, and I'll try to guess it!")
            guess = random.randint(1, 10)
            speak(f"Is it {guess}?")

        speak("Your order is ready! I am bringing to You soon")
        order_complete = True
        
        return


# Navigation + Interaction Workflow
def navigate_and_interact():
    try:
        navigate_to_customer()
        
        # Interact with the customer 
        interact_with_customer()
        
        navigate_to_kitchen()
        
        kitchen_to_customer()
        
        greeting_at_end()
        
        after_end()
        
          # Move backward to the base
    finally:
        GPIO.cleanup()

# Main Execution
if _name_ == "_main_":
    navigate_and_interact()