from functools import partial
from tkinter import Tk, Label, Button, Frame
import _thread as thread

from src.Game import get_symbol
from src.Utils.Enums import BoardTile


class TicTacToeWindow:
    def __init__(self, execute, clicked):
        self.fb_1 = None
        self.fb_2 = None
        self.fb_3 = None
        self.fb_4 = None
        self.fb_5 = None
        self.fb_6 = None
        self.fb_7 = None
        self.fb_8 = None
        self.fb_9 = None

        self.win_label = None
        self.player_label = None
        self.clicked = clicked
        self.execute = execute

    def update_window(self, board, wins_player_1: int, wins_player_2: int, player: BoardTile) -> None:
        self.fb_1.config(text=get_symbol(board[0][0]))
        self.fb_2.config(text=get_symbol(board[0][1]))
        self.fb_3.config(text=get_symbol(board[0][2]))
        self.fb_4.config(text=get_symbol(board[1][0]))
        self.fb_5.config(text=get_symbol(board[1][1]))
        self.fb_6.config(text=get_symbol(board[1][2]))
        self.fb_7.config(text=get_symbol(board[2][0]))
        self.fb_8.config(text=get_symbol(board[2][1]))
        self.fb_9.config(text=get_symbol(board[2][2]))

        self.win_label.config(text=f"Siege\n{wins_player_1} - X | O - {wins_player_2}")
        self.player_label.config(text=f"{get_symbol(player)} ist dran.")

    def create_window(self):
        window = Tk()
        window.title("TICTACTOE")
        window.config(width=500, height=500)
        window.resizable(width=False, height=False)

        self.win_label = Label(window, text="Siege\n0 - X | O - 0")

        self.player_label = Label(window, text="X ist dran.")

        field = Frame(master=window, width=150, height=150)
        self.fb_1 = Button(field, command=partial(self.clicked, 0, 0))
        self.fb_1.place(width=50, height=50)

        self.fb_2 = Button(field, command=partial(self.clicked, 0, 1))
        self.fb_2.place(x=50, width=50, height=50)

        self.fb_3 = Button(field, command=partial(self.clicked, 0, 2))
        self.fb_3.place(x=100, width=50, height=50)

        self.fb_4 = Button(field, command=partial(self.clicked, 1, 0))
        self.fb_4.place(y=50, width=50, height=50)

        self.fb_5 = Button(field, command=partial(self.clicked, 1, 1))
        self.fb_5.place(x=50, y=50, width=50, height=50)

        self.fb_6 = Button(field, command=partial(self.clicked, 1, 2))
        self.fb_6.place(x=100, y=50, width=50, height=50)

        self.fb_7 = Button(field, command=partial(self.clicked, 2, 0))
        self.fb_7.place(y=100, width=50, height=50)

        self.fb_8 = Button(field, command=partial(self.clicked, 2, 1))
        self.fb_8.place(x=50, y=100, width=50, height=50)

        self.fb_9 = Button(field, command=partial(self.clicked, 2, 2))
        self.fb_9.place(x=100, y=100, width=50, height=50)

        self.win_label.pack(pady=10)
        self.player_label.pack()
        field.pack(padx=50, pady=40)

        thread.start_new_thread(self.execute, ())

        window.mainloop()
        pass
