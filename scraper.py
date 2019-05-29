import csv
from bs4 import BeautifulSoup
from requests import get



def remove_unicode(string):
    #Used to remove unicode characters from the parsed data
    return (str(string).replace("\xa0",'').replace("\ufeff",'').replace('\\xa0',''))

def get_data(url):
    # Gets the content from the specified url
    resp = get(url, stream=True)
    return resp.content


def parser(content,element,class_name=None):
    """Parses content data from get_data function
    
    The type of HTML element and its respective class
    can be passed to the function to parse a different
    part of the HTML page
    """
    html_data = BeautifulSoup(content,'html.parser')
    return(html_data.find_all(element, class_=class_name))
    
def csv_formatter(data):
    #Formats data to be written to a csv file
    
    formatted_data = []
    for i in data:
        if '<th colspan="2">' in str(i): #Checks for the column with sq miles and sq kilometers to format the csv file
            formatted_data.append(i.text.strip()+',')
        else:
            formatted_data.append(remove_unicode(i.text.strip()))
    return formatted_data

def write_csv(data,file_name):
    #Writes data to a csv file
    #file_name parameter should have a .csv extension
    with open('file_name', mode='a+',encoding="utf-8-sig",newline='') as city_wiki:
        city_writer = csv.writer(city_wiki, delimiter=',',escapechar=' ',quoting=csv.QUOTE_NONE)
        city_writer.writerow(data)
        
def add_col(old_file,new_file,col_name):
    """Adds a new column to an existing csv file (returns a new file)
    
    old_file is the name of your existing csv flie
    new_file is the name of the new csv file with the new column
    col_name is the column name you wish to add
    """
    with open(old_file,'r',encoding="utf-8-sig") as no_add, open(new_file,'w',newline='',encoding="utf-8-sig") as additional_data:
        no_add_reader = list(csv.reader(no_add, delimiter=','))
        additional_writer = csv.writer(additional_data)
        first_row = no_add_reader[0]+[col_name] #Add a column for elevation
        additional_writer.writerow(first_row)
        for row in no_add_reader[1:len(no_add_reader)]:
            additional_writer.writerow(row)

def add_data(old_file,new_file,data):
    """Adds data to a new column to an existing csv file (returns a new file)
    
    old_file is the name of your existing csv file
    new_file is the name of the new csv file with the new column
    data is the name of the list with your new data
    """
    with open(old_file,'r',encoding="utf-8-sig") as no_add, open(new_file,'w',encoding="utf-8-sig",newline='') as additional_data:
        no_add_reader = list(csv.reader(no_add, delimiter=','))
        for index in range(1,len(data)):
            no_add_reader[index].append(data[index-1])
        additional_writer = csv.writer(additional_data)
        for row in no_add_reader:
            additional_writer.writerow(row)
            
            
#Get data from the link
data = parser(get_data("https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population"),'table'
              ,'wikitable sortable')

#Write the first row that contains the categorical variables
write_csv(csv_formatter(data[0].find_all('th')),'data.csv')


#Filter data by table
data2 = csv_formatter(data[0].find_all('td'))


#Process to get rid of commas and also get the data in a suitable csv format in a list
filtered_data = []
for index in range(0,len(data2),11):
    filtered_data += (data2[index:index+10] + [(data2[index+10].split('/')[1])])
    
for i in range(len(filtered_data)):
    filtered_data[i] = filtered_data[i].replace(',','')
    
#Write data to file
for index in range(0,len(data2),11):
    write_csv(filtered_data[index:index+11],'data.csv')
    
    
#Add elevation column as additional data
add_col('city wiki without additional data.csv','city wiki with additional data.csv','Elevation')


#Get each city's wikipedia url

data = parser(get_data("https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population"),'table'
              ,'wikitable sortable')

links = []
rows = data[0].find_all('tr')
for html in rows[1:len(rows)]:
    links.append(html.find('a',href=True).get('href'))

#Get elevation data
elevation = []
for link in links:
    page = parser(get_data("https://en.wikipedia.org"+link),'table','infobox geography vcard')
    for i in page:
        for x in i.find_all('tr',class_='mergedtoprow'):
            if 'Elevation' in x.text:
                elevation.append(remove_unicode(x.find('td').text))
                
#Add elevation data
add_data('city wiki with additional data.csv','city wiki with elevation data.csv',elevation)

