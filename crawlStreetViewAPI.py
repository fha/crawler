import math
import numpy as np
import urllib
import json
from time import sleep
import matplotlib.pylab as plt
import os
import glob
import re
from PIL import Image
import pandas as pd
import ast
import argparse
import time
import ast
from tqdm import tqdm

parser=argparse.ArgumentParser()
parser.add_argument("-i","--inputPath", help="file containing lat,lon,orientation", type=str,default=None)
parser.add_argument("-m","--metaPath", help="path to place metadata", type=str,default=None)
parser.add_argument("-d","--imagesPath", help="path to where to download the images", type=str,default=None)
parser.add_argument("-k","--APIkey", help="your API key", type=str,default=None)
args=parser.parse_args()


inputPath=args.inputPath
metaOutputPath=args.metaPath
imagesOutputPath=args.imagesPath
key=args.APIkey


def saveImage(imageData,row,id=""):
    if len(id)==0:
        imageName="{}_{}_{}.jpg".format(row['lat'],row['lon'],row['heading'])
    else:
        imageName = "{}.jpg".format(id)
    try:
        if not os.path.exists(outputPath):
            os.makedirs(outputPath)
        with open(imagesOutputPath+"/"+imageName, 'wb') as file:
            file.write(imageData)
        return True

    except:
        print('failed to save image {}'.format(imageName))
        return False


def CrawlPoint(lat,lon,angle,metaFlag=True,wait=True,radius=10,lag=0.5):
    if metaFlag:
        url_ = 'https://maps.googleapis.com/maps/api/streetview/metadata?source=outdoor&location=' + \
               str(lat) + ',' + str(lon) + '&heading=' + str(angle) + '&pitch=0&radius='+str(radius)+'&key=' + key
    else:
        url_ = 'https://maps.googleapis.com/maps/api/streetview?size=640x640&source=outdoor&location=' + \
               str(lat) + ',' + str(lon) + '&heading=' + str(angle) + '&pitch=0&radius='+str(radius)+'&key=' + key

    response = urllib.request.urlopen(url_)
    data = response.read()
    if metaFlag:
        data=data.decode("utf-8")
    if wait:
        time.sleep(lag)
    return data;


def Crawl(row,metaFlag=True):
    cameraHeading=row['heading']
    lat,lon=row["lat"],row["lon"]
    try:
        if metaFlag:
            metaData=CrawlPoint(lat,lon,cameraHeading)
            return metaData
        else:
            saveImage(CrawlPoint(lat,lon,cameraHeading),row,metaFlag=False)
            return True;
    except:
        print('not crawled successfully, check code for row {}'.format(row))
        return False;

def parseMetaData(row):
    metaDict=ast.literal_eval(row["meta"])
    del row["meta"]
    row["status"]=metaDict["status"]
    if metaDict["status"]=="OK":
        row["meta_copyright"]=metaDict["copyright"]
        row["meta_date"]=metaDict["date"]
        row["meta_lon"] = metaDict["location"]["lng"]
        row["meta_lat"]=metaDict["location"]["lat"]
        row["meta_pano_id"] = metaDict["pano_id"]

    else:
        row["meta_copyright"]=""
        row["meta_date"]=""
        row["meta_lat"]=""
        row["meta_lon"] = ""
        row["meta_pano_id"] = ""
    return row

def main():
    if args.imagesPath is None:
        metaFlag=True

    data=pd.read_csv(args.inputPath,delimiter=";")
    data.set_index('id')
    tqdm.pandas()
    if not metaFlag:
        print("NOTE: this code will start downloading images in 5 seconds")
        time.sleep(5)
    if metaFlag:
        print("collecting meta data")
        data["meta"]=data.progress_apply(lambda row: Crawl(row,metaFlag),axis=1)
        print("parsing meta data")
        data=data.progress_apply(lambda row: parseMetaData(row),axis=1)
        data.to_csv(args.metaPath)

    else:
        data.progress_apply(lambda row: Crawl(row,metaFlag),axis=1)


main()

