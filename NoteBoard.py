import Buttons, CoreFuncs
import typing, pygame


# ---------------------------------------- Renderers ----------------------------------------


# a text box renderer
class Renderer:
    def __init__(self, x, y, sx, sy, text) -> None:
        self.__x = x
        self.__y = y
        self.__sx = sx
        self.__sy = sy
        self.__text = text

        self.__nx = self.__x
        self.__ny = self.__y

    # rendering the box
    def Render(self, boardId: int, screen: object, fadedText: typing.Tuple[int] = (200, 200, 200), *args) -> None:
        # the difference between the new and old x/y
        dx = self.__nx - self.__x
        dy = self.__ny - self.__y

        # checking fi the position is close enough to the new one
        if dx < 0.5:
            self.__x += dx
        if dy < 0.5:
            self.__y += dy

        # interpalating the old and new to smoothly move the box
        self.__x = CoreFuncs.Lerp(self.__nx, self.__x, 0.5)
        self.__y = CoreFuncs.Lerp(self.__ny, self.__y, 0.5)

        # the color of the text
        textColor = (255, 255, 255)

        # checking if this is the active board
        if currentBoard != boardId:
            textColor = fadedText

        # rendering the box and the text
        pygame.draw.rect(screen, (125, 125, 125), [self.__nx + 5, self.__ny + self.__sy - 3, self.__sx - 10, 3])
        CoreFuncs.UI.text(screen, self.__text, textColor, (self.__x + 5, self.__y + 5), 20)
    
    # getters and setters/adders for position
    def GetX(self) -> int:
        return self.__nx
    def GetY(self) -> int:
        return self.__ny
    def GetOldX(self) -> int:
        return self.__x
    def GetOldY(self) -> int:
        return self.__y
    def SetX(self, x: int) -> None:
        self.__nx = x
    def SetY(self, y: int) -> None:
        self.__ny = y
    def AddX(self, dx: int) -> None:
        self.__nx += dx
    def AddY(self, dy: int) -> None:
        self.__ny += dy
    
    # getters for size
    def GetSizeX(self) -> int:
        return self.__sx
    def GetSizeY(self) -> int:
        return self.__sy
    
    # updating stuff when moved
    def Moved(self, *args) -> None:
        pass  # doing nothing


# for rendering notes, just adds rendering stuff
class RendererNote (Renderer):
    def __init__(self, x, y, sx, sy, text, noteJson: typing.Dict, noteId: int) -> None:
        super().__init__(x, y, sx, sy, text)

        # if the sub-nots is dropped down or not
        self.__droppedDown = False

        # the dict for notes
        self.__noteJson = noteJson
        
        # the id of the note
        self.__noteId = noteId
    
    # the renderer
    def Render(self, boardId: int, screen: object, *args) -> None:
        # rendering the general stuff
        super().Render(id, screen, fadedText=(255, 255, 255))
        
        # getting the char for the drop down button
        char = "v"  # down button
        if self.__droppedDown:
            char = "^"  # up button

            # rendering a + to add a sub note
            CoreFuncs.UI.text(screen, f"+", (255, 255, 255), (self.GetX() + self.GetSizeX() - 20, self.GetY() + self.GetSizeY()), 20)

            # rendering the sub notes
            notes = self.__noteJson[[key for key in self.__noteJson][currentBoard]]["Notes"]
            subNotes = notes[[key for key in notes][self.__noteId]]["SubNotes"]

            # looping through all the sub notes
            i = 0
            for subNote in subNotes:
                CoreFuncs.UI.text(screen, f"    • {subNote}", (255, 255, 255), (self.GetX() + 5, self.GetY() + 45 + i * 20), 15)
                i += 1   # incrementing i
        
        # renderering the button for the drop down menu
        CoreFuncs.UI.text(screen, char, (255, 255, 255), (self.GetX() + self.GetSizeX() - 20, self.GetY() + self.GetSizeY() - 20), 15)
    
    # updating the drop down menus when the box is moved
    def Moved(self, this: object, boxId: int, *args) -> None:
        # getting the real index
        realIndex = this.GetIndex(boxId)

        # checking if the menu is down
        if self.__droppedDown:
            # resseting the position
            self.__droppedDown = False

            # getting the size of the drop down
            notes = self.__noteJson[[key for key in self.__noteJson][currentBoard]]["Notes"]
            subNotes = notes[[key for key in notes][self.__noteId]]["SubNotes"]

            size = len(subNotes) * 20 + 5
            if size == 5:
                size = 0

            # moving the boxes
            this.ShiftBoxesY(realIndex, -size)

    # gets/sets if the sub-notes is dropped
    def GetDropped(self) -> bool:
        return self.__droppedDown
    def SetDropped(self, dropped: bool) -> None:
        self.__droppedDown = dropped



