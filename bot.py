from decouple import config
from datetime import date
import time
import datetime
import csv
import telegram
import telegram.ext
import long_responses as long
import responses as rp
import emoji
from googletrans import Translator

# Importing login credentials and Telegram API for bot from .env file
USERNAME = config('USERNAME')
TOKEN = config('TOKEN')
COMMAND = "init"
# TOKEN = os.environ['TOKEN']

# Making object of Translator
translator = Translator(service_urls=['translate.googleapis.com'])

# Start command to start the bot
def start(update, context):
    global COMMAND
    COMMAND = 'start'
    update.message.reply_text(emoji.emojize("Hello! :open_hands:\nI am Sylvie, bot head at 'Bots Around Us'. :robot:\nTo dive in type /help."))
#  emoji.emojize is used to send emoji in the message.
#  update.message.reply_text is replying the text to user

# Help command lists all the available commands that can be used to run the bot
def help(update,context):
    global COMMAND
    COMMAND = 'help'
    update.message.reply_text(emoji.emojize("""I can help you with the following:  
/start -> Welcome to the channel
/help  -> This message
/hackathon -> Details of the Hackathon 
/registration -> Handles the registration process
/resources -> Shares the resources 
/chat -> Handles the FAQ's of student
/reminders -> Gives reminders for registered students
/contact -> Contact information 
/feedback -> Enter feedback for this bot
/announcements -> Recent Notices and Announcements
    """))

# hackthon command:It has all the details about the hackathon
def hackathon(update, context):
    global COMMAND
    COMMAND = 'hackathon'
    time.sleep(0.5)
    #  The time.sleep function generates a gap between two messages
    update.message.reply_text("So, 'Bots Around Us' is a hackathon with a vision of building fun and beautiful bots like me.\n\nUnder this student-led hackathon you will get a chance to compete with participants all over India. The team who will build the best bot will be declared as winner!!")
    time.sleep(0.8)
    update.message.reply_text('''
The details are as followed:

1. Schedule : 25-27th Feb 2023
2. Location : Online
3. Rules: Register before 18th Feb.
    You can use any tech stack to build my fellow bot friends.
4. Prizes : The winner will be getting a cash prize of Rs. 10,000/-.

All the participants will be getting participation certis signed by Meta Head''')
    time.sleep(1)
    update.message.reply_text("Isn't it interesting??")
    time.sleep(0.8)
    update.message.reply_text("What are you waiting for? Head to '/registration' to register yourself!!")

# Registration command: All registration-related tasks will be handled by it.
# In addition, it has three functions, namely register, cancel, and confirm.
def registration(update, context):
    global COMMAND
    COMMAND = 'registration'
    update.message.reply_text("""I can help you with the following:

/register -> Register yourself for the hackathon
/confirm  -> Confirm your registration
/cancel   -> Cancel your registration""")
    update.message.reply_text("Make sure to register before the deadline - 18th February as this will give you an opportunity to collaborate and compete with students from different universities and develop a telegram bot. You stand to win exciting cash prizes and certificates. It's a chance to learn, develop and present your protypes and seek feedback on the same. ")

# Resources command: It will provide users with resources, sample projects, and documentation.
def resources(update, context):
    global COMMAND
    COMMAND = 'resources'
    update.message.reply_text("tutorial link 1: https://www.youtube.com/watch?v=PTAkiukJK7E\ntutorial link 2: https://www.youtube.com/watch?v=CNkiPN_WZfA")
    time.sleep(0.1)
    update.message.reply_text('''
    Sample Projects:
    https://www.pragnakalp.com/create-telegram-bot-using-python-tutorial-with-examples/
    
    https://pythonprogramming.org/making-a-telegram-bot-using-python/                              
                              ''')
    time.sleep(0.2)
    update.message.reply_text("Explore these tutorials to see how smart bots like me are made.")
    time.sleep(3)
    update.message.reply_text("Just kidding!")
    time.sleep(0.1)
    update.message.reply_text("I know you can make an even smatter bot. So register yourself fast and grab this chance to learn and showcase your creativity.\nSee you at the Hackathon!!")
    time.sleep(2)
    help(update, context)

# Chat command: It will resolve user's query regarding hackathon.
def chat(update, context):
    global COMMAND
    COMMAND = 'chat'
    update.message.reply_text("How can I help you?")

