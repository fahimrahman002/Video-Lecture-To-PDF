from skimage.metrics import structural_similarity as compare_ssim
import img2pdf
import cv2
import glob
import os
from pathlib import Path
import shutil

frameRate = 5  # Change frameRate to skip frames
matchScore = 0.97 # [Skip frames if SimilarityScore > 0.97]

def main():
    Path(f"ProcessedVideos").mkdir(parents=True, exist_ok=True)
    Path(f"images").mkdir(parents=True, exist_ok=True)
    Path(f"pdf").mkdir(parents=True, exist_ok=True)
    for videoFile in glob.glob("Videos/*.mp4"):
        videoName = Path(videoFile).stem
        print(f"Processing {videoName}.mp4")
        videoNameModified = videoName.replace("[", "")
        videoNameModified = videoNameModified.replace("]", "")
        generateImages(videoFile, videoNameModified)
        imagesToPdf(videoNameModified)
        shutil.move(videoFile, f"ProcessedVideos/{videoName}.mp4")
        print(f"Processing done")

count = 1
def generateImages(videoFilePath, videoName):
    global count,frameRate
    frameSec = 0.5  # Start from 0.5 sec
    videoCapture = cv2.VideoCapture(videoFilePath)
    # fps = videoCapture.get(cv2.CAP_PROP_FPS)
    success = True
    Path(f"images/{videoName}").mkdir(parents=True, exist_ok=True)
    while success:
        videoCapture.set(
            cv2.CAP_PROP_POS_MSEC, frameSec*1000)
        hasFrames1, image1 = videoCapture.read()
        videoCapture.set(
            cv2.CAP_PROP_POS_MSEC, (frameSec+frameRate)*1000)
        hasFrames2, image2 = videoCapture.read()
        if hasFrames1 and hasFrames2:
            matchImages(image1, image2, videoName)
        if hasFrames1 and not hasFrames2:
            videoCapture.set(
                cv2.CAP_PROP_POS_MSEC, (frameSec-frameRate)*1000)
            hasFramesPrev, imagePrev = videoCapture.read()
            if hasFramesPrev:
                matchImages(image1, imagePrev, videoName)
        success = hasFrames1 and hasFrames2
        frameSec = frameSec+frameRate
    count = 1


def matchImages(image1, image2, videoName):
    global count, matchScore
    # convert the images to grayscale
    grayA = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
    # compute the Structural Similarity Index (SSIM) between the two
    # images, ensuring that the difference image is returned
    (score, diff) = compare_ssim(grayA, grayB, full=True)
    if(round(score, 2) <= matchScore):
        print(f"SSIM of image{count} and image{count+1}: {round(score, 2)}")
        cv2.imwrite(f"images/{videoName}/image{str(count)}.jpg", image1)
        count = count+1


def imagesToPdf(videoName):
    pdfFilePath = f'pdf/{videoName}.pdf'
    img_list = []
    images = sorted(
        glob.glob(f"images/{videoName}/*.jpg"), key=os.path.getmtime)
    for img in images:
        img_list.append(img)

    if(len(images) > 0):
        with open(pdfFilePath, "wb") as f:
            f.write(img2pdf.convert(img_list))

    try:
        shutil.rmtree(f"images/{videoName}")
    except:
        print(f"images/{videoName} do not exist.")


main()
