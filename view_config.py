from tkinter import *
from tkinter import ttk
from style import *
from view_webcam import *


class View_Config():
    def __init__(self, master=None, device_list=None):

        self.master = master
        self.master.geometry("400x220")
        self.master.title('')
        self.master.resizable(False, False)

        self.style = Style()

        self.master.configure(bg=self.style.color_background)

        self.title_bar_frame = Frame(
            self.master, bg=self.style.color_detail, width=400, height=30)
        self.title_bar_frame.pack(fill=X)

        self.text_title = Label(self.title_bar_frame, text='WebCam View',
                                font=self.style.font_title, bg=self.style.color_detail, fg=self.style.color_text)
        self.text_title.pack()

        self.webcam_section_frame = Frame(
            self.master, bg=self.style.color_background, width=400, height=100)
        self.webcam_section_frame.pack(pady=10)

        self.text_webcam = Label(
            self.webcam_section_frame, text='Webcam Devices:', font=self.style.font_menus, fg=self.style.color_text, bg=self.style.color_background)
        self.text_webcam.pack(side=LEFT)

        self.combobox_webcam = ttk.Combobox(
            self.webcam_section_frame, values=device_list)
        self.combobox_webcam.set(device_list[0])
        self.combobox_webcam.pack(side=LEFT)

        self.scale_section_frame = Frame(
            self.master, width=400, height=100, bg=self.style.color_background)
        self.scale_section_frame.pack()

        self.text_scale = Label(self.scale_section_frame, text='Video Scale:',
                                bg=self.style.color_background, fg=self.style.color_text, font=self.style.font_menus, anchor=S)
        self.text_scale.pack(side=LEFT, anchor=S)

        self.scale_var = IntVar(value=40)
        self.scale_scale_video = Scale(self.scale_section_frame, orient=HORIZONTAL, relief=FLAT, variable=self.scale_var, resolution=5,
                                       font=self.style.font_menus, fg=self.style.color_text, bg=self.style.color_background, width=10,
                                       sliderlength=20, length=150, bd=0, troughcolor=self.style.color_detail, highlightthickness=0)
        self.scale_scale_video.pack(side=LEFT)

        self.round_section_frame = Frame(
            self.master, width=400, height=100, bg=self.style.color_background)
        self.round_section_frame.pack(pady=10)

        self.var_check_round = BooleanVar(value=True)
        self.check_round_video = Checkbutton(
            self.round_section_frame, text='Round Video', variable=self.var_check_round, bg=self.style.color_background, fg=self.style.color_text,
            selectcolor=self.style.color_background)
        self.check_round_video.pack()

        self.bt_start = Button(self.master, text='Start',
                               font=self.style.font_menus)
        self.bt_start.bind("<Button-1>", self.start_webcam)
        self.bt_start.pack()

    def start_webcam(self, event):
        device_selected = self.combobox_webcam.get()
        video_scale = self.scale_var.get()
        round_option = self.var_check_round.get()

        self.master.destroy()
        app = View_Webcam(device_selected, video_scale, round_option)


if __name__ == "__main__":
    root = Tk()
    device_list = ['Device 0', 'Device 1']
    app = View_Config(root, device_list)
    root.mainloop()
