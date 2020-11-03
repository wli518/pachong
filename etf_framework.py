import os.path
import unittest
import random
from bs4 import BeautifulSoup
import sys
from HTMLTestRunner import HTMLTestRunner
from xlrd import open_workbook
import time
from selenium import webdriver
from collections import OrderedDict
import re

def getinfo(tick,fw,mydic):
    mysource=getDriver("https://www.etf.com/" + tick)
    #print(mysource)
    mybody = re.findall(r'<body(.+?)</body>', mysource, re.DOTALL)
    mydd = mybody[0].replace('\n', '')

    soup = BeautifulSoup(mydd, "html.parser")
    secs = soup.select("div.generalData > section.generalDataBox")

    for sec in secs:
        dd = BeautifulSoup(str(sec), "html.parser")
        # title=dd.select_one("section h4")
        # print "*** ", title.text, " ***"
        divs = dd.select("section div")
        for div in divs:
            nn = BeautifulSoup(str(div), "html.parser")
            ll = nn.select_one("div label")
            pp = nn.select_one("div span")
            vv = nn.select_one("div div")
            if ll and pp:
                myvalue = pp.text
                mylabel = ll.text
            if ll and vv:
                myvalue = vv.text
                mylabel = ll.text
            if mydic.has_key(mylabel):
                mydic[mylabel] = myvalue
    print(mydic)
    mydic['Tick']=tick
    valueStr = ";".join(mydic.values())
    print(valueStr)
    fw.write(valueStr)
    fw.write("\n")

def getDriver(myurl):
    chromedriver = "C://Users//polly//Desktop//selenium-java-3.3.1//chromedriver"
    os.environ["webdriver.chrome.driver"] = chromedriver
    driver = webdriver.Chrome(chromedriver)
    driver.get(myurl)
    waitsecond = random.randint(1, 3) * 10
    print(str(waitsecond) + "s")
    driver.implicitly_wait(waitsecond)
    # driver.maximize_window()
    mysource = driver.page_source
    driver.quit()
    return mysource

def read_etf_data(tsname,tsinfo):
    mydic = OrderedDict()
    mydic["Tick"] = "Not Found"
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

    fw = open(tsinfo,"w")
    labelStr = ";".join(mydic.keys())
    fw.write(labelStr)
    fw.write("\n")

    read_sym = True
    if os.path.exists(tsname):
        wbexcel=open_workbook(tsname)
        ws=wbexcel.sheet_by_index(0)
        for irow in range(0,ws.nrows):
            tick=ws.cell(irow,0).value
            getinfo(tick.upper(),fw,mydic)
    else:
        read_sym=False
    fw.close()
    return read_sym


class MyTest(unittest.TestCase):
    def setUp(self):
        pass

    def testetf(self):
        #tspath = os.path.abspath('.')
        tsname = 'C://Users//polly//Desktop//etflist.xls'
        tsinfo='C://Users//polly//Desktop//etf.txt'
        print tsname
        print tsinfo
        self.assertTrue(read_etf_data(tsname,tsinfo))

    def tearDown(self):
        pass


if __name__ == '__main__':
    test = unittest.TestSuite()
    test.addTest(MyTest('testetf'))
    runner = HTMLTestRunner(stream=None, title='', description='')
    runner.run(test)
