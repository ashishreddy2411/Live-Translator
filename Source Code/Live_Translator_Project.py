# Imports
from tkinter import *
from tkinter.ttk import *
import speech_recognition as sr
from textblob import TextBlob
from gtts import gTTS
import pyglet, time, os, sys
from languages_data import languages

# Main Logic
def start():
    # Collecting FROM and TO Languages
    pre_lang = From_Picker.get()
    post_lang = To_Picker.get()
    pre_lang_code = languages[From_Picker.get()]
    post_lang_code = languages[To_Picker.get()]
    # Checking Conversion Type and Source for Output
    conv_type = conversion_type.get()
    out_sou = output_source.get()
    if conv_type == "speech":
        # If Conversion Type is Speech, then Initialize the Microphone
        r = sr.Recognizer()
    elif conv_type == "text":
        # If Conversion Type is Text, then  Output Souce Does Not Matter (Output is Always Continuous)
        out_sou = ""
        # Setting the User Text as per FROM Language so that User can Understand
        if pre_lang == "English":
            user_input_text = "Enter Text to be Translated (In " + pre_lang + "):\n"
        else:
            user_input_text = str(TextBlob("Enter Text to be Translated (In " + pre_lang + "):\n").translate(to=pre_lang_code))
    # Closing the Window
    window.destroy()
    # Initializing Microphone
    while True:
        try:
            # If Conversion Type is Speech
            if conv_type == "speech":
                # Listening Using Microphone and Capturing Audio
                print("Listening..")
                with sr.Microphone() as source:
                    audio = r.listen(source)
                # Converting Speech to Text
                pre_lang_text = r.recognize_google(audio, language=pre_lang_code)
                print(pre_lang + ": " + pre_lang_text)
            # If Conversion Type is Text
            elif conv_type == "text":
                # Taking Input of the Text From User
                pre_lang_text = input(user_input_text)
            # Translating the Converted Text
            print("Translating..")
            post_lang_text = str(TextBlob(pre_lang_text).translate(to=post_lang_code))
            print(post_lang + ": " + post_lang_text)
            # Converting Translated Text to Speech
            speech = gTTS(post_lang_text, lang=post_lang_code)
            # Saving the Converted Speech
            fn = "temp.mp3"
            speech.save(fn)
            # Playing the Saved Speech
            music = pyglet.media.load(fn, streaming=False)
            music.play()
            if out_sou == "speaker":
                time.sleep(music.duration)
            os.remove(fn)
        except Exception:
            print("Could'nt Recognize")


# Loading Data
languages_names = tuple(i[0] for i in languages)
languages_codes = tuple(i[1] for i in languages)
languages = dict(languages)

# Creating GUI
# Creating Window
window = Tk()
window.title("Live Language Translator")
window.geometry("600x150")
# Creating Components
# From and To Pickers to Select Languages
From_Label = Label(window, text="From : ")
From_Picker = Combobox(window, values=languages_names)
To_Label = Label(window, text="To : ")
To_Picker = Combobox(window, values=languages_names)
# Conversion Type Radio Button to Choose Speech or Text as Type
conversion_type = StringVar()
conversion_type.set("speech")
Type_Label = Label(window, text="Type of Translation: ")
Text_Radio = Radiobutton(window, text="Text", variable=conversion_type, value="text")
Speech_Radio = Radiobutton(window, text="Speech", variable=conversion_type, value="speech")
# Output Source Radio Button to Choose Earphones or Speaker as Source
output_source = StringVar()
output_source.set("speaker")
Output_Label = Label(window, text="Source of Output (Only for Speech Type): ")
Earphones_Radio = Radiobutton(window, text="Earphones(Continuous)", variable=output_source, value="earphones")
Speaker_Radio = Radiobutton(window, text="Speaker(Sentence by Sentence)", variable=output_source, value="speaker")
# Button to Start the Translation Algorithm (Start Function) Based on the Inputs Provided
Start_Label = Label(window, text="Click Below to Start Translating")
Start_Button = Button(window, text="Start", command=start)
Stop_Label = Label(window, text="(Stop the Program from Terminal)")

# Aligning the Components Inside the Window
From_Label.grid(column=0, row=0)
From_Picker.grid(column=1, row=0)
To_Label.grid(column=0, row=1)
To_Picker.grid(column=1, row=1)
Type_Label.grid(column=0, row=2)
Text_Radio.grid(column=1, row=2)
Speech_Radio.grid(column=2, row=2)
Output_Label.grid(column=0, row=3)
Earphones_Radio.grid(column=1, row=3)
Speaker_Radio.grid(column=2, row=3)
Start_Label.grid(column=1, row=4)
Start_Button.grid(column=1, row=5)
Stop_Label.grid(column=1, row=6)

# Running the Window
window.mainloop()
