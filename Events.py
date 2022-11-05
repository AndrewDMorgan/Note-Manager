import pygame, typing


# a class that stores information regarding events
class Events:
    def __init__(self) -> None:
        # keyboard stuff
        self.events = []

        self.shiftHeld = False
        self.optionHeld = False
        self.controlHeld = False
        self.commandHeld = False

        # mouse pressed stuff
        self.mouseDown = False
        self.mouseUp = False
        self.mouseHeld = False
        
        # mouse position stuff
        self.mouseX = -1
        self.mouseY = -1
        self.lastMouseX = -1
        self.lastMouseY = -1

    # inits the values
    def Init(self, events: typing.List[str], mouseDown: bool=False, mouseUp: bool=False, mouseHeld: bool=False, mouseX: int=-1, mouseY: int=-1, lastMouseX: int=-1, lastMouseY: int=-1, shiftHeld: bool=False, optionHeld: bool=False, controlHeld: bool=False, commandHeld: bool=False) -> None:
        # keyboard stuff
        self.events = events

        self.shiftHeld = shiftHeld
        self.optionHeld = optionHeld
        self.controlHeld = controlHeld
        self.commandHeld = commandHeld

        # mouse pressed stuff
        self.mouseDown = mouseDown
        self.mouseUp = mouseUp
        self.mouseHeld = mouseHeld
        
        # mouse position stuff
        self.mouseX = mouseX
        self.mouseY = mouseY
        self.lastMouseX = lastMouseX
        self.lastMouseY = lastMouseY

    # updating the mouse position
    def UpdateMousePosition(self) -> None:
        # updating the last position of the mouse
        self.lastMouseX = self.mouseX
        self.lastMouseY = self.mouseY

        # updating the current position of the mouse
        self.mouseX, self.mouseY = pygame.mouse.get_pos()

    # updates events
    def UpdateEvents(self) -> bool:
        # resetting the mouse sate
        self.mouseDown = False
        self.mouseUp = False

        # resetting the events
        self.events = []

        # looping through the events
        for event in pygame.event.get():
            # checking if the application was quit
            if event.type == pygame.QUIT:
                return False  # returning that the program quit
            
            # checking if any other events happened
            elif event.type == pygame.KEYDOWN:
                # checking if shift or option or command or control are being pressed
                if event.key in [pygame.K_LSHIFT, pygame.K_RSHIFT]:
                    self.shiftHeld = True
                elif event.key in [pygame.K_LALT, pygame.K_RALT]:
                    self.optionHeld = True
                elif event.key in [pygame.K_LCTRL, pygame.K_RCTRL]:
                    self.controlHeld = True
                elif event.key in [pygame.K_LMETA, pygame.K_RMETA]:
                    self.commandHeld = True
                else:
                    # logging the pressed key
                    self.events.append(pygame.key.name(event.key))
            elif event.type == pygame.KEYUP:
                # checking if shift or option are being pressed
                if event.key in [pygame.K_LSHIFT, pygame.K_RSHIFT]:
                    self.shiftHeld = False
                elif event.key in [pygame.K_LALT, pygame.K_RALT]:
                    self.optionHeld = False
                elif event.key in [pygame.K_LCTRL, pygame.K_RCTRL]:
                    self.controlHeld = False
                elif event.key in [pygame.K_LMETA, pygame.K_RMETA]:
                    self.commandHeld = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # checking if the correct mouse button was pressed
                if event.button == 1:
                    self.mouseDown = True
                    self.mouseHeld = True
            elif event.type == pygame.MOUSEBUTTONUP:
                # checking if the correct mouse button was pressed
                if event.button == 1:
                    self.mouseUp = True
                    self.mouseHeld = False

        # returning the events
        return True

