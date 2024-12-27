from time import sleep
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
from itertools import count, cycle
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import numpy as np
from matplotlib.ticker import ScalarFormatter

###########################################################################################
m_i = 6.7e-26
e = 1.60217663 * 10**-19
m_e = 9.1093837e-31
T_iv = .0259 #Energy of gaseous Argon at room temperature in eV

a = 0.5e-5  # slope of ion current for VB < VP
b = 0.1e-3 # slope of electron current for VB > VP
height_modifier = 1    #Electron current simulated max of theoretical max
stretch_modifier = 10 #Electron current simulation horizontal spread

##############################################################################################################################3

class ImageLabel(tk.Label):
    """
    A Label that displays images, and plays them if they are gifs
    :im: A PIL Image instance or a string filename
    """
    def load(self, im):
        if isinstance(im, str):
            im = Image.open(im)
        frames = []

        try:
            for i in count(1):
                frames.append(ImageTk.PhotoImage(im.copy()))
                im.seek(i)
        except EOFError:
            pass
        self.frames = cycle(frames)

        try:
            self.delay = im.info['duration']
        except:
            self.delay = 100

        self.next_frame()

    def next_frame(self):
        if self.frames:
            self.config(image=next(self.frames))
            self.after(self.delay, self.next_frame)

#################################################################################################################################

root = tk.Tk()
root.title("IV Curve GUI")

lbl = ImageLabel(root)
lbl.pack()
lbl.load('starsmall.gif')

##########################################################################################################################33    
voltage_frame = LabelFrame(root, text = "Voltage Range",bg="#ccef1b", font="Z003")
voltage_frame.pack()
voltage_frame.place(relx=.2,rely=.9,anchor=CENTER)

t5 = Label(voltage_frame, text="Units of V",bg="#ccef1b", font=("Arial", 10))
t5.pack()

textBox1=Text(voltage_frame, height=1, width=5)
textBox1.pack(side=tk.LEFT)

t4 = Label(voltage_frame, text=" to ",bg="#ccef1b", font=("Arial", 12))
t4.pack(side=tk.LEFT)

textBox2=Text(voltage_frame, height=1, width=5)
textBox2.pack(side=tk.LEFT)

#########################################################################################################################
temp_frame = LabelFrame(root, text = "e- Temperature",bg="#1BCCEF", font="Z003")
temp_frame.pack()
temp_frame.place(relx=.4,rely=.9,anchor=CENTER)

t3 = Label(temp_frame, text=" ",bg="#1BCCEF")
t3.pack(side=tk.LEFT)

textBox3=Text(temp_frame, height=1, width=5)
textBox3.pack(side=tk.LEFT)

t4 = Label(temp_frame, text=" ",bg="#1BCCEF")
t4.pack(side=tk.LEFT)

options = [ 
    "eV"
] 
  
# datatype of menu text 
clicked = StringVar() 
  
# initial menu text 
clicked.set( "eV" ) 
  
# Create Dropdown menu 
drop_temp = OptionMenu(temp_frame , clicked , *options ) 
drop_temp.pack(side=tk.LEFT) 

##########################################################################################################################

density_frame = LabelFrame(root, text = "e- Density",bg="#ccef1b", font="Z003")
density_frame.pack()
density_frame.place(relx=.6,rely=.9,anchor=CENTER)

t4 = Label(density_frame, text=" ",bg="#ccef1b")
t4.pack(side=tk.LEFT)

textBox4=Text(density_frame, height=1, width=5)
textBox4.pack(side=tk.LEFT)

t4 = Label(density_frame, text=" ",bg="#ccef1b")
t4.pack(side=tk.LEFT)

options = [ 
    "cm^-3", 
    "m^-3", 
    "Angstrom^-3"
] 
  
# datatype of menu text 
clicked = StringVar() 
  
# initial menu text 
clicked.set( "cm^-3" ) 
  
# Create Dropdown menu 
drop_temp = OptionMenu(density_frame, clicked , *options ) 
drop_temp.pack(side=tk.LEFT) 

##########################################################################################################################

area_frame = LabelFrame(root, text = "Probe Area",bg="#1BCCEF", font="Z003")
area_frame.pack()
area_frame.place(relx=.8,rely=.9,anchor=CENTER)

t4 = Label(area_frame, text=" ",bg="#1BCCEF")
t4.pack(side=tk.LEFT)

textBox5=Text(area_frame, height=1, width=5)
textBox5.pack(side=tk.LEFT)

t4 = Label(area_frame, text=" ",bg="#1BCCEF")
t4.pack(side=tk.LEFT)

options = [ 
    "mm^2"
    "cm^2", 
    "m^3", 
    "in^2"
] 
  
# datatype of menu text 
clicked = StringVar() 
  
# initial menu text 
clicked.set( "mm^2" ) 
  
# Create Dropdown menu 
drop_temp = OptionMenu(area_frame, clicked , *options ) 
drop_temp.pack(side=tk.LEFT) 

#######################################################################################################################

