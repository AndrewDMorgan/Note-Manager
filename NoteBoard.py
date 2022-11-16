import UI, CoreFuncs, Events, BoardCreator
import typing, pygame, math


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
    def Render(self, boardId: int, screen: object, dt: float, screenWidth: int, screenHeight: int, fadedText: typing.Tuple[int] = (200, 200, 200), *args) -> None:
        # the difference between the new and old x/y
        dx = self.__nx - self.__x
        dy = self.__ny - self.__y

        # checking if the position is close enough to the new one
        if abs(dx) < 0.5:
            self.__x += dx
        if abs(dy) < 0.5:
            self.__y += dy

        # interpalating the old and new to smoothly move the box
        self.__x = CoreFuncs.Lerp(self.__x, self.__nx, dt * 25)
        self.__y = CoreFuncs.Lerp(self.__y, self.__ny, dt * 25)

        # the color of the text
        textColor = (255, 255, 255)

        # checking if this is the active board
        if currentBoard != boardId:
            textColor = fadedText

        # rendering the box and the text
        pygame.draw.rect(screen, (125, 125, 125), [self.__nx + 5, self.__ny + self.__sy - 3, self.__sx - 10, 3], border_radius=1)
        pygame.draw.circle(screen, (125, 125, 125), (self.GetX() + 17, self.GetY() + 15), 8, 2)
        UI.UI.Text(screen, self.__text, textColor, (self.__x + 30, self.__y + 5), 20)
    
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

    # removing the thing attached
    def Del(self) -> None:
        pass


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

        # the changing in size
        self.sizeOssolation = 0

        # the rate of fading/the fade animation
        self.__fadeRate = 1  # no fading
        self.__faded = 1  # the amount of fading

        # the fade rates and fading amount for sub-notes
        self.__subFadeRate = []
        self.__subFaded = []
    
    # the renderer
    def Render(self, boardId: int, screen: object, dt: float, screenWidth: int, screenHeight: int, events: Events, *args) -> None:
        # rendering the general stuff
        super().Render(id, screen, dt, screenWidth, screenHeight, fadedText=(255, 255, 255))
        
        # getting the subnotes
        notes = self.__noteJson[[key for key in self.__noteJson][currentBoard]]["Notes"]
        subNotes = notes[[key for key in notes][self.__noteId]]["SubNotes"]
        
        # updating the subnote fading incase a new one was added
        while len(self.__subFadeRate) != len(subNotes):
            self.__subFadeRate.append(1)
            self.__subFaded.append(1)

        # rendering the check mark
        checkScalar = min((1 - self.__faded) + 0.5, 1)
        checkSize = round(checkScalar * 15)
        if checkSize >= 1:
            UI.UI.Text(screen, "√", (55, 200, 55), (self.GetX() + 17, self.GetY() + 15), checkSize, center=True, trans=255*checkScalar)

        # updating the fading
        self.__faded *= 1 - ((1 - self.__fadeRate) * dt * 60)
        
        # updating the fading for the subnotes
        for subI in range(len(self.__subFadeRate)):
            self.__subFaded[subI] *= 1 - ((1 - self.__subFadeRate[subI]) * dt * 60)

        # the change in height to account for the height differece between v and ^
        heightChange = 0
        plusSprite = None

        # getting the char for the drop down button
        char = "v"  # down button
        if self.__droppedDown:
            char = "^"  # up button
            heightChange = -4

            # rendering a + to add a sub note
            plusSprite = UI.UI.Text(screen, f"+", (55, 165, 55), (self.GetX() + self.GetSizeX() - 20, self.GetY() + self.GetSizeY()), 30)

            # looping through all the sub notes
            i = 0
            for subNote in subNotes:
                # rendering the check (when completing sub-notes)
                checkScalar = min((1 - self.__subFaded[i]) + 0.5, 1)
                checkSize = round(checkScalar * 15)
                if checkSize >= 1:
                    UI.UI.Text(screen, "√", (55, 200, 55), (self.GetX() + 29, self.GetY() + 53 + i * 20), checkSize, center=True, trans=255*checkScalar)

                # rendering the subnotes
                pygame.draw.circle(screen, (255, 175, 55), (self.GetX() + 29, self.GetY() + 54 + i * 20), 6, 2)
                UI.UI.Text(screen, f"• {subNote}", (255, 175, 55), (self.GetX() + 40, self.GetY() + 45 + i * 20), 15)
                i += 1   # incrementing i
        
        # renderering the button for the drop down menu
        arrowSprite = UI.UI.Text(screen, char, (255, 55, 55), (self.GetX() + self.GetSizeX() - 20, self.GetY() + self.GetSizeY() - 25 - heightChange), 20)

        left = self.GetX() + self.GetSizeX() - 20
        top  = self.GetY() + self.GetSizeY() - 25
        if arrowSprite.collidepoint(events.mouseX, events.mouseY):
            # making it change sizes slowely
            self.sizeOssolation += dt * 2
            # rendering the circle
            pygame.draw.circle(screen, (255, 255, 255), [left + 6, top + 11], 10 + math.cos(self.sizeOssolation) * 2, 2)
        elif plusSprite != None and plusSprite.collidepoint(events.mouseX, events.mouseY):
            # making it change sizes slowely
            self.sizeOssolation += dt * 2
            # rendering the circle
            pygame.draw.circle(screen, (255, 255, 255), [left + 7, top + 11 + 29], 10 + math.cos(self.sizeOssolation) * 2, 2)
        else:
            # removing any size change
            self.sizeOssolation = 0

    # updating the drop down menus when the box is moved
    def Moved(self, this: object, boxId: int, *args) -> None:
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
            this.ShiftBoxesY(boxId, -size)

    # gets/sets if the sub-notes is dropped
    def GetDropped(self) -> bool:
        return self.__droppedDown
    def SetDropped(self, dropped: bool) -> None:
        self.__droppedDown = dropped

        # getting the subnotes
        notes = self.__noteJson[[key for key in self.__noteJson][currentBoard]]["Notes"]
        subNotes = notes[[key for key in notes][self.__noteId]]["SubNotes"]

        # adding their fading value things
        self.__subFaded = []
        self.__subFadeRate = []
        for i in range(len(subNotes)):
            self.__subFadeRate.append(1)
            self.__subFaded.append(1)

    # removing the note
    def Del(self) -> None:
        # making it so the note fades in some manner (maybe a movement or something)
        self.__fadeRate = 0.85
    def DelSubNote(self, i: int) -> None:
        self.__subFadeRate[i] = 0.85
    
    # gets the fading amount
    def GetFade(self) -> float:
        return self.__faded
    def GetSubFades(self) -> typing.List[float]:
        return self.__subFaded
    def RemoveSubFading(self, i: int) -> None:
        del self.__subFadeRate[i]
        del self.__subFaded[i]
    
    # adds to the note id
    def AddNoteId(self, dif: int) -> None:
        self.__noteId += dif



