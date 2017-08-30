import sys
from lxml import html
import requests

#url = "http://econpy.pythonanywhere.com/ex/001.html"
url = "https://dining.williams.edu/eats4ephs/?unitid=27&meal=BREAKFAST"
page = requests.get(url)
tree = html.fromstring(page.content)


date = tree.xpath('//h5[@class="collection-date"]/text()')

#fooditems = tree.xpath()

#//*[@id="dining-app"]/h5

#foods = tree.xpath('//li[@data-ng-repeat="(course, items) in menu.filteredMeals" class="ng-scope"]/text()')
#//*[@id="dining-app"]/div/div[4]/ul/li[1]/ul/li[1]

#This will create a list of buyers:
#buyers = tree.xpath('//div[@title="buyer-name"]/text()')
#This will create a list of prices
#prices = tree.xpath('//span[@class="item-price"]/text()')




#print(buyers)

print('Date:')
print(date)
#print(fooditems)
