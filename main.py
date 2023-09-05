import random
from tkinter import *
import pandas


BACKGROUND_COLOR = "#B1DDC6"
current_card = {}

# ------------------READ CSV -------------- #

try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")

# --------------- CARD ----------- #


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    random_word = random.choice(to_learn)
    current_card = random_word

    canvas_card.itemconfig(card_title, text="French", fill="black")
    canvas_card.itemconfig(card_word, text=current_card["French"], fill="black")
    canvas_card.itemconfig(card_image, image=card_front_image)

    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    canvas_card.itemconfig(card_image, image=card_back_image)
    canvas_card.itemconfig(card_title, text="English", fill="white")
    canvas_card.itemconfig(card_word, text=current_card["English"], fill="white")


def is_known():
    to_learn.remove(current_card)
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)

    next_card()

# ------------------- UI ------------------ #


window = Tk()
window.title("Flash Card")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

# ----- IMAGES ----- #
right_image = PhotoImage(file="images/right.png")
wrong_image = PhotoImage(file="images/wrong.png")
card_front_image = PhotoImage(file="images/card_front.png")
card_back_image = PhotoImage(file="images/card_back.png")

# ----- CANVASES ----- #

canvas_card = Canvas(
    width=800,
    height=526,
    bg=BACKGROUND_COLOR,
    highlightthickness=0
)
card_image = canvas_card.create_image(400, 263, image=card_front_image)
card_title = canvas_card.create_text(400, 150, text="Title", font=("Ariel", 40, "italic"))
card_word = canvas_card.create_text(400, 263, text="word", font=("Ariel", 60, "bold"))
canvas_card.grid(row=0, column=0, columnspan=2)

# ----- BUTTONS ---- #
right_button = Button(
    image=right_image,
    highlightthickness=0,
    borderwidth=0,
    bg=BACKGROUND_COLOR,
    command=next_card,
)
right_button.grid(row=1, column=0)

wrong_button = Button(
    image=wrong_image,
    highlightthickness=0,
    borderwidth=0,
    bg=BACKGROUND_COLOR,
    command=is_known,
)
wrong_button.grid(row=1, column=1)


next_card()

window.mainloop()
