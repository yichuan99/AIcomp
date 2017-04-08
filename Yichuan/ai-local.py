# pip install ws4py
from ws4py.client.threadedclient import WebSocketClient
import json

url = 'ws://localhost:8080/wsplay'
key = "ShaquanasCorrectlyTestedDuck"

class WSBot(WebSocketClient):
    
    frame = 0
    playerNum = 0    
    
    def opened(self):
        print "sending key"
        self.send(key)

    def closed(self, code, reason=None):
        print "Closed down", code, reason

    def received_message(self, m):
        data = json.loads(m.data)
        print data
        
        # expect status message
        if self.frame == 0:
            print "Username:", data["Username"], " Player: ", data["Player"], " Gamename: ", data["Gamename"]
            self.playerNum = data["Player"]
            self.frame += 1
            return
        # Win or lose
        if data["p1"]["mainCore"]["hp"] <= 0 or data["p2"]["mainCore"]["hp"] <= 0:
            if (data["p1"]["mainCore"]["hp"] <= 0 and self.playerNum == 1) or (data["p2"]["mainCore"]["hp"] <= 0 and self.playerNum == 2):
                print "User lost :("
            else:
                print "User won :)"
            ws.close()
        self.frame += 1
        
        #OPERATION
        if data["p1"]["bits"] >= 300:
            self.send("b01 01")

if __name__ == '__main__':
    try:
        ws = WSBot(url, protocols=['http-only'])
        ws.connect()
        ws.run_forever()
    except KeyboardInterrupt:
        ws.close()