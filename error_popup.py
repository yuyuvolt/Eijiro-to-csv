import tkinter as tk

def error_popup(mes:str):
    root = tk.Tk()
    root.title("Error")
    frame = tk.Frame(root, padx=8, pady=8)
    frame.pack()
    error_message = tk.Label(frame, text=mes, justify=tk.LEFT, wraplength=282)
    button = tk.Button(frame, text="OK", command=lambda : root.destroy())
    button.pack(side=tk.BOTTOM)
    error_message.pack(expand=True, anchor="nw")
    root.mainloop()