from urlextract import  URLExtract
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import re
import emoji
#import matplotlib.pyplot as plt
import plotly.express as px
extract=URLExtract()
def fetch_stats(selected_user,df):
    if selected_user!="Overall" :
        df = df[df["Sender"] == selected_user]
    # Number of messages
    num_msg = df.shape[0]
    # number of words
    word = []
    for i in df["Message"]:
        word.extend(i.split())
    #fetch number of media in chats
    num_media=df[df["Message"]=="<Media omitted>"].shape[0]
    #fetch number of links
    links=[]
    for i in df["Message"]:
        links.extend(extract.find_urls(i))
    return num_msg, len(word),num_media,len(links)


def most_busy_sender(df):
    x=df["Sender"].value_counts().head()
    name=x.index
    count=x.values
    return name,count

def msg_sender_p(df):
    y=round(df["Sender"].value_counts()/df.shape[0]*100,2).reset_index().rename(columns={'index':'name',"Sender":"percent"})

    return y
#wordclod
def cr_wordcloud(selected_user, df):

    if selected_user != "Overall":
        df = df[df["Sender"] == selected_user]

    # Remove media messages
    df = df[df["Message"] != "<Media omitted>"]

    # Join all messages
    text = df["Message"].dropna().str.cat(sep=" ")

    # Check if text is empty
    if not text.strip():
        return None

    wc = WordCloud(width=500, height=500, background_color="white")
    df_wc = wc.generate(text)

    return df_wc



def word_counter(selected_user,df):
    if selected_user != "Overall":
        df = df[df["Sender"] == selected_user]

    # Remove media messages
    df = df[df["Message"] != "<Media omitted>"]

    # Remove group notifications (if column exists)
    if "Sender" in df.columns:
        df = df[df["Sender"] != "group_notification"]

    # Basic English stopwords
    stop_words = {
    # Basic verbs / helpers
    "hai","ho","hun","hoon","tha","thi","the","hoga","hogi","honge","raha","rahi","rahe",
    "hua","hui","hue","kar","kara","kare","karo","karna","karne","karta","karti","karte",
    "kiya","kiye","ki","ke","ka","diya","di","deta","deti","dete","liya","liye","leta",
    "leti","lete","mil","mila","mile","milta","milti","milte","jata","jati","jate","jaa",
    "ja","gaya","gayi","gaye","aaya","aayi","aaye","aa","ana","aana","hona","hota","hoti",
    "hote","rakha","rakhi","rakhe","rakh","rakhna","de","do","dena","deni","dene",

    # Pronouns
    "main","me","mai","mein","m","hum","ham","hamara","hamari","hamare",
    "mera","meri","mere","tera","teri","tere","tum","tumhara","tumhari","tumhare",
    "aap","aapka","aapki","aapke","tu","tera","teri","ye","yeh","yah","wo","woh",
    "is","us","in","un","inka","unki","iske","uske","inko","unko",

    # Connectors
    "aur","or","par","per","lekin","magar","kyunki","toh","to","fir","phir",
    "jab","tab","agar","warna","balki","ya","yaa","kyu","kyun","kya","kaise",
    "kab","kahan","kaha","kaun","kitna","kitni","kitne",

    # Fillers
    "na","haan","haa","han","hmm","hm","achha","acha","accha","ok","okay","okk",
    "bro","bhai","yaar","arey","arre","abe","chal","chalo","bas","sirf","hi","bhi",
    "matlab","waise","vaise","shayad","maybe","actually","literally","seriously",
    "sach","sahi","galat","theek","thik","bilkul","pakka","jarur","zarur",

    # Chat short forms
    "h","hn","ha","nhi","nahi","ni","mt","kr","k","b","fr","plz","pls",
    "btw","lol","lmao","rofl","omg","idk","ikr","bt","gm","gn","tc",

    # Common conversational
    "ab","abhi","pehle","baad","baadme","baadmein","andar","bahar","upar","neeche",
    "idhar","udhar","waha","yaha","yahaan","wahaan","har","koi","kuch","sab","sabhi",
    "alag","saath","sath","andar","bahut","bohot","zyada","jada","kam","thoda","thodi",
    "itna","utna","aisa","waisa","aisi","waisi","aise","waise","apna","apni","apne",
    "dusra","dusri","dusre","pe","se","tak","liye","liyehi","wala","wali","wale",

    # Emotional fillers
    "uff","are","arre","oho","acha","haye","wah","wow","hehe","haha","hahaha",
    "lolz","hehehe","hmmm","hmmmm","oh","oye","sun","suno",

    # Time words
    "kal","aaj","raat","din","subah","shaam","jaldi","late","abtak","tabtak",

    # Agreement / reaction
    "haanji","ji","jiha","right","correct","yes","no","nah","nope","yup","yess",
    "okies","done","fine","cool","great","nice","good",

    # Question casual
    "ky","kyo","kyu","kyun","kaisa","kaisi","kaise","kabhi","kahin",

    # Misc common chat words
    "bhaiya","didi","sir","madam","uncle","aunty","beta","bhaii","yaara",
    "bc","mc","abe","arey","sunna","sunana","bol","bolo","bolna","bata",
    "batao","batana","samajh","samjha","samjho","lag","laga","lage","lagta",
    "lagti","lagte","chahiye","chalega","chaliye","ruk","rukna","rukja","rukjao",
    "nikal","niklo","nikalna","aao","jao","jaana","aana","reh","rehna","rehne",
    "rehte","rehna","rehraha","rehrahi","rehrahe",

    # English filler commonly mixed
    "just","only","even","also","because","but","so","though","still",
    "very","much","more","most","some","any","all","each","every",
    "can","could","should","would","will","shall","may","might","must",

    # Extra frequent WhatsApp tokens
    "msg","message","call","video","pic","photo","dp","status",
    "group","admin","link","send","sent","forward","fwd"
    }

    words = []

    for message in df["Message"]:
        # remove links
        message = re.sub(r"http\S+", "", message)

        # remove punctuation & make lowercase
        message = re.sub(r"[^\w\s]", "", message).lower()

        for word in message.split():
            if word not in stop_words and len(word) > 2:
                words.append(word)

    # Count top 20
    most_common = Counter(words).most_common(20)

    return pd.DataFrame(most_common, columns=["Word", "Frequency"])

