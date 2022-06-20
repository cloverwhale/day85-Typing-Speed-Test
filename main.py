from math import floor
from tkinter import *

total_time = 60
timer = None
HIGHLIGHT = "highlight"
INCORRECT = "incorrect"

# Read source file
with open("source.txt", "r") as file:
    source_file = file.readlines()
    all_chars = source_file[0]
    all_words = all_chars.split(" ")


# Count down timer
def count_down(count):
    global timer

    count_min = floor(count / 60)
    count_sec = count % 60

    if count > 0:
        timer = root.after(1000, count_down, count - 1)
        user_input = get_user_entry()
        highlight_current_progress(user_input)
    else:
        text_speed.config(state="disabled", fg="#CCC")
        final_input = get_user_entry()
        check_final_result(final_input)

    if count_sec < 10:
        lb_timer.config(text=f"{count_min}:0{count_sec}")
    else:
        lb_timer.config(text=f"{count_min}:{count_sec}")


def start(event):
    global total_time
    # Clear original text
    text_speed.delete(1.0, END)
    text_speed.unbind("<Button-1>")
    # Start timer
    count_down(total_time)


def get_user_entry():
    user_text = text_speed.get(1.0, END)
    return user_text, user_text.split(" ")


def highlight_current_progress(user_input):
    current_chars = user_input[0]
    current_char_idx = len(current_chars)
    text_typing_source.tag_remove(HIGHLIGHT, "1.0", END)
    text_typing_source.tag_remove(INCORRECT, "1.0", END)
    text_typing_source.tag_add(HIGHLIGHT, f"1.0", f"1.{current_char_idx - 1}")
    for i in range(current_char_idx - 1):
        if current_chars[i] != all_chars[i]:
            text_typing_source.tag_add(INCORRECT, f"1.{i}", f"1.{i + 1}")
    text_typing_source.tag_configure(HIGHLIGHT, background="#CED89E")
    text_typing_source.tag_configure(INCORRECT, background="#F87474")


def check_final_result(final_input):
    highlight_current_progress(final_input)
    final_chars, final_words = final_input[0], final_input[1]
    num_chars = len(final_chars) - 1
    num_words = len(final_words) - 1
    # Compare chars
    diff_chars = [final_chars[i] for i in range(num_chars) if final_chars[i] != all_chars[i]]
    cpm = (num_chars - len(diff_chars)) / (total_time / 60)
    # Compare words
    diff_words = [final_words[i] for i in range(num_words) if final_words[i] != all_words[i]]
    wpm = (num_words - len(diff_words)) / (total_time / 60)
    # Update result
    lb_result.config(text=f"Your typing speed is: {cpm} CPM, {wpm} WPM", fg="#4CACBC")


def reset():
    global total_time
    # Reset timer
    root.after_cancel(timer)
    total_time = 60
    lb_timer.config(text="1:00")
    # Reset highlight
    text_typing_source.tag_remove(HIGHLIGHT, "1.0", END)
    text_typing_source.tag_remove(INCORRECT, "1.0", END)
    # Reset entry
    text_speed.config(state="normal", fg="#333")
    text_speed.delete(1.0, END)
    text_speed.insert("end", "Click here to start")
    text_speed.bind("<Button-1>", start)


# UI setup ------------------------------------------- #
root = Tk()
root.title("Typing Speed Test")

# Display timer
lb_timer = Label(root, text="1:00", font=("Courier New", 18, "normal"), padx=10, pady=5)
lb_timer.grid(row=0, column=0, sticky="w")

# Display final result
lb_result = Label(root, font=("Courier New", 18, "normal"), text=f"Your typing speed is: 0 CPM, 0 WPM", pady=5)
lb_result.grid(row=0, column=1)

# Display article source
lb_description = Label(root, font=("Verdana", 14, "normal"), text=f"Article source: {source_file[1]}", padx=10, pady=5)
lb_description.grid(row=1, column=0, columnspan=2, sticky="w")

# Display source, highlight bg color :#DAE5D0
text_typing_source = Text(root, width=90, height=10, spacing2=5,
                          wrap="word", font=("Arial", 16, "normal"),
                          padx=5, pady=5, bg="#F9EBC8", fg="#666")
y_scroll = Scrollbar(root, orient='vertical', command=text_typing_source.yview)
text_typing_source.config(yscrollcommand=y_scroll.set)
text_typing_source.insert("end", source_file[0])
text_typing_source.config(state="disabled")
text_typing_source.grid(column=0, row=2, columnspan=2, sticky="nwes")
y_scroll.grid(column=2, row=2, sticky="ns")

# Display user entry field
text_speed = Text(root, width=60, height=5, spacing2=5,
                  wrap="word", font=("Arial", 16, "normal"),
                  padx=5, pady=5, bg="#FEFBE7", fg="#333")
text_speed.grid(column=0, row=3, columnspan=2, sticky="nwes")
text_speed.insert("end", "Click here to start")
text_speed.bind("<Button-1>", start)

# Restart
btn_restart = Button(root, text="Reset", command=reset)
btn_restart.grid(column=0, row=4, columnspan=2, pady=10, sticky="e")

root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)
root.mainloop()
