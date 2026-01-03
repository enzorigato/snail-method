import tkinter as tk

# in questo vogliamo creare una sequenza di finestre, una di introduzione per la selezione dei parametri, una di 
# visualizzazione dei risultati.

intro_window = tk.Tk()

# setting specifiche
intro_window.geometry('400x400')
intro_window.title('Snail Method')
intro_window.resizable(height=False, width=False)
intro_window.configure(background='grey')


# Create a Frame widget with all options

# un frame funge da contenitore per altri widgets
title_frame = tk.Frame(intro_window, 
                       bg='lightblue',
                       bd=3,
                       height=100,
                       highlightthickness=2,
                       highlightbackground='black', 
                       relief=tk.RAISED,
                       width=100)

# posizionamento del frame
title_frame.pack(pady=30)

# nel senso che un label può avere come master un frame:
# widget
label = tk.Label(master=title_frame, text='Find how many small rectangles \n can be fitted into the big one!', font=('Helvetica', 15))
label.pack(fill='both', expand=True)

# insert part

# small rectangle dimensions insert part
small_frame = tk.Frame(intro_window, 
                       bg='lightblue',
                       bd=3,
                       height=100,
                       highlightthickness=2,
                       highlightbackground='black', 
                       relief=tk.RAISED,
                       width=100)




if __name__ == '__main__':
    intro_window.mainloop()