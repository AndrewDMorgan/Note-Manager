import Buttons, CoreFuncs, NoteBoard
import pygame, json, typing

pygame.init()


# setting up the screen
screenWidth = 1200
screenHeight = 750
screen = pygame.display.set_mode((screenWidth, screenHeight), pygame.RESIZABLE)


# a test case for this
# try 2d collumns
# try horizontal collomns


# opening the save data for the noteboard
noteJson = CoreFuncs.Json.LoadFile("save.json")

noteBoards = NoteBoard.GetNoteBoards(noteJson["NoteBoards"])


# event stuff
mouseX, mouseY = 0, 0
lastMouseX, lastMouseY = 0, 0

mouseDown = False
mouseHeld = False

# the state of the application
running = True

# the main loop running everything
while running:
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
    
    # updating the note boards self: object, baordId: int, mouseDown: bool, mx: int, my: int, *args
    noteBoards.Update(mouseX, mouseY, lastMouseX, lastMouseY, mouseHeld, noteBoards, noteJson["NoteBoards"], mouseDown, mouseX, mouseY)
    NoteBoard.currentBoardManager.Update(mouseX, mouseY, lastMouseX, lastMouseY, mouseHeld)

    # clearing the screen
    screen.fill((68, 68, 68))
    pygame.draw.rect(screen, (45, 45, 45), [0, 0, 195, screenHeight])

    noteBoards.Render(screen)
    NoteBoard.currentBoardManager.Render(screen)

    # updating the screen
    pygame.display.update()


