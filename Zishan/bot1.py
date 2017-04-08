# pip install ws4py
from ws4py.client.threadedclient import WebSocketClient
import json

url = "ws://localhost:8080/wsplay"
key = "LouisasCorrectlyScaredRamen"

class WSBot(WebSocketClient):
    frame = 0
    playerNum = 0
    myself = ""
    rival = ""

    
    def opened(self):
        # print "opened"
        self.send(key)

    def closed(self, code, reason=None):
        print "Closed down", code, reason

    def init(self, data):
        self.playerNum = data['Player']
        if self.playerNum == 1:
            self.myself = "p1"
            self.rival = "p2"
        else:
            self.myself = "p2"
            self.rival = "p1"
        # self.myself = (self.playerNum == 1) ? "p1" : "p2"
        # self.rival = (self.playerNum == 2) ? "p1" : "p2"
        print "Username:", data["Username"], " Player: ", data["Player"], " Gamename: ", data["Gamename"]

    def terminates(self, data):
        if data[self.myself]["mainCore"]["hp"] <= 0:
            print "User lost :("
            return True
        elif data[self.rival]["mainCore"]["hp"] <= 0:
            print "User won :)"
            return True
        return False

    def received_message(self, m):
        data = json.loads(m.data)
        print data
        if self.frame == 0: # expect status message
            self.init(data)
            self.frame += 1
            return
        if self.terminates(data):
            ws.close()
        self.frame += 1
        if data[self.myself]["bits"] >= 10000:
            for i in range(50):
                self.send("b00 03")

if __name__ == '__main__':
    try:
        ws = WSBot(url, protocols=['http-only'])
        ws.connect()
        ws.run_forever()
    except KeyboardInterrupt:
        ws.close()
