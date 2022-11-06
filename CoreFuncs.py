import json, pygame


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

