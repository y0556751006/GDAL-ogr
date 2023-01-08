from app import *

features = [feature for feature in layer if(feature.GetGeometryRef().GetArea()>1)]
f = features[0]

def test_get_area():
    assert GetAreaByFeature(f) == 1.118915072336633

def test_get_fid():
    assert getFid(f) == 11

def test_get_NAME_2():
    assert getName_2.__eq__('Wakhan')

def test_by_name():
    assert returnFeatureByName("Wakhan").__eq__(f) 

def test_get_points():
    assert getTwoPoints().__eq__("POINT (63.129810333252 30.7998237609864 0), POINT (69.4896545410157 33.5040779113771 0)")

def test_new_line():
    assert createNewLine().__eq__("LINESTRING (63.129810333252 30.7998237609864 0,69.4896545410157 33.5040779113771 0)")