from PIL import Image
from osgeo import gdal
import numpy as np

# משימה א

# a

    
def getSizeOfRaster(fileUrl):
    raster = gdal.Open(fileUrl)
    if raster is None:
        return "No such file or directory"
    xres, yres = raster.GetGeoTransform()[1:6:4]
    width = raster.RasterXSize * xres
    height = raster.RasterYSize * yres
    return width * height


def getTheBiggestRaster(raster1, raster2):
    raster1Size = getSizeOfRaster(raster1)
    raster2Size = getSizeOfRaster(raster2)
    if (raster1Size > raster2Size):
        return 1
    else:
        return 2


print(getTheBiggestRaster("exe2/data/pic1.jpg", "exe2/data/pic2.jpg"))

# b


def mergeRasters(raster1, raster2):
    src=gdal.Open(raster1)
    print(src.GetMetadata().values)
    files_to_mosaic = [raster1, raster2]
    g = gdal.Warp("output.jpg", files_to_mosaic, format="TIFF") 
    # image1 = Image.open(raster1)
    # # image1.show()
    # image2 = Image.open(raster2)
    # # image2.show()
    # # image1 = image1.resize((426, 240))
    # image1_size = image1.size
    # image2_size = image2.size
    # print('image1_size', image1_size)
    # new_image = Image.new(
    #     'RGB', (image1_size[0], 2*image1_size[1]), (250, 250, 250))
    # new_image.paste(image1, (0, 0))
    # new_image.paste(image2, (0, image1_size[1]))
    # new_image.save("merged_image.jpg", "JPEG")


def cropAndCreateRaster(raster, point1, point2):
    upper_left_x, upper_left_y = point1
    lower_right_x, lower_right_y = point2
    window = (upper_left_x, upper_left_y, lower_right_x, lower_right_y)
    cropRaster=raster.split(".")[0]+"crop.jpg"
    gdal.Translate(cropRaster, raster, projWin=window)
    if gdal.Open(cropRaster) != None:
        return cropRaster
    return "Failed"


def newRaster(raster1, raster2):
    newRaster1 = cropAndCreateRaster(raster1, (0, 0), (2560, 720))
    newRaster2 = cropAndCreateRaster(raster2, (0, 0), (2560, 720))
    # newRaster2=cropAndCreateRaster(raster2, (0, 0), (3968, 1488))
    mergeRasters(newRaster1, newRaster2)


# newRaster("exe2/data/pic2.jpg", "exe2/data/pic3.jpg")
newRaster("exe2/data/data1.jpg", "exe2/data/data2.jpg")

# משימה ב


def convertToTiff(raster):
    src = gdal.Open(raster)
    if src is None:
        return "No such file or directory"
    newRaster = raster.split(".")[0]+".tif"
    gdal.Translate(newRaster, src)
    if gdal.Open(newRaster) != None:
        return newRaster
    return "Failed"

def getColor(j):
    if all(element == j[0] for element in j):
        return 1
    else:
        return 0


def findTheWay(arrayMask):
    maxArr = []
    arr = []
    tempArr = []
    for i in range(len(arrayMask)):
        for j in range(len(arrayMask[i])):
            if (arrayMask[i][j] == 1):
                arr.append([i, j])
            else:
                if (arr != []):
                    if (len(arr) > len(tempArr)):
                        tempArr = arr
                    arr = []
        if (len(arr) < len(tempArr)):
            arr = tempArr
        if (len(arr) > len(maxArr)):
            maxArr = arr
        arr = []
    return maxArr


def SetDataToMask(raster, mask):
    ds = gdal.Open(mask)
    if ds is None:
        return "No such file or directory"
    arrayMask = ds.ReadAsArray()
    src = gdal.Open(raster)
    band1 = src.GetRasterBand(1).ReadAsArray()
    band2 = src.GetRasterBand(2).ReadAsArray()
    band3 = src.GetRasterBand(3).ReadAsArray()
    rgb_array = np.dstack([band1, band2, band3])
    for i in range(len(rgb_array)):
        for j in range(len(rgb_array[i])):
            color = getColor(rgb_array[i][j])
            if (color == 1):
                arrayMask[i][j] = 1
    return arrayMask


def markTheWay(arrayMask):
    way = findTheWay(arrayMask)
    for i in range(len(way)):
        arrayMask[way[0][0]][way[0][1]+i] = 2
    for i in range(len(arrayMask)):
        for j in range(len(arrayMask[i])):
            if (arrayMask[i][j] == 2):
                print(i, j)
    return arrayMask


def getWay(raster):
    # raster = convertToTiff(raster)
    src = gdal.Open(raster)
    src.CreateMaskBand(gdal.GMF_NODATA)
    maskRaster = gdal.Open(raster+".msk", 1)
    arrayMask = SetDataToMask(raster, raster+".msk")
    arrMask = markTheWay(arrayMask)
    maskRaster.GetRasterBand(1).WriteArray(arrMask)


getWay("exe2/data/pic4.tif")
