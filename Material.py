

class Material:
    def __init__(self, ID, baseelement, dopedelement, step, config, note):
        self.ID = ID
        self.baseelement = baseelement
        self.dopedelement = dopedelement
        self.step = step
        self.config = config
        self.note = note

    def generatelog(self):
    	logfile = self.baseelement
        if self.dopedelement != "":
			logfile += self.dopedelement
        if self.config != 0:
			logfile += str(self.config)
        logfile += self.step
        logfile += ".log"
        return logfile
