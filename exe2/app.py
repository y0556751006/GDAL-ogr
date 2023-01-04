from osgeo import gdal
import numpy as np

# משימה א

# a


def getSizeOfRaster(fileUrl):
    raster = gdal.Open(fileUrl)
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
    newRaster1 = cropAndCreateRaster(raster1, (0, 0), (2560, 720))
    newRaster2 = cropAndCreateRaster(raster2, (0, 0), (2560, 720))
    # newRaster2=cropAndCreateRaster(raster2, (0, 0), (3968, 1488))
    filesToMerge = [newRaster1, newRaster2]
    gdal.Warp("output.jpg", filesToMerge, format="JPEG",
              options=["COMPRESS=LZW", "TILED=YES"])


def cropAndCreateRaster(raster, point1, point2):
    upper_left_x, upper_left_y = point1
    lower_right_x, lower_right_y = point2
    window = (upper_left_x, upper_left_y, lower_right_x, lower_right_y)
    gdal.Translate(raster.split(".")[0]+"crop.jpg", raster, projWin=window)
    return raster.split(".")[0]+"crop.jpg"

# mergeRasters("exe2/data/pic2.jpg", "exe2/data/pic3.jpg")

# משימה ב


def convertToTiff(raster):
    src = gdal.Open(raster)
    newRaster = raster.split(".")[0]+".tif"
    gdal.Translate(newRaster, src)
    return newRaster


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
    raw = way[0][0]
    for i in range(len(way)):
        arrayMask[raw][i] = 2
    for i in range(len(arrayMask)):
        for j in range(len(arrayMask[i])):
            if (arrayMask[i][j] == 2):
                print(i, j)
    return arrayMask


def getWay(raster):
    # raster = convertToTiff(raster)
    src = gdal.Open(raster, 1)
    src.CreateMaskBand(gdal.GMF_NODATA)
    maskRaster = gdal.Open("exe2/data/pic4.tif.msk", 1)
    arrayMask = SetDataToMask(raster, raster+".msk")
    arrMask = markTheWay(arrayMask)
    maskRaster.GetRasterBand(1).WriteArray(arrMask)


getWay("exe2/data/pic4.tif")
