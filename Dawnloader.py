import os
import json
from pprint import pprint
import pafy

# specify download directory
directory = '/content/Dataset/'

videoCounter = 0
unavailable = 0
unavailable_tr = 0
unavailable_tst = 0
unavailable_val = 0

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
    try:
        # start to download
        video = pafy.new(url)
        best = video.getbest()     
        filename = best.download(filepath=label_dir + '/' + key)
        print('Downloading... ' + str(videoCounter) + '\n')
        videoCounter += 1
        
    except Exception as inst:
        if subset == 'training':
            unavailable_tr += 1
            print('Number of Unavailable Training Videos: ', unavailable_tr)
            print('URL: ', url)
            
        if subset == 'validation':
            unavailable_val += 1
            print('Number of Unavailable Validation Videos: ', unavailable_val)
            print('URL: ', url)
            
        if subset == 'testing':
            unavailable_tst += 1
            print('Number of Unavailable Testing Videos: ', unavailable_tst)
            print('URL: ', url)
            
        
