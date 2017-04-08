# pip install ws4py
from ws4py.client.threadedclient import WebSocketClient
import json

url = 'ws://localhost:8080/wsplay'
key = ""


class WSBot(WebSocketClient):
    
    frame = 0
    playerNum = 0    
    playerNumStr = ""

    def opened(self):
        print "sending key"
        self.send(key)

    def closed(self, code, reason=None):
        print "Closed down", code, reason

    def bot_init(self, data):
        # expect status message
        if self.frame == 0:
            print "Username:", data["Username"], " Player: ", data["Player"], " Gamename: ", data["Gamename"]
            self.playerNum = data["Player"]
            if self.playerNum==1:self.playerNumStr="p1"
            elif self.playerNum==2:self.playerNumStr="p2"
            else: print "ERROR: INVALID PLAYER NUMBER"
            self.frame += 1

    def winOrlose(self, data):
        # Win or lose
        if data[self.playerNumStr]["mainCore"]["hp"] <= 0 or data["p2"]["mainCore"]["hp"] <= 0:
            if (data[self.playerNumStr]["mainCore"]["hp"] <= 0 and self.playerNum == 1) or (data["p2"]["mainCore"]["hp"] <= 0 and self.playerNum == 2):
                print "User lost :("
            else:
                print "User won :)"
            ws.close()

    def operation(self, data):
        #OPERATION
        #print data[self.playerNumStr]["bits"]
        if data[self.playerNumStr]["bits"] >= 15000:
            print "Bots engaged\n"
            for i in range(500):
                self.send("b00 01")

    def received_message(self, m):
        data = json.loads(m.data)
        if(self.frame == 0):
            self.bot_init(data)
            return

        self.winOrlose(data)

        self.operation(data)
        
        self.frame += 1


if __name__ == '__main__':
    try:
        ws = WSBot(url, protocols=['http-only'])
        ws.connect()
        ws.run_forever()
    except KeyboardInterrupt:
        ws.close()
        
