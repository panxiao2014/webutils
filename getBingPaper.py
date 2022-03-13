import os
from bs4 import BeautifulSoup
import requests
import ssl
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

websiteBase = 'https://www.bwallpaperhd.com/'
picCategories = ["nature", "animal", "plant", "people", "modern", "space", "other"]

localDownloadPath = "c:/_temp"
numDownloaded = 0

for picCategory in picCategories:
    website = "%s%s" % (websiteBase, picCategory)
    result = requests.get(website, verify=False, timeout=60)
    content = result.text
    soupCategory = BeautifulSoup(content, 'lxml')

    #find maxinum pages for this category
    pageNum = []
    pageLinks = soupCategory.findAll("a", {"class": "page-numbers"})
    for pageLink in pageLinks:
        if(pageLink['class'][0] == "next"):
            continue
        pageNum.append(int(pageLink.text))

    maxNum = max(pageNum)
    print("%s has %d pages" % (picCategory, maxNum))

    catPath = os.path.join(localDownloadPath, picCategory)
    if(os.path.isdir(catPath) == False):
        os.mkdir(catPath)

    #go to every page:
    picPage = ''
    for i in range(1, maxNum+1):
        if(i == 1):
            picPage = website
        else:
            picPage = "%s/page/%d" % (website, i)

        print("Go to page %s" % (picPage))
        try:
            result = requests.get(picPage, verify=False, timeout=60)
        except Exception as e:
            print(e)
            continue

        content = result.text
        soupPicPage = BeautifulSoup(content, 'lxml')
    
        #each page contains 8 links to the pictures:
        picLinks = []
        boxes = soupPicPage.findAll(class_='view view-first')
        for box in boxes:
            links = [link['href'] for link in box.find_all('a', href=True)]
            picLinks.append(links[0])

        print("Found links:")
        print(picLinks)

        #go to each picutre page and download:
        for picLink in picLinks:
            try:
                result = requests.get(picLink, verify=False, timeout=60)
            except Exception as e:
                print(e)
                continue

            content = result.text
            soupPicture = BeautifulSoup(content, 'lxml')
            downloadLink = soupPicture.find('a', href=True, text=' 1920x1080')
            print("  Download link:")
            print(downloadLink)
            if(downloadLink == None):
                continue
            
            #check if picture already downloaded:
            picUrl = downloadLink.get('href')
            picName = os.path.basename(picUrl)
            picFile = os.path.join(localDownloadPath, picCategory, picName)
            if(os.path.isfile(picFile)):
                print("%s already downloaded" % (picFile))
                numDownloaded += 1
            else:
                #download picture:
                with open(picFile, "wb") as f:
                    try:
                        webImage = requests.get(picUrl)
                    except Exception as e:
                        print(e)
                        continue

                    f.write(webImage.content)
                    numDownloaded += 1
                    print("%s downloaded. Total files: %d" % (picName, numDownloaded))

        print("\n\n")
        

        

#print(soup.prettify())


# boxes = soupCategory.findAll(class_='view view-first')


# picLinks = []

# for box in boxes:
#     links = [link['href'] for link in box.find_all('a', href=True)]
#     picLinks.append(links[0])

# for picLink in picLinks:
#     result = requests.get(picLink, verify=False)
#     content = result.text
#     soupPicPage = BeautifulSoup(content, 'lxml')
#     downloadLink = soupPicPage.find('a', href=True, text=' 1920x1080')
#     picUrl = downloadLink.get('href')
#     picName = os.path.basename(picUrl)
#     with open(picName, "wb") as f:
#         f.write(requests.get(picUrl).content)