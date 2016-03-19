"""
A simple example script to get all posts on a user's timeline.
Originally created by Mitchell Stewart.
<https://gist.github.com/mylsb/10294040>
"""
import facebook
import requests


#get your access token from here:
access_token = 'CAACEdEose0cBAPZAXZC4oLGfMrACtj5fIRlMb2nhGaBCZBaxIRApRsaPJbFujzbnHlnc2D3LEevqCgPRg6ZBMSF2PbIWTkdHZCa6r3sQGRxb2ISc6VSspkMsnSZChT0xuA5X0MxkmDbuRZCncKuM2C9H0cVnPZCapQWHCrvCTUB39vhp8pIkHvmYmVn7Fm0MLLEDBPtNKHPwFVs513RVHVnUrRtkQffKPikZD'
pic = '10205355984653648/likes'


def processNames(names):
    fname=[]
    for i in names:
        fname.append(i["name"].split()[0])
    return fname

def writeToFile():
    femaleLikes=[]
    text_file = open("Output.txt", "w")
    for fname in fnames:
        r = requests.get("http://api.genderize.io/?name="+fname)
        result=r.json()
        femaleLikes.append(result["gender"])
        text_file.write("%s\n" % result["gender"])
    text_file.write("%s\n" % femaleLikes.count("female") )


graph = facebook.GraphAPI(access_token)
picData = graph.get_object(pic)
names=[]
while True:
    try:
        [names.append(name) for name in picData['data']]
        picData = requests.get(picData['paging']['next']).json()
    except KeyError:
        break

fnames=processNames(names)
print len(fnames)
writeToFile()

