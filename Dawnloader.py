#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 10 14:51:14 2019

@author: gabir
"""
import os
import json
from pprint import pprint
import pafy

# specify download directory
directory = '/home/gabir/Desktop/Dawnload_Activitynet_dataset'
videoCounter = 0

# open json file
with open('activity_net.v1-3.min.json') as data_file:    
    data = json.load(data_file)

# take only video informations from database object
videos = data['database']

# iterate through dictionary of videos
for key in videos:
    # take video
    video = videos[key]
    
    # find video subset
    subset = video['subset']

    # find video label
    annotations = video['annotations']
    label = ''
    if len(annotations) != 0:
        label = annotations[0]['label']
        label = '/' + label.replace(' ', '_')

    # create folder named as <label> if does not exist
    label_dir = directory + subset + label
    if not os.path.exists(label_dir):
        os.makedirs(label_dir)

    # take url of video
    url = video['url']

    # start to download
    video = pafy.new(url)
    best = video.getbest()     
    filename = best.download(filepath=label_dir + '/' + key)
    print('Downloading... ' + str(videoCounter) + '\n')
    videoCounter += 1
    
# =============================================================================
# 	try:
# 		video = pafy.new(url)
# 		best = video.getbest()
# 		filename = best.download(filepath=label_dir + '/' + key)
# 		print('Downloading... ' + str(videoCounter) + '\n')
# 		videoCounter += 1
# 	except Exception as inst:
# 		print('Error!')
# =============================================================================
        
    
