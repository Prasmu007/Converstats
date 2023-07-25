
import matplotlib.pyplot as plt
import pylab as pl
import streamlit as st
import preprocesser, helper
import seaborn as sns
st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a File")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocesser.preprocess(data)

    st.dataframe(df)

    ## fetching unique users

    # fetch unique users

    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")
    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)

    if st.sidebar.button("Show Analysis"):
        num_messages, words, media_mess, links = helper.fetch_stats(selected_user, df)
        st.title("Top Statistics:")
        col1, col2, col3, col4 = st.columns([5, 5, 5, 1])


        with col1:
            st.subheader("Total_Messages:")
            st.header(num_messages)
        with col2:
            st.subheader("Total_Words:")
            st.header(words)
        with col3:
            st.subheader("Media_items:")
            st.header(media_mess)
        with col4:
            st.subheader("Links:")
            st.header(links)
        ## Monthly chat
        st.title("Monthly Chat Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        plt.plot(timeline['time'], timeline['message'], color = 'red')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        ## Daily Timeline

        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='violet')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        ## activity map
        st.title("Weekly Activity Map")
        col1, col2 = st.columns(2)
        with col1:
            st.header("Most busy day")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color = 'green')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.header("Most busy Month")
            busy_month = helper.monthly_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='violet')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)






        ## Finding the Busiest user in the group {only for group level)

        if selected_user == 'Overall':
            st.title('Most Busy Users')
            x, new_df= helper.most_busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns([5,5])
            with col1:
                ax.bar(x.index, x.values, color = 'blue')
                plt.xticks(rotation = 'vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        ## word cloud
            st.title("Word Cloud")
            df_wc = helper.word_cloud(selected_user, df)
            fig, ax = plt.subplots()
            ax.imshow(df_wc)
            st.pyplot(fig)
        ## most common used words
        st.title("Most Commonly Used Words")
        most_common_df = helper.commonly_words(selected_user, df)
        fig, ax = plt.subplots()
        plt.xticks(rotation='vertical')
        ax.barh(most_common_df[0], most_common_df[1])
        st.pyplot(fig)

        ## Emoji Analysis
        ## time line

        ## Daily time activity map
        st.title("Weekly Activity Time-zone")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)







