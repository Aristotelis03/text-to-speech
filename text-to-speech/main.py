import json
from gtts import gTTS
from customtkinter import *
from CTkListbox import *
import pyglet
import os

set_appearance_mode("dark")
set_default_color_theme("dark-blue")
history = []
json_file = "history.json"

class App(CTk):
    history_labels = []

    def __init__(self):
        super().__init__()

        self.title("Text To Speech")
        self.geometry("620x420")

        self.frame = CTkFrame(self)
        self.frame.grid(row=1, column=1, pady=10, padx=20, sticky="ew")
        
        self.labelH = CTkLabel(self.frame, text="History")
        self.labelH.pack(pady=5, padx=5)

        self.historyFrame = CTkScrollableFrame(self.frame, width=500)
        self.historyFrame.pack(pady=5, padx=5)

        self.frame2 = CTkFrame(self)
        self.frame2.grid(row=2, column=1, pady=10, padx=20, sticky="ew")

        self.input = CTkTextbox(self.frame2, height=80, width=450)
        self.input.grid(row=2, column=1, pady=10, padx=10, sticky="ew")

        self.submit = CTkButton(self.frame2, text="Play", command=lambda: self.convert_and_history(self.input.get("1.0", END)), width=70, height=35)
        self.submit.grid(row=2, column=2, pady=10, padx=20, sticky="ew")

    def on_enter_pressed(self, event):
        self.convert_and_history(self.input.get("1.0", END))
        
    def text_to_speech(self, text):
        # text = self.input.get("1.0", END)

            obj = gTTS(text=text, lang='en', slow=False)
            obj.save("test.mp3")

            # Using pydub to play the audio
            audio = pyglet.media.load('test.mp3')
            audio.play()
            os.remove("test.mp3")


    def text_to_history(self,text):
        history.append({"prompt": text.strip()})

        with open(json_file, "w") as file:
            json.dump(history, file, indent=4)
            print("JSON file created and data has been saved.")

        # Read data from JSON file
        with open(json_file, "r") as file:
            loaded_data = json.load(file)

        print("Loaded data:", loaded_data)
    
    def update_history(self):
        # Clear existing labels
        for label in self.history_labels:
            label.destroy()
        self.history_labels = []  # Clear the list
            
        with open(json_file, "r") as file:
            loaded_data = json.load(file) 
        for item in loaded_data:
            self.history_item = CTkLabel(self.historyFrame,text=item["prompt"], wraplength=450, bg_color="#3c3c3c")
            self.history_item.pack(fill="both", expand=True, padx=10, pady=10)
            self.history_item.bind("<Button-1>", command=self.on_history_item_click)
            self.history_labels.append(self.history_item)
    
    def convert_and_history(self, text):
        if text.strip() != "":
            self.text_to_speech(text)
            self.text_to_history(text)
            self.update_history()
        else:
            print("empty")

    def on_history_item_click(self,event):
        if event.widget.winfo_exists():
            label_text = event.widget.cget("text")
            self.text_to_speech(label_text)
        else:
            print("Widget does not exist.")

if __name__ == "__main__":
    app = App()
    app.mainloop()