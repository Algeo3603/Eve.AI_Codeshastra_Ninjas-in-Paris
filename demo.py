from search import google_shit
from terminal import do_terminal_shit
from echo import display

while True:
    n = int(input("choose a number: "))
    if (n==1):
        google_shit()
    elif (n==2):
        do_terminal_shit()
    elif n==3:
        display()
