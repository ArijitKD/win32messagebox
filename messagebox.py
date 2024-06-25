# Icon images from Freeimages.com

# Sound-effects by UNIVERSFIELD <https://pixabay.com/users/universfield-28281460/> (License: <https://pixabay.com/service/terms/>)

# Font used: Selawik
# Copyright 2015, Microsoft Corporation (License: SIL OPEN FONT LICENSE Version 1.1; License file: assets/fonts/LICENSE.txt)
# Selawik is a trademark of Microsoft Corporation in the United States and/or other countries.


import tkinter as tk
import tkinter.ttk as ttk
from platform import system
from os import path, remove
from shutil import copy
from subprocess import Popen, PIPE
from time import sleep



# Not for Windows! Use tkinter's messagebox, it's a lot better, atleast for Windows
if (system() == 'Windows'):
    raise ImportError("This module is not for Windows. Please use tkinter\'s messagebox module.")



class Messagebox(tk.Toplevel):
    def __init__(self, master=None, title="messagebox", message="Message", **options):

        # Initailize the super class 
        super().__init__(master)

        # Initialization based on options, load the default options if not specified
        buttons = options.get('buttons', ['ok', ])
        self.default = options.get('default', buttons[0])
        self.color_attr = options.get('color_attr',
                     {
                        'border':               'black',
                        'titlebar':             '#fefffc',
                        'body':                 '#fefffc',
                        'button_onhover':       '#e5f1fb',
                        'button_offhover':      '#dfe1de',
                        'button_onclick':       '#cce4f7',

                        'titletext':            'black',
                        'bodytext':             'black',
                        'buttontext_onhover':   'black',
                        'buttontext_offhover':  'black'
                     })
        self.icon = options.get('icon', None)
        
        # On some non-standard Linux systems, font scaling is not proper due to tkinter's limitations
        # In that case, specify the proper font size, default is 9
        fontsize = options.get('fontsize', 9)
        
        # Initialize a dictionary to store the button names as keys and buttons as ttk.Button objects in reverse order
        self.button_widgets = {}
        for button in buttons[::-1]:
            self.button_widgets[button] = None
        
        # Initialize the title and the message
        self.title = title
        self.message = message

        # Determine the appropriate dimensions based on the message length, title length and number of buttons
        self.dimensions = self.get_appropriate_dimensions()

        # Get the height and width from the dimensions and center the messagebox window on the master window
        self.height = int(self.dimensions[self.dimensions.index('x')+1::])
        self.width = int(self.dimensions[0:self.dimensions.index('x')])
        center_x = int(self.master.winfo_rootx()+self.master.winfo_width()-self.width-self.master.winfo_width()/2+self.width/2)
        center_y = int(self.master.winfo_rooty()+self.master.winfo_height()-self.height-self.master.winfo_height()/2+self.height/2)

        if (center_x+self.width > self.winfo_screenwidth()):
            center_x = self.winfo_screenwidth() - self.width - 20
        if (center_y+self.height > self.winfo_screenheight()):
            center_y = self.winfo_screenheight() - self.height - 20
        if (center_x+self.width < self.master.winfo_width()//2):
            center_x = 20
        if (center_y+self.height < self.master.winfo_height()//2):
            center_y = 20   
        if (center_x < 0):
            center_x = int(self.master.winfo_screenwidth()/2 - self.width/2)
        if (center_y < 0):
            center_y = int(self.master.winfo_screenheight()/2 - self.height/2)

        self.geometry(self.dimensions+"+%d+%d"%(center_x, center_y))

        # Initialize a variable that will store the name of the button that was clicked by the user
        self.button_clicked = None

        # Set the titlebar height, border width
        self.titlebar_height = 32
        self.border_width = 1.5

        # Set window attributes
        self.resizable(0,0)
        self.attributes('-topmost', True)
        self.overrideredirect(True)
        self.protocol("WM_DELETE_WINDOW", self.exit)

        # Remove master's close callback to avoid multiple toplevel windows from appearing on clicking the 'x' button
        self.master_close_function = self.master.protocol("WM_DELETE_WINDOW")
        self.master.protocol("WM_DELETE_WINDOW", self._dummy)

        # Keep track of whether the Selawik font is being installed
        self.installed_font = False

        # Font files
        self.font_file = path.join(path.dirname(__file__), "assets/fonts/selawk.ttf")
        self.font_file_linux = path.expanduser("~/.local/share/fonts/selawk.ttf")
        self.font_file_macos = path.expanduser("~/Library/Fonts/selawk.ttf")
        
        # Default font, will be used in case system is a non-standard Linux
        self.font = ('Helvetica', fontsize)

        # Load the Selawik font
        self._load_font()

        # Draw the window (Load all widgets)
        self.draw_window()


    def get_appropriate_dimensions(self):
        return "320x160"


    def _load_font(self):
        try:
            if (system() == 'Darwin'):
                if (not path.isfile(self.font_file_macos)):
                    copy(self.font_file, self.font_file_macos)
                    self.installed_font = True
                self.font = ("Selawik", 9)
            elif (system() == "Linux"):
                if (not path.isfile(self.font_file_linux)):
                    copy(self.font_file, self.font_file_linux)
                    Popen(["fc-cache", "-f", "-v"], stdout=PIPE, stderr=PIPE, shell=False)
                    self.installed_font = True
                self.font = ("Selawik", 9)
        except FileNotFoundError:
            return 1
            
    
    def _unload_font(self):
        if (self.installed_font):
            try:
                if (system() == 'Darwin'):
                    remove(self.font_file_macos)
                else:
                    remove(self.font_file_linux)
                    Popen(["fc-cache", "-f", "-v"], stdout=PIPE, stderr=PIPE, shell=False)
            except FileNotFoundError:
                return 1
        return 0


    def _fade_in(self):
        self.withdraw()
        self.update_idletasks()
        self.deiconify()
        alpha = 0
        while (alpha < 1.25):
            self.attributes('-alpha', alpha)
            self.update_idletasks()
            sleep(0.03)
            alpha += 0.25
        self.focus_set()
        self.grab_set()


    def _fade_out(self):
        self.withdraw()
        self.update_idletasks()
        self.deiconify()
        self.config(bg=self.color_attr['body'])
        alpha = 1
        while (alpha > -0.25):
            self.attributes('-alpha', alpha)
            self.update_idletasks()
            sleep(0.04)
            alpha -= 0.25
        self.master.focus_set()


    def draw_window(self):

        # Make the toplevel window the color of the border to add a bordering effect
        self.config(bg=self.color_attr['border'])

        # Titlebar
        self.titlebar = tk.Frame(self, height=self.titlebar_height, background=self.color_attr['titlebar'])
        self.titlebar.pack_propagate(0)
        self.titlebar.pack(fill='x', padx=self.border_width-1, pady=(self.border_width-1, 0), side='top')
        

        # Close button
        self.close_btn = tk.Label(self.titlebar, text='×', foreground=self.color_attr['titletext'], background=self.color_attr['titlebar'], font=('Helvetica', self.font[1]*2+2))
        self.close_btn.pack(side='right', ipadx=10, fill='y')
        self.close_btn.bind('<Enter>', lambda event: event.widget.configure(background='#e81123', foreground="white"))
        self.close_btn.bind('<Leave>', lambda event: event.widget.configure(background=self.color_attr['titlebar'], foreground=self.color_attr['titletext']))
        self.close_btn.bind('<Button-1>', lambda event: event.widget.configure(background='#d43341', foreground="white"))
        self.close_btn.bind('<ButtonRelease-1>', lambda event, button='titlebar_cross': self._button_release_callback(event, button))


        # Titlebar text
        self.title_label = tk.Label(self.titlebar, text=self.title, background=self.color_attr['titlebar'], foreground=self.color_attr['titletext'], font=self.font)
        self.title_label.pack(side='left', padx=8, pady=5)


        # Body
        self.body = tk.Canvas(self, height=self.height-20, width=self.width-10, background=self.color_attr['body'], highlightthickness=0)
        self.body.create_rectangle(
                                    self.border_width//2, -5,
                                    self.width-self.border_width+1, self.height-self.titlebar_height-self.border_width,
                                    outline = self.color_attr['border'],
                                    width = self.border_width
                                    )
        self.body.pack(anchor='center', fill='both', expand=True)


        # Body frame for the message and icon
        self.body_frame = tk.Frame(self.body, background=self.color_attr['body'])
        self.body_frame.pack(side='top', fill='x', padx=self.border_width, pady=self.border_width)


        # Icon
        try:
            self.iconfile = path.join(path.dirname(__file__), "assets/icons/messagebox-%s.png"%(self.icon,))
            self.iconimage = tk.PhotoImage(file=self.iconfile)
            tk.Label(self.body_frame, image=self.iconimage, background=self.color_attr['body']).pack(side='left', padx=(20, 0), pady=(20,0))
        except:
            self.iconfile = None
            self.iconimage = None


        # Message text
        self.message_label = tk.Label(self.body_frame, text=self.message, font=self.font, background=self.color_attr['body'], foreground=self.color_attr['bodytext'], justify='left')
        if (self.iconfile == None):
            self.message_label.pack(pady=(20, 0))
        else:
            self.message_label.pack(side='left', padx=10, pady=(20, 0))


        # Buttons frame for holding the buttons
        self.btn_frame = tk.Frame(self.body, background=self.color_attr['body'])
        self.btn_frame.pack(side='bottom', fill='x', padx=self.border_width, pady=self.border_width)


        # Button styles for on-hover and off-hover
        self.button_style = ttk.Style()
        self.button_style.configure("onhover.TButton", background=self.color_attr['button_onhover'], relief='solid', font=self.font)
        self.button_style.configure("offhover.TButton", background=self.color_attr['button_offhover'], relief='solid', font=self.font)
        self.button_style.configure("press.TButton", background=self.color_attr['button_onclick'], relief='solid', font=self.font)
        self.button_style.configure("release.TButton", background=self.color_attr['button_onhover'], relief='solid', font=self.font)        


        # Buttons
        for button in self.button_widgets:
            self.button_widgets[button] = ttk.Label(self.btn_frame, text=button.capitalize(), width=8, style="offhover.TButton")
            if (list(self.button_widgets.keys()).index(button) == 0):
                self.button_widgets[button].pack(side='right', padx=(5,15), pady=15, ipadx=8)
            else:
                self.button_widgets[button].pack(side='right', padx=(5,5), pady=15, ipadx=8)
            if (button == 'ok'):
                self.button_widgets[button].configure(text='OK')
            self.button_widgets[button].bind('<Enter>', lambda event: event.widget.configure(style="onhover.TButton"))
            self.button_widgets[button].bind('<Leave>', lambda event: event.widget.configure(style="offhover.TButton"))
            self.button_widgets[button].bind('<Button-1>', lambda event: event.widget.configure(style="press.TButton"))
            self.button_widgets[button].bind('<ButtonRelease-1>', lambda event, button='general': self._button_release_callback(event, button))
            self.button_widgets[button].bind('<B1-Motion><Enter>', lambda event: event.widget.configure(style="press.TButton"))
            self.button_widgets[button].bind("<Tab>", self._tab_handler)


        # Bind events to messagebox
        self.bind("<Tab>", self._tab_handler)
        # Add a fade-in effect on window open
        self._fade_in()
        self.button_widgets[self.default].focus_force()
        #self.focus_lastfor(self.button_widgets[self.default])
        

    def _tab_handler(self, event):
        self.button_widgets[self.default].focus_force()


    def _button_release_callback(self, event, button='general'):
        if (button == 'titlebar_cross'):
            event.widget.configure(background='#e81123')
        else:
            event.widget.configure(style="release.TButton")
        event_xy = (event.x_root, event.y_root)
        widget_bounds = {
                        'upper-left': (event.widget.winfo_rootx(), event.widget.winfo_rooty()),
                        'lower-bottom': (event.widget.winfo_rootx()+event.widget.winfo_width(), event.widget.winfo_rooty()+event.widget.winfo_height())
                        }
        if ((widget_bounds['upper-left'][0] <= self.winfo_pointerx() <= widget_bounds['lower-bottom'][0]) and (widget_bounds['upper-left'][1] <= self.winfo_pointery() <= widget_bounds['lower-bottom'][1])):
            if (button == 'general'):
                self.button_clicked = event.widget.cget('text').lower()
            self.exit()


    def _update_btn_color(self, event, event_type):
        if (event_type == 'enter'):
            print (event_type)
            event.widget.configure(style="onhover.TButton")
        else:
            event.widget.configure(style="offhover.TButton")
        

    def settitle(self, title):
        self.title_label.configure(text=title)


    def setmessage(self, message):
        self.message_label.configure(text=message)


    def _dummy(self):
        pass

    def exit(self):
        # Add a fade-out effect on window close
        self._fade_out()
        
        # Restore master's close callback
        self.master.protocol("WM_DELETE_WINDOW", self.master_close_function)

        # Destroy the toplevel window
        self.destroy()

        # Unload the Selawik font
        self._unload_font()



def askokcancel(title="", message="", **options):
    detail = options.get('detail', "")
    if (detail != ""):
        message = message + "\n\n" + detail
    master = options.get('master', None)
    icon = options.get('icon', 'help')
    default = options.get('default', 'ok')
    fontsize = options.get('fontsize', 9)

    mbox = Messagebox(master, title, message, icon=icon, buttons=['ok', 'cancel'], default=default, fontsize=fontsize)
    mbox.master.wait_window(mbox)

    return (mbox.button_clicked == 'ok')


def askquestion(title="", message="", **options):
    detail = options.get('detail', "")
    if (detail != ""):
        message = message + "\n\n" + detail
    master = options.get('master', None)
    icon = options.get('icon', 'help')
    default = options.get('default', 'yes')
    fontsize = options.get('fontsize', 9)

    mbox = Messagebox(master, title, message, icon=icon, buttons=['yes', 'no'], default=default, fontsize=fontsize)
    mbox.master.wait_window(mbox)

    if (mbox.button_clicked == 'yes'):
        return 'yes'
    return 'no'


def askretrycancel(title="", message="", **options):
    detail = options.get('detail', "")
    if (detail != ""):
        message = message + "\n\n" + detail
    master = options.get('master', None)
    icon = options.get('icon', 'warning')
    default = options.get('default', 'retry')
    fontsize = options.get('fontsize', 9)

    mbox = Messagebox(master, title, message, icon=icon, buttons=['retry', 'cancel'], default=default, fontsize=fontsize)
    mbox.master.wait_window(mbox)

    return (mbox.button_clicked == 'retry')


def askyesno(title="", message="", **options):
    detail = options.get('detail', "")
    if (detail != ""):
        message = message + "\n\n" + detail
    master = options.get('master', None)
    icon = options.get('icon', 'help')
    default = options.get('default', 'yes')
    fontsize = options.get('fontsize', 9)

    button = askquestion(title, message, master=master, icon=icon, buttons=['yes', 'no'], default=default, fontsize=fontsize)

    return (button == 'yes')


def askyesnocancel(title="", message="", **options):
    detail = options.get('detail', "")
    if (detail != ""):
        message = message + "\n\n" + detail
    master = options.get('master', None)
    icon = options.get('icon', 'help')
    default = options.get('default', 'yes')
    fontsize = options.get('fontsize', 9)

    mbox = Messagebox(master, title, message, icon=icon, buttons=['yes', 'no', 'cancel'], default=default, fontsize=fontsize)
    mbox.master.wait_window(mbox)

    if (mbox.button_clicked == 'yes'):
        return True
    elif (mbox.button_clicked == 'no'):
        return False
    else:
        return None


def showerror(title="", message="", **options):
    detail = options.get('detail', "")
    if (detail != ""):
        message = message + "\n\n" + detail
    master = options.get('master', None)
    icon = options.get('icon', 'error')
    fontsize = options.get('fontsize', 9)

    mbox = Messagebox(master, title, message, icon=icon, buttons=['ok',], fontsize=fontsize)
    mbox.master.wait_window(mbox)

    return 'ok'


def showinfo(title="", message="", **options):
    detail = options.get('detail', "")
    if (detail != ""):
        message = message + "\n\n" + detail
    master = options.get('master', None)
    icon = options.get('icon', 'info')
    fontsize = options.get('fontsize', 9)

    mbox = Messagebox(master, title, message, icon=icon, buttons=['ok',], fontsize=fontsize)
    mbox.master.wait_window(mbox)

    return 'ok'


def showwarning(title="", message="", **options):
    detail = options.get('detail', "")
    if (detail != ""):
        message = message + "\n\n" + detail
    master = options.get('master', None)
    icon = options.get('icon', 'warning')
    fontsize = options.get('fontsize', 9)

    mbox = Messagebox(master, title, message, icon=icon, buttons=['ok',], fontsize=fontsize)
    mbox.master.wait_window(mbox)

    return 'ok'


if __name__ == "__main__":
    root = tk.Tk()
    ret = askyesno(master=root, title="Message", message="This is an askyesno() messagebox.")
    print (ret)
    root.bind("<Button-1>", lambda event: root.destroy())
    root.mainloop()
