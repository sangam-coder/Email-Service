import smtplib
import speech_recognition as sr
import traceback
import email
import imaplib
import pyttsx3




# -*- creating a email list  -*-
email_list = {
    'Dad': 'Enter Email ID here',
    'Buddy': 'Enter Email ID here',
    'Doctor':'Enter Email ID here',
    'Executive:'Enter Email ID here',
    'uncle':'Enter Email ID here'

}



# -*-  Setting up Voice engine Properties -*-

listener = sr.Recognizer()
engine=pyttsx3.init() #  object creation


rate = engine.getProperty('rate')   
engine.setProperty('rate', 150)           #  setting up new voice rate. The default value of rate is 200
voices = engine.getProperty('voices')     #  getting details of current voice
engine.setProperty('voice', voices[1].id) #  changing index, changes voices. o for male and 1 for female




# -*- creating a talk function for output Audio -*-
def talk(text):
    engine.say(text)
    engine.runAndWait()
    
    
sender_email="sender's Email here" 
password ="sender's email password here"  
    
    
# -*-get_info() is for get information from the user with the help of microphone as primary source -*-

def get_info():
    try:
        with sr.Microphone() as source:  # use the default microphone as the audio source
            listener.adjust_for_ambient_noise(source)
            # listen for 1 second to calibrate the energy threshold for ambient noise levels
            print('listening...'+'\n')
            talk("listening.....")
            voice = listener.listen(source)
      # now when we listen, the energy threshold is already set to a good value, and we can reliably catch speech right away

            info = listener.recognize_google(voice)  # recognize speech using Google Speech Recognition
            print(info)
            return info.lower()
    except:
        pass
    
    


    
# -*- take infromation about email -*-

def get_email():
    talk('To Whom you want to send email')
    name = get_info()
    receiver = email_list[name]
    print(receiver)
    talk('What is the subject of your email?')
    subject = get_info()
    talk('Tell me the text in your email')
    message = get_info()
    send_email(receiver, subject, message)
    talk('Hey, Your email is sent')
    talk('Do you want to send more email or want to check inbox?')
    send_more = get_info()
    if 'yes' in send_more:
        get_email()
    elif 'exit' in send_more:
        talk("Thank You !")
    elif "check inbox" in send_more:
        get_inbox()

        
        
        
        
        
    
# -*- This function create full structure of our email and also help to establish secure server -*-


def send_email(receiver, subject, message):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, password)
    Email = email.message.EmailMessage()
    Email['From'] = "Rahul Khushwah"
    Email['To'] = receiver
    Email['Subject'] = subject
    Email.set_content(message)
    talk("Sending mail")
    print("Sending mail......."+'\n')
    server.send_message(Email)
    
    
    
        
# -*-  this funtion help us to establish secure connection with gmail and help out to read out inbox -*-



def get_inbox():
    try:
       
        mail = imaplib.IMAP4_SSL("imap.gmail.com",993)
        mail.login(sender_email,password)
        mail.select('inbox')

        data = mail.search(None, 'ALL')
        mail_ids = data[1]
        id_list = mail_ids[0].split()   
        first_email_id = int(id_list[0])
        latest_email_id = int(id_list[-1])

        for i in range(latest_email_id,first_email_id, -1):
            data = mail.fetch(str(i), '(RFC822)' )
            for response_part in data:
                arr = response_part[0]
                if isinstance(arr, tuple):
                    msg = email.message_from_string(str(arr[1],'utf-8'))
                    email_subject = msg['subject']
                    email_from = msg['from']
                    talk("Checking inbox")
                    print("Checking inbox......"+'\n')
                    print('From : ' + email_from + '\n')
                    talk('From : ' + email_from + '\n')
                    print('Subject : ' + email_subject + '\n')
                    talk('Subject : ' + email_subject + '\n')
            talk("You want check next mail or send a new mail?")
            c=get_info()
            if "send mail" in c:
                get_email()
                break
            elif "exit" in c:
                talk("Thank You !")
                break
            elif "next mail" in c:
                continue
                

    except Exception as e:
        traceback.print_exc() 
        talk(str(e))

        
        
        
        
        
        
# -*- This is the main function -*
def user_input():
    talk("Hello Sir, my name is Sara. I am your personal assistant.")
    talk("I am here to help you to send mail or check your inbox by only listening your command")
    talk("Do You want to send mail or want to check inbox?")
    choice=get_info()
    if "send mail" in choice:
        get_email()
    elif "check inbox" in choice:
        get_inbox()
    elif "exit" in choice:
        talk("Thank You !")
        
        
        
        
        
        
# -*-  calling the main function -*-     
user_input()
