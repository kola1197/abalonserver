import datetime
import os
import easygui
class Logger:
    def __init__(self):
        self.logFileName = ""
        self.gameInfoFileName = ""
        current_path = os.path.dirname(__file__)
        logPath = current_path + "\\logs"
        game_log_path = current_path + "\\gameInfo"
        self.createLogFile(logPath)
        self.createGameInfoPath(game_log_path)



    def createLogFile(self, path):
        self.logFileName = path + str(self.get_file_name(path, '\\Log'))
        print('Writing logs to %s' % self.logFileName)
        f = open(self.logFileName, 'w')
        f.close()

    def createGameInfoPath(self, path):
        self.gameInfoFileName = path + str(self.get_file_name(path, '\\Game'))
        print('Writing logs to %s' % self.gameInfoFileName)
        f = open(self.gameInfoFileName, 'w')
        f.close()

    def get_file_name(self, path, suffix):
        try:
            if not os.path.exists(path):
                os.mkdir(path)
        except OSError:
            print("Creation of the logs directory %s failed" % path)
        else:
            print("Successfully created the logs directory %s " % path)
        i = 0
        while os.path.exists(path + suffix + str(i) + ".txt"):
            i += 1
        return suffix + str(i) + ".txt"

    def Write(self, msg):
        f = open(self.logFileName, 'a')
        f.writelines(str(datetime.datetime.now()) + ' —---— ' + str(msg))
    #    print('»»»»»»»> ' + str(msg))
        f.writelines('\n')
        f.close()

    def WriteGameInfo(self, msg):
        f = open(self.gameInfoFileName, 'a')
        f.writelines(str(msg))
     #   print('»»»»»»»> ' + str(msg))
        f.writelines('\n')
        f.close()

    def WriteNotInConsole(self, msg):
        f = open(self.fileName, 'a')
        f.writelines(str(datetime.datetime.now()) + ' —---— ' + str(msg))
        f.writelines('\n')
        f.close()

    def read_file(self, fileName):
        f = open(fileName, 'r')
        l=[]
        for line in f:
            l.append(line)
        return l
    def directory(self):
        filename = easygui.fileopenbox(filetypes=["*.txt"])
        return filename

    def line_del(self):
        f=open(self.gameInfoFileName)
        lines = f.readlines()
        f.close()
        f=open(self.gameInfoFileName, 'w')
        f.writelines([i for i in lines[:-1]])
        f.close()