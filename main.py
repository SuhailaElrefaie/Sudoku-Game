import tkinter as tk
from tkinter import ttk
import random

class setup():
    def __init__(self):
        self.solved_puzzle = [] # Stores the solved sudoku puzzle
        self.filled = [[False for _ in range(9)] for _ in range(9)] # Tracks the filled boxes
        self.checked = [[False for _ in range(9)] for _ in range(9)] # Tracks whether or not the box has been checked
        self.canvas = tk.Canvas(width = 500, height = 520, bg="grey")
        self.canvas.grid(row=1, column=0, columnspan=4, padx=10, pady=10) # Positioning the sudoku grid below
        self.cell = None # Tracks the selected cell
        self.entry = None # Holds the entry widget when clicked
        self.user_input = [[None for _ in range(9)] for _ in range(9)] # Stores the user input
        self.unsolved_puzzle=[[0 for _ in range(9)] for _ in range(9)] # Stores the unsolved puzzle

    def load_puzzles(self,d):
        '''
        Loads a randomly chosen puzzle based on the difficulty level sent from the choices function.
        Calls and sends the puzzle to solve_sudoku and stores the solution in variable solved_puzzle.
        Calls the display_puzzle function.
        '''
        # Opening file with sudoko puzzle samples
        with open('GRIDS.txt', 'r') as file:
            content = file.read().strip().split('Grid ')

            # Choosing random puzzle according to difficulty level
            if d == 'Easy':
                index=random.randint(0,17)
            elif d=='Medium':
                index=random.randint(17,34)
            else:
                index=random.randint(34,51)

            for numbers in content:
                i='' # i represents the sudoko puzzle number in 'file'
                numbers = numbers.strip().replace('\n', ' ') # Removing new lines
                numbers = ''.join([char for char in numbers if char.isdigit()]) # Keeping only digits 
                for num in numbers:
                    i+=num
                    if len(i)==2: # Each number is 2 digits
                        if int(i) == index: # Randomly selected puzzle found
                            puz = numbers[2:] # String of the numbers of our puzzle
                            puz = list(puz) # Converting it to a list of strings

                            # Adding puz into placeholder
                            for row in range(9):
                                for col in range(9):
                                    self.unsolved_puzzle[row][col] = int(puz.pop(0)) # Adding each value
                            
                            self.solved_puzzle = self.solve_sudoku([row[:] for row in self.unsolved_puzzle]) # Solving the puzzle and adding it to our variable

                            if self.solved_puzzle==[] or self.solved_puzzle==None: # If the puzzle is invalid
                                self.load_puzzles(d)
                            else:
                                self.display_puzzle() # Calling method to display the unsolved puzzle
                            return

    def solve_sudoku(self, board):
        '''
        Solves the sudoku puzzle that was randomly chosen.
        This function is called on by the load_puzzles function.
        '''
        for row in range(9):
            for col in range(9):
                if board[row][col] == 0: # Unsolved cell
                    
                    for num in range(1, 10): # Placing the numbers from 1-9
                        row_check = all(board[row][i] != num for i in range(9)) # No duplicate numbers in the row
                        col_check = all(board[i][col] != num for i in range(9)) # No duplicate numbers in the column

                        # Determining the starting imdex of the 3x3 subgrid
                        start_row = (row // 3) * 3
                        start_col = (col // 3) * 3

                        box_check = True
                        for r in range(start_row, start_row + 3): # Checking duplicates in the row of the box cell
                            for c in range(start_col, start_col + 3): # Checking duplicates in the column of the box cell
                                if board[r][c] == num:
                                    box_check = False # Invalid number
                                    break
                            if not box_check:
                                break
                        
                        if row_check and col_check and box_check: # Valid number
                            board[row][col] = num
                            result = self.solve_sudoku(board) # Recursivly repeating the code for the rest of the cells
                            if result:
                                return result                            
                            board[row][col] = 0
                    return None
        return board

    def line(self, x1, y1, x2, y2, **args): # Lines that will make the grid
        self.canvas.create_line(coord(x1), coord(y1), coord(x2), coord(y2), **args)

    def display_grid(self):
        '''
        Displays a 9x9 sudoku grid using the line function.
        '''
        for i in range(10):
            if i==0 or i == 3 or i== 6 or i==9:
                self.line(i,0,i,9,width=3,fill="purple") # Thick purple vertical line
                self.line(0,i,9,i,width=3,fill="purple") # Thick purple horizontal lines
            else:
                self.line(i,0,i,9) # Vertical line
                self.line(0,i,9,i) # Horizontal lines
    
    def choices(self):
        '''
        Displays the difficulty buttons the user selects from. Once selected, the display_puzzle function is called.
        Displays the Check Puzzle button that, when clicked, calls the check_puzzle function.
        '''
        diff = ['Easy', 'Medium', 'Hard']
        ttk.Label(root, text='Select Difficulty:').grid(row=0, column=0) # Label for difficulty

        button_frame = ttk.Frame(root) # Making the buttons close together
        button_frame.grid(row=0, column=1, sticky='W')

        for i, c in enumerate(diff):
            b = ttk.Radiobutton(button_frame, text=c, value=c, command=lambda d=c: a.load_puzzles(d)) # Sends the selection to the load_puzzles method
            b.grid(row=0, column=i, padx=10, sticky='W')
        
        ttk.Button(root, text='Check Puzzle', command=self.check_puzzle).grid(row=9, column=1, sticky='W', padx=45) # Check puzzle button

    def display_puzzle(self):
        '''
        Displays the pre-filled puzzle numbers on the grid boxes.
        This function is called on by the load_puzzles function. 
        Allows the cell_click function to be called when activated by the button.
        '''
        self.canvas.delete("all") # Clearing the current puzzle
        self.filled=[[False for _ in range(9)] for _ in range(9)] # Clearing the filled cells
        self.user_input = [[None for _ in range(9)] for _ in range(9)] # Reseting user inputs
        self.display_grid() # Displaying the grid again
        for i in range(9):
            for j in range(9):
                num = self.unsolved_puzzle[i][j]
                # Calculating the x, y coordinates for the center of the cell
                x = coord(j) + SQUARE // 2
                y = coord(i) + SQUARE // 2

                # Displaying the number on the canvas based on difficulty chosen
                if num!=0:
                    self.canvas.create_text(x, y, text=num, font=("Times New Roman", 20), fill="purple")
                    self.filled[i][j]=True
    
        a.canvas.bind("<Button>", a.cell_click)

    def cell_click(self, event):
        '''
        Allows the user to click on any empty box.
        Allows the submit_entry function to be called.
        '''
        x, y = event.x, event.y
        # Determining which cell is clicked
        row = (event.y - MARGIN) // SQUARE 
        col = (event.x - MARGIN) // SQUARE

        if 0 <= row < 9 and 0 <= col < 9:
            if not self.filled[row][col]: # Clicking on the non-filled cells
                self.cell = (row, col) # Storing the selected cell coordinates
                
                # Removing old entry widget
                if self.entry:
                    self.entry.destroy()
                
                # Deleting old input
                self.canvas.delete("all") # Deleting all items on the canvas
                self.display_grid() # Re-dsiplaying the grid
                for i in range(9):
                    for j in range(9):
                        m = coord(j) + SQUARE // 2
                        k = coord(i) + SQUARE // 2
                        num = self.unsolved_puzzle[i][j]
                        if num!=0:
                            self.canvas.create_text(m, k, text=num, font=("Times New Roman", 20), fill="purple") # Re-displaying the unsolved puzzle
                        if self.filled[i][j] !=False and self.checked[i][j]==True:
                            self.canvas.create_text(m, k, text=self.user_input[i][j], font=("Times New Roman", 20), fill="purple") # Re-displaying the user's correct inputs
                        if self.filled[i][j] !=False and self.checked[i][j]!=True:
                            self.canvas.create_text(m, k, text=self.user_input[i][j], font=("Times New Roman", 20), fill="white") # Re-displaying the user's unchecked inputs


                self.entry = ttk.Entry(root)
                self.entry.place(x=coord(col), y=coord(row), width=SQUARE, height=SQUARE)
                self.entry.focus_set()

                self.entry.bind("<Return>", self.submit_entry)
        else:
            # User clicking outside the grid
            if self.entry:
                self.entry.destroy()
            self.entry = None
            self.cell = None

    def submit_entry(self, event):
        '''
        Allows the user to write his solutions in the chosen box.
        '''
        row, col = self.cell
        try:
            num = int(self.entry.get())
            if num <1 or num > 9:
                return
        except ValueError:
            return

        self.user_input[row][col] = num # Storing the user's input
        x = coord(col) + SQUARE // 2
        y = coord(row) + SQUARE // 2

        self.canvas.create_text(x, y, text=num, font=("Times New Roman", 20), fill="white") # Displaying the number on the canvas
        self.filled[row][col] = True
        self.entry.destroy()
        self.entry = None # Reset the entry widget
        self.cell = None # Reset selected cell

    def check_puzzle(self):
        '''
        Updates the grid based on whether the user's answers are correct or not.
        Activated by the Check Puzzle button.
        Displays 'Congratulations' when the puzzle is solved.
        '''
        count=0 # The correct numbers on the board
        for i in range(9):
            for j in range(9):
                if self.user_input[i][j] !=None:
                    x = coord(j) + SQUARE // 2
                    y = coord(i) + SQUARE // 2
                    if self.solved_puzzle[i][j] == self.user_input[i][j]: # If user input is correct
                        self.canvas.create_text(x, y, text=self.user_input[i][j], font=("Times New Roman", 20), fill="purple")
                        self.checked[i][j]=True
                        count+=1
                    else: # If user input is incorrect
                        self.canvas.create_text(x, y, text=self.user_input[i][j], font=("Times New Roman", 20), fill="red")
                        self.checked[i][j]=False
                        self.user_input[i][j]=None
                        self.filled[i][j] = False # Allowing user to re-attempt answer
                elif self.unsolved_puzzle[i][j]!=0:
                    count+=1
        if count==81: # Puzzle complete
            self.canvas.create_text(250, 500, text="Congratulations!", font=("Times New Roman", 20), fill="purple")

root = tk.Tk()
root.title('SUDOKU')
root.geometry('525x615')

MARGIN = 20 # Margin size in pixels
SQUARE = 50 # Square size in pixels
BOARD_SIZE = 9 * SQUARE + 2 * MARGIN

def coord(x): # map user coordinates to canvas coordinates
    return MARGIN + SQUARE * x

a = setup()
a.choices()
a.display_grid()
root.mainloop()

