from tkinter import Tk, END, ANCHOR, Entry, Button, Frame, Label, Listbox, StringVar, OptionMenu
from json import load, dump

with open("storage.json", "r") as read_obj:
    storage = load(read_obj)

def save(files):
    with open("storage.json", "w") as write_obj:
        dump(files, write_obj)

def list_selection(event):
    show_selection.delete(0, END)
    var_show_selection.set(main_selection.get(ANCHOR))
    if main_selection.get(ANCHOR) == "Currently Playing":
        lbl_show_selection.config()
        for game in storage["Currently Playing"]:
            show_selection.insert(END, game)
    elif main_selection.get(ANCHOR) == "Completed":
        for game in storage["Completed"]:
            show_selection.insert(END, game)
    elif main_selection.get(ANCHOR) == "Backlog":
        for game in storage["Backlog"]:
            show_selection.insert(END, game)
    elif main_selection.get(ANCHOR) == "Abandoned":
        for game in storage["Abandoned"]:
            show_selection.insert(END, game)
    else:
        return event

def add(select):
    win_add = Tk()
    win_add.resizable(False, False)
    win_add.title(f"Add to {select}")


    ent_add_name = Entry(master=win_add, width=40)
    ent_add_name.insert(0, " Enter game name here... ")
    option_add_platform = StringVar(win_add)
    option_add_platform.set("Select Platform")
    ent_add_platform = OptionMenu(win_add, option_add_platform, *storage["Platforms"])

    ent_add_name.grid(row=1, column=0)
    ent_add_platform.grid(row=1, column=1)
    btn_add_submit = Button(win_add, text="Submit", width=10, anchor="center", command=lambda: [
        storage[select].append(f"{ent_add_name.get()}, {option_add_platform.get()}"),
        show_selection.insert(END, f"{ent_add_name.get()}, {option_add_platform.get()}"),
        win_add.destroy(),
        save(storage)
    ])
    btn_add_submit.grid(row=2, columnspan=2)

def delete(key, value):
    if value not in key:
        pass
    else:
        key.remove(value)

# --- Root Window
root = Tk()
root.title("VG Tracker")
root.resizable(False, False)

# --- Widgets
# Left Box, Main Selection
frm_left = Frame(master=root, padx=5)
lbl_main_selection = Label(master=frm_left, text="Selection Menu")
main_selection = Listbox(master=frm_left)
for item in storage["Menu"]:
    main_selection.insert(END, item)
lbl_credit = Label(master=frm_left, text=" VG Tracker\ngithub.com/AlexGeorgevich", font=("Arial", 7, "bold"), foreground="blue")
lbl_credit.place(anchor="center")
 
# Right Box, Show Selection
frm_right = Frame(master=root, padx=5)
var_show_selection = StringVar(value="")
lbl_show_selection = Label(master=frm_right, textvariable=var_show_selection)
show_selection = Listbox(master=frm_right, width=55)
main_selection.bind("<<ListboxSelect>>", list_selection)

# Right Bottom, Buttons
frm_btm_right = Frame(master=root, pady=2)
btn_add = Button(master=frm_btm_right, text="Add", command=lambda:add(select=main_selection.get(ANCHOR)))
btn_delete = Button(master=frm_btm_right, text="Delete", command=lambda: [delete(
    key=storage[main_selection.get(ANCHOR)],
    value=show_selection.get(ANCHOR)),
    show_selection.delete(ANCHOR),
    save(storage)])

# --- Grid of Widgets
# Left Frame
frm_left.grid(rowspan=2, column=0, sticky="n")
lbl_main_selection.grid(row=0, column=0)
main_selection.grid(row=1, column=0)
lbl_credit.grid(row=2, column=0)

# Right Frame
frm_right.grid(row=0, column=1)
lbl_show_selection.grid(row=0, column=0)
show_selection.grid(row=1, column=0)

# Right Bottom Frame
frm_btm_right.grid(row=1, column=1)
btn_add.grid(row=0, column=0)
btn_delete.grid(row=0, column=2)

root.mainloop()
save(storage)
