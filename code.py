import os,random,sys,time
from urllib.parse import urlparse
import csv
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import lxml

def initiateConnectionInvite(browser):
    with open('visited.txt') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        totalInvites = 0;
        for row in csv_reader:
            if totalInvites == 25:
                with open('visited.txt', 'w+') as file:
                    file.close()
                logout(browser)
                break
            else:
             if line_count == 0:
                print('Initiating Invites')
                sent = sendConnectionInivite(totalInvites, row[1], row[2], browser)
                if(sent):
                    totalInvites += 1
                else:
                    line_count += 1
             else:
                sent = sendConnectionInivite(totalInvites, row[1], row[2], browser)
                if (sent):
                    totalInvites += 1
                else:
                    line_count += 1
        print('ALL-DONE')

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
     element_1 = browser.find_element_by_class_name('ml1').click()
     actions = ActionChains(browser)
     actions.click(element_1)
     actions.perform()
     strsp = name.split("View")
     with open('sent.txt', 'a', newline='\n') as file:
         writer = csv.writer(file)
         writer.writerow([strsp[0], link])
     print('Sent to',strsp[0])
     return True
    except:
        print('Error')
        return False
def initiateSearch(browser,url):
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



#browser = webdriver.Chrome('chromedriver.exe')
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('window-size=1920x1480')
browser = webdriver.Chrome(options=chrome_options, executable_path='/project/chromedriver')
browser.get('https://linkedin.com/uas/login')
usernamePassword = input('Enter your Username & Password (Should be space between username and password)')
upArr = usernamePassword.split(" ")
searchKey = input('Enter Search Query')
searchQuery = searchKey.replace(" ","%20")
elementID = browser.find_element_by_id('username')
elementID.send_keys(upArr[0])
elementID = browser.find_element_by_id('password')
elementID.send_keys(upArr[1])
elementID.submit()
print('logging In ......')
print('logged In Successfully!')
url1 = 'https://www.linkedin.com/search/results/people/?keywords='+searchQuery+'&origin=SWITCH_SEARCH_VERTICAL'
url2 = 'https://www.linkedin.com/search/results/people/?keywords='+searchQuery+'&origin=SWITCH_SEARCH_VERTICAL&page=2'
url3 = 'https://www.linkedin.com/search/results/people/?keywords='+searchQuery+'&origin=SWITCH_SEARCH_VERTICAL&page=3'
url4 = 'https://www.linkedin.com/search/results/people/?keywords='+searchQuery+'&origin=SWITCH_SEARCH_VERTICAL&page=4'
initiateSearch(browser, url1)
initiateSearch(browser, url2)
initiateSearch(browser, url3)
initiateSearch(browser, url4)
initiateConnectionInvite(browser)
