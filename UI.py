import enum, CoreFuncs, typing, pygame, math
from types import FunctionType
import Events


# ---------------------------------------- Buttons ----------------------------------------


# for a basic button
class Button:
    # the current state of the button
    class State (enum.Enum):
        Down = 0
        Up = 1
        Pressed = 2
        Realeased = 3

    def __init__(self, x: int, y: int, sizeX: int, sizeY: int, action: FunctionType, renderer: object) -> None:
        # the postion and size of the button
        self.__x = x
        self.__y = y
        self.__sizeX = sizeX
        self.__sizeY = sizeY

        # the action done after being pressed
        self.__action = action

        # the renderer for the button
        self.__renderer = renderer

        # the state of the button
        self.__state = self.State.Up
    
    # updating the button
    def Update(self, events: Events.Events, *args) -> None:
        self.UpdateState(events)

        # checking if the button has been pressed
        pressed = False
        if self.__state == self.State.Realeased:
            pressed = True
        
        # calling the update function
        self.__action(pressed, *args)

    # updating the state of the button
    def UpdateState(self, events: Events.Events) -> None:
        # checking if the button should be clicked
        boundsX = CoreFuncs.Range(events.mouseX, self.__x, self.__x + self.__sizeX)
        boundsY = CoreFuncs.Range(events.mouseY, self.__y, self.__y + self.__sizeY)

        # checking wich state the button is in
        if events.mouseHeld and boundsX and boundsY:
            if self.__state == self.State.Up:
                self.__state = self.State.Pressed
            else:
                self.__state = self.State.Down
        elif not events.mouseHeld:
            if self.__state == self.State.Down:
                self.__state = self.State.Realeased
            else:
                self.__state = self.State.Up
    
    # rendering the button
    def Render(self, *args) -> None:
        self.__renderer.Render(*args)
    
    # setters and getters for position
    def SetX(self, x: int) -> None:
        self.__x = x
    def SetY(self, y: int) -> None:
        self.__y = y
    def GetX(self) -> None:
        return self.__x
    def GetY(self) -> None:
        return self.__y


# manages a set of buttons
class ButtonManager:
    def __init__(self, buttons: typing.List[Button]) -> None:
        self.__buttons = buttons
    
    # updating the buttons
    def Update(self, mx: int, my: int, mouseHeld: bool) -> None:
        # looping through all buttons
        for button in self.__buttons:
            # updating the button
            button.Update(mx, my, mouseHeld)
    
    # renders all the boxes
    def Render(self, *args) -> None:
        # looping through all buttons
        for button in self.__buttons:
            # rendering the button
            button.Render(*args)

    # adds a button
    def AddButton(self, button: Button) -> None:
        self.__buttons.append(button)  # adding the button



# ---------------------------------------- Text Boxes ----------------------------------------


# a text box with extra properties
class TextBoxContainer:
    def __init__(self, renderer: object, updateFunc: FunctionType = lambda *args: None) -> None:
        self.__renderer = renderer
        self.Update = updateFunc  # setting the update function
    
    # a base update method incase non is given, does nothing takes anything
    def Update(*args) -> None:
        pass

    # renders using the render function
    def Render(self, *args) -> None:
        self.__renderer.Render(*args)
    
    # checking for a collision with a given point
    def CheckCollision(self, x: int, y: int) -> bool:
        # getting the buttons position
        obX = self.GetX()
        obY = self.GetY()

        # checking for collision
        boundsX = CoreFuncs.Range(x, obX, obX + self.__renderer.GetSizeX())
        boundsY = CoreFuncs.Range(y, obY, obY + self.__renderer.GetSizeY())

        # the x collision and y collision combined
        return boundsX and boundsY
    
    # getters for possition
    def GetX(self) -> int:
        return self.__renderer.GetX()
    def GetY(self) -> int:
        return self.__renderer.GetY()
    
    # getters for size
    def GetSizeX(self) -> int:
        return self.__renderer.GetSizeX()
    def GetSizeY(self) -> int:
        return self.__renderer.GetSizeY()
    
    # adders/setters for position
    def AddX(self, dx: int) -> None:
        self.__renderer.AddX(dx)
    def AddY(self, dy: int) -> None:
        self.__renderer.AddY(dy)
    def SetX(self, x: int) -> None:
        self.__renderer.SetX(x)
    def SetY(self, y: int) -> None:
        self.__renderer.SetY(y)
    
    # gets the renderer
    def GetRenderer(self) -> object:
        return self.__renderer
    
    # updates the renderers that the boxes are being moved
    def Moved(self, this: object, boxId: int) -> None:
        self.__renderer.Moved(this, boxId)


