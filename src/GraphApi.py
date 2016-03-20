import requests
from src import facebook

#get your access token from here: https://developers.facebook.com/tools/explorer
access_token = 'CAACEdEose0cBACy3vnaBT071Lup3mn4kH8NauM4XHeyY1hMByDAvLlb2W4EUSsZBBg880XRKY00ZA9xmkDP6RXbZAEZA59pzJLGKxcGp48ZAgcMTcbM7ZC4K4Os8qFdWXGQdqiMUx2wu4bJZAOcwwvo4CwKcp3DraWFCylVYaOXb7d8WHiFbZBPPpgNJU6VrIK5JpyNtjyFAaEMC21iRFu9g0ZBZCUKYaUuhkZD'

#https://www.facebook.com/photo.php?fbid=10205355984653648&set=pb.1669607551.-2207520000.1458430750.&type=3&theater
#when I say replace the id of the pic, I mean fbId of any of the pic as shown in the above url.

picId = '10205355984653648/likes'

#extracting the first names from the returned JSON
def processNames(names):
    fname=[]
    for i in names:
        fname.append(i["name"].split()[0])
    return fname


#calling the API and writing the results to the File
def writeToFile():
    genderList=[]
    text_file = open("Output.txt", "w")
    for fname in fnames:
        r = requests.get("http://api.genderize.io/?name="+fname)
        result=r.json()
        genderList.append(result["gender"])
        text_file.write("The gender of the person is: %s\n" % result["gender"])
    femaleCount=float(genderList.count("female"))
    totalCount=float(len(fnames))
    percentage=int((femaleCount/totalCount)*100.0)
    text_file.write("The total number of female likes is: %s\n" % femaleCount )
    text_file.write("percentage wise: %s\n" % percentage )
    if percentage > 50:
        text_file.write("Girls think you are hot :)\n")
    else:
        text_file.write("Nope buddy, not hot according to girls :(\n")





#doing all the initializations
graph = facebook.GraphAPI(access_token)
picData = graph.get_object(picId)

#As the data is returned in forms of pagination, need to retrieve rest by pulling in next pages.
names=[]
while True:
    try:
        [names.append(name) for name in picData['data']]
        picData = requests.get(picData['paging']['next']).json()
    except KeyError:
        break

#processing the data retrieved by querying
fnames=processNames(names)

print "Teh total number of likes on the pic is: ", len(fnames)

#writing to file
writeToFile()

print "Execution completed, see the results in Output.txt file."

