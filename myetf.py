from selenium import webdriver
import os
import random
import sys
from bs4 import BeautifulSoup
import re
from collections import OrderedDict
import time

def getinfo(tick):
    driver.get("https://www.etf.com/"+tick)
    waitsecond=random.randint(1,3)*10
    print(str(waitsecond)+"s")
    driver.implicitly_wait(waitsecond)
#driver.maximize_window()
    mysource=driver.page_source
    driver.quit()

    mybody=re.findall(r'<body(.+?)</body>',mysource,re.DOTALL)
    mydd=mybody[0].replace('\n','')

    soup=BeautifulSoup(mydd,"html.parser")
    secs=soup.select("div.generalData > section.generalDataBox")

    for sec in secs:
        dd=BeautifulSoup(str(sec),"html.parser")
        #title=dd.select_one("section h4")
        #print "*** ", title.text, " ***"
        divs=dd.select("section div")
        for div in divs:
        #print(str(div))
            nn = BeautifulSoup(str(div), "html.parser")
            ll=nn.select_one("div label")
            pp = nn.select_one("div span")
            vv = nn.select_one("div div")
            if ll and pp:
            #print ll.text, "---",pp.text
                myvalue=pp.text
                mylabel = ll.text
            if ll and vv:
            #print ll.text, "---", vv.text
                myvalue=vv.text
                mylabel = ll.text

            if mylabel in mylist:
                mydic[mylabel]=myvalue

    print(mydic)

    labelStr=";".join(mydic.keys())
    valueStr=";".join(mydic.values())
    print(labelStr)
    print(valueStr)


    if not file_exist:
        fw.write(labelStr)
        fw.write("\n")
    fw.write(valueStr)
    fw.write("\n")


if __name__ == "__main__":
    chromedriver = "C://Users//polly//Desktop//selenium-java-3.3.1//chromedriver"
    os.environ["webdriver.chrome.driver"] = chromedriver
    driver = webdriver.Chrome(chromedriver)

    if sys.argv[1]:
        tick=sys.argv[1]
    else:
        print("etf tick is missing")
        sys.exit(-1)

    mylist=["Tick", "Issuer", "Inception Date", "Expense Ratio", "Assets Under Management", "Price / Earnings Ratio", "Price / Book Ratio", "Distribution Yield", "Number of Holdings", "Index Tracked", "Index Weighting Methodology", "Index Selection Methodology", "Median Tracking Difference (12 Mo)", "Max. Upside Deviation (12 Mo)", "Max. Downside Deviation (12 Mo)", "Max LT/ST Capital Gains Rate", "Securities Lending Active", "Fund Closure Risk", "Portfolio Disclosure", "Max. Premium / Discount (12 Mo)", "Net Asset Value (Yesterday)", "ETF.com Implied Liquidity", "Beta", "Up Beta", "Down Beta", "Downside Standard Deviation", "Shared Holdings", "Shared Holdings Weight"]

    mydic = OrderedDict()
    mydic["Tick"] = tick.upper()
    mydic["Issuer"] = "Not Found"
    mydic["Inception Date"] = "Not Found"
    mydic["Expense Ratio"] = "Not Found"
    mydic["Assets Under Management"] = "Not Found"
    mydic["Price / Earnings Ratio"] = "Not Found"
    mydic["Price / Book Ratio"] = "Not Found"
    mydic["Distribution Yield"] = "Not Found"
    mydic["Number of Holdings"] = "Not Found"
    mydic["Index Tracked"] = "Not Found"
    mydic["Index Weighting Methodology"] = "Not Found"
    mydic["Index Selection Methodology"] = "Not Found"
    mydic["Median Tracking Difference (12 Mo)"] = "Not Found"
    mydic["Max. Upside Deviation (12 Mo)"] = "Not Found"
    mydic["Max. Downside Deviation (12 Mo)"] = "Not Found"
    mydic["Max LT/ST Capital Gains Rate"] = "Not Found"
    mydic["Securities Lending Active"] = "Not Found"
    mydic["Fund Closure Risk"] = "Not Found"
    mydic["Portfolio Disclosure"] = "Not Found"
    mydic["Max. Premium / Discount (12 Mo)"] = "Not Found"
    mydic["Net Asset Value (Yesterday)"] = "Not Found"
    mydic["ETF.com Implied Liquidity"] = "Not Found"
    mydic["Beta"] = "Not Found"
    mydic["Up Beta"] = "Not Found"
    mydic["Down Beta"] = "Not Found"
    mydic["Downside Standard Deviation"] = "Not Found"
    mydic["Shared Holdings"] = "Not Found"
    mydic["Shared Holdings Weight"] = "Not Found"

    myfile="C://Users//polly//Desktop//ETF.txt"
    if os.path.exists(myfile):
        file_exist=1
    else:
        file_exist=0
    fw=open(myfile, "a")
    getinfo(tick.upper())
    fw.close()
