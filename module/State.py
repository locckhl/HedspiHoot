from enum import IntEnum

class State(IntEnum):
   LOBBY = 0
   START_GAME = 1
   SHOW_QUESTION = 2
   SHOW_RESULT = 3
   NEXT_QUEST = 4
   END_GAME = 5

