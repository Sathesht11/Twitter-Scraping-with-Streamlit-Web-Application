import streamlit as st
import snscrape.modules.twitter as sntwitter
import pandas as pd
import pymongo
import json
import requests
from streamlit_lottie import st_lottie

# Header or Title of the page
st.markdown("<h1 style='text-align: center; color: yellow;'>Twitter Web Scrapping</h1>", unsafe_allow_html=True)

def load_lottieURl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


lottie_bird = load_lottieURl("https://assets10.lottiefiles.com/packages/lf20_nkf5e15x.json")

st_lottie(lottie_bird, height=300, width=700, key='bird')

hashtag = st.text_input('Enter your Hashtag:')
startDate = st.date_input("Enter starting time:")
endDate = st.date_input("Enter ending time:")
noOfTweet = st.number_input('Enter the no. of tweets you want:')


# ----------------------------------Scraping the Twitter Data---------------------------------------------------
def scrapeTwitterData(hashtag, startDate, endDate, noOfTweet):
    scraper = sntwitter.TwitterSearchScraper(
        f"#{hashtag} since:{startDate} until:{endDate}")

    tweets = []

    for i, tweet in enumerate(scraper.get_items()):
        data = [tweet.date,
                tweet.id,
                tweet.url,
                tweet.content,
                tweet.user.username,
                tweet.replyCount,
                tweet.retweetCount,
                tweet.lang,
                tweet.source,
                tweet.likeCount]
        tweets.append(data)
        if i >= noOfTweet-1:
            break

    tweet_df = pd.DataFrame(tweets,
                            columns=['Date', 'ID', 'URL', 'Content',
                                     'UserName', 'ReplyCount', 'ReTweetCount',
                                     'Language', 'Source', 'LikeCount'])

    return tweet_df


# -------------------------------Uploading Data to Mongo DB--------------------------------------------------------
def uploadDataToMDB(tweet_df):
    # convert dataframe into documents
    dataToMDB = tweet_df.to_dict('records')
    # Here, I took the keyword 'Scraped'
    tweet_data = []
    for i in range(len(dataToMDB)):
        data = {}
        for key, val in dataToMDB[i].items():
            data[f"Scraped {key}"] = val
        tweet_data.append(data)

    # Storing scrapped data to MongoDB
    # you can replace your own password in *****
    connString = 'mongodb://sathesht11:********@ac-pdkcaeq-' \
                 'shard-00-00.p3oqjnt.mongodb.net:27017,ac-' \
                 'pdkcaeq-shard-00-01.p3oqjnt.mongodb.net:27017,' \
                 'ac-pdkcaeq-shard-00-02.p3oqjnt.mongodb.net:' \
                 '27017/?ssl=true&replicaSet=atlas-jw3sl9-shard-' \
                 '0&authSource=admin&retryWrites=true&w=majority'
    conn = pymongo.MongoClient(connString)
    db = conn['Twitter']
    coll = db['scraped_tweets']
    coll.insert_many(tweet_data)


# ------------------------------------Buttons-----------------------------------------------------------------------
enter_btn = st.button('Enter')

if st.session_state.get('button') != True:
    st.session_state['button'] = enter_btn  # Saved the state

if st.session_state['button'] == True:
    tweet_df = scrapeTwitterData(hashtag, startDate, endDate, noOfTweet)
    st.dataframe(tweet_df)

    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        if st.button('Upload to MongoDB'):
            uploadDataToMDB(tweet_df)
            st.write('You have successfully uploaded the twitter scraped data to MongoDB!!!')


    def convert_csv(df):
        return df.to_csv(index=False).encode("utf-8")


    csv = convert_csv(tweet_df)

    with col2:
        st.download_button(
            label="Download as CSV",
            data=csv,
            file_name="Twitter_data.csv",
            mime="text/csv",
        )

    jsonFile = tweet_df.to_json(orient="records")

    with col3:
        st.download_button(
            label='Download as Json',
            data=jsonFile,
            file_name="twitter_json.json",
            mime="text/json",
        )

# -------------------------------Buttons------------------------------------------------------------
