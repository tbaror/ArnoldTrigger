__author__ = 'Coco'


class
def getIpHost(self,host):
        try:
            return socket.gethostbyname(host)

        except(socket.gaierror):
            with open(os.getcwd()+'/errors.log', "a") as f:

                f.write(host+':no ip resolved')
                f.Close()
            return 'noip'


