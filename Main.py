import CoreFuncs, NoteBoard, Events, BoardCreator
import pygame, time

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


# event stuff
events = Events.Events()

dt = 0


# the state of the application
running = True

# the main loop running everything
while running:
    # the start time of the frame
    start = time.time()

    # getting the windows size for proper scalling/rendering
    screenWidth, screenHeight = pygame.display.get_surface().get_size()

    # updating the mouse position
    events.UpdateMousePosition()

    # updating the keyboard events and the running state of the application
    running = events.UpdateEvents()


    # -------- Updating Stuff --------

    # updating the TextBoxContainers
    NoteBoard.noteBoards.Update(events, NoteBoard.noteBoards, NoteBoard.noteJson["NoteBoards"])
    NoteBoard.currentBoardManager.Update(events, NoteBoard.currentBoardManager)

    # updating the typingCreator and boardCreator
    BoardCreator.typingCreator.Update(events, dt, screenWidth, screenHeight)
    BoardCreator.boardCreator.Update()
    BoardCreator.newNoteButton.Update(events, BoardCreator.newNoteButton, screenWidth)
    

    # -------- Rendering Stuff --------

    # clearing the screen
    screen.fill((50, 50, 50))

    # drawing the left collumn with the boards
    pygame.draw.rect(screen, (40, 40, 40), [0, 0, 195, screenHeight])

    # rendering all the TextBoxContainers
    NoteBoard.noteBoards.Render(screen, dt, screenWidth, screenHeight)
    NoteBoard.currentBoardManager.Render(screen, dt, screenWidth, screenHeight, events)

    # rendering the typingCreator
    BoardCreator.typingCreator.Render(screen)
    BoardCreator.newNoteButton.Render(screen, events, dt, screenWidth, 0)

    # updating the screen
    pygame.display.update()


    # the end time of the frame and 1/the change in time (dt)
    end = time.time()
    dt = end - start

