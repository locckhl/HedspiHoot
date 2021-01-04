# from enum import IntEnum
from enum import Enum
class MessType(Enum):
   SEND_ROLE = 0
   CONFIRM_ROLE = 1
   NEW_QUIZ = 2
   SEND_NEW_QUIZ = 3
   SEND_QUIZZES = 4
   SEND_QUIZ_CHOICE = 5

