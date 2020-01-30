from PIL.ExifTags import GPSTAGS
from PIL.ExifTags import TAGS
from PIL import Image
import os

def get_exif(filename):
    image = Image.open(str(filename))
    image.verify()
    return image._getexif()

#exif = get_exif('test.jpg')

def get_labeled_exif(exif):
    labeled = {}
    for (key, val) in exif.items():
        labeled[TAGS.get(key)] = val

    return labeled

#exif = get_exif('test.jpg')
#labeled = get_labeled_exif(exif)


def get_geotagging(exif):
    if not exif:
        raise ValueError("No EXIF metadata found")

    geotagging = {}
    for (idx, tag) in TAGS.items():
        if tag == 'GPSInfo':
            if idx not in exif:
                raise ValueError("No EXIF geotagging found")

            for (key, val) in GPSTAGS.items():
                if key in exif[idx]:
                    geotagging[val] = exif[idx][key]

    return geotagging

def get_decimal_from_dms(dms, ref):

    degrees = dms[0][0] / dms[0][1]
    minutes = dms[1][0] / dms[1][1] / 60.0
    seconds = dms[2][0] / dms[2][1] / 3600.0

    if ref in ['S', 'W']:
        degrees = -degrees
        minutes = -minutes
        seconds = -seconds

    return round(degrees + minutes + seconds, 5)

def get_coordinates(geotags):
    lat = get_decimal_from_dms(geotags['GPSLatitude'], geotags['GPSLatitudeRef'])

    lon = get_decimal_from_dms(geotags['GPSLongitude'], geotags['GPSLongitudeRef'])

    return [lat,lon]

'''path = 'Mt_Fuji'
files = []
# r=root, d=directories, f = files
for r, d, f in os.walk(path):
    for file in f:
        print file
        if '.JPG' in file:
            files.append(os.path.join(r, file))

#files = ['IMG_5689.JPG','IMG_5731.JPG','IMG_5725.JPG']
#files = 
geos = []
for i in files:
    exif = get_exif(i)
    print(exif)
    geotags = get_geotagging(exif)
    #print('--------------------')
    #print(get_coordinates(geotags))
    geos.append(get_coordinates(geotags))
print files
print '--------'
print geos'''

def return_gps(path):
    files = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk('static\\trips\\'+path+'\\images'):
        for file in f:
            print file
            if 1:
                files.append([str('trips\\'+path+'\\images\\'+file)])
    geos = []
    for n in files:
        for i in n:
            exif = get_exif('static\\'+i)
            #print(exif)
            geotags = get_geotagging(exif)
            geos.append(get_coordinates(geotags))
            i=i.replace('\\','/')
    print files,geos
    return files,geos

'''for i in files:
    exif=get_exif(i)
    geotags=get_geotagging(exif)
    j=get_coordinates(geotags)
    print("L.marker(["+str(j[0])+","+str(j[1])+"]).addTo(map).bindPopup('<center><img src=%s height=100px/>');") %(i)'''
