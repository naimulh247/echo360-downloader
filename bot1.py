from selenium import webdriver
import time
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import os

chrome_options = webdriver.ChromeOptions()
prefs = {'download.default_directory' : '/Users/naimulhasan/Desktop/abcooper/'}
chrome_options.add_experimental_option('prefs', prefs)



driver =  webdriver.Chrome(chrome_options=chrome_options,executable_path="./chromedriver")
driver.get("https://echo360.org/")

x=input("please press y if you have scrolled all the way to the bottom of the recording and signed in: ")

imgLinks = driver.find_elements_by_xpath('/html/body/div[2]/div[2]/div[2]/div[2]/div[2]/div/div[3]/div[1]/div/div[8]/div/img')
img=["null"]*(len(imgLinks))

dateTime=driver.find_elements_by_xpath('/html/body/div[2]/div[2]/div[2]/div[2]/div[2]/div/div[3]/div[1]/div/div[2]/span[1]')
dateAndTime=["null"]*(len(imgLinks))

titleNames=driver.find_elements_by_xpath('/html/body/div[2]/div[2]/div[2]/div[2]/div[2]/div/div[3]/div[1]/div/div[3]/div[2]')
folderNames=["null"]*(len(imgLinks))

audioDivs = driver.find_elements_by_xpath('/html/body/div[2]/div[2]/div[2]/div[2]/div[2]/div/div[3]/div[1]/div/div[8]/div')
audioDivsCopy=["null"]*(len(audioDivs))


index=0
folderTracker = 1
while index != len(imgLinks):
    img[index]=imgLinks[index].get_attribute("src").split('/')[4]
    dateAndTime[index]=dateTime[index].text
    folderNames[index]=titleNames[index].text
    audioDivsCopy[index] = audioDivs[index].get_attribute("class")
    index += 1

def loadPage():
    global img
    global folderTracker
    for i in range(0,len(img)):
        print("on the " + str(i) +" recording")
        driver.get("https://echo360.org/media/"+img[i])
        time.sleep(2)
        clickOnButton()
        
        
    
def check_exists_by_link_text(text):
    try:
        driver.find_element_by_partial_link_text(text)
    except NoSuchElementException:
        return False
    return True

def wait_for_downloads(fileDirectory):
    print("Waiting for downloads", end="")
    while any([filename.endswith(".crdownload") for filename in 
               os.listdir(fileDirectory)]):
        time.sleep(2)
        print(".", end="")
    print("done!")

def move_items(foldername, foldernumber):
    try:
        os.system("mv /Users/naimulhasan/Desktop/abcooper/*.mp4 /Users/naimulhasan/Desktop/abcooper/" + str(foldernumber) + ".*/")
        print("moved .mp4 into " + foldername)
        time.sleep(5)
    except:
        print("couldnt move or didnt find .mp4 to be moved to " + foldername)
        time.sleep(5)
        pass
    
    try:
        os.system("mv /Users/naimulhasan/Desktop/abcooper/*.mp3 /Users/naimulhasan/Desktop/abcooper/" + str(foldernumber) + ".*/")
        print("moved audio into " + foldername)
        time.sleep(5)
    except:
        print("couldnt move audio into " + foldername)
        time.sleep(5)
        pass

    
def make_folder():
    global folderTracker
    folder = str(folderTracker+1)+". "+folderNames[folderTracker] + " (" + dateAndTime[folderTracker] + ")"
    folder = folder.replace("/", " of ")
    os.makedirs("/Users/naimulhasan/Desktop/abcooper/" + folder)
    print("created folder: " + folder)
    time.sleep(5)
    move_items(folder, folderTracker+1)
    folderTracker += 1

def clickOnButton():
    details= driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[3]/div/ul/li[3]/button/span')
    details.click()
    time.sleep(2)
    sd1 = check_exists_by_link_text('sd1.mp4')
    hd1 = check_exists_by_link_text('hd1.mp4')
    audio = check_exists_by_link_text('audio.mp3')

    if(hd1 and sd1):
        print("found hd1 and downloading")
        hd1Path = driver.find_element_by_partial_link_text('hd1.mp4')
        hd1Path.click()
        print("waiting for download hd1")
        time.sleep(3)
    elif(sd1 and not hd1):
        print("didnt find hd1, downloading sd1")
        sd1Path = driver.find_element_by_partial_link_text('sd1.mp4')
        sd1Path.click()
        print("waiting for download sd1")
        time.sleep(3)
    elif(not sd1 and not hd1):
        print("did not find sd1 or hd1")
        time.sleep(2)

    if(audio):
        print("found audio and downloading")
        audioPath = driver.find_element_by_partial_link_text('audio.mp3')
        audioPath.click()
        print("waiting for download audio")
        time.sleep(3)    
    wait_for_downloads("/Users/naimulhasan/Desktop/abcooper/")
    make_folder()
    



loadPage()


    




