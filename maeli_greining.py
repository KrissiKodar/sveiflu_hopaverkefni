import numpy as np
import PySimpleGUI as sg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import pandas as pd
from scipy.fft import fft,fftfreq

sg.theme('SystemDefault')

def func(message='Default message'):
    print(message)

def draw_figure_w_toolbar(canvas, fig, canvas_toolbar):
    if canvas.children:
        for child in canvas.winfo_children():
            child.destroy()
    if canvas_toolbar.children:
        for child in canvas_toolbar.winfo_children():
            child.destroy()
    figure_canvas_agg = FigureCanvasTkAgg(fig, master=canvas)
    figure_canvas_agg.draw()
    toolbar = Toolbar(figure_canvas_agg, canvas_toolbar)
    toolbar.update()
    figure_canvas_agg.get_tk_widget().pack(side='right', fill='both', expand=1)

class Toolbar(NavigationToolbar2Tk):
    def __init__(self, *args, **kwargs):
        super(Toolbar, self).__init__(*args, **kwargs)


layout = [[sg.Text('Mæliforrit', size=(23, 1), justification='center', font=("Helvetica", 15), relief=sg.RELIEF_RIDGE)],      
                 [sg.B('Innlestur')],      
                 [sg.T('Söfnunartíðni', size=(12, 1)),sg.InputText(size=(12, 1))],
                 [sg.T('Fjöldi mæligilda', size=(12, 1)),sg.InputText(key='fjoldi_maeli',size=(12, 1))],
                 [sg.B('Mæling')],
                 [sg.T('Vista í skrá', size=(12, 1)),sg.InputText(size=(12, 1))],
                 [sg.B('Vista')],
                 [sg.B('FFT greining')],#key=lambda: func('FFT greining')
                 [sg.T('Controls:')],
                 [sg.Canvas(key='controls_cv')],
                 [sg.T('Graf')],
                 [sg.Column(layout=[[sg.Canvas(key='fig_cv',
                       # it's important that you set this size
                       size=(400 * 2, 400))]], background_color='#DAE0E6', pad=(0, 0)
    )],[sg.B('Hætta')]]

window = sg.Window('Mæliforrit fyrir sveiflufræði', layout, element_justification='c')

while True:             # Event Loop
    event, values = window.read()
    if event in (None, 'Hætta'):
        break
    if callable(event):
        event()
    #elif event == 'Innlestur':
    #    func('hahahahahah')
    elif event == 'Mæling':
        # ------------------------------- PASTE YOUR MATPLOTLIB CODE HERE
        plt.clf()
        plt.figure(1)
        fig = plt.gcf()
        DPI = fig.get_dpi()
        # ------------------------------- you have to play with this size to reduce the movement error when the mouse hovers over the figure, it's close to canvas size
        fig.set_size_inches(404 * 2 / float(DPI), 404 / float(DPI))
        # -------------------------------
        #x = np.linspace(0, 2 * np.pi)
        #y = np.cos(x)
        #N=fjoldi maeligildia
        N = int(values['fjoldi_maeli'])
        # sample spacing
        T = 1.0 / 800.0
        x = np.linspace(0.0, N*T, N, endpoint=False)
        y = np.sin(50.0 * 2.0*np.pi*x) + 0.5*np.sin(80.0 * 2.0*np.pi*x)
        plt.plot(x, y)
        plt.title('Mæling')
        plt.xlabel('Tími $[s]$')
        plt.ylabel('Hröðun $[m/s^2]$')
        plt.grid()
        #print(values)

        # ------------------------------- Instead of plt.show()
        draw_figure_w_toolbar(window['fig_cv'].TKCanvas, fig, window['controls_cv'].TKCanvas)
    elif event == 'FFT greining':
        # ------------------------------- PASTE YOUR MATPLOTLIB CODE HERE
        plt.clf()
        plt.figure(1)
        fig = plt.gcf()
        DPI = fig.get_dpi()
        # ------------------------------- you have to play with this size to reduce the movement error when the mouse hovers over the figure, it's close to canvas size
        fig.set_size_inches(404 * 2 / float(DPI), 404 / float(DPI))
        # -------------------------------
        #N=fjoldi maeligildia
        N = int(values['fjoldi_maeli'])
        T = 1.0 / 800.0
        x = np.linspace(0.0, N*T, N, endpoint=False)
        y = np.sin(50.0 * 2.0*np.pi*x) + 0.5*np.sin(80.0 * 2.0*np.pi*x)
        yf = fft(y)
        xf = fftfreq(N, T)[:N//2]
        plt.plot(xf,2.0/N * np.abs(yf[0:N//2]))
        plt.title('FFT-greining')
        plt.xlabel('Tíðni [Hz]')
        plt.ylabel('Hröðun $[m/s^2]$')
        plt.grid()
    
        # ------------------------------- Instead of plt.show()
        draw_figure_w_toolbar(window['fig_cv'].TKCanvas, fig, window['controls_cv'].TKCanvas)

window.close()

sg.Text('(Almost) All widgets in one Window!', size=(30, 1), justification='center', font=("Helvetica", 25), relief=sg.RELIEF_RIDGE)
