import os
from discord_webhook import DiscordWebhook
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import time
import requests

def MultiHookSend():
    modeMulti = modeTitle_combobox.get()
    delayMulti = SchedulerDelaySpinbox.get()

    hooks = [MultiHookInput1.get(), MultiHookInput2.get(), MultiHookInput3.get(), MultiHookInput4.get(), MultiHookInput5.get()]
    message = MultiHookMessageInput.get()

    if modeMulti == 'Sender':
        MultiHook = DiscordWebhook(url=hooks, content=message)
        responseMulti = MultiHook.execute()
    elif modeMulti == 'Spammer':
        while True:
            MultiHook = DiscordWebhook(url=hooks, content=message)
            responseMulti = MultiHook.execute()
            time.sleep(0.7)
    elif modeMulti == 'Scheduler':
        while True:
            MultiHook = DiscordWebhook(url=hooks, content=message)
            responseMulti = MultiHook.execute()
            time.sleep(int(delayMulti))


def delete():
    deleteURL = DeleteURLEntry.get()
    deleteRequest = requests.get(deleteURL)
    if deleteRequest.status_code != 200:
        messagebox.showinfo('Error', 'Webhook Does not exist or has already been deleted.')
    else:
        os.system('curl -X DELETE ' + deleteURL)
        messagebox.showinfo('Success', 'Webhook deleted successfully')
    

def send():
    sendIt = False
    url = hookURLEntry.get()
    msg = WebhookMessageEntry.get()
    mode = modeTitle_combobox.get()
    delay = SchedulerDelaySpinbox.get()

    if "https://" in url:
        hook404Check = requests.get(url)
        if hook404Check.status_code == 404 or msg == None:
            messagebox.showinfo('Error', 'Webhook does not exist.')
            sendIt = False
        else:
            sendIt = True
    else:
        messagebox.showinfo('Error', 'Please put a real webhook url')

    hook = DiscordWebhook(url=url, content=msg)

    if sendIt == True:
        match mode:
            case 'Spammer':
                while True:
                    spam = hook.execute()
                    time.sleep(0.7)
            case 'Sender':
                sendMessage = hook.execute()
            case 'Scheduler':
                while True:
                    sendScheduledMessage = hook.execute()
                    time.sleep(int(delay))
            case 'Nuker Preset':
                for i in range(15):
                    Nuke = hook.execute()
                os.system('curl -X delete ' + url)
    else:
        messagebox.showinfo('Error', 'Webhook does not exist or your message is empty.')

 


Window = tk.Tk()
Window.title('ANACONDA by defrost#0628')

frame = tk.Frame(Window)
frame.pack()


#getting hook info
hookInfoFrame = tk.LabelFrame(frame, text='Information')
hookInfoFrame.grid(row=0, column=0)

hookURL = tk.Label(hookInfoFrame, text='Webhook URL', font=('Arial', 11))
hookURL.grid(row=0, column=0)
WebhookMessage = tk.Label(hookInfoFrame, text='Webhook Message', font=('Arial', 10))
WebhookMessage.grid(row=0, column=1)

hookURLEntry = tk.Entry(hookInfoFrame)
WebhookMessageEntry = tk.Entry(hookInfoFrame)
hookURLEntry.grid(row=1, column=0)
WebhookMessageEntry.grid(row=1, column=1)

modeTitle = tk.Label(hookInfoFrame, text='Mode')
modeTitle_combobox = ttk.Combobox(hookInfoFrame, values=["Spammer", "Sender", "Scheduler"])
modeTitle.grid(row=2, column=1)
modeTitle_combobox.grid(row=3, column=1)

imageURL = tk.Label(hookInfoFrame, text='Times to send (if sender is selected)')
imageURLSpinbox = tk.Spinbox(hookInfoFrame, from_=1, to_='infinity')
imageURL.grid(row=2, column=0)
imageURLSpinbox.grid(row=3, column=0)

SchedulerDelay = tk.Label(hookInfoFrame, text='Scheduler Delay')
SchedulerDelaySpinbox = tk.Spinbox(hookInfoFrame, from_=1, to='infinity')
SchedulerDelay.grid(row=0, column=2)
SchedulerDelaySpinbox.grid(row=1, column=2)

DeleteURL = tk.Label(hookInfoFrame, text='Webhook Deleter')
DeleteURLEntry = tk.Entry(hookInfoFrame)
DeleteButton = tk.Button(hookInfoFrame, text='Delete Webhook!', command=delete, activebackground='#f93432')
DeleteButton.grid(row=4, column=2)
DeleteURL.grid(row=2, column=2)
DeleteURLEntry.grid(row=3, column=2)


sendButton = tk.Button(hookInfoFrame, text='Start!', width=10, height=1, command=send, activebackground='#f93432')
sendButton.grid(row=4, column=0)

MultiHookURL1 = tk.Label(hookInfoFrame, text='URL 1')
MultiHookURL2 = tk.Label(hookInfoFrame, text='URL 2')
MultiHookURL3 = tk.Label(hookInfoFrame, text='URL 3')
MultiHookURL4 = tk.Label(hookInfoFrame, text='URL 4')
MultiHookURL5 = tk.Label(hookInfoFrame, text='URL 5')
MultiHookInput1 = tk.Entry(hookInfoFrame)
MultiHookInput2 = tk.Entry(hookInfoFrame)
MultiHookInput3 = tk.Entry(hookInfoFrame)
MultiHookInput4 = tk.Entry(hookInfoFrame)
MultiHookInput5 = tk.Entry(hookInfoFrame)

MultiHookURL1.grid(row=1, column=5)
MultiHookURL2.grid(row=2, column=5)
MultiHookURL3.grid(row=3, column=5)
MultiHookURL4.grid(row=4, column=5)
MultiHookURL5.grid(row=5, column=5)
MultiHookInput1.grid(row=1, column=6)
MultiHookInput2.grid(row=2, column=6)
MultiHookInput3.grid(row=3, column=6)
MultiHookInput4.grid(row=4, column=6)
MultiHookInput5.grid(row=5, column=6)

MultiHookMessage = tk.Label(hookInfoFrame, text='Message')
MultiHookMessage.grid(row=6, column=6)

MultiHookMessageInput = tk.Entry(hookInfoFrame)
MultiHookMessageInput.grid(row=7, column=6)

MultiHookSendButton = tk.Button(hookInfoFrame, text='Send to all hooks!', command=MultiHookSend)
MultiHookSendButton.grid(row=8, column=6)


for widget in hookInfoFrame.winfo_children():
    widget.grid_configure(padx=1, pady=1)

#----------------------------------------------------------
Window.mainloop()
