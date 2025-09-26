#===============================================
# NAME: Joshua Preuss
# DATE: 3/21/2024
# CLASS: CSC 340-001
#===============================================
import cv2
import numpy as np

def main():
    imgname = "Camaro3.png"
    # read in an image in opencv
    image = cv2.imread(imgname,0)
    colorim = cv2.imread(imgname)
    print("image loaded")

    # get size of an image
    numRows = image.shape[0] # height of image
    numCols = image.shape[1] # width of image
    print("size:", numRows, numCols)

    # Create empty images
    gradientImY = np.zeros( (numRows,numCols), np.float32)
    gradientImX = np.zeros( (numRows,numCols), np.float32)
    gradientImXX = np.zeros( (numRows,numCols), np.float32)
    gradientImXY = np.zeros( (numRows,numCols), np.float32)
    gradientImYY = np.zeros( (numRows,numCols), np.float32)

    # iterate over every pixel
    # Solve for Iy image
    for i in range(numRows-1): #height of image, y coordinates
        for j in range(numCols): # width of image, x coordinates
            gradientImY[i][j] = abs(int(image[i+1][j]) - int(image[i-1][j]))
    # Solve for Ix image
    for i in range(numRows): 
        for j in range(numCols-1): 
            gradientImX[i][j] = abs(int(image[i][j+1]) - int(image[i][j-1]))
    # Find IxIx, IyIy, and IxIy
    for i in range(numRows):
        for j in range(numCols): 
            gradientImXX[i][j] = int(gradientImX[i][j]) * int(gradientImX[i][j])
            gradientImYY[i][j] = int(gradientImY[i][j]) * int(gradientImY[i][j])
            gradientImXY[i][j] = int(gradientImX[i][j]) * int(gradientImY[i][j])
    # Create Cornerness Image
    cornernessIM = np.zeros( (numRows,numCols), np.float32)
    maxc = 0
    # Loop through all pixels
    for i in range(numRows-1): 
        for j in range(numCols-1):
            IxIx = 0
            IyIy = 0
            IxIy = 0
            # Geting values of pixels in a 3x3 area around current pixel
            # and stbtracting them from current pixel
            for di in range(-1, 2):
                for dj in range(-1,2):
                    IxIx += int(gradientImXX[i + di][j + dj])
                    IyIy += int(gradientImYY[i + di][j + dj])
                    IxIy += int(gradientImXY[i + di][j + dj])
            #Create matrix using IxIx IxIx and IxIy values
            M = [[IxIx,IxIy],[IxIy,IyIy]]

            # Calculate determinate
            DetM = (M[0][0] * M[1][1]) - (M[1][0] * M[0][1])

            #Calculate Trace
            TraceM = M[0][0] + M[1][1]

            k = .05

            #Calculate cornerness
            C = DetM - (k*((TraceM)**2))
            
            if C > maxc:
                maxc = C
            # Save value in cornerness image
            cornernessIM[i][j] = (C)
            
    cornerIM = np.zeros( (numRows,numCols), np.float32)
    
    # Loop through pixels 
    for i in range(numRows):
        for j in range(numCols):
            # If cornerness value of current pixel is within a certain percentage of the max cornerness
            if cornernessIM[i][j] > (.09 * (maxc)):
                # That corner value is identified as a corner
                # and is highlighted
                cornerIM[i][j] = cornernessIM[i][j]
                cv2.circle(colorim,(j,i),2,(0,255,255))
                
                
            
            
    # Displaty images       
    cv2.imshow("This is an image",image)

    cv2.imshow("IY image", gradientImY/255.0)
    cv2.imshow("IX image", gradientImX/255.0)
    cv2.imshow("IXX image", gradientImXX/255.0)
    cv2.imshow("IYY image", gradientImYY/255.0)
    cv2.imshow("IXY image", gradientImXY/255.0)
    cv2.imshow("Cornerness Image", cornernessIM/(255.0**2))
    cv2.imshow("Updated Corner Image", cornerIM/(255.0**2))
    cv2.imshow("Final Corner Image", colorim/(255.0))
    cv2.waitKey(0) #pause program, proceed when you hit "enter"
    cv2.destroyAllWindows() #closes all windows created with imhsow

    # Save images
    cv2.imwrite("GradientY.png", gradientImY)
    cv2.imwrite("GradientX.png", gradientImX)
    cv2.imwrite("GradientXX.png", gradientImXX)
    cv2.imwrite("GradientYY.png", gradientImYY)
    cv2.imwrite("GradientXY.png", gradientImXY)
    cv2.imwrite("savedImage.png", image)
    cv2.imwrite("Cornerness.png", cornernessIM)
    cv2.imwrite("Corner.png", cornerIM)
    cv2.imwrite("ColorCorner.png", colorim)





if __name__ == "__main__":
    main()
