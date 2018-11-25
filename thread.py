import threading
import time

def dowork():
    print("Working")
    threading.Timer(2.0, dowork).start()
    #t.start()

def main():
    threading.Timer(2.0, dowork).start()
    #t.start()
    while (1):
        pass

if __name__ == '__main__':
    main()