# Set_Reminder: User-specified date and time will be used to set the reminder 
# and remind the user on that day that the hackathon is approaching.
def set_reminder(update, context, user_input):
    d, t = user_input.split("\n")[0], user_input.split("\n")[1]
    d = list(map(int, d.split("-")))
    t = list(map(int, t.split(":")))
    entered_date = datetime.datetime(d[0], d[1], d[2], t[0], t[1])
    # Extracting presnt date and time
    present_date_datetime = datetime.datetime.now()
    difference = entered_date - present_date_datetime
    # total seconds
    time_difference_in_seconds = difference.total_seconds()

    # Schedule the reminder using the time difference
    context.job_queue.run_once(send_reminder, time_difference_in_seconds, context=update.message.chat_id)
    update.message.reply_text("Reminder set for {} and {}".format(d, t))
    time.sleep(1)
    help(update, context)

# Send_reminder: It will send reminder on the date time set by the user
def send_reminder(context):
    # Send the reminder message to the user
    context.bot.send_message(chat_id=context.job.context, text="REMINDER:\nBuck Up Mate, Hackathon is approaching !!\nI hope you are all decked up for the submission. Excited to meet my fellow bot.")

def reminders(update, context):
    global COMMAND
    COMMAND = 'reminders'
    # tells the user the correct format
    update.message.reply_text("""Enter Date(yyyy-mm-dd): 
Enter Time (hh:mm)""")

# Contact: It will give the contact details of organisers
def contact(update, context):
    global COMMAND
    COMMAND = 'contact'
    update.message.reply_text('''
    Reach out to the organisers via:
    Ph No: +91 923497621
    Email id: botsaroundus@gmail.com
    Instagram Handle: @BotsAroundUs
    ''')

# Announcements: It will show if there are any updates/notice by the admin
def announcements(update, context):
    global COMMAND
    COMMAND = 'announcements'
    update.message.reply_text("ANNOUNCEMENTS:\nNo new announcements!")
    help(update, context)

# handle_message : It is helping to recognise the command entered by user whichis not a command
# and also handling is the user writes something unwanted
def handle_message(update, context):
    global COMMAND
    usertext = update.message.text
    if COMMAND == 'register':
        get_details(update, context, usertext)
    elif COMMAND == 'confirm':
        confirm_details(update, context, usertext)
    elif COMMAND == 'cancel':
        delete_record(update, context, usertext)
    elif COMMAND == 'reminders':
        set_reminder(update, context, usertext)
    elif COMMAND == 'feedback':
        save_feedback(update, context, usertext)
    elif COMMAND == 'chat':
        detected_language = translator.detect(usertext).lang
        if detected_language != 'en':
            translated_text = translator.translate(usertext, dest='en').text
            update.message.reply_text(rp.get_response(translated_text))
        else:
            update.message.reply_text(rp.get_response(usertext))

# Is_invalid: Checking constraints for mobile number
def is_invalid(number):
    if len(number) != 10:
        return True
    
    digits = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}
    for i in number:
        if int(i) not in digits:
            return True
    return False

# Write_record: Writes the details entered by user into csv file after validating them
def write_record(details):
    file = open('registrationDetails.csv', 'a+', newline ='')
 
    with file:   
        write = csv.writer(file)
        write.writerow(details)

# Not_primary: Checks if the entered email id is already registered or not.
def not_primary(email_id):
    with open('registrationDetails.csv', 'r') as fp:
        s = fp.read()
        # print(s)
        for row in s.split("\n"):
            # print(row)
            if len(row) == 0:
                return False
            # print(row)
            words = row.split(",")
            # print(words)
            if words[3] == email_id:
                return True
    return False

# get_details: It takes input from users about the details of team members and validates them.
def get_details(update, context, user_input):
        details = user_input.split("\n")
        if len(details) != 5:
            update.message.reply_text("Insufficient Details")
        else:
            members = int(details[0])
            flag = 0
            if members not in {1, 2, 3}:
                update.message.reply_text("Number of members can only be 1 ,2 or 3")
                flag = 1
            if '@' not in details[3] or '.' not in details[3]:
                update.message.reply_text("Please Enter Valid Email")
                flag = 1
            if is_invalid(details[4]):
                update.message.reply_text("Please Enter valid 10 digit mobile number")
                flag = 1
            
            if not_primary(details[3]):
                flag = 1
                update.message.reply_text("This email is already registered. Please use another id.")
            if flag == 0:
                now = date.today()
                details.append(now)
                write_record(details)
                update.message.reply_text("You have successfully registered for the Bots Around Us hackathon.")
                update.message.reply_text("Excited to see that you are keen to learn and participate. You can explore the /resources and /confirm sections as well.")

# register command: Handles the registration process
def register(update, context):
    global COMMAND
    COMMAND = 'register'

    update.message.reply_text("""Welcome to the registration portal. Please provide the following details in separate lines.""")
    time.sleep(0.5)
    update.message.reply_text("""No Of Members
Team Name
Your Full Name
Your Email ID
Your Phone Number""")

