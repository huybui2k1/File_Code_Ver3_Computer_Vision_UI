import cv2

def resize(imgPath,pathSaveOutputImg):
    image = cv2.imread(imgPath)
    if image is None:
        print("Isn't have picture!!")
        return
    img_width, img_height = image.shape[1] // 4, image.shape[0] // 4
    outputImageSize = cv2.resize(image,(img_width, img_height))
    cv2.imwrite(pathSaveOutputImg, outputImageSize)
    

