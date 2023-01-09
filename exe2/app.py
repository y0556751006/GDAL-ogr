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

def convertToJpg(raster1,raster2):
    options_list = [
    '-ot Byte',
    '-of JPEG',
    '-b 1',
    '-scale'
    ]           
    options_string = " ".join(options_list)
    gdal.Translate(
        raster1,
        raster1.split(".")[0] + ".tif",
        options = options_string
    )
    gdal.Translate(
        raster2,
        raster2.split(".")[0] + ".tif",
        options = options_string
    )


def mergeRasters(raster1, raster2):
    g = gdal.Warp("exe2/data/output.jpg", [raster1, raster2])
    g = None


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
    newRaster1 = cropAndCreateRaster(raster1,(696278.000, 3668042.000),( 700374.000,3665994.000))
    newRaster2 = cropAndCreateRaster(raster2,(700373.500, 3663946.500),(704469.500,3661898.500))
    mergeRasters(newRaster1, newRaster2)


newRaster("exe2/data/p1.jpg", "exe2/data/p2.jpg")
# convertToJpg("exe2/data/p1.jpg", "exe2/data/p2.jpg")

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
