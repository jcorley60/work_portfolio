import tkinter as tk
import random

# try:
#     import tkinter
# except ImportError: # try-except block added in the event of python2 only
#     import Tkinter as tkinter

def load_images(card_images):
    suits = ['heart', 'club', 'diamond', 'spade']
    face_cards = ['jack', 'queen', 'king']

    if tk.TkVersion >= 8.6: # the newer version of tkinter can handle the desirable (scalable) PNG format
        extension = 'png'
    else:
        extension = 'ppm'

    # for each suit, retrieve the image for the cards
    for suit in suits:
        # first the numbered cards 1 to 10
        for card in range(1, 11):
            name = f"{str(card)}_{suit}.{extension}" # this follows the naming convention of each card
            image = tk.PhotoImage(file=name)        # https://effbot.org/tkinterbook/photoimage.htm
            card_images.append((card, image, ))

            # next the face cards
            for card in face_cards:
                name = f"{str(card)}_{suit}.{extension}"
                image = tk.PhotoImage(file=name)
                card_images.append((10, image,))


def _deal_card(frame): # pack manager is much easier than grid to use
    # pop the next card off the top of the deck
    next_card = deck.pop(0) # 0 means to pop the card sitting on the top of the deck
    # add the image to a label and display the label
    deck.append(next_card) # this can be used to place the popped card at the end of the deck
    tk.Label(frame, image=next_card[1], relief='raised').pack(side='left')
    # now return the card's face value
    return next_card


def score_hand(hand):
    """Calc the total score of all cards in the list.
    Only one ace can have the value 11, and this will
    be reduced to 1 if the hand would bust"""
    score = 0
    ace = False
    for next_card in hand: # go through each card, card-by-card
        card_value = next_card[0] # this gets the value from the first card
        if card_value == 1 and not ace:
            ace = True
            card_value = 11
        score += card_value
        # if we would bust then check if there's an ace and subtract 10 if that's the case
        if score > 21 and ace:
            score -= 10
            ace = False
    return score



def deal_dealer():
    dealer_score = score_hand(dealer_hand)
    while 0 < dealer_score < 17:    # arbitrary: if dealer score less than 17 they get another card
        dealer_hand.append(_deal_card(dealer_card_frame))
        dealer_score = score_hand(dealer_hand)
        dealer_score_label.set(dealer_score)

    player_score = score_hand(player_hand)
    if player_score > 21:
        result_text.set("Dealer wins!")
    elif dealer_score > 21 or dealer_score < player_score:
        result_text.set("Player wins!")
    elif dealer_score > player_score:
        result_text.set("Dealer wins!")
    else:
        result_text.set("Draw!")


def deal_player():
   player_hand.append(_deal_card(player_card_frame))
   player_score = score_hand(player_hand)

   player_score_label.set(player_score)
   if player_score > 21:
       result_text.set("Dealer Wins!")
    # global player_score
    # global player_ace
    # card_value = deal_card(player_card_frame)[0] # we need to specify the facevalue of the card
    # if card_value == 1 and not player_ace:        # if ace drawn from deck, and no ace already drawn
    #     player_ace = True
    #     card_value = 11
    # player_score += card_value
    # # if we should bust, check if there's an ace and subtract
    # if player_score > 21 and player_ace:
    #     player_score -= 10
    #     player_ace = False
    # player_score_label.set(player_score)
    # if player_score > 21:
    #     result_text.set("Dealer wins!")
    # print(locals())

def initial_deal():
    deal_player() # deals first card for player
    dealer_hand.append(_deal_card(dealer_card_frame)) # deals card to dealer
    dealer_score_label.set(score_hand(dealer_hand)) # calc's dealer score
    deal_player() # deals 2nd card for player


def new_game():
    """This function will:

     1). start a new game
     2). reset player and dealer hands
     3). start a new game"""
    global dealer_card_frame
    global player_card_frame
    global dealer_hand
    global player_hand
    # global cards
    # embedded frame to hold the card images
    dealer_card_frame.destroy()
    dealer_card_frame = tk.Frame(card_frame, background='green')
    dealer_card_frame.grid(row=0, column=1, sticky='ew', rowspan=2)
    # embedded frame to hold the card images
    player_card_frame = tk.Frame(card_frame, background='green')
    player_card_frame.grid(row=2, column=1, sticky='ew', rowspan=2)

    result_text.set("")

    dealer_hand, player_hand = [], []
    # cards = []

    initial_deal()


