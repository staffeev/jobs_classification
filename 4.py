from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()



print(similar("Собака бульдог","Бульдог собака"))