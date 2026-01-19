import tkinter as tk
import snail_method as sm
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# in questo vogliamo creare una sequenza di finestre, una di introduzione per la selezione dei parametri, una di 
# visualizzazione dei risultati.

intro_window = tk.Tk()

# setting specifiche
intro_window.geometry('400x310')
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



def get_results():

    # save parameters
    cnt = sm.Container(length=float(big_height.get()), width=float(big_width.get()))
    box = sm.Box(x=float(small_width.get()), y=float(small_height.get())) 

    intro_window.withdraw() # permette di nascondere la intro_window temporaneamente (la recuperiamo nel caso si voglia ritornare indietro)

    # top level - finestra secondaria
    res_window = tk.Toplevel(master=intro_window)
    res_window.geometry('800x620')
    res_window.title('Snail Method')
    res_window.resizable(height=False, width=False)
    res_window.configure(background='grey')
    
    # protocol needed in order to have the app converging when window are closed
    def close_trigger():
        plt.close('all')
        intro_window.destroy()

    res_window.protocol('WM_DELETE_WINDOW', close_trigger)

    # backend computations
    opt = cnt.optimize(box)

    res_frame = tk.Frame(res_window, 
                         bg='lightblue',
                         bd=3, 
                         height=100,
                         highlightthickness=2,
                         highlightbackground='black', 
                         relief=tk.RAISED,
                         width=100)
    
    res_frame.pack(pady=30)

    res_title = tk.Label(master=res_frame,
                         text=f'{opt.card} boxes have been displaced.',
                         font=('Helvetica', 15))
    
    res_title.pack(fill='both', expand=True)


    fig = opt.show(cnt.width, cnt.length)


    # creating the Tkinter canvas containing the Matplotlib figure
    canvas = FigureCanvasTkAgg(fig, master=res_frame)  
    canvas.draw()

    # placing the toolbar on the Tkinter window
    canvas.get_tk_widget().pack()


    # return to parameter setting button
    def reset_parameters():
        '''
        Restores the parameters setting window and destroy the viz one.
        '''
        intro_window.deiconify() # restoring intro window
        plt.close('all')
        res_window.destroy()
        

    reset_button = tk.Button(master=res_window,
                             text='back to parameters...',
                             fg='blue',
                             command=reset_parameters)
    
    reset_button.pack()



# Computation/viz of the results trigger

compute_button = tk.Button(text='Elaborate',
                           fg='green',
                           command=get_results)

compute_button.pack(pady=15)

if __name__ == '__main__':
    intro_window.mainloop()