# manages a set of text boxes
class TextBoxManager:
    def __init__(self, boxes: typing.List[TextBoxContainer]) -> None:
        self.__boxes = boxes
        self.__indexes = list(range(0, len(self.__boxes)))

    # updates all the boxes
    def Update(self, *args) -> None:
        # looping through all the boxes
        i = 0
        for box in self.__boxes:
            # updating the box
            box.Update(self.__indexes[i], *args)
            i += 1

    # renders all the boxes
    def Render(self, *args) -> None:
        # looping through all the boxes
        i = 0
        for box in self.__boxes:
            # rendering the box
            box.Render(self.__indexes[i], *args)
            i += 1
    
    # adds a box
    def AddTextBox(self, box: TextBoxContainer) -> None:
        self.__boxes.append(box)  # adding the box
    
    # setters and getters for the boxes
    def GetBoxes(self) -> typing.List[TextBoxContainer]:
        return self.__boxes
    def SetBoxes(self, boxes: typing.List[TextBoxContainer]) -> None:
        self.__boxes = boxes
    
    # gets a box at an index accounting for movement of the boxes
    def GetBox(self, i: int) -> TextBoxContainer:
        return self.__boxes[self.__indexes.index(i)]
    def AddBox(self, box: TextBoxContainer) -> None:
        self.__boxes.append(box)
        self.__indexes.append(len(self.__boxes) - 1)
    
    # removing a box
    def RemoveBox(self, id: int) -> None:
        # removing the box and index
        breakPoint = self.__indexes[id]

        del self.__boxes[id]
        del self.__indexes[id]

        # checking if any boxes are left
        if len(self.__boxes) > 0:
            # getting the lowest index after the value removed
            minAft = max(self.__indexes)
            for i in range(id, len(self.__indexes)):
                minAft = min(self.__indexes[i], minAft)
            
            # adjusting the values
            dif = max(minAft - breakPoint, 0)
            for i in range(id, len(self.__indexes)):
                self.__indexes[i] -= dif
                self.__boxes[i].GetRenderer().AddNoteId(-dif)  # updating the indexes stored in the boxes

    # getting and setting the indexes
    def GetIndexes(self) -> typing.List[int]:
        return self.__indexes
    def SetIndexes(self, indexes: int) -> None:
        self.__indexes = indexes
    
    # gets the boxes actual index
    def GetIndex(self, i: int) -> int:
        return self.__indexes.index(i)


# manages a list of text boxes that are arranged in a collumn and are moveable
class TextBoxCollumnManager (TextBoxManager):
    def __init__(self, boxes: typing.List[TextBoxContainer], lockX: int = 0, lockY: int = 1) -> None:
        super().__init__(boxes)

        self.__heldI = -1  # the index of the held box -1 if none held

        # locking the movement in different directions
        self.lockX = lockX
        self.lockY = lockY
    
    # shifts all boxes bellow the given box down
    def ShiftBoxesY(self, boxIndex: int, dy: int) -> None:  # bug, bug, make sure boxes to the right/left dont get moved only boxes in the came collumn
        # getting the boxes
        boxes = self.GetBoxes()

        # getting the height of the box
        box = boxes[boxIndex]
        height = box.GetY()

        # looping through and moving all boxes bellow the current box down
        for box in boxes:
            # checking if the box is bellow the one inputed
            if box.GetY() > height:
                box.AddY(dy)  # moving the box

        # updating the boxes
        self.SetBoxes(boxes)

    # updating the text boxes
    def Update(self, events: Events, *args) -> None:
        # updating the boxes from the base class
        super().Update(events, *args)

        # getting the boxes
        boxes = self.GetBoxes()

        # checking if a box is currently being held
        if self.__heldI == -1:
            # checking if a box should be picked up
            if events.mouseHeld:
                # looping through all the boxes
                for box in boxes:
                    if box.CheckCollision(events.mouseX, events.mouseY):
                        # setting the new held box
                        self.__heldI = boxes.index(box)  # getting the index of the box
        else:
            # moving the box around
            # getting the box thats being moved
            box = boxes[self.__heldI]

            # getting the mouse position for the moving
            px, py = events.mouseX, events.mouseY
            if self.lockX == 0:
                px = box.GetX()
            if self.lockY == 0:
                py = box.GetY()

            # looping through all the boxes checking for which the mouse is over
            otherBoxI = -1
            for box_ in boxes:
                if box_.CheckCollision(px, py):
                    otherBoxI = boxes.index(box_)  # getting the index of the box

            # checking if the outter boxes should be swapped
            if py > boxes[len(boxes) - 1].GetY():
                otherBoxI = len(boxes) - 1
            elif py < boxes[0].GetY():
                otherBoxI = 0
            
            # checking if the mouse is over a box
            if otherBoxI != -1 and otherBoxI != self.__heldI:
                # telling the boxes that they are being moved
                boxes[self.__heldI].Moved(self, self.__heldI)
                boxes[otherBoxI   ].Moved(self, otherBoxI)

                # changing the position of the boxes
                boxX = boxes[self.__heldI].GetX()
                boxY = boxes[self.__heldI].GetY()

                boxes[self.__heldI].SetX(boxes[otherBoxI].GetX())
                boxes[self.__heldI].SetY(boxes[otherBoxI].GetY())

                boxes[otherBoxI].SetX(boxX)
                boxes[otherBoxI].SetY(boxY)

                # swapping the index of the boxes
                boxes[self.__heldI], boxes[otherBoxI] = boxes[otherBoxI], boxes[self.__heldI]

                # swapping the index of the boxes
                indexes = self.GetIndexes()
                indexes[self.__heldI], indexes[otherBoxI] = indexes[otherBoxI], indexes[self.__heldI]
                self.SetIndexes(indexes)

                # changing the held index to the boxes new index
                self.__heldI = otherBoxI

        # setting the boxes
        self.SetBoxes(boxes)

        # removing all held boxes once the mouse is no longer being pressed
        if not events.mouseHeld:
            self.__heldI = -1



