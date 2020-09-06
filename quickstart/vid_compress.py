import cv2
import os
import sys


def compress(videoName, compVal):
    vid = cv2.VideoCapture("{}".format(videoName[1:]))

    width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = round(vid.get(cv2.CAP_PROP_FPS))
    isColor = True

    # name = "test.file.mp4"
    outputName = ".".join(videoName.split(".")[:-1])
    outputFormat = videoName.split(".")[-1]

    # fourccList = {"mp4": "mp4v", "mpg": "MPGI",  "mkv": "XVID",
    #   "webm": "vp80", "wmv": "XVID", "mov": "3IVD", "avi": "XVID"}

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    outputFormat = "mp4"
    # if outputFormat.lower() not in fourccList:
    #     print("in")
    # else:
    #     fourcc = cv2.VideoWriter_fourcc(
    #         *'{}'.format(fourccList[outputFormat.lower()]))

    out = cv2.VideoWriter('{}_compress.{}'.format(outputName[1:], outputFormat), fourcc,
                          fps, (round((width*compVal)/100), round((height*compVal)/100)), isColor)

    while(True):
        ret, img = vid.read()
        if ret == True:
            imgNew = cv2.resize(
                img, (round((width*compVal)/100), round((height*compVal)/100)))
            out.write(imgNew)
            # cv2.imshow('Initial', img)
            # cv2.imshow('Final', imgNew)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break

    vid.release()
    out.release()
    cv2.destroyAllWindows()
    print("Done")
    return('{}_compress.{}'.format(outputName[1:], outputFormat))