# ---------------------------------------- Update Functions ----------------------------------------


# update function for notes
def NoteUpdateFunc(boxId: int, events: Events, self: object, *args) -> None:
    # getting the box
    box = self.GetBox(boxId)

    # the renderer
    renderer = box.GetRenderer()

    # getting the actual index
    realIndex = self.GetIndex(boxId)
    
    # getting the notes and sub notes
    notes = noteJson["NoteBoards"][[key for key in noteJson["NoteBoards"]][currentBoard]]["Notes"]
    note = notes[[key for key in notes][boxId]]
    subNotes = note["SubNotes"]

    # checking if the box was clicked
    if events.mouseDown:
        # the objects position
        obX = box.GetX()
        obY = box.GetY()

        # checking if the dropdown menu or +sub note was clicked
        colLeft = obX + box.GetSizeX() - 20
        colTop  = obY + box.GetSizeY() - 25
        collisionX = CoreFuncs.Range(events.mouseX, colLeft, colLeft + 20)
        collisionY = CoreFuncs.Range(events.mouseY, colTop, colTop + 22)
        collisionY2 = CoreFuncs.Range(events.mouseY, colTop + 25, colTop + 50)  # collision for new sub note

        #pygame.draw.circle(screen, (125, 125, 125), (self.GetX() + 17, self.__y + 15), 8, 2)
        completionCollisionX = CoreFuncs.Range(events.mouseX, obX + 9, obX + 25)
        completionCollisionY = CoreFuncs.Range(events.mouseY, obY + 7, obY + 23)

        # checking if the dropdown button was pressed
        if collisionX and collisionY:
            # getting the size of the drop down
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
            # making sure nothing else is using the typingCreator
            if not BoardCreator.typingCreator.GetActive():
                # adding a new subnote
                BoardCreator.boardCreator.AddAdder(BoardCreator.BoardCreator.SubNoteAdder(subNotes, boxId, self), BoardCreator.boardCreator.States.SUBNOTE)
        # checking if the completion button was pressed
        elif completionCollisionX and completionCollisionY:
            renderer.Del()  # removing the note
        else:
            # going through all the sub notes and checking if any of them have been completed
            for i in range(len(subNotes)):
                #pygame.draw.circle(screen, (255, 175, 55), (self.GetX() + 29, self.GetY() + 45 + i * 20 + 9), 6, 2)
                centerX = obX + 29
                centerY = obY + 54 + i * 20
                colX = CoreFuncs.Range(events.mouseX, centerX - 6, centerX + 6)
                colY = CoreFuncs.Range(events.mouseY, centerY - 6, centerY + 6)
                if colX and colY:
                    # adding the note to the fading notes
                    renderer.DelSubNote(i)
    
    # removing the note if the fade animation is complete
    fadeAmount = renderer.GetFade()
    if fadeAmount <= 0.05:
        # getting the size of the drop down
        size = len(subNotes) * 20 + 5
        if size == 5 or not renderer.GetDropped():
            size = 0

        size += 50  # the size of a note

        # moving the boxes to the correct positions
        self.ShiftBoxesY(realIndex, -size)

        # swapping the dropped state
        renderer.SetDropped(False)

        # removing the note from the json
        del notes[[key for key in notes][boxId]]

        # removing the note from the board manager
        self.RemoveBox(boxId)
    
    # checking if any subnotes need removing
    i = 0
    for subFade in renderer.GetSubFades():
        # checking if the subnote has fully faded
        if subFade <= 0.05:
            # removing the subnote from the json
            del subNotes[i]

            # shifting the boxes to match it
            self.ShiftBoxesY(realIndex, -20)
            if len(subNotes) == 0:
                self.ShiftBoxesY(realIndex, -5)
            
            # updating the fade rates and fading of the subnotes
            renderer.RemoveSubFading(i)

            # correcting the index for the removed subnote
            i -= 1
        i += 1


