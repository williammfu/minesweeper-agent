'''
gui.py

the following file is used to define
the agent's GUI
'''

# Python Standard Library imports
import tkinter as tk
from constant import *

class Board(tk.Tk):

    def __init__(self, all_states, opened_tiles, *args, **kwargs):
        self.dark_mode = not False
        self.BG_COLOR = '#000' if self.dark_mode else '#fff'
        self.TEXT_COLOR = '#fff' if not self.dark_mode else '#fff'
        self.COLORS = ['#4285F4', '#F4B400', '#0F9D58', '#DB4437', '#DB4437', '#DB4437', '#DB4437', '#DB4437']
        self.OUTLINE_COLOR = '#fff' if self.dark_mode else "#000"

        tk.Tk.__init__(self, *args, **kwargs)
        self.title("MineSweeper AI")
        self.resizable(False, False)
        self.configure(bg=self.BG_COLOR)
        print(opened_tiles)
        self.states = all_states
        self.opened_tiles = opened_tiles
        self.moves = len(all_states) if len(all_states) >= len(opened_tiles) else len(opened_tiles)
        self.current_move = 0
        self.board = all_states[self.current_move]
        self.b_size = len(self.board)

        self.prev_button = tk.Button(self, anchor="c", font=(None, 16),
            bg=self.COLORS[1], fg=self.TEXT_COLOR, text="Prev move", command=lambda: self.change_move(self.current_move - 1))
        self.next_button = tk.Button(self, anchor="c", font=(None, 16),
            bg=self.COLORS[0], fg=self.TEXT_COLOR, text="Next move", command=lambda: self.change_move(self.current_move + 1))
        self.init_button = tk.Button(self, anchor="c", font=(None, 16),
            bg=self.COLORS[3], fg=self.TEXT_COLOR, text="Final state", command=lambda: self.change_move(self.moves))
        self.final_button = tk.Button(self, anchor="c", font=(None, 16),
            bg=self.COLORS[3], fg=self.TEXT_COLOR, text="Initial state", command=lambda: self.change_move(0))

        self.prev_button.grid(row=2, column=0, columnspan=(self.b_size + 5)//4)
        self.next_button.grid(row=2, column=(self.b_size + 5)//4, columnspan=(self.b_size + 5)//4)
        self.init_button.grid(row=2, column=2*(self.b_size + 5)//4, columnspan=(self.b_size + 5)//4)
        self.final_button.grid(row=2, column=3*(self.b_size + 5)//4, columnspan=(self.b_size + 5)//4)

        self.canvas = tk.Canvas(self, width=550, height=550, background=self.BG_COLOR, highlightthickness=0)
        self.canvas.grid(row=7, column=2, columnspan=self.b_size, rowspan=self.b_size)

        self.status = tk.Button(self, anchor="c", font=(None, 12), bg=self.COLORS[0], fg=self.TEXT_COLOR, text="MineSweeper", command=self.toggle_theme)
        self.status.grid(row=0, column=0, columnspan=self.b_size + 5, sticky="ewns")

        self.progress = tk.Label(self, anchor="c", font=(None, 16), bg=self.BG_COLOR, fg=self.COLORS[2], text="Recent opened location: (0, 0)")
        self.progress.grid(row=1, column=0, columnspan=self.b_size + 5, sticky="ewns")

        self.canvas.bind("<Configure>", self.draw_tiles)
        self.columnconfigure(0, minsize=48)
        self.rowconfigure(3, minsize=0.5*48)
        self.columnconfigure(self.b_size + 4, minsize=48)
        self.rowconfigure(self.b_size + 10, minsize=48)


    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.BG_COLOR = '#000' if self.dark_mode else '#fff'
        self.TEXT_COLOR = '#fff' if self.dark_mode else '#fff'
        self.OUTLINE_COLOR = '#fff' if self.dark_mode else "#000"
        self.prev_button.config(fg=self.TEXT_COLOR)
        self.next_button.config(fg=self.TEXT_COLOR)
        self.final_button.config(fg=self.TEXT_COLOR)
        self.init_button.config(fg=self.TEXT_COLOR)
        self.status.config(fg=self.TEXT_COLOR)
        self.canvas.config(background=self.BG_COLOR)
        self.progress.config(bg=self.BG_COLOR)
        self.configure(bg=self.BG_COLOR)
        self.draw_tiles()


    def change_move(self, adv_move):
        if adv_move >= self.moves:
            self.current_move = self.moves - 1
        elif adv_move < 0:
            self.current_move = 0
        else:
            self.current_move = adv_move
        self.board = self.states[self.current_move]

        if self.current_move == 0:
            self.status.configure(text="MineSweeper", bg=self.COLORS[0])
            self.progress.configure(text='Recent opened location: (0, 0)', fg=self.COLORS[2])
        elif self.current_move == self.moves - 1:
            all_bomb_location = self.get_all_bomb_location(self.current_move)
            self.status.configure(text="Final bombs: " + all_bomb_location, font=(None, 12), bg=self.COLORS[2])
            text, color = self.get_prev_location(self.current_move)
            self.progress.configure(text=text, fg=color)
        else:
            all_bomb_location = self.get_all_bomb_location(self.current_move)
            self.status.configure(text="Current bombs: " + all_bomb_location, font=(None, 12), bg=self.COLORS[1])
            text, color = self.get_prev_location(self.current_move)
            self.progress.configure(text=text, fg=color)

        self.draw_tiles()

    def get_prev_location(self, time):
        if self.opened_tiles[time][0] == -9 and self.opened_tiles[time][1] == -9:
            return 'New flag', self.COLORS[5]
        return 'Recent opened location: ' + str(self.opened_tiles[time]), self.COLORS[2]

    def get_all_bomb_location(self, time):
        board = self.states[time]
        new = [(i, j) for i in range(len(board)) for j in range(len(board[i])) if board[i][j] == FLAGGED]
        string = ""
        for n in new:
            string += "(" + str(n[0]) + ", " + str(n[1]) + ")"
        return string


    def draw_tiles(self, event = None, board=None):
        if board is not None:
            self.board = board

        # self.canvas.delete("tile")
        cell_width = int(self.canvas.winfo_width() / self.b_size)
        cell_height = int(self.canvas.winfo_height() / self.b_size)
        border_size = 2

        for col in range(self.b_size):
            for row in range(self.b_size):

                board_tile = self.board[row][col]                
                x1 = col * cell_width + border_size / 2
                y1 = row * cell_height + border_size / 2
                x2 = (col + 1) * cell_width - border_size / 2
                y2 = (row + 1) * cell_height - border_size / 2

                if self.opened_tiles[self.current_move][1] == col and self.opened_tiles[self.current_move][0] == row:
                    self.canvas.create_rectangle(x1, y1, x2, y2,
                        tags="tile", width=border_size, outline=self.OUTLINE_COLOR, fill=self.OUTLINE_COLOR)
                elif board_tile == CLOSED:
                    self.canvas.create_rectangle(x1, y1, x2, y2,
                        tags="tile", width=border_size, outline=self.OUTLINE_COLOR, fill=self.COLORS[2])
                else:
                    self.canvas.create_rectangle(x1, y1, x2, y2,
                        tags="tile", width=border_size, outline=self.OUTLINE_COLOR, fill=self.BG_COLOR)
 
                if board_tile == -1 :
                    self.canvas.create_rectangle(x1, y1, x2, y2,
                        tags="tile", width=border_size, outline=self.OUTLINE_COLOR, fill=self.COLORS[5])

        self.draw_pieces()


    def draw_pieces(self, board=None):

        if board is not None:
            self.board = board

        cell_width = int(self.canvas.winfo_width() / self.b_size)
        cell_height = int(self.canvas.winfo_height() / self.b_size)
        border_size = 20

        for col in range(self.b_size):
            for row in range(self.b_size):

                board_tile = self.board[row][col]

                x1 = col * cell_width + border_size / 2
                y1 = row * cell_height + border_size / 2
                x2 = (col + 1) * cell_width - border_size / 2
                y2 = (row + 1) * cell_height - border_size / 2
                
                if board_tile == -1:
                    piece = self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, font="36",
                        text=FLAG, fill=self.BG_COLOR)
                elif board_tile != 0 and board_tile != -999:
                    piece = self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, font="36",
                        text=str(board_tile), fill=self.COLORS[board_tile - 1])
                else:
                    continue                
                self.canvas.tag_bind(piece, "<1>")

        self.update()