# ---------------------------------------- Typing Boxes + Combinations ----------------------------------------


# global for the typing box
_ALLOWED_CHARS = list("abcdefghijklmnopqrstuvwxyz0123456789`-=[]\\;',./")
_CAP_CHARS     = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ)!@#$%^&*(~_+{}|:\"<>?")
_OPT_CHARS     = list("å∫ç∂´ƒ©˙ˆ∆˚¬µ˜øπœ®ß†¨√∑≈¥ º¡™£¢∞§¶•¡`–≠“‘«…æ≤≥÷")


# a basic text box
class TypingBox:
    def __init__(self, centerX: int, centerY: int, baseText: str="Type Here") -> None:
        self.__centerX = centerX
        self.__centerY = centerY
        self.__baseText = baseText

        self.__currentText = ""
        self.__currentChar = 0
    
    # updating the typing box
    def Update(self, events: Events, dt: float, *args) -> None:
        # getting the correct character set
        chars = _ALLOWED_CHARS
        if events.shiftHeld:
            chars = _CAP_CHARS
        elif events.optionHeld:
            chars = _OPT_CHARS
        
        # moving the cursor
        if "left" in events.events:
            self.__currentChar -= 1
        if "right" in events.events:
            self.__currentChar += 1
        
        # checking if its a command not typing
        if events.commandHeld or events.controlHeld:
            return

        # looping through the events and adding them to the text
        for event in events.events:
            # checking for deletion of letters
            if event == "backspace":
                self.__currentText = self.__currentText[:self.__currentChar - 1] + self.__currentText[self.__currentChar:]
                self.__currentChar -= 1

            # checking for the space key
            elif event == "space":
                self.__currentText = self.__currentText[:self.__currentChar] + " " + self.__currentText[self.__currentChar:]
                self.__currentChar += 1

            # checking if the event is a valid typable keypress
            elif event in _ALLOWED_CHARS:
                # getting the correct char
                char = chars[_ALLOWED_CHARS.index(event)]
                self.__currentText = self.__currentText[:self.__currentChar] + char + self.__currentText[self.__currentChar:]
                self.__currentChar += 1
        
        # setting the bounds of the cursor
        self.__currentChar = min(max(self.__currentChar, 0), len(self.__currentText))
    
    # rendering the typing box
    def Render(self, screen: pygame.Surface, *args) -> None:
        # checking if anything is writen or not and setting the text accordingly
        text = self.__currentText
        if text == "":
            text = self.__baseText

        # adding the cursor
        cursor = "|"
        text = text[:self.__currentChar] + cursor + text[self.__currentChar:]

        # rendering the text
        textSurf = pygame.Surface((self.__centerX*2, self.__centerY*2))
        textSurf.set_colorkey((0, 0, 0))
        textSprite = UI.Text(textSurf, text, (255, 255, 255), (self.__centerX, self.__centerY), 25, center=True)

        # rendering a faded box under it to make it more visable
        sizeX, sizeY = textSprite.size
        sizeX += 4
        sizeY += 2
        surf = pygame.Surface((sizeX, sizeY))
        pygame.draw.rect(surf, (0, 0, 0), [0, 0, sizeX, sizeY], border_radius=4)
        surf.set_alpha(50)
        screen.blit(surf, (self.__centerX - sizeX//2, self.__centerY - sizeY//2))
        screen.blit(textSurf, (0, 0))
    
    # getters and setters for the text
    def GetText(self) -> str:
        return self.__currentText
    def SetText(self, text: str) -> None:
        self.__currentText = text
        # resetting the cursors position
        self.__currentChar = 0
    
    # setters for the position
    def SetX(self, x: int) -> None:
        self.__centerX = x
    def SetY(self, y: int) -> None:
        self.__centerY = y


# for a text box with a typing box
class TextTypingBox (TextBoxContainer):
    def __init__(self, renderer: object, updateFunc: FunctionType, typingBox: TypingBox) -> None:
        super().__init__(renderer, updateFunc=updateFunc)

        self.typingBox = typingBox
    
    # updating the text box and typing box
    def Update(self, *args) -> None:
        # updating the base box
        super().Update()

        # updating the typingbox
        self.typingBox.Update(*args)

    # rendering the text box and typing box
    def Render(self, *args) -> None:
        # rendering the base box
        super().Render(*args)

        # rendering the typing box
        self.typingBox.Render(*args)

    # gets the typing box
    def GetTypingBox(self) -> TypingBox:
        return self.typingBox



# ---------------------------------------- Basic Renderers / General UI ----------------------------------------


# renders text, moves based on window size
class ButtonTextRenderer:
    def __init__(self, dx: int, dy: int, size: int, text: str, color: typing.Tuple[int]=(55,165,55)) -> None:
        self.dx = dx
        self.dy = dy
        self.size = size
        self.text = text
        self.color = color

        # the changing in size
        self.sizeOssolation = 0
    
    # redners the text
    def Render(self, screen: pygame.Surface, events: Events.Events, dt: float, screenWidth: int, screenHeight: int) -> None:
        # rendering the text
        textSprite = UI.Text(screen, self.text, self.color, (screenWidth + self.dx, screenHeight + self.dy), self.size, center=True)

        # rendering the circle thingy
        left = screenWidth + self.dx+1
        top  = screenHeight + self.dy
        if textSprite.collidepoint(events.mouseX, events.mouseY):
            # making it change sizes slowely
            self.sizeOssolation += dt * 2
            # rendering the circle
            pygame.draw.circle(screen, (255, 255, 255), [left, top], 13 + math.cos(self.sizeOssolation) * 2, 2)
        else:
            # removing any size change
            self.sizeOssolation = 0


# ui (just text for now)
class UI:
    # rendering text with many options (transparecy, size, centering, color, font, ect...)
    def Text(screen: object, text: str, color, pos, size: float, center: bool = False, font: str = 'Neon.ttf', trans: int = 255) -> pygame.Rect:
        largeText = pygame.font.Font(font, size)
        textSurface = largeText.render(text, True, color)
        TextSurf, TextRect = textSurface, textSurface.get_rect()
        if trans != 255:  # checking if the text is transparent
            surf = pygame.Surface(TextRect.size)
            if color == (0, 0, 0):  # making sure black text still works with transparecy
                surf.fill((255, 255, 255))
                surf.set_colorkey((255, 255, 255))
            else:
                surf.fill((0, 0, 0))
                surf.set_colorkey((0, 0, 0))
            surf.set_alpha(trans)
            n_pos = pos
            if center:  # checking if the text should be centered
                pos = (TextRect.size[0] // 2, TextRect.size[1] // 2)
            else:
                pos = (0, 0)
        else:
            surf = screen
        if center:  # checking if the text should be centered
            TextRect.center = pos
            sprite = surf.blit(TextSurf, TextRect)
        else:
            sprite = surf.blit(TextSurf, pos)
        
        if trans != 255:  # a bit more with transparecy
            if center:
                screen.blit(surf, (n_pos[0] - TextRect.size[0] // 2, n_pos[1] - TextRect.size[1] // 2))
            else:
                screen.blit(surf, n_pos)
        return sprite


