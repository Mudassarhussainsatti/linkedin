import os,random,sys,time
from urllib.parse import urlparse
import csv
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

totalInvites = 0
page=2
searchQuery =''
sentTo = []
def initiateConnectionInvite(browser):
    global totalInvites
    global page
    global searchQuery
    global sentTo
    with open('visited.txt') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0

        for row in csv_reader:
         if line_count == 0:
            print('Initiating Invites')
            if(row[2] in sentTo):
                continue
            else:
             sentTo.append(row[2])
             sent = sendConnectionInivite(totalInvites, row[1], row[2], browser)
             if(sent):
                 totalInvites += 1
                 if totalInvites >= 5:
                     break
                 else:
                     print()
             else:
                line_count += 1
         else:
            if(row[2] in sentTo):
                continue
            else:
             sentTo.append(row[2])
             sent = sendConnectionInivite(totalInvites, row[1], row[2], browser)
             if (sent):
                 sentTo.append(row[2])
                 totalInvites += 1
                 if totalInvites >= 5:
                  break
                 else:
                    print()
             else:
                    line_count += 1
        print('Total Invites sent so far',totalInvites)
        if totalInvites >= 5:
            with open('visited.txt', 'w+') as file:
                file.close()
            logout(browser)
            print('ALL-DONE')
        else:
            with open('visited.txt', 'w+') as file:
                file.close()
            page +=1
            initiateSearch(browser,searchQuery,page)

def logout(browser):
    browser.get('https://www.linkedin.com/m/logout')
    print('Logged Out')

def sendConnectionInivite(number,name,link,browser):
    try:
     print('sending Invites')
     browser.get(link)
     element = browser.find_element_by_class_name('pv-s-profile-actions')
     actions = ActionChains(browser)
     actions.click(element)
     actions.perform()
     try:
         element = browser.find_element_by_class_name("msg-form__contenteditable")
         actions = ActionChains(browser)
         actions.click(element)
         actions.perform()
         element = browser.find_element_by_id('email')
         actions = ActionChains(browser)
         actions.click(element)
         actions.perform()
         print('Error')
         return False
     except:
         element_1 = browser.find_element_by_class_name('ml1').click()
         actions = ActionChains(browser)
         actions.click(element_1)
         actions.perform()
         strsp = name.split("View")
         with open('sent.txt', 'a', newline='\n') as file:
            writer = csv.writer(file)
            writer.writerow([strsp[0], link])
         print('Sent to',strsp[0])
         try:
             element = browser.find_element_by_class_name('ip-fuse-limit-alert__warning')
             print('You’ve reached the weekly invitation limit')
             return False
         except:
             print()
         return True
    except:
        print('Error')
        return False
def initiateSearch(browser,sq,page):
    print('Getting page ',page)
    url = 'https://www.linkedin.com/search/results/people/?keywords=' + sq + '&origin=SWITCH_SEARCH_VERTICAL&page='+str(page)
    print(url)
    browser.get(url)
    print('Searching ........')
    soup = BeautifulSoup(browser.page_source)
    search_section = soup.find('div', {'class': 'pv2 artdeco-card ph0 mb2'})
    all_links = search_section.find_all('a', {'class': 'app-aware-link'})
    n = 0
    addProfile = []
    with open('visited.txt', 'a', newline='\n') as file:
        writer = csv.writer(file)
        for link in all_links:
            profile_link = link.get('href')
            profile_name = link.text
            if (profile_name not in addProfile):
                addProfile.append(profile_name)
                if (profile_name == "\n        \n\n\n" or 'other shared' in profile_name):
                    print('')
                else:
                    n = n + 1
                    writer.writerow([n, profile_name.strip(), profile_link.strip()])
    initiateConnectionInvite(browser)


#browser = webdriver.Chrome('chromedriver.exe')
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('window-size=1920x1480')
browser = webdriver.Chrome(options=chrome_options, executable_path='/project/chromedriver')
with open('sent.txt') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0

    for row in csv_reader:
        sentTo.append(row[1])

with open('sent.txt', 'a', newline='\n') as file:
    writer = csv.writer(file)
    writer.writerow('------------------')
userInput = sys.argv[1]
print("userInput",userInput)
browser.get('https://linkedin.com/uas/login')
upArr = userInput.split("|")
searchQuery = upArr[2]
#searchQuery = searchKey.replace(" ","%20")
elementID = browser.find_element_by_id('username')
elementID.send_keys(upArr[0])
elementID = browser.find_element_by_id('password')
elementID.send_keys(upArr[1])
elementID.submit()
print('logging In ......')
print('logged In Successfully!')
try:
    elementID = browser.find_element_by_id('input__email_verification_pin')
    print('Kindly verify your Email By entering OTP sent on email\n')
    otp = input("Enter Your Email OTP here")
    elementID.send_keys(otp)
    elementID.submit()
    print('Sent Request')
except:
    print()
with open('visited.txt', 'w+') as file:
    file.close()
initiateSearch(browser,searchQuery,page)
