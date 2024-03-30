import webbrowser
import pywhatkit

def google_shit():
    term = input("What to search: ")
    # query = "https://www.google.com/search?q=" + term
    # webbrowser.open(query)
    # webbrowser.close()
    try:
        pywhatkit.search(term)
        return
    except:
        print("An unknown error occurred")

