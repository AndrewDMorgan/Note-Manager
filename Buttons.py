import enum, CoreFuncs, typing
from types import FunctionType


# ---------------------------------------- Buttons ----------------------------------------


# for a basic button
class Button:
    # the current state of the button
    class State (enum.Enum):
        Down = 0
        Up = 1
        Pressed = 2
        Realeased = 3

    def __init__(self, x: int, y: int, sizeX: int, sizeY: int, action: FunctionType, renderer: FunctionType) -> None:
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
        self.__state = self.State.up
    
    # updating the button
    def Update(self, mx: int, my: int, mouseHeld: bool) -> None:
        self.GetState(mx, my, mouseHeld)

        # checking if the button has been pressed
        if self.__state == self.State.Realeased:
            self.__action()  # calling the function assosiated with the pressing of the button

    # updating the state of the button
    def UpdateState(self, mx: int, my: int, mouseHeld: bool) -> None:
        # checking if the button should be clicked
        boundsX = CoreFuncs.Range(mx, self.__x, self.__x + self.__sizeX)
        boundsY = CoreFuncs.Range(my, self.__y, self.__y + self.__sizeY)

        # checking wich state the button is in
        if mouseHeld and boundsX and boundsY:
            if self.__state == self.Sate.Up:
                self.__state = self.State.Pressed
            else:
                self.__state = self.State.Down
        else:
            if self.__state == self.State.Down:
                self.__state = self.State.Realeased
            else:
                self.__state = self.State.Up
    
    # rendering the button
    def Render(self) -> None:
        self.__renderer.Render()


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
    def Update(self, mx: int, my: int, lmx: int, lmy: int, mouseHeld: bool, *args) -> None:
        # updating the boxes from the base class
        super().Update(*args)

        # getting the boxes
        boxes = self.GetBoxes()

        # checking if a box is currently being held
        if self.__heldI == -1:
            # checking if a box should be picked up
            if mouseHeld:
                # looping through all the boxes
                for box in boxes:
                    if box.CheckCollision(mx, my):
                        # setting the new held box
                        self.__heldI = boxes.index(box)  # getting the index of the box
        else:
            # moving the box around
            # getting the box thats being moved
            box = boxes[self.__heldI]

            # getting the mouse position for the moving
            px, py = mx, my
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
        if not mouseHeld:
            self.__heldI = -1

