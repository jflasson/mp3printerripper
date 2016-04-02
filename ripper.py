#This program rips song playing on the mp3printer

import requests
import time

checkinterval = 15
currentnp = ''
jobid = ''

#Finds the id of current job
def findcurrentjob():
    findjobresp = requests.get('http://lp3/')
    findjobresp = findjobresp.text
    for i in range(len(findjobresp)):
        if findjobresp[i:i+20] == '<tbody id="mp3_jobs"':
#            print("POTATIS!")
            findjobresp = findjobresp[i:]
    for i in range(len(findjobresp)):
        if findjobresp[i:i+20] == '<tr class="mp3_job" ':
            job = findjobresp[i+28:i+31]
#            print(job)
            return job
            break

#Dowloads job with id id and saves it as filename
def downloadid(id, filename):
    url = "http://lp3/download.php?job=" + id
#    print('download url is: ' + url)
    download = requests.get(url)
    if filename == "Loading....mp3":
        currentnp = ''
    print("Writing " + filename + " to disk.")
    file = open(filename, 'wb')
    file.write(download.content)
    file.close()

#Finds the name of the song currently being played. Strips : as it is not
#supported in windows filenames
def findsongname(songtext):
#    print("in finding songname: " + songtext)
    first = 0
    for i in range(200):
        if songtext[i:i+30] == '<span id="mp3_title_metadata">':
            first = i+30
#            print("first found!")
            break
    last = 0
    for i in range(200):
        if songtext[i:i+7] == '</span>':
            last = i
#            print("last found!")
            break
    songname = songtext[first:last] + ".mp3"
    songname = songname.replace(':', ".")
    print("Songname is: " + songname)
    return songname

#Checks for new songs and issues apporopriate commands when a new song is found
print("Ripper is running, checking for new song every " + str(checkinterval) + " seconds.")
while(1):
    response = requests.get('http://lp3/')
    print('Checking for new song.')
    responsetext = response.text
    np = responsetext[1000:2000]
    for i in range(1000):
        if(np[i:i+22]) == "&nbsp; &nbsp; Now Play":
            np = np[i:i+200]
            if np != currentnp:
                print("New song detected!")
                currentnp = np
                filename = findsongname(np)
                jobid = findcurrentjob()
#                print(jobid)
                downloadid(jobid, filename)
    time.sleep(checkinterval)