# ---------------------------------------- Update Functions ----------------------------------------


# update function for notes
def NoteUpdateFunc(boxId: int, self: object, notes: typing.Dict, mouseDown: bool, mx: int, my: int, *args) -> None:
    # getting the box
    box = self.GetBox(boxId)

    # the renderer
    renderer = box.GetRenderer()

    # getting the actual index
    realIndex = self.GetIndex(boxId)
    
    # checking if the box was clicked
    if mouseDown:
        # the objects position
        obX = box.GetX()
        obY = box.GetY()
        
        # checking if the dropdown menu or +sub note was clicked
        colLeft = obX + box.GetSizeX() - 20
        colTop  = obY + box.GetSizeY() - 20
        collisionX = CoreFuncs.Range(mx, colLeft, colLeft + 15)
        collisionY = CoreFuncs.Range(my, colTop, colTop + 15)
        collisionY2 = CoreFuncs.Range(my, colTop + 20, colTop + 35)  # collision for new sub note

        # checking if the dropdown button was pressed
        if collisionX and collisionY:
            # getting the size of the drop down
            notes = notes[[key for key in notes][currentBoard]]["Notes"]
            subNotes = notes[[key for key in notes][boxId]]["SubNotes"]

            size = len(subNotes) * 20 + 5
            if size == 5:
                size = 0

            # checking if its dropped or undropped
            if renderer.GetDropped():
                # moving the boxes to the correct positions
                self.ShiftBoxesY(realIndex, -size)

                # swapping the dropped state
                renderer.SetDropped(False)
            else:
                # moving the boxes to the correct positions
                self.ShiftBoxesY(realIndex, size)

                # swapping the dropped state
                renderer.SetDropped(True)
        # checking if the new sub note button was pressed
        elif renderer.GetDropped() and collisionX and collisionY2:
            print("adding note")


# the update function for note boards, take any number of args but only up to my is used
def NoteBoardUndateFunc(boardId: int, self: object, notes: typing.Dict, mouseDown: bool, mx: int, my: int, *args) -> None:
    global currentBoard, currentBoardManager

    # checking if the board was messed with
    if mouseDown and self.GetBox(boardId).CheckCollision(mx, my):
        # setting the active board to this one
        currentBoard = boardId
        # updating the board
        currentBoardManager = GetBoard(notes)



# ---------------------------------------- Data Loading/Parsing ----------------------------------------


# sets up the noteboard
def GetNoteBoards(noteBoards: typing.Dict) -> Buttons.TextBoxCollumnManager:
    # setting the current board
    global currentBoard, currentBoardManager
    currentBoardManager = GetBoard(noteBoards)
    
    # the note boards
    boxes = []

    # looping through all the note boards
    i = 0
    for board in noteBoards:
        box = Buttons.TextBoxContainer(Renderer(10, 10 + i * 40, 175, 40, board), updateFunc=NoteBoardUndateFunc)

        # adding the box
        boxes.append(box)
        i += 1
    
    # returning the noteboard, locked x
    return Buttons.TextBoxCollumnManager(boxes)


def GetBoard(noteBoards: typing.Dict) -> Buttons.TextBoxCollumnManager:
    # getting the notes for the note board
    notes = noteBoards[[key for key in noteBoards][currentBoard]]["Notes"]

    # the note boards
    boxes = []

    # looping through all the note boards
    i = 0
    for note in notes:
        box = Buttons.TextBoxContainer(RendererNote(195, 20 + i * 50, 500, 40, note, noteBoards, i), updateFunc=NoteUpdateFunc)

        # adding the box
        boxes.append(box)
        i += 1
    
    # returning the noteboard, locked x
    return Buttons.TextBoxCollumnManager(boxes)



# ---------------------------------------- Setting Data ----------------------------------------


# adds a new noteboard
def AddNoteBoard(notesJson: typing.Dict, boardName: str) -> None:
    # looping until a unique name is found
    i = 0
    found = False
    while not found:
        # checking if the name is already in the json
        if boardName in notesJson["NoteBoards"]:
            i += 1
        else:
            found = True

    # adding the board
    notesJson["NoteBoards"][boardName + i] = {}


# adds a note
def AddNote(notesJson: typing.Dict, boardName: str, noteName: str, subNotes: typing.List[str] = []) -> None:
    notesJson["NoteBoards"][boardName]["Notes"][noteName] = {"SubNotes": subNotes}


# adds a sub note
def AddSubNote(notesJson: typing.Dict, boardName: str, noteName: str, newSubNotes: typing.List[str]) -> None:
    [notesJson["NoteBoards"][boardName]["Notes"][noteName]["SubNotes"].append(note) for note in newSubNotes]



# ---------------------------------------- Globals ----------------------------------------


# the active board
currentBoard = 0

