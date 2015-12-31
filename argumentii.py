import sys, getopt



def main(argv):

   try:
      opts, args = getopt.getopt(argv,"v",)
   except getopt.GetoptError:
      pass
   for opt, arg in opts:
      if opt == '-v':
         print ('DetainAgent Version 1.0 ,Dalet IT')
         sys.exit()


def test():
    print('next def')

if __name__ == "__main__":
   main(sys.argv[1:])