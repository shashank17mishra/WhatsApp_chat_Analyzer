import pandas as pd
import re
def preprocess(data):
    # Split into lines
    lines = data.split("\n")

    pattern = r'^(\d{1,2}/\d{1,2}/\d{2}),\s(\d{1,2}:\d{2}\s?[ap]m)\s-\s([^:]+):\s(.*)'

    messages = []
    current_message = None

    for line in lines:
        match = re.match(pattern, line)

        if match:
            # If new message starts, save previous
            if current_message:
                messages.append(current_message)

            current_message = {
                "Date": match.group(1),
                "Time": match.group(2),
                "Sender": match.group(3),
                "Message": match.group(4)
            }
        else:
            # Multiline message continuation
            if current_message:
                current_message["Message"] += " " + line

    # Append last message
    if current_message:
        messages.append(current_message)

    # Convert to DataFrame
    df = pd.DataFrame(messages)

    df["DateTime"] = pd.to_datetime(
        df["Date"] + " " + df["Time"],
        format="%d/%m/%y %I:%M %p"
    )
    df['year'] = df['DateTime'].dt.year
    df['month'] = df['DateTime'].dt.month_name()
    df['day'] = df['DateTime'].dt.day
    df['hour'] = df['DateTime'].dt.hour
    df['minute'] = df['DateTime'].dt.minute
    df["month_num"]=df['DateTime'].dt.month
    df['date_']=df['DateTime'].dt.date
    df["Day_name"] = df["DateTime"].dt.day_name()
    return df