def emoji_f(selected_user,df):
    if selected_user != "Overall":
        df = df[df["Sender"] == selected_user]
    emoji_list = []

    for message in df["Message"]:
        emoji_list.extend([e['emoji'] for e in emoji.emoji_list(message)])

    emoji_df = pd.DataFrame(
        Counter(emoji_list).most_common(),
        columns=["Emoji", "Frequency"]
    )

    return emoji_df


def emoji_plotly_chart(selected_user, df):

    if selected_user != "Overall":
        df = df[df["Sender"] == selected_user]

    emoji_list = []

    for message in df["Message"]:
        emoji_list.extend([e['emoji'] for e in emoji.emoji_list(str(message))])

    if len(emoji_list) == 0:
        return None

    emoji_freq = Counter(emoji_list).most_common(10)

    emojis = [i[0] for i in emoji_freq]
    counts = [i[1] for i in emoji_freq]

    fig = px.bar(
        x=counts,
        y=emojis,
        orientation='h',
        title="Top Emojis",
    )

    return fig

#finding most active month and year
def m_a_month(selected_user, df):

    if selected_user != "Overall":
        df = df[df["Sender"] == selected_user]

    timeline = df.groupby(
        ['year', 'month_num', 'month']
    ).count()['Message'].reset_index()

    timeline = timeline.sort_values(['year', 'month_num'])

    # Create proper datetime column
    timeline['time'] = pd.to_datetime(
        timeline['year'].astype(str) + "-" +
        timeline['month_num'].astype(str) + "-01"
    )

    return timeline

