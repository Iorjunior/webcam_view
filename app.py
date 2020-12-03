import cv2
from PIL import Image, ImageTk, ImageDraw, ImageFilter
from tkinter import Tk, Pack, Label, BOTH

class Application():
    def __init__(self, master = None):
        self.master = master

        self.canvas = Label(self.master)
        self.canvas.pack(fill=BOTH,expand=True)

        self.webcam = cv2.VideoCapture(1 + cv2.CAP_DSHOW)
        
        self.webcam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.webcam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        

        self.loopVideo()


    def loopVideo(self):

        self.startStrem(self.webcam,self.canvas)

        self.master.after(30,self.loopVideo)


    def startStrem(self,video,widget):
        
        resp, videoContent = self.readStreamWebcam(video)

        if resp == True:
            
            resizedVideo = self.resizeVideo(videoContent,20)
            coloredVideo = self.convertToColor(resizedVideo)
            imagedVideo = self.convertToImage(coloredVideo)
            
            self.renderVideoInWidget(imagedVideo,widget)

        else:
            self.video.release()
            print("Errou!!")

    def readStreamWebcam(self,video):
        
        resp, videoContent = self.webcam.read()

        if resp == True:
            return resp, videoContent
        else:
            return False

    def resizeVideo(self,video, scalePercent):

        widthVideo = int(video.shape[1] * scalePercent / 100)
        heightVideo = int(video.shape[0] * scalePercent / 100)
        
        dsize = (widthVideo, heightVideo)
     
        videoResized = cv2.resize(video, dsize, interpolation = cv2.INTER_AREA)

        return videoResized

    def convertToColor(self,video):
        
        videoColored = cv2.cvtColor(video,cv2.COLOR_BGR2RGB) 
        
        return videoColored

    def convertToImage(self,video):

        videoImaged = Image.fromarray(video)
        videoImagedTk = ImageTk.PhotoImage(videoImaged)

        return videoImagedTk

    def renderVideoInWidget(self,video,widget):

        widget.configure(image=video)
        widget.image = video



if __name__ == "__main__":
    root = Tk()
    app = Application(root)
    root.mainloop()