# the update function for note boards, take any number of args but only up to my is used
def NoteBoardUndateFunc(boardId: int, events: Events, self: object, notes: typing.Dict, *args) -> None:
    global currentBoard, currentBoardManager

    # checking if the board was messed with
    if events.mouseDown and self.GetBox(boardId).CheckCollision(events.mouseX, events.mouseY):
        # setting the active board to this one
        currentBoard = boardId
        # updating the board
        currentBoardManager = GetBoard(notes)



# ---------------------------------------- Data Loading/Parsing ----------------------------------------


# sets up the noteboard
def GetNoteBoards(noteBoards: typing.Dict) -> UI.TextBoxCollumnManager:
    # setting the current board
    global currentBoard, currentBoardManager
    currentBoardManager = GetBoard(noteBoards)
    
    # the note boards
    boxes = []

    # looping through all the note boards
    i = 0
    for board in noteBoards:
        box = UI.TextBoxContainer(Renderer(10, 10 + i * 40, 175, 40, board), updateFunc=NoteBoardUndateFunc)

        # adding the box
        boxes.append(box)
        i += 1
    
    # returning the noteboard, locked x
    return UI.TextBoxCollumnManager(boxes)


# getts the note objects from the given board
def GetBoard(noteBoards: typing.Dict) -> UI.TextBoxCollumnManager:
    # getting the notes for the note board
    notes = noteBoards[[key for key in noteBoards][currentBoard]]["Notes"]

    # the note boards
    boxes = []

    # looping through all the note boards
    i = 0
    for note in notes:
        box = UI.TextBoxContainer(RendererNote(195, 20 + i * 50, 500, 40, note, noteBoards, i), updateFunc=NoteUpdateFunc)

        # adding the box
        boxes.append(box)
        i += 1
    
    # returning the noteboard, locked x
    return UI.TextBoxCollumnManager(boxes)



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
currentBoardManager = None
currentBoard = 0

# opening the save data for the noteboard and reading it
noteJson = CoreFuncs.Json.LoadFile("save.json")
noteBoards = GetNoteBoards(noteJson["NoteBoards"])


