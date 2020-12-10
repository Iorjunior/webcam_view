from tkinter import *
import cv2
from PIL import Image, ImageTk, ImageDraw, ImageFilter
from style import *


class View_Webcam():
    def __init__(self, device_selected, video_scale, round_option):
        self.master = Tk()
        self.master.title(f'{device_selected}')
        self.master.overrideredirect(1)
        self.master.wm_attributes('-transparentcolor', 'red')
        self.master.attributes("-topmost", True)

        self.device_selected = int(device_selected[7])
        print(self.device_selected)
        self.video_scale = video_scale
        self.round_option = round_option

        self.style = Style()

        self.navbar_frame = Frame(
            self.master, bg=self.style.color_detail, width=50, height=30)
        self.navbar_frame.pack(fill=X)

        self.content = Frame(self.master, bg=self.style.color_background)
        self.content.pack(side=LEFT, fill=BOTH, expand=True)

        self.canvas = Label(self.content, bg=self.style.color_background)

        self.canvas.bind("<ButtonPress-1>", self.start_move)
        self.canvas.bind("<ButtonRelease-1>", self.stop_move)
        self.canvas.bind("<B1-Motion>", self.do_move)

        self.canvas.bind("<Double-Button-1>", self.double_click_check)

        self.canvas.bind("<ButtonPress-3>", self.donw_scale)
        self.canvas.bind("<Double-Button-3>", self.up_scale)

        self.canvas.pack(fill=BOTH, expand=True)

        self.double_clicked = False

        self.webcam = cv2.VideoCapture(self.device_selected + cv2.CAP_DSHOW)

        self.webcam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.webcam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        self.loopVideo()

        self.master.mainloop()

    def loopVideo(self):

        self.startStrem(self.webcam, self.canvas)

        self.master.after(30, self.loopVideo)

    def startStrem(self, video, widget):

        resp, videoContent = self.readStreamWebcam(video)

        if resp == True:

            resizedVideo = self.resizeVideo(
                videoContent, int(self.video_scale))
            coloredVideo = self.convertToColor(resizedVideo)
            imagedOfVideo = self.convertToImage(coloredVideo)

            if self.round_option:
                transformImage = self.transformImage(imagedOfVideo)
                tkImage = self.convertToTkImage(transformImage)
                self.renderVideoInWidget(tkImage, widget)
            else:
                tkImage = self.convertToTkImage(imagedOfVideo)
                self.renderVideoInWidget(tkImage, widget)

        else:
            print("Errou!!")
            video.release()

    def readStreamWebcam(self, video):

        resp, videoContent = self.webcam.read()

        if resp == True:
            return resp, videoContent
        else:
            return False

    def resizeVideo(self, video, scalePercent):

        widthVideo = int(video.shape[1] * scalePercent / 100)
        heightVideo = int(video.shape[0] * scalePercent / 100)

        dsize = (widthVideo, heightVideo)

        videoResized = cv2.resize(video, dsize, interpolation=cv2.INTER_AREA)

        return videoResized

    def convertToColor(self, video):

        videoColored = cv2.cvtColor(video, cv2.COLOR_BGR2RGB)

        return videoColored

    def convertToImage(self, video):

        videoImaged = Image.fromarray(video)
        # print(videoImaged.size) 256x144

        return videoImaged

    def transformImage(self, video):

        imageTransparent = self.transparentImage(video.size)

        mask = Image.new("L", imageTransparent.size, 0)

        x, y = imageTransparent.size  # 640x360

        cord_x1 = x / 4
        cord_x2 = 0

        cord_y1 = y + cord_x1
        cord_y2 = y

        draw = ImageDraw.Draw(mask)
        draw.ellipse((cord_x1, cord_x2, cord_y1, cord_y2), fill=255)  # 144

        videoTranformed = Image.composite(video, imageTransparent, mask)

        return videoTranformed

    def convertToTkImage(self, video):

        videoImagedTk = ImageTk.PhotoImage(video)

        return videoImagedTk

    def renderVideoInWidget(self, video, widget):

        widget.configure(image=video)
        widget.image = video

    def transparentImage(self, size):

        try:
            imageTransparent = Image.open("transparent.png").resize(size)

            return imageTransparent

        except FileNotFoundError:

            imageTransparent = Image.new("RGBA", (1, 1))
            imageTransparent.save("transparent.png")

            imageTransparent = Image.open("transparent.png").resize(size)

            return imageTransparent

    def double_click_check(self, event=None):

        if not self.double_clicked:
            self.double_clicked = True

        elif self.double_clicked:
            self.double_clicked = False

        self.background_transparent()

    def background_transparent(self, event=None):
        if self.double_clicked:

            self.navbar_frame.configure(bg='red')
            self.canvas.configure(bg='red')
            self.round_option = True

        elif self.double_clicked == False:
            self.navbar_frame.configure(bg=self.style.color_detail)
            self.canvas.configure(bg=self.style.color_background)
            self.round_option = False

    def up_scale(self, event):
        self.video_scale = 50

    def donw_scale(self, event):
        self.video_scale = 25

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def stop_move(self, event):
        self.x = None
        self.y = None

    def do_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.master.winfo_x() + deltax
        y = self.master.winfo_y() + deltay

        self.master.geometry("+{}+{}".format(x, y))
