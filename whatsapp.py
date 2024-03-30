import pywhatkit

def send_whatsapp_message():
    number = int(input("Enter number: "))
    content = input("Enter message content: ")
    pywhatkit.sendwhatmsg_instantly(f"+91{number}", content, 1)



