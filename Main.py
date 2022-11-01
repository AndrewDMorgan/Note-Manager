import pygame, typing, time
import CoreFuncs, NoteBoard

pygame.init()


"""
try 2D collumns

211 ish Buttons.py bug
def ShiftBoxesY(self, boxIndex: int, dy: int) -> None:
# bug, bug, make sure boxes to the right/left dont get moved only boxes in the came collumn

Try horizontal collumns maybe

Objectives:
    * Add catagories within boards (multiple collumns, can be swapped around, notes can be moved between them)
    * Maybe clean up movement after drop down goes up, it jumps a couple of boxes wich might be fixed but maybe should be left, idk
    * Move event parsing to a class in another file, also add more/better/cleaner interactions with the data
    * Add creation of boards and notes and sub-notes
    * Add saving/auto saving
    * Add the other things I have on the github page

"""


# setting up the screen
screenWidth = 1200
screenHeight = 750

pygame.display.set_caption("Task Manager")
screen = pygame.display.set_mode((screenWidth, screenHeight), pygame.RESIZABLE)


# opening the save data for the noteboard
noteJson = CoreFuncs.Json.LoadFile("save.json")

noteBoards = NoteBoard.GetNoteBoards(noteJson["NoteBoards"])


# event stuff, move to another class and file
mouseX, mouseY = 0, 0
lastMouseX, lastMouseY = 0, 0

mouseDown = False
mouseHeld = False

dt = 0


# the state of the application
running = True

# the main loop running everything
while running:
    # the start time of the frame
    start = time.time()

    # getting the windows size for proper scalling/rendering
    screenWidth, screenHeight = pygame.display.get_surface().get_size()

    # getting the mosues last and current position
    lastMouseX, lastMouseY = mouseX, mouseY
    mouseX, mouseY = pygame.mouse.get_pos()

    # setting mouseDown to False unless the mouse is clicked
    mouseDown = False

    # checking events (move to class/separate script)
    for event in pygame.event.get():
        # checking if the window was quit
        if event.type == pygame.QUIT:
            # stopping the main loop as the application was quit
            running = False
            break
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseDown = True
            mouseHeld = True
        if event.type == pygame.MOUSEBUTTONUP:
            mouseHeld = False

    # checking if the application was quit
    if not running:
        break
    

    # updating the TextBoxContainers
    noteBoards.Update(mouseX, mouseY, lastMouseX, lastMouseY, mouseHeld, noteBoards, noteJson["NoteBoards"], mouseDown, mouseX, mouseY)
    NoteBoard.currentBoardManager.Update(mouseX, mouseY, lastMouseX, lastMouseY, mouseHeld, NoteBoard.currentBoardManager, noteJson["NoteBoards"], mouseDown, mouseX, mouseY)


    # clearing the screen
    screen.fill((50, 50, 50))

    # drawing the left collumn with the boards
    pygame.draw.rect(screen, (40, 40, 40), [0, 0, 195, screenHeight])

    # rendering all the TextBoxContainers
    noteBoards.Render(screen, dt, screenWidth, screenHeight)
    NoteBoard.currentBoardManager.Render(screen, dt, screenWidth, screenHeight, mouseX, mouseY)

    # updating the screen
    pygame.display.update()

    # the end time of the frame and 1/the change in time (dt)
    end = time.time()
    dt = end - start

