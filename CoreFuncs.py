import json, pygame


# ---------------------------------------- Screen Stuff/UI ----------------------------------------


# ui (just text for now)
class UI:
    # rendering text with many options (transparecy, size, centering, color, font, ect...)
    def text(screen: object, text: str, color, pos, size: float, center: bool = False, font: str = 'Neon.ttf', trans: int = 255) -> pygame.Rect:
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



# ---------------------------------------- Data Loading/Parsing ----------------------------------------


# for managing json files
class Json:
    # reads/opens a json file
    def LoadFile(file: str) -> dict:
        return json.load(open(file))

    # writes to a json file
    def WriteFile(file: str, info: dict) -> None:
        jsonObj = json.dumps(info, indent=4)  # getting the object form of the dict
 
        # Writing to the file
        with open(file, "w") as out:
            out.write(jsonObj)



# ---------------------------------------- Math Functions ----------------------------------------


# checks if a value is in a range of values
def Range(v: int, l: int, r: int) -> bool:
    return v >= l and v <= r


# linear interpalation
def Lerp(l: int, r: int, m: int) -> float:
    return l * (1 - m) + r * m

