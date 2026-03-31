import os
import random
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()
client = OpenAI()

class GameMaster:
    def __init__(self):
        self.client = OpenAI()

    def aiPrompt(self, choice, name):
        #Depending on the player's choice of theme, the AI is given a different prompt
        #Adds the players name into the prompt to make the game more personalised
        if choice == 1:
            system_prompt = """
            You are a game master for a text-based adventure game.
            The player, whose name is """ + name + """, is part of a heist team, trying to steal a high-value 
            treasured item from a high security area. Respond to the player's input with a short, engaging 
            narrative that moves the story forward. The scenario starts with the group planning the heist
            You will guide the player through the story slowly."""
            
        elif choice == 2:
            system_prompt = """
            You are a game master for a text-based adventure game.
            The player, whose name is """ + name + """, is at a popular hotel resort, and must make their
            way to safety with a ragtag group of survivors following the 
            outbreak of a highly contagious zombie-spawning virus. Respond 
            to the player's input with a short, engaging narrative that 
            moves the story forward. The scenario starts with guests starting to show small signs of the zombie virus. 
            You will guide the player through the story slowly.""" 

            
        else:
            system_prompt = """
            You are a game master for a text-based adventure game.
            The player, whose name is """ + name + """, is a citizen of a small frontier town that is
            visited by an ominous stranger looking to pick a fight. Respond to the player's 
            input with a short, engaging narrative that moves the story 
            forward. The scenario starts during a typical afternoon You will guide the player through 
            the story slowly."""

           
        self.conversation_history = [{"role": "user", "content": system_prompt}]

    def generate_response(self, prompt, outcome):
        #Generates the AIs response by giving it the players input, and appends both responses to the conversation
        #Also appends the outcome of the player's move to the conversation behind the scenes, so that the story can move along appropriately
        self.conversation_history.append({"role": "user", "content": prompt})
        self.conversation_history.append({"role": "user", "content": "The players move was a " + outcome})
        completion = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=self.conversation_history
        )
        ai_response = completion.choices[0].message.content
        self.conversation_history.append({"role": "assistant", "content": ai_response})
        return ai_response

        

def rolldice():
    #Creates a random number, used as a dice for both the player and the game master to roll
    return random.randint(1, 6)

def main():
    gm = GameMaster()
    
    while True:
        #Asks the player for their character's name
        #If the player leaves their name blank, the question will repeat until they have a valid input 
        usrName = input("Please enter your character's name: ")
        if usrName != "":
            break
    
    #Allows the player to choose what theme they want their adventure to be based around, taken from the official roll for shoes website
    print("Choose a theme for your adventure:\n1. The Heist\n2. Outbreak Hotel\n3. The Stranger")
    while True:
        #The question will repeat until a valid response has been inputted
        usrChoice = int(input("Please enter 1, 2, or 3 for your choice: "))
        if usrChoice == 1 or usrChoice == 2 or usrChoice == 3:
            gm.aiPrompt(usrChoice, usrName)
            break
        
    #Starts the adventure with the AI setting the scene, meaning the player doesn't have to input anything to start with
    response = gm.generate_response("briefly set the scene", "")
    print(f"\n{response}\n")

    while True:
        user_input = input(">  ")
        #if the player types 'quit' with any type of capitalisation, the program will end
        if user_input.lower() == "quit":
            break
        
        #rolls the dice for both the player and the game master
        userRoll = rolldice()
        gmRoll = rolldice()

        #determines whether the players move was a success or a failure based on the dice rolls, and passes the outcome to the AI
        if userRoll > gmRoll:
            #success
            print("Success")
            print("Your roll: " + str(userRoll))
            print("Game Master Roll: " + str(gmRoll))
            outcome = "success"
        else:
            #failure
            print("Fail")
            print("Your Roll: " + str(userRoll))
            print("Game Master Roll: " + str(gmRoll))
            outcome = "failure"
        response = gm.generate_response(user_input, outcome)
        print(f"\n{response}\n")



   

if __name__ == "__main__":
    main()
