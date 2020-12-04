import cv2
from PIL import Image, ImageTk, ImageDraw, ImageFilter
from tkinter import Tk, Pack, Label, BOTH, Scale, Frame, HORIZONTAL, LEFT, RIGHT


class Application():
    def __init__(self, master=None):
        self.master = master

        self.content = Frame(self.master, bg="red")
        self.content.pack(side=LEFT, fill=BOTH, expand=True)

        self.canvas = Label(self.content)
        self.canvas.pack(fill=BOTH, expand=True)

        self.webcam = cv2.VideoCapture(1 + cv2.CAP_DSHOW)

        self.webcam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.webcam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        self.loopVideo()

    def loopVideo(self):

        self.startStrem(self.webcam, self.canvas)

        self.master.after(30, self.loopVideo)

    def startStrem(self, video, widget):

        resp, videoContent = self.readStreamWebcam(video)

        if resp == True:

            resizedVideo = self.resizeVideo(videoContent, 30)
            coloredVideo = self.convertToColor(resizedVideo)
            imagedOfVideo = self.convertToImage(coloredVideo)
            transformImage = self.transformImage(imagedOfVideo)
            tkImage = self.convertToTkImage(transformImage)
            
            self.renderVideoInWidget(tkImage, widget)
        

        else:
            video.release()
            print("Errou!!")

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
        
        x,y = imageTransparent.size #640x360

        cord_x1 = x / 4
        cord_x2 = 0

        cord_y1 = y + cord_x1
        cord_y2 = y 

        draw = ImageDraw.Draw(mask)
        draw.ellipse((cord_x1,cord_x2,cord_y1,cord_y2), fill=255)  # 144

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


if __name__ == "__main__":
    root = Tk()
    app = Application(root)
    root.mainloop()
