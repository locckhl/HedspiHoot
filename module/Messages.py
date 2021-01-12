
from module.MessType import MessType


class Messages():
    def __init__(self, type: str, username: str = "none", session: str = "none",state: bool = True, body: str = "none"):
        self.type = type
        self.username = username
        self.session = session
        self.state = state
        self.header = f"{type};{username};{session};{state}"
        self.body = body

    def to_message(self) -> bytes:
        return f"{str(self.header)}\n{str(self.body)}".encode("ascii") 

def convert_message(message: str) -> Messages:
    print(f"Message received : {message}")
    message = message.decode("ascii")
    if(message == ''):
        print("close")
        return Messages(MessType.CLOSE.name)
    # if(message == EOF):
    #     return
    # print(f"Message received from: {message}")
    header, body = message.split("\n")
    # print(header)
    # print(body)
    type, username, session, state = header.split(";")
    # print("---")
    # print(type)
    # print(username)
    # print(session)
    # print(state)

    return Messages(type, username, session, state, body)
# a = Messages(MessType.CONFIRM_ROLE)
# mess = a.to_message()
# print(mess)
# print(mess.split(";"))