import os
import pywhatkit

def do_terminal_shit():
    os.system("ls")

def google_shit():
    try:
        pywhatkit.search("Ninjas in Paris")
        print("Searching...")
        pass
    except:
        print("An unknown error occurred")

n = int(input("choose a number: "))
if (n==69):
    do_terminal_shit()
elif (n==1):
    google_shit()
