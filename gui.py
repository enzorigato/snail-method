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

# INSERT PART 1

# small rectangle dimensions insert part
small_frame = tk.Frame(intro_window, 
                       bg='lightblue',
                       bd=3,
                       width=50,
                       height=70,
                       highlightthickness=2,
                       highlightbackground='black', 
                       relief=tk.RAISED)

small_frame.pack(fill='x', padx=15, pady=5)

# text
small_descr = tk.Label(master=small_frame,
                       text='Insert small rectangle dimensions:',
                       height=1,
                       width=50,
                       bg='lightblue',
                       font=('Helvetica', 11))
small_descr.pack()

# insert
'''
small_x_frame = tk.Frame(small_frame, 
                        bg='light goldenrod',
                        width=20,
                        height=20,
                        relief=tk.RAISED)

small_x_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=5)
'''

# oggetto per ricevere le specifiche

# entry 1
small_x_text = tk.Label(master=small_frame, 
                        text='Width',
                        bg='light goldenrod',
                        height=1,
                        width=5
                        )

small_x_text.pack(side=tk.LEFT)

small_width = tk.Entry(master=small_frame, bg='white')
small_width.pack(side=tk.LEFT, fill='x')

# entry 2
small_y_text = tk.Label(master=small_frame, 
                        text='Height',
                        bg='light goldenrod',
                        height=1,
                        width=5
                        )

small_y_text.pack(side=tk.LEFT)

small_height = tk.Entry(master=small_frame, bg='white')
small_height.pack(side=tk.LEFT, fill='x')



# INSERT PART 2

# big rectangle dimensions insert part
big_frame = tk.Frame(intro_window, 
                    bg='lightblue',
                    bd=3,
                    width=50,
                    height=70,
                    highlightthickness=2,
                    highlightbackground='black', 
                    relief=tk.RAISED)

big_frame.pack(fill='x', padx=15, pady=5)

# text
big_descr = tk.Label(master=big_frame,
                       text='Insert container rectangle dimensions:',
                       height=1,
                       width=50,
                       bg='lightblue',
                       font=('Helvetica', 11))
big_descr.pack()

# oggetto per ricevere le specifiche

# entry 1
big_x_text = tk.Label(master=big_frame, 
                        text='Width',
                        bg='light goldenrod',
                        height=1,
                        width=5
                        )

big_x_text.pack(side=tk.LEFT)

big_width = tk.Entry(master=big_frame, bg='white')
big_width.pack(side=tk.LEFT, fill='x')
big_width.insert(1, '120')

# entry 2
big_y_text = tk.Label(master=big_frame, 
                        text='Height',
                        bg='light goldenrod',
                        height=1,
                        width=5,
                        )

big_y_text.pack(side=tk.LEFT)

big_height = tk.Entry(master=big_frame, bg='white')
big_height.pack(side=tk.LEFT, fill='x')
big_height.insert(1, '80')

# todo: BUTTON PART




if __name__ == '__main__':
    intro_window.mainloop()