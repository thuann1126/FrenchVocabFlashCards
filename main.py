import random
import time
from threading import Timer
from tkinter import *

import pandas
from pandas import *

# CONSTANT PROPERTIES
BG = "#b3fff0"
KEY_BG = "#FF8080"
CARD_WIDTH = 800
CARD_HEIGHT = 526
TITLE_FONT = ("Ariel", 40, "italic")
TEXT_FONT = ("Ariel", 40, "bold")
SCORE_FONT = ("Ariel", 20, "bold")

# GLOBAL VARIABLE
current_card = []
data = pandas.read_csv("./data/french_words.csv")
data_to_dict = data.to_dict(orient="records")
words_to_learn = []
words = 0


#----------------------Files management---------------------



#----------------------Functions---------------------
def know_the_word():
    global current_card, words_to_learn, words # Get global keyword to use global variable
    record = random.choice(data_to_dict)
    if record in words_to_learn:
        try:
            know_the_word()
        except RecursionError:
            print("You already learn all the words")
            canvas.itemconfig(card_title, text="You have learned all the words")
            canvas.itemconfig(word, text="")
            canvas.itemconfig(card_sides, image=card_front)

    else:
        current_card = record
        words += 1
        canvas.config(bg=BG)
        canvas.itemconfig(card_title, text="French")
        canvas.itemconfig(word, text=record["French"])
        canvas.itemconfig(card_sides, image=card_front)
        canvas.itemconfig(words_count, text=f"Words Learned: {words}")

        #flip the card
        window.after(5000, func=show_answer)

        # Write learned words to file
        words_to_learn.append(record)
        df = pandas.DataFrame(words_to_learn)
        df.to_csv("./data/words_to_learn.csv")

        print(words)


def show_answer():
    global current_card

    canvas.config(bg=BG)
    canvas.itemconfig(card_title, text="English")
    canvas.itemconfig(word, text=current_card["English"])
    canvas.itemconfig(card_sides, image=card_back)




#----------------------UI Implementation---------------------
window = Tk()
window.title("French Flash Cards")
window.config(padx=50, pady=50, bg=BG)
window.after(3000, func=show_answer)
#tk.after(time, function)
#canvas.itemconfig(card_sides, image=card_back)

#******Note********
# Difference between tk.after(ms, function) and time.sleep
# tk.after: delay, but trigger all the function before it
# time.sleep: delay, but hold all the process

# Initial card
canvas = Canvas(width=CARD_WIDTH, height=CARD_HEIGHT)
card_front = PhotoImage(file="./images/card_front.png")
card_back = PhotoImage(file="./images/card_back.png")
card_sides = canvas.create_image(CARD_WIDTH/2,CARD_HEIGHT/2 , image= card_front)
card_title = canvas.create_text(CARD_WIDTH/2,CARD_HEIGHT/3, text="", font=TITLE_FONT)
word = canvas.create_text(CARD_WIDTH/2,CARD_HEIGHT/1.5, text="", font=TEXT_FONT)
words_count = canvas.create_text(CARD_WIDTH*0.8, CARD_HEIGHT/12, text=f"Words learn: {words}", font=SCORE_FONT)
canvas.grid(column=0, row=0, columnspan=2)
canvas.config(bg=BG, highlightthickness=0)


#Intial the buttons
#Wrong button
cross_image = PhotoImage(file="./images/wrong.png")
unknown_button = Button(image=cross_image, highlightthickness=0, bg=BG, command= show_answer)
unknown_button.grid(column=0, row=1)

#Check button
check_image = PhotoImage(file="./images/right.png")
check_button = Button(image=check_image, highlightthickness=0, bg=BG, command=know_the_word)
check_button.grid(column=1, row=1)

know_the_word()

window.mainloop()

