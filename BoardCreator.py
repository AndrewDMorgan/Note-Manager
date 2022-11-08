import UI, CoreFuncs, Events, NoteBoard
import pygame, typing, enum


# ---------------------------------------- Typing Creator Stuff ----------------------------------------


# allows creation of typing box to get noteboard/note name/infor
class TypingCreator:
    def __init__(self, screenWidth: int, screenHeight: int) -> None:
        # the typing box
        self.__typingBox = UI.TypingBox(screenWidth//2, screenHeight//2)
        self.__active = False  # the state of it, opened or closed

    # updates the typing box
    def Update(self, events: Events, dt: float, screenWidth: int, screenHeight: int) -> None:
        # updating the position
        self.__typingBox.SetX(screenWidth//2)
        self.__typingBox.SetY(screenHeight//2)

        # checking if the box is active
        if self.__active:
            self.__typingBox.Update(events, dt)
        
        # checking if the typing box should be closed
        if "return" in events.events:
            self.__active = False  # updating the state of typing
    
    # renders the box
    def Render(self, screen: pygame.Surface) -> None:
        # checking fit he box is active
        if self.__active:
            self.__typingBox.Render(screen)

    # getting the text from the typing box
    def GetText(self) -> str:
        return self.__typingBox.GetText()
    
    # getters and setters for the state
    def GetActive(self) -> bool:
        return self.__active
    def SetActive(self, active: bool) -> None:
        self.__active = active
        self.__typingBox.SetText("")  # resetting the text


# manages the typingCreator
class BoardCreator:

    # ---------------- Adder Classes ----------------

    # stores the subnotes and adds to them
    class SubNoteAdder:
        def __init__(self, subNotes: typing.List[str], boxId: int, boardManager: UI.TextBoxCollumnManager) -> None:
            self.__boardManager = boardManager
            self.__subNotes = subNotes
            self.__boxId = boxId
        
        # adding the subnote
        def Add(self, text: str) -> None:
            self.__subNotes.append(text)
            self.__boardManager.ShiftBoxesY(self.__boxId, 20)
    
    # stores the notes and adds one
    class NotesAdder:
        def __init__(self, notes: typing.Dict) -> None:
            self.__notes = notes
        
        # adding the note
        def Add(self, text: str) -> None:
            # adding a number at the end to make the note unique
            num = 0
            newText = text
            while newText in self.__notes:
                num += 1
                newText = text + str(num)
            
            if num > 0:
                text += str(num)

            # adding the note
            self.__notes[text] = {"SubNotes":[]}

            # getting the boxes
            boxes = NoteBoard.currentBoardManager.GetBoxes()

            # finding the lowest box
            if len(boxes) == 0:
                lowest = -30
            else:
                heights = [key.GetY() for key in boxes]
                lowest = max(heights)
                
                # checking if this box is dropped
                boxIndex = heights.index(lowest)
                box = boxes[boxIndex]
                if box.GetRenderer().GetDropped():
                    # getting the sub-notes
                    notes = NoteBoard.noteJson["NoteBoards"][[key for key in NoteBoard.noteJson["NoteBoards"]][NoteBoard.currentBoard]]["Notes"]
                    subNotes = notes[[key for key in notes][NoteBoard.currentBoardManager.GetIndex(boxIndex)]]["SubNotes"]
                    
                    # accounting for the size
                    size = len(subNotes) * 20 + 5
                    if size == 5:
                        size = 0
                    
                    # moving the new box bellow the sub notes
                    lowest += size

            # creating and adding the box
            box = UI.TextBoxContainer(NoteBoard.RendererNote(195, lowest + 50, 500, 40, text, NoteBoard.noteJson["NoteBoards"], len(boxes)), updateFunc=NoteBoard.NoteUpdateFunc)
            NoteBoard.currentBoardManager.AddBox(box)


    # stores and adds a board
    class BoardAdder:
        def __init__(self, boards: typing.Dict) -> None:
            self.boards = boards
        
        # adding the board
        def Add(self, text: str) -> None:
            # adding the board
            self.boards[text] = {"Notes":{}}
            
            # setting up the new board
            NoteBoard.currentBoard = [key for key in self.boards].index(text)
            NoteBoard.noteBoards = NoteBoard.GetNoteBoards(NoteBoard.noteJson["NoteBoards"])


    # ---------------- Main Class Stuff ----------------

        # the state of what is going on
    class States (enum.Enum):
        NONE = 0
        SUBNOTE = 1
        NOTE = 2
        BOARD = 3

    # the constructor
    def __init__(self) -> None:
        self.__state = self.States.NONE
    
    # adds a subnote
    def AddAdder(self, adder: object, state: enum.Enum) -> None:
        # setting the typingCreator to active to get the name
        typingCreator.SetActive(True)
        self.__state = state
        self.__adder = adder
    
    # updating the boardCreator
    def Update(self) -> None:
        # checking if the typing was completed if something is also being added
        if self.__state != self.States.NONE and not typingCreator.GetActive():
            # adding the item
            self.__adder.Add(typingCreator.GetText())
            # updating the state
            self.__state = self.States.NONE



# ---------------------------------------- Upate Functions ----------------------------------------


# update function for creating a new note
def NewNoteUpdateFunc(pressed: bool, button: UI.Button, screenWidth: int, *args) -> None:
    # adjusting the position of the button
    button.SetX(screenWidth - 15 - 21//2)

    # making sure nothing else is using the typingCreator
    if pressed and not typingCreator.GetActive():
        # getting the note boards
        boards = NoteBoard.noteJson["NoteBoards"]
        currentBoardNotes = boards[[key for key in boards][NoteBoard.currentBoard]]["Notes"]
        # adding a new subnote
        boardCreator.AddAdder(BoardCreator.NotesAdder(currentBoardNotes), boardCreator.States.NOTE)


# update function for creating a new note
def NewBoardUpdateFunc(pressed: bool, *args) -> None:
    # making sure nothing else is using the typingCreator
    if pressed and not typingCreator.GetActive():
        # adding a new subnote
        boardCreator.AddAdder(BoardCreator.BoardAdder(NoteBoard.noteJson["NoteBoards"]), boardCreator.States.BOARD)



# ---------------------------------------- Globals ----------------------------------------


# setting up the typing creator
typingCreator = TypingCreator(1200, 750)
boardCreator = BoardCreator()


# buttons, make it so the new tile is rendered on the current board without having to refreshing it
newNoteButton = UI.Button(1200-15-21//2, -1, 45, 45, NewNoteUpdateFunc, UI.ButtonTextRenderer(-15, +20, 45, "+"))
newBoardButton = UI.Button(180-21//2, 26-21//2, 45, 45, NewBoardUpdateFunc, UI.ButtonTextRenderer(180, 26, 45, "+"))

