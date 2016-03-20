import requests
import facebook

# get your access token from here: https://developers.facebook.com/tools/explorer
access_token = 'CAACEdEose0cBAGs2ANb6E2VOTJmz32u7ZByJEGsyXEL71VUbcu4KjOvYdpzM60lurYEhffCZCgtk0ZBhs6I8iFkIdmtZAQy9HdGrcIjndZAYtWGCYortiSOoZAjLSoHxBQiHxAheqjZBMSuoAZB2WFNPSdKba6KU7dX0cjE03wIuUkgyf1pOnTeR13ut4Fzw41sKYfpgqkEPgjpuXto8UxS8PzhmfZAd6TsYZD'

# create an account on https://gender-api.com and append your server key below.
ApiKey = 'ZJHjMWWHLZyVhSeJRT'

# https://www.facebook.com/photo.php?fbid=10205355984653648&set=pb.1669607551.-2207520000.1458430750.&type=3&theater
# when I say replace the id of the pic, I mean fbId of any of the pic as shown in the above url.

# List of picIds of the most recent pics
picIDList = ['10205355984653648', '10204664229920212', '10201859340079719']
text_file = open("Output.txt", "w")
# doing all the initializations
graph = facebook.GraphAPI(access_token)
count = 0
resultList = []


# extracting the first names from the returned JSON
def processNames(names):
    fname = []
    for i in names:
        fname.append(i["name"].split()[0])
    return fname


# calling the API and writing the results to the File
def writeToFile(count, resultList):
    genderList = []
    for fname in fnames:
        r = requests.get("https://gender-api.com/get?name=" + fname + "&key=" + ApiKey)
        result = r.json()
        genderList.append(result["gender"])
    femaleCount = float(genderList.count("female"))
    totalCount = float(len(fnames))
    percentage = int((femaleCount / totalCount) * 100.0)
    text_file.write("Pic number: %s\n" % count)
    text_file.write("The total number of likes is: %s\n" % totalCount)
    text_file.write("The total number of female likes is: %s\n" % femaleCount)
    text_file.write("percentage wise: %s\n" % percentage)
    text_file.write("\n")
    resultList.append(percentage)


# iterating through all the pics
for picId in picIDList:
    picData = graph.get_object(picId + '/likes')
    # As the data is returned in forms of pagination, need to retrieve rest by pulling in next pages.
    count += 1
    names = []
    while True:
        try:
            [names.append(name) for name in picData['data']]
            picData = requests.get(picData['paging']['next']).json()
        except KeyError:
            break
    # processing the data retrieved by querying
    fnames = processNames(names)
    print "Teh total number of likes on the pic is: ", len(fnames)
    writeToFile(count, resultList)

#calculating average of the female likes
average = sum(resultList, 0.0) / len(resultList)

text_file.write("Average percentage of female likes: %s\n" % average)

print "Execution completed, see the results in Output.txt file."
