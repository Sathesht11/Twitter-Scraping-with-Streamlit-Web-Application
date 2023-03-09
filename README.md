# Twitter-Scraping-with-Streamlit-Web-Application

## Problem Statement: 
Currently, data is dispersed throughout the entire planet. There may be a large amount of data on Facebook, Instagram, YouTube, Twitter, and other social media platforms. This includes images and videos on YouTube and Instagram as opposed to Facebook and Twitter. To uncover the genuine factual information on Twitter, we must scrape the data and then scrutinize the additional insight. In this project, I scraped data from Twitter such as (date, id, url, tweet text, user, reply count, retweet count, language, source, like count, and so on).

## Approach: 
* **Scraping** the Twitter data from the Twitter Reference using the "**snscrape**" Library.
* **Creating a dataframe** with the following fields: date, id, url, tweet content, user, reply count, retweet count, language, source, and like count.
* **Inserting** each collection of data in **Mongodb** as a document, along with the hashtag or key phrase used to scrape from Twitter.
e.g. ("Scraped Word" : "Elon Musk", "Scraped Date" : "15-02-2023", "Scraped Data" : [1000 Scraped data from the previous 100 days ]).
* **Building a streamlit GUI** with the feature for entering the keyword or Hashtag to be searched, 
   * Specifying the **date period**, and 
   * limiting the **number of tweets** to be scraped. 
   * Upon scraping, the dataframe should be presented on the page, 
   * With a **button to upload the sraped data to a MongoDB** database and, 
   * **Downloading** the data in **csv and json** format.

## Packages:
* snscrapre
* streamlit
* pandas
* pymongo
* streamlit_lottie
