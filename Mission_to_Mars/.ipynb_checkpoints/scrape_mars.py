def scrape():
    from bs4 import BeautifulSoup as bs
    import requests
    from splinter import Browser
    import pandas as pd
    import time

    mars_dict={}

    executable_path={'executable_path':"chromedriver.exe"}
    browser=Browser("chrome", **executable_path, headless=False)

    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    html = browser.html
    news_soup = bs(html, 'html.parser')
    title = news_soup.select_one('ul.item_list li.slide')
    title1 = title .find('div', class_='content_title').text

    paragraph = title.find('div', class_='article_teaser_body').text
    
    # JPL Image

    featured_image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(featured_image_url)

    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(5)
    browser.click_link_by_partial_text('more info')
    time.sleep(5)
    html=browser.html
    soup2=bs(html,'html.parser')
    
    mars_image=soup2.find('figure', class_='lede')
    mars_image2=mars_image.a["href"]
    mars_image2

    featured_image = 'https://www.jpl.nasa.gov'+ mars_image2

    # Mars Facts
    mars_facts_url='https://space-facts.com/mars/'

    tables = pd.read_html(mars_facts_url)[0]
    tables.columns=["Facts","Value"]


    #########
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    response = requests.get(url)
    soup = bs(response.text, 'html.parser').find_all("a",class_ = "itemLink product-item")
    hemi_titles = []
    for i in soup:
        title = i.find("h3").text
        link= i["href"]
        # or i.a["href"]
        hemi_titles.append(title)
        

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    
    hemi_imglist = []
    for x in range(len(hemi_titles)):
        try:
                browser.click_link_by_partial_text(hemi_titles[x])
        except:
                browser.find_link_by_text('2').first.click()
                browser.click_link_by_partial_text(hemi_titles[x])
        html = browser.html
        soup2 = bs(html, 'html.parser')
        hemi_soup = soup2.find('div', 'downloads')
        hemi_url = hemi_soup.a['href']
        #urls.append(hemi_url)
        hemi_dict={"title": hemi_titles[x], 'img_url': hemi_url}
        hemi_imglist.append(hemi_dict)
    


    mars_dict["news_title"]=title1
    mars_dict["paragraph"]=paragraph
    mars_dict["featured_image"]=featured_image
    mars_dict["facts_table"]=tables
    mars_dict["hemisphere"]=hemi_imglist

    return mars_dict