def shuffle():
    random.shuffle(deck)


def play():
    initial_deal()

    mainWindow.mainloop()


mainWindow = tk.Tk() # this creates the main window.

# Set up the screen and frames for the dealer and player. (frame for dealer and another for player).  The following code modifies the main window.
mainWindow.title("Blackjack")
mainWindow.geometry('640x320')
mainWindow.configure(background='green')
# mainWindow.geometry--This method is used to set the dimensions of the Tkinter window
# as well as being used to set the position of the main window on the user’s desktop.

result_text = tk.StringVar()
result = tk.Label(mainWindow, textvariable=result_text)
result.grid(row=0, column=0, columnspan=3)
# Label widget is a standard Tkinter widget used to display text or an image on the screen.
# The label can only display text in a single font, but the text may span more than one
# line. In addition, one of the characters can be underlined, for example to mark a
# keyboard shortcut.
# tkinter.StringVar() has to do with TCL & is complex

card_frame = tk.Frame(mainWindow, relief='sunken', borderwidth=1, background='green')
card_frame.grid(row=1, column=0, sticky='ew', columnspan=3, rowspan=2)
# Frame widget is very important for the process of grouping and organizing other widgets
# in a somehow friendly way. It works like a container, which is responsible for
# arranging the position of other widgets.
# It uses rectangular areas in the screen to organize the layout and to provide padding
# of these widgets. A frame can also be used as a foundation class to implement
# complex widgets.

dealer_score_label = tk.IntVar()
tk.Label(card_frame, text='Dealer', background='green', fg='white').grid(row=0, column=0)
tk.Label(card_frame, textvariable=dealer_score_label, background='green', fg='white').grid(row=1, column=0)
#embedded frame to hold the card images
dealer_card_frame = tk.Frame(card_frame, background='green')
dealer_card_frame.grid(row=0, column=1, sticky='ew', rowspan=2)

# Global variables
player_score_label = tk.IntVar()
# player_score = 0
# player_ace = False

tk.Label(card_frame, text="Player", background='green', fg='white').grid(row=2, column=0)
tk.Label(card_frame, textvariable=player_score_label, background='green', fg='white').grid(row=3, column=0)
# embedded frame to hold the card images
player_card_frame = tk.Frame(card_frame, background='green')
player_card_frame.grid(row=2, column=1, sticky='ew', rowspan=2)

button_frame = tk.Frame(mainWindow)
button_frame.grid(row=3, column=0, columnspan=3, sticky='w')

dealer_button = tk.Button(button_frame, text="Dealer", command=deal_dealer) # fxn associated to buttons using command widget. We must pass only the fxn & not a parameter in the fxn! (otherwise None results)
dealer_button.grid(row=0, column=0)
# We're assiging the function to command, instead of calling the function

player_button = tk.Button(button_frame, text='Player', command=deal_player)
player_button.grid(row=0, column=1)

reset_button = tk.Button(button_frame, text="New Game", command=new_game)
reset_button.grid(row=1, column=0, sticky='ew')

shuffle_button = tk.Button(button_frame, text='Shuffle', command=shuffle)
shuffle_button.grid(row=1, column=2)

# load cards
cards =[]
load_images(cards)
print(cards)

# Create a new deck of cards and shuffle them
deck = list(cards)
# random.shuffle(deck)
shuffle()

# create the list to store the dealer's and player's hands
dealer_hand = []
player_hand = []

#Tkinter works by starting a tcl/tk interpreter under the covers, and then translating
# tkinter commands into tcl/tk commands. The main window and this interpreter are
# intrinsically linked, and both are required for a tkinter application to work.

#Creating an instance of Tk initializes this interpreter and creates the root window.
# If you don't explicitly initialize it, one will be implicitly created when you create
# your first widget.

# I don't think there are any pitfalls by not initializing it yourself, but as the zen
# of python states, "explicit is better than implicit". Your code will be slightly
# easier to understand if you explicitly create the instance of Tk. It will, for instance,
# prevent other people from asking the same question about your code that you just asked
    # about this other code.

if __name__ == "__main__":
    play()