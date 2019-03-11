import os
import json
import pafy

# specify download directory
directory = '/content/Dataset/'

videoCounter = 0

# these lists will record unavailable videos by their key so we can find them 
# in the downloaded files. it's important to remove these fake files from 
# datset files for proper training.
unavailable_tr = []
unavailable_tst = []
unavailable_val = []

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
    print(key)
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
            unavailable_tr.append(key)
            print('Number of Unavailable Training Videos: ',len(unavailable_tr))
            print('URL: ', url)
            
        if subset == 'validation':
            unavailable_val.append(key)
            print('Number of Unavailable Validation Videos: ', len(unavailable_val))
            print('URL: ', url)
            
        if subset == 'testing':
            unavailable_tst.append(key)
            print('Number of Unavailable Testing Videos: ', len(unavailable_tst))
            print('URL: ', url)

# overall unavailable videos
print('Number of Unavailable training videos: ',len(unavailable_tr))
print('Number of Unavailable validation videos: ',len(unavailable_val))
print('Number of Unavailable testing videos: ',len(unavailable_tst))