t3 = Label(root, text="Parameterized IV Curve Generator",bg="#ef1bcc", font=("Arial Bold", 25))
t3.pack()
t3.place(relx=.5,rely=.05,anchor=CENTER)

t4 = Label(root, text="Russell Burns '25 Honors EPAD Capstone",bg="#ef1bcc", font=("Arial", 15))
t4.pack()
t4.place(relx=.5,rely=.1,anchor=CENTER)

def exitApp():
  root.destroy()

exitButton = Button(root, command = exitApp, text="Exit", bg ='red', highlightcolor="pink")
exitButton.pack(side=TOP)

############################################################################################################
fig = Figure(figsize=(5.5, 5), dpi=100)

plot_frame = None
canvas = None
toolbar = None

def plot():
    global plot_frame, canvas, toolbar  # Reference the outer variables
    
    if plot_frame is None:
        plot_frame = tk.Frame(root)
        plot_frame.pack()
        plot_frame.place(relx=.5,rely=.5,anchor=CENTER)

        # Create the canvas object for the figure
        canvas = FigureCanvasTkAgg(fig, master=plot_frame)
        canvas.get_tk_widget().pack()

        # Create the toolbar for the canvas
        toolbar = NavigationToolbar2Tk(canvas, plot_frame)
        toolbar.update()
    fig.clear()

    v1_str = textBox1.get(1.0, "end-1c")
    print(v1_str)
    v2_str = textBox2.get(1.0, "end-1c")
    T_ev_str = textBox3.get(1.0, "end-1c")
    n_e_str = textBox4.get(1.0, "end-1c")
    A_probe_str = textBox5.get(1.0, "end-1c")
    

    try:
        v1 = int(v1_str)
        v2 = int(v2_str)
        T_ev = float(T_ev_str)
        n_e = float(n_e_str)
        A_probe = float(A_probe_str)
    except ValueError:
        print("Error: Input values must be numbers.")
        return

    n_i = n_e

    V_P = T_ev * np.log(np.sqrt(m_i / (2 * np.pi * m_e)))
    V_f = V_P + (T_ev * np.log(.6*np.sqrt(2*np.pi*(m_e/m_i))))
    I_is = .6 * e * n_i * np.sqrt(T_ev*1.62e-19/m_i) * A_probe
    I_es = .25 * e * n_e * np.sqrt((8*T_ev*1.62e-19)/(np.pi * m_e)) * A_probe

    x = np.linspace(v1, v2, 100)


    def Ii(VB, a):
        if VB < V_P:
            return -(I_is + a * (V_P - VB))
        else:
            return -I_is * np.exp((V_P - VB) / T_iv)


    def Ie(VB, b):
        if VB < V_P:
            return I_es * np.exp(-(V_P - VB) / T_ev)
        else:
            return I_es + b * (VB - V_P)
        

    def smooth_transition_curve(Ie_vals, Vp_index, height_modifier, stretch_modifier): #scaling method borrowed from gnacode. shrunk slightly
        smoothed_vals = Ie_vals.copy() 
        for val in smoothed_vals:
            height_modifier * val
        transition_start = max(0, Vp_index - int(5 * stretch_modifier))
        transition_end = min(len(smoothed_vals), Vp_index + int(10 * stretch_modifier))
        window_size = int(1 * stretch_modifier)  

        for i in range(transition_start, transition_end):
                    if i >= window_size and i < len(smoothed_vals) - window_size:
                        smoothed_vals[i] = np.mean(smoothed_vals[i - window_size:i + window_size])
        return smoothed_vals
    



    VB_range = np.linspace(v1, v2, 500)
    Vp_index = np.searchsorted(VB_range, V_P)
    raw_Ie_vals = [Ie(VB, b) for VB in VB_range]

    smoothed_Ie_vals = smooth_transition_curve(raw_Ie_vals, Vp_index, height_modifier, stretch_modifier)

    total_current = np.array(smoothed_Ie_vals) + np.array([Ii(VB, a) for VB in VB_range])
    ideal_current = np.array([Ie(VB, b=0) for VB in VB_range]) + np.array([Ii(VB, a=0) for VB in VB_range])


    plot1 = fig.add_subplot(111)
    fig.suptitle("Simulated Langmuir IV Curves")
    fig.supxlabel("Probe Bias (V)")
    fig.supylabel("Current (A)")
    plot1.tick_params(axis='y', labelsize=8) 
    plot1.plot(VB_range, ideal_current, color='blue', linestyle='-', linewidth=1, label = "Ideal Sweep")
    plot1.plot(VB_range, total_current, color='red', linestyle='-.', linewidth=1.5, label = "Smoothed Sweep")
    plot1.grid(True)
    fig.legend(fontsize=8, loc="upper right")
    canvas.draw()


plot_button = Button(root, command = plot, height = 2, width = 10, text="Plot")
plot_button.pack()
plot_button.place(relx=.9,rely=.75,anchor=CENTER)

  

root.mainloop()																																			
