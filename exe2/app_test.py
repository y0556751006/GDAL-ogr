from app import *


def test_get_size():
    assert getSizeOfRaster("exe2/data/pic1.jpg") == 3840000.0
    assert convertToTiff("exe2/data/x.jpg") == "No such file or directory"


def test_convert():
    assert convertToTiff("exe2/data/pic4.jpg") == "exe2/data/pic4.tif"
    assert convertToTiff("exe2/data/x.jpg") == "No such file or directory"


def test_big_raster():
    assert getTheBiggestRaster("exe2/data/pic1.jpg", "exe2/data/pic2.jpg") == 1


def test_crop_raster():
    assert cropAndCreateRaster(
        "exe2/data/data1.jpg", (0, 0), (2560, 720)) == "exe2/data/data1crop.jpg"


def test_color():
    assert getColor([35, 35, 35]) == 1
    assert getColor([34, 350, 35]) == 0


def test_get_way():
    arrayMask = [[0, 1, 1, 1, 1, 1], [1, 0, 0, 0, 1, 1], [1, 1, 1, 0, 0, 0], [1, 1, 0, 0, 0, 0]]
    assert findTheWay(arrayMask) == [[0, 1], [0, 2], [0, 3], [0, 4], [0, 5]]


def test_mark_way():
    arrayMask = [[0, 1, 1, 1, 1, 1], [1, 0, 0, 0, 1, 1], [1, 1, 1, 0, 0, 0], [1, 1, 0, 0, 0, 0]]
    assert markTheWay(arrayMask) == [[0, 2, 2, 2, 2, 2], [1, 0, 0, 0, 1, 1], [1, 1, 1, 0, 0, 0], [1, 1, 0, 0, 0, 0]]
