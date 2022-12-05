import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import seaborn as sns
import os
from tkinter import *
# import sys
# print (sys.version)
from tkinter import *
from tkinter import filedialog as fd
import demoji

demoji.download_codes()

def find_replace_emo(text):
    # find emoji and write new text
    all_emoji = demoji.findall(text)
    new_text = 'Emojis: \n'
    if len(all_emoji)>0:
        for i,j in enumerate(all_emoji):
            item = all_emoji[j]
            new_text = new_text+str(i+1)+' '+all_emoji[j]+'\n'
            text = text.replace(j,'_')
            text = text+'\n\n'+new_text
    else:
        text = text+'\n\n'+ new_text+'\n None'
    return text

def next_review():
    # load next review
    global review_df
    global rev_index
    if (var_sent.get()) and (var_emp.get()):
        # write annotation in dataframe
        review_df['sentiment'].loc[rev_index[window._my_hidden_value]] = var_sent.get()
        review_df['reviewer'].loc[rev_index[window._my_hidden_value]] = var_emp.get()
        window._my_hidden_value = window._my_hidden_value+1
        message_1.config(text='')
        txtfld.delete(1.0,END)
        # load new review
        text = review_df['review_EN'].loc[rev_index[window._my_hidden_value]]
        text = find_replace_emo(text)
        txtfld.insert(END, text)
        var_sent.set('')
        var_emp.set('')
        # set message in remaining review count
        remaining = len(review_df[review_df['reviewer'].isnull()].index)
        message_ld2.config(text=str(remaining)+' ('+str(np.round(100*remaining/review_df.shape[0],2))+"%)",
                       font=("Avenir", 12,'bold'))
        
    else:
        # set message in incomplete review text
        message_1.config(text='Message: Please, complete the annotation of current review before going to the Next',
                     fg='red',font=("Avenir", 12,'bold'))
        
def save_annot():
    # save annotation
    global review_df
    global filename
    message_1.config(text='')
    review_df.reset_index(inplace = True)
    review_df.to_csv(filename)
    # set message in save annotation text
    message_2.config(text='Message: Annotations have been saved',
                 fg='green',font=("Avenir", 12,'bold'))
    
    
def load_annot():
    # load annotation
    global review_df
    global rev_index
    global filename
    
    filetypes = (
        ('text files', '*.csv'),
    )

    filename = fd.askopenfilename(
        title='Open a file',
        initialdir='./Data/',
        filetypes=filetypes)
    
    # load annotation file from director
    review_df = pd.read_csv(filename,index_col = 0)
    # get index of missing annotation
    review_df.set_index('index',inplace = True)
    mask = review_df['reviewer'].isnull()
    rev_index = review_df[mask].index
    # randomize index
    np.random.shuffle(rev_index.values)
    # set text in review text
    text = review_df['review_EN'].loc[rev_index[window._my_hidden_value]]
    text = find_replace_emo(text)
    txtfld.insert(END, text)
    # set message in remaining review count
    remaining = len(review_df[review_df['reviewer'].isnull()].index)
    message_ld0.config(text=filename.split('/')[-1],font=("Avenir", 10),fg='gray')
    message_ld1.config(text='Left: ',font=("Avenir", 12))
    remaining = len(review_df[review_df['reviewer'].isnull()].index)
    message_ld2.config(text=str(remaining)+' ('+str(np.round(100*remaining/review_df.shape[0],2))+"%)",
                       font=("Avenir", 12,'bold'))


###################
x_all = 50
window=Tk()
# set window size
window.geometry("600x600+10+10")
# set window title
window.title('© SAAC 2022  - TOM in Logistics: Annotation GUI - ')
# resize to false
window.resizable(False, False) 
# initial value to take from random index
window._my_hidden_value = 0

# Create a scrollbar
scrollbar = Scrollbar(window)
scrollbar.pack( side = RIGHT, fill = Y )
# title
lbl=Label(window, text="Reviews Annotation", fg='black', font=("Avenir", 16,'bold'))
lbl.place(x=10, y=10)

k = 50

# load button
Load_bt = Button(window, text ="Load Annotation File", command = load_annot, 
                 font=("Avenir", 10,'bold'),bg='red', fg='black', padx=5, pady = 3)
Load_bt.place(x = 10, y = k)

# message from load
message_ld0 = Label(window, text ="")
message_ld0.place(x = 150, y = k)
# message from remaining review
message_ld1 = Label(window, text ="")
message_ld1.place(x = 320, y = k)
# message count remaining review
message_ld2 = Label(window, text ="")
message_ld2.place(x = 350, y = k)

k = k+50
# title of reading review text
lbl=Label(window, text="Read the review (scroll text to see more)", fg='black', font=("Avenir", 12,'bold'))
lbl.place(x=x_all, y=k)

# text of review
txtfld = Text(window, height = 5, width = 60, wrap="word", bg = "lightgray", 
              yscrollcommand=scrollbar.set,padx = 20, pady = 20, font = ("Courier", 12))
txtfld.pack( side = LEFT, fill = BOTH )

# set scrollbar for text review
scrollbar.config(command=txtfld.yview)
scrollbar.pack(fill=Y)
# position of text review
txtfld.place(x=x_all, y=k+30)

k = k+120
# title for sentiment selection
lbl=Label(window, text="Indicate if you think it is a positive/neutral/negative review", fg='black', 
          font=("Avenir", 12,'bold'))
lbl.place(x=x_all, y=k+50)

# radiobutton for sentiment selection
var_sent = StringVar()
Good = Radiobutton(window, text="Positive", variable=var_sent, value='Positive',font = ("Courier", 12))
Good.place(x=x_all, y=k+100)
Neutral = Radiobutton(window, text="Neutral/Unclear", variable=var_sent, value='Neutral',font = ("Courier", 12))
Neutral.place(x=x_all+100, y=k+100)
Bad = Radiobutton(window, text="Negative", variable=var_sent, value='Negative',font = ("Courier", 12))
Bad.place(x=x_all+250, y=k+100)


# title for reviewer profile
lbl=Label(window, text="Indicate if you think the review was written by client/employee/unknown", 
          fg='black', font=("Avenir", 12,'bold'))
lbl.place(x=x_all, y=k+150)

# radiobutton for review profile
var_emp = StringVar()
Client = Radiobutton(window, text="Client", variable=var_emp, value='Client',font = ("Courier", 12))
Client.place(x=x_all, y=k+200)
Employee = Radiobutton(window, text="Employee", variable=var_emp, value='Employee',font = ("Courier", 12))
Employee.place(x=x_all+100, y=k+200)
Unknown = Radiobutton(window, text="Undefined", variable=var_emp, value='Undefined',font = ("Courier", 12))
Unknown.place(x=x_all+250, y=k+200)

# button for go to next review
next_bt = Button(window, text ="Go to Next Review >>>", command = next_review, font=("Avenir", 10,'bold'), 
                 padx=5, pady = 3)
next_bt.place(x = 10, y = k+250)

# message for unselected review
message_1 = Label(window)
message_1.place(x = 10, y = k+290)

# save button
save_bt = Button(window, text ="Save Annotations", command = save_annot, font=("Avenir", 10,'bold'), 
                 padx=5, pady = 3)
save_bt.place(x = 10, y = k+320)

# message for save button
message_2 = Label(window)
message_2.place(x = 150, y = k+320)

window.mainloop()