#daily
def daily_timeline(selected_user, df):

    if selected_user != "Overall":
        df = df[df["Sender"] == selected_user]

    daily = df.groupby("date_").count()["Message"].reset_index()

    daily = daily.sort_values("date_")

    return daily

def most_active_day(selected_user, df):

    if selected_user != "Overall":
        df = df[df["Sender"] == selected_user]

    day_activity = df["Day_name"].value_counts().reset_index()
    day_activity.columns = ["Day", "Message"]

    # Proper weekday order
    order = ["Monday", "Tuesday", "Wednesday",
             "Thursday", "Friday", "Saturday", "Sunday"]

    day_activity["Day"] = pd.Categorical(day_activity["Day"],
                                         categories=order,
                                         ordered=True)

    day_activity = day_activity.sort_values("Day")

    return day_activity


def most_active_month(selected_user, df):

    if selected_user != "Overall":
        df = df[df["Sender"] == selected_user]

    month_activity = df.groupby(
        ["month", "month_num"]
    ).count()["Message"].reset_index()

    month_activity = month_activity.sort_values("month_num")

    return month_activity

def generate_pdf(stats):

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer)

    elements = []
    styles = getSampleStyleSheet()

    elements.append(Paragraph("WhatsApp Chat Analytics Report", styles["Title"]))
    elements.append(Spacer(1, 0.5 * inch))

    data = [
        ["Metric", "Value"],
        ["Total Messages", stats[0]],
        ["Total Words", stats[1]],
        ["Media Shared", stats[2]],
        ["Links Shared", stats[3]],
    ]

    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0),colors.grey),
        ('GRID',(0,0),(-1,-1),1,colors.black)
    ]))

    elements.append(table)

    doc.build(elements)
    buffer.seek(0)
    return buffer

def monthly_animation(selected_user, df):

    if selected_user != "Overall":
        df = df[df["Sender"] == selected_user]

    df["Year"] = df["DateTime"].dt.year
    df["Month"] = df["DateTime"].dt.month_name()

    anim = df.groupby(["Year", "Month"]).size().reset_index(name="Message")

    return anim

def activity_heatmap(selected_user, df):

    if selected_user != "Overall":
        df = df[df["Sender"] == selected_user]

    df["Hour"] = df["DateTime"].dt.hour
    df["Day"] = df["DateTime"].dt.day_name()

    heatmap = df.groupby(["Day", "Hour"]).size().reset_index(name="Message")

    # Proper weekday order
    order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    heatmap["Day"] = pd.Categorical(heatmap["Day"], categories=order, ordered=True)
    heatmap = heatmap.sort_values("Day")

    pivot = heatmap.pivot(index="Day", columns="Hour", values="Message").fillna(0)

    return pivot

from textblob import TextBlob


def sentiment_analysis(selected_user, df):

    if selected_user != "Overall":
        df = df[df["Sender"] == selected_user]

    sentiments = []

    for message in df["Message"]:
        try:
            polarity = TextBlob(str(message)).sentiment.polarity
        except:
            polarity = 0
        sentiments.append(polarity)

    df = df.copy()
    df["Sentiment"] = sentiments

    # Labeling
    def label(p):
        if p > 0:
            return "Positive"
        elif p < 0:
            return "Negative"
        else:
            return "Neutral"

    df["Sentiment_Label"] = df["Sentiment"].apply(label)

    sentiment_counts = df["Sentiment_Label"].value_counts().reset_index()
    sentiment_counts.columns = ["Sentiment", "Count"]

    return df, sentiment_counts

def sentiment_timeline(selected_user, df):

    df_sent, _ = sentiment_analysis(selected_user, df)

    df_sent["date_only"] = df_sent["DateTime"].dt.date

    timeline = df_sent.groupby(
        ["date_only", "Sentiment_Label"]
    ).size().reset_index(name="Count")

    return timeline