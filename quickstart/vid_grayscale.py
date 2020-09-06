import cv2
import os
import sys


def convert(videoName):
    vid = cv2.VideoCapture("{}".format(videoName[1:]))
    print(videoName[1:])
    width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = round(vid.get(cv2.CAP_PROP_FPS))
    isColor = False
    # name = "test.file.mp4"
    outputName = ".".join(videoName.split(".")[:-1])
    outputFormat = videoName.split(".")[-1]

    # fourccList = {"mp4": "mp4v", "mpg": "MPGI",  "mkv": "XVID",
    #   "webm": "vp80", "wmv": "XVID", "mov": "3IVD", "avi": "XVID"}

    fourcc = cv2.VideoWriter_fourcc(*'divx')
    outputFormat = "mp4"
    # if outputFormat.lower() not in fourccList:
    #     print("in")
    # else:
    #     fourcc = cv2.VideoWriter_fourcc(
    #         *'{}'.format(fourccList[outputFormat.lower()]))

    print(width, height, fps, outputName, outputFormat, fourcc)
    out = cv2.VideoWriter('{}_output.{}'.format(outputName[1:], outputFormat), fourcc,
                          fps, (width, height), isColor)
    while(True):
        ret, img = vid.read()
        if ret == True:
            imgGray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            out.write(imgGray)
            # cv2.imshow('Initial', img)
            # cv2.imshow('Final', imgGray)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break

    vid.release()
    out.release()
    cv2.destroyAllWindows()
    print("Done")

    return('{}_output.{}'.format(outputName[1:], outputFormat))
