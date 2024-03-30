import webbrowser
import pywhatkit

def google_shit():
    term = input("What to search: ")
    try:
        pywhatkit.search(term)
        return
    except:
        print("An unknown error occurred")

