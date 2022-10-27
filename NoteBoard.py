import Buttons, CoreFuncs
import typing, pygame


# a text box renderer
class Renderer:
    def __init__(self, x, y, sx, sy, text) -> None:
        self.x = x
        self.y = y
        self.sx = sx
        self.sy = sy
        self.text = text

        self.nx = self.x
        self.ny = self.y

    # rendering the box
    def Render(self, id: int, screen: object) -> None:
        # the difference between the new and old x/y
        dx = self.nx - self.x
        dy = self.ny - self.y

        # checking fi the position is close enough to the new one
        if dx < 0.5:
            self.x += dx
        if dy < 0.5:
            self.y += dy

        # interpalating the old and new to smoothly move the box
        self.x = CoreFuncs.Lerp(self.nx, self.x, 0.5)
        self.y = CoreFuncs.Lerp(self.ny, self.y, 0.5)

        # rendering the box and the text
        pygame.draw.rect(screen, (125, 125, 125), [self.nx + 5, self.ny + self.sy - 3, self.sx - 10, 3])
        CoreFuncs.UI.text(screen, self.text, (255, 255, 255), (self.x+5, self.y+5), 20)
    
    # getters and setters/adders for position
    def GetX(self) -> int:
        return self.nx
    def GetY(self) -> int:
        return self.ny
    def SetX(self, x: int) -> None:
        self.nx = x
    def SetY(self, y: int) -> None:
        self.ny = y
    def AddX(self, dx: int) -> None:
        self.nx += dx
    def AddY(self, dy: int) -> None:
        self.ny += dy
    
    # getters for size
    def GetSizeX(self) -> int:
        return self.sx
    def GetSizeY(self) -> int:
        return self.sy


# for rendering notes, just adds rendering stuff
class RendererNote (Renderer):
    # the renderer
    def Render(self, id: int, screen: object) -> None:
        super().Render(id, screen)  # rendering the other stuff

        # the drop down menu for the sub tasks
        CoreFuncs.UI.text(screen, "V", (255, 255, 255), (self.nx + self.sx - 20, self.ny + self.sy - 20), 15)


# update function for notes
def NoteUpdateFunc(boardId: int, self: object, notes: typing.Dict, mouseDown: bool, mx: int, my: int, *args) -> None:
    # getting the box
    box = self.GetBox(boardId)
    
    # checking if the box was clicked
    if mouseDown and box.CheckCollision(mx, my):
        # the objects position
        obX = box.GetX()
        obY = box.GetY()

        # checking if the dropdown menu was clicked
        colLeft = obX + box.GetSizeX() - 20
        colTop  = obY + box.GetSizeY() - 20
        collsionX = CoreFuncs.Range(mx, colLeft, colLeft + 15)
        collsionY = CoreFuncs.Range(my, colTop, colTop + 15)
        if collsionX and collsionY:
            # getting the actual index
            realIndex = self.GetIndex(boardId)

            # checking the size fromt he sub notes, make it go out and change the icon to an up arrow and than when pressed make it go up, also render sub notes when down under the renderer
            size = 40  # just for now
            self.ShiftBoxesY(realIndex, size)

            #CoreFuncs.UI.text(screen, "V", (255, 255, 255), (self.x + self.sx - 20, self.y + self.sy - 20), 15)


# the update function for note boards, take any number of args but only up to my is used
def NoteBoardUndateFunc(boardId: int, self: object, notes: typing.Dict, mouseDown: bool, mx: int, my: int, *args) -> None:
    global currentBoard, currentBoardManager

    # checking if the board was messed with
    if mouseDown and self.GetBox(boardId).CheckCollision(mx, my):
        # setting the active board to this one
        currentBoard = boardId
        # updating the board
        currentBoardManager = GetBoard(notes)


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
        box = Buttons.TextBoxContainer(RendererNote(195, 20 + i * 50, 500, 40, note), updateFunc=NoteUpdateFunc)

        # adding the box
        boxes.append(box)
        i += 1
    
    # returning the noteboard, locked x
    return Buttons.TextBoxCollumnManager(boxes)


# the active board
currentBoard = 0

