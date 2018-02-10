'''
Created on Jul 1, 2017

@author: alex
'''
#TODO add default firefox profile to get around needing save option. How to access appdata?
import os,shutil
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
def main(): #will scrape through each section
    #!!all sections are scraped for half
 #   try:scrape('elementary',9)
 #   except:print('exception on elementary scrape')
 #   try:scrape('pre-intermediate',2)
 #   except:print('exception on pre-intermediate scrape')
#    try:scrape('intermediate',16)
#    except:print('exception on intermediate scrape')
#    try:scrape('upper-intermediate',6)
#    except:print('exception on upper-intermediate scrape')
    try:scrape('advanced',4)
    except:print('exception on advanced scrape')
        
def scrape(section,pages):
    if section=='elementary':  #selects the appropriate parameters for each diffuculty level
        url='https://chinesepod.com/library/channels/list/elementary/desc/?page='
        lesson_basefolder=r'C:\Users\alex\Desktop\chinesepod extract\Elementary'
    elif section=='pre-intermediate':
        url='https://chinesepod.com/library/channels/list/pre+intermediate/desc/?page='
        lesson_basefolder=r'C:\Users\alex\Desktop\chinesepod extract\PreIntermediate'
    elif section=='intermediate':
        url='https://chinesepod.com/library/channels/list/intermediate/desc/?page='
        lesson_basefolder=r'C:\Users\alex\Desktop\chinesepod extract\Intermediate'
    elif section=='upper-intermediate':
        url='https://chinesepod.com/library/channels/list/upper+intermediate/desc/?page='
        lesson_basefolder=r'C:\Users\alex\Desktop\chinesepod extract\UpperIntermediate'
    elif section=='advanced':
        url='https://chinesepod.com/library/channels/list/advanced/desc/?page='
        lesson_basefolder=r'C:\Users\alex\Desktop\chinesepod extract\Advanced'
    else:
        print('no match')
        
    lesson_url='https://chinesepod.com'
            
    #logs into chinesepod
    fp=webdriver.FirefoxProfile(r'C:\Users\alex\AppData\Roaming\Mozilla\Firefox\Profiles\fuwz3yda.default')
    driver=webdriver.Firefox(fp)
    driver.get('https://chinesepod.com/accounts/signin')
    
    for i in range (1,pages): #for each page in the elementary
        try:
            print('Downloading page {}'.format(i))
            driver.get(url+str(i))
            element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "fb-root")))
            soup=BeautifulSoup(driver.page_source,'html.parser')
            
            lessons=soup.find_all('div',{"class":'col-sm-3 col-xs-6 free'})
            for lesson in lessons: #for each lesson
                
                href_element=lesson.find('a',href=True)
                append_url=href_element['href'] #finds lesson title
                print(append_url)
                
                lesson_folder=lesson_basefolder + "\\"+ append_url[9:]
                os.makedirs(lesson_folder) #makes folder for lesson
                
                driver.get(lesson_url+append_url) #goes to lesson page
                
                element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "fb-root")))
                driver.find_element_by_id("lessonReviewDownloads").click() #clicks drop down box
                time.sleep(1)   
                
                driver.find_element_by_link_text("Dialogue").click() #download the dialog and move to correct folder
                path=r'C:\Users\alex\Downloads'
                for i in os.listdir(path):
                    if os.path.isfile(os.path.join(path,i)) and 'chinesepod' in i:
                        shutil.move(os.path.join(path,i),lesson_folder+"\\"+'dialogAudio.mp3')
                
                pdf_link=driver.find_element_by_link_text("text version").get_attribute('href') #clicks dialog text link and downloads
                driver.get(pdf_link)
                
                soup=BeautifulSoup(driver.page_source,'html.parser')
                html_texts=soup.find_all(text=True)
                f=open(lesson_folder+"\\"+'dialog.txt','w+',encoding='utf-8')
                for j in range(6,len(html_texts)-3): #writes each line of the pdf to the text file
                    if not html_texts[j].isspace():
                        f.write(html_texts[j]+'\n')
                f.close()             
            
        except:
            print('exception on lesson {}'.format(append_url))
            #scrapepdf(lesson_folder,driver,'dialog')
            #cant get this working because of printer dialog box. If its part of browser i could click away. but its still bad quality because its embedded pdf
            #driver.get(lesson_url+append_url + '\\'+'print-grammar')
            #scrapepdf(lesson_folder,driver,'grammar')
            #driver.get(lesson_url+append_url + '\\'+'print-expansion')
            #scrapepdf(lesson_folder,driver,'expansion')
                 
#function not currently used as i dont scrape the grammer and expansion
def scrapepdf(lesson_folder,driver,filetype):
    html_source=driver.page_source
    soup=BeautifulSoup(driver.page_source,'html.parser')
    html_texts=soup.find_all(text=True)
    if filetype=='dialog':
        f=open(lesson_folder+"\\"+'dialog.txt','w+',encoding='utf-8')
    elif filetype=='expansion':
        f=open(lesson_folder+"\\"+'expansion.txt','w+',encoding='utf-8')
    elif filetype=='grammar':
        f=open(lesson_folder+"\\"+'grammar.txt','w+',encoding='utf-8')
        start_j=13
    else:
        pass
    
    for j in range(6,len(html_texts)-3): #writes each line of the pdf to the text file
        if not html_texts[j].isspace():
            f.write(html_texts[j]+'\n')
    f.close()
    
        
        
        
        
        
        
    
    
    
    
if __name__ == '__main__':
    main()