#confirm_details: It confirms the registration of user and return their details.
def confirm_details(update, context, email_id):
    data  = ""
    with open('registrationDetails.csv', 'r+') as fp:
        s = fp.read()
        for row in s.split("\n"):
            if len(row) == 0:
                break
            words = row.split(",")
            # print(words)
            if words[3] == email_id:
                data = row
                break

    if len(data) != 0:
        update.message.reply_text("You are registered and your details are as follows:")
        entries = data.split(",")
        update.message.reply_text("""No Of Members: {}
Team Name: {}
Full Name: {}
Email ID: {}
Phone Number: {}
Date Of Registration : {}""".format(entries[0], entries[1], entries[2], entries[3], entries[4], entries[5]))
    else:
        update.message.reply_text("This Email Id is not registered yet.")
    
    time.sleep(1)
    help(update, context)

# confirm: Confirms the registration of user by checking the email id
def confirm(update, context):
    global COMMAND
    COMMAND = 'confirm'
    update.message.reply_text("Enter your Email ID to confirm your registration.")

def delete_record(update, context, email_id):
    global COMMAND
    data  = ""
    with open('registrationDetails.csv', 'r+') as fp:
        s = fp.read()
        for row in s.split("\n"):
            if len(row) == 0:
                break
            words = row.split(",")
            # print(words)
            if words[3] == email_id:
                data = row
                break

    if len(data) != 0:
        update.message.reply_text("Your details are as follows:")
        entries = data.split(",")
        update.message.reply_text("""No Of Members: {}
Team Name: {}
Full Name: {}
Email ID: {}
Phone Number: {}
Date Of Registration : {}""".format(entries[0], entries[1], entries[2], entries[3], entries[4], entries[5]))
        update.message.reply_text("Cancelling your registration")
        time.sleep(1)
        input = open('registrationDetails.csv', 'r+')
        output = open('edit.csv', 'w+')
        writer = csv.writer(output)
        for row in csv.reader(input):
            if row[3] != email_id:
                writer.writerow(row)
        input.close()
        output.close()

        input = open('edit.csv', 'r+')
        output = open('registrationDetails.csv', 'w+')
        writer = csv.writer(output)
        for row in csv.reader(input):
            writer.writerow(row)
        input.close()
        output.close()
        update.message.reply_text("Your registration was cancelled. Sorry to see you go.")
        time.sleep(0.5)
        update.message.reply_text("If there was a particular problem that you faced please let us know in the /feedback section")
        time.sleep(1)
        help(update, context)
    else:
        update.message.reply_text("This Email Id is not registered yet.")

# Cancel: Cancels the registration of user
def cancel(update, context):
    global COMMAND
    COMMAND = 'cancel'
    update.message.reply_text("Enter your Email ID to cancel your registration.")

# Save_feedback: Saves the feeback given by user in text file.
def save_feedback(update, context, usertext):
    f = open('feedback.txt', 'a+')
    f.write(usertext + "\n")
    f.close()
    time.sleep(1)
    update.message.reply_text("Feedback was received successfully. Hope to continue providing services to you.")
    time.sleep(1)
    help(update, context)

# Feedback: Allows user to give feedback .
def feedback(update, context):
    global COMMAND
    COMMAND = 'feedback'
    update.message.reply_text("We would love to hear what you think about the experience. Don't hold back and let us know everything.")

updater = telegram.ext.Updater(TOKEN, use_context=True)
disp = updater.dispatcher

# Adding all functions as handlers
disp.add_handler(telegram.ext.CommandHandler('start',start))
disp.add_handler(telegram.ext.CommandHandler('help',help))
disp.add_handler(telegram.ext.CommandHandler('hackathon',hackathon))
disp.add_handler(telegram.ext.CommandHandler('registration',registration))
disp.add_handler(telegram.ext.CommandHandler('resources',resources))
disp.add_handler(telegram.ext.CommandHandler('chat',chat))
disp.add_handler(telegram.ext.CommandHandler('reminders',reminders))
disp.add_handler(telegram.ext.CommandHandler('contact',contact))
disp.add_handler(telegram.ext.CommandHandler('register',register))
disp.add_handler(telegram.ext.CommandHandler('confirm',confirm))
disp.add_handler(telegram.ext.CommandHandler('cancel',cancel))
disp.add_handler(telegram.ext.CommandHandler('feedback',feedback))
disp.add_handler(telegram.ext.CommandHandler('announcements',announcements))
disp.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.text, handle_message))
updater.start_polling()
updater.idle()