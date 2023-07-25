from urlextract import URLExtract
import pandas as pd
import emoji
from collections import Counter
extractor = URLExtract()
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def fetch_stats(selected_user, df):
    if selected_user == 'Overall':
        df = df  # Use the original dataframe
    else:
        df = df[df['user'] == selected_user]
        # 1 fetching the number of messages
    num_messages = df.shape[0]

        # 2 fetching the number of words
    words = []
    for message in df['message']:
        words.extend(message.split())
     ## fetch number of media messages

    media_mess = df[df['message']=='<Media omitted>\n'].shape[0]

    ## fetching links
    links = []
    for message in df['message']:
        links.extend(extractor.find_urls(message))

    return num_messages, len(words), media_mess, len(links)
def most_busy_users(df):
    x = df['user'].value_counts().head()
    new_df = round((df['user'].value_counts().head()/df.shape[0])*100, 2).reset_index().rename(columns={'index': 'name','user': 'percentage'})
    return x, new_df
## word cloud
# def word_cloud(selected_user, df):
#     if selected_user == 'Overall':
#         df = df  # Use the original dataframe
#     else:
#         df = df[df['user'] == selected_user]
#     wc = WordCloud(width=550, height=550, min_font_size=10, background_color='pink')
#     df_wc = wc.generate(df['message'].str.cat(sep=" "))
#
#     return df_wc
def word_cloud(selected_user, df):


    if selected_user == 'Overall':
        temp = df
    else:
        temp = df[df['user'] == selected_user]



    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']



    # Concatenate messages into a single string
    # messages = filtered_df['message'].str.cat(sep=' ')
    def remove_stop_words(message):
        y =[]
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    wc = WordCloud(width=550, height=550, min_font_size=10, background_color='pink')
    temp ['message']= temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc
# def commonly_words(selected_user, df):
#     if selected_user == 'Overall':
#         df = df  # Use the original dataframe
#     else:
#         df = df[df['user'] == selected_user]
#         temp = df[df['user'] != 'group_notification']
#         temp = temp[temp['message'] != '<Media omitted>\n']
#
#         f = open('stop_hinglish.txt', 'r')
#         stop_words = f.read()
#
#         words = []
#         for message in temp['message']:
#             for word in message.lower().split():
#                 if word not in stop_words:
#                     words.append(word)
#
#         most_common_df = pd.DataFrame(Counter(words).most_common(20))
#         return most_common_df

def commonly_words(selected_user, df):
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>']


    if selected_user == 'Overall':
        temp = df
    else:
        temp = df[df['user'] == selected_user]



    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    commonwords = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                commonwords.append(word)

    most_common_df = pd.DataFrame(Counter(commonwords).most_common(20))
    return most_common_df

# def emoji_help(selected_user, df):
#     if selected_user == 'Overall':
#         temp = df
#     else:
#         temp = df[df['user'] == selected_user]
#
#     emojis = []
#     for message in df['message']:
#         emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])

def monthly_timeline(selected_user, df):
    if selected_user == 'Overall':
        df = df
    else:
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    timeline['time'] = time

    return timeline

## daily timeline graph

def daily_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline
## activity map

def week_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

def monthly_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()

## activity map

def activity_heatmap(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index = 'day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_heatmap














