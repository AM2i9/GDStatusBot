import time
import sys

# Some basic error handling functions. This is all I really need to do.
def fatalError(errorMsg):
    """
    For when the error is so bad you need to shut down the program
    """
    print(f"[Error] {errorMsg}. Stopping in 5 seconds.")
    time.sleep(5)
    sys.exit("[Info] Shutdown due to previous error")

def softError(errorMsg):
    """
    For when the error has no effect on the program running smoothly, but is still nice to know that it happened
    """
    print(f"[Error] {errorMsg}.")