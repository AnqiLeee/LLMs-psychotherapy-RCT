import os
import numpy as np
import pandas as pd
from datetime import datetime

group_time_gap_dict = {"novice_human": 2, "AI_50min": 2, "AI_anytime_anywhere": 2}

def convert_timestr_to_timestamp(timestr, pattern="%Y-%m-%d %H:%M:%S"):
    timestamp = datetime.strptime(timestr, pattern)
    return timestamp

def get_time_duration(time1, time2, duration_pattern="day"):
    if duration_pattern == "day":
        return (time2 - time1).days
    if duration_pattern == "hour":
        return (time2 - time1).seconds/3600 + (time2 - time1).days * 24
    if duration_pattern == "minute":
        return (time2 - time1).seconds/60 + (time2 - time1).days * 24 * 60
    if duration_pattern == "second":
        return (time2 - time1).seconds + (time2 - time1).days * 24 * 60 * 60

def get_group_conversations(datapath, group_name):
    time_gap = group_time_gap_dict[group_name]
    group_conversations = {}
    all_filenames = [f for f in os.listdir(datapath) if f.startswith(group_name) and f.endswith(".xlsx")]
    for filename in all_filenames:
        conversation_df = pd.read_excel(os.path.join(datapath, filename))[::-1]  # df按照消息时间列从前到后进行排列
        conversations = []
        conversation = []
        last_timestamp = ""

        for idx, row in conversation_df.iterrows():
            # print(row)
            user_id = row.get("用户Id")
            message_content = row.get("消息内容")
            speaker = row.get("发送方")

            time_str = row.get("消息时间")
            timestamp = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')

            if not last_timestamp:
                conversation = [(time_str, speaker, message_content)]
            elif get_time_duration(last_timestamp, timestamp, "hour") >= time_gap:
                conversations.append(conversation)
                conversation = [(time_str, speaker, message_content)]
            else:
                conversation.append((time_str, speaker, message_content))

            last_timestamp = timestamp
            # print(message_content, timestamp)
        if conversation:
            conversations.append(conversation)
        group_conversations[user_id] = conversations
    return group_conversations

def get_avg_duration_and_messages(user2conversations):
    all_durations = []
    all_messages = []
    for user_id, conversations in user2conversations.items():
        for conv_id, conversation in enumerate(conversations):
            messages_sent_by_patient = sum([1 for _, speaker, _ in conversation if speaker == "用户"])
            last_time, first_time = convert_timestr_to_timestamp(conversation[-1][0]), convert_timestr_to_timestamp(conversation[0][0])
            # print(f"{first_time} ~ {last_time}")
            duration_minutes = get_time_duration(first_time, last_time, duration_pattern="minute")
            all_durations.append(duration_minutes)
            all_messages.append(messages_sent_by_patient)
    print(f"duration: avg={"%0.2f"%np.average(all_durations)} mins, std={"%0.2f"%np.std(all_durations)}, median={"%0.2f"%np.median(all_durations)} mins, min={"%0.2f"%np.min(all_durations)} mins, max={"%0.2f"%np.max(all_durations)} mins")
    print(f"messages sent by patients: avg={"%0.2f"%np.average(all_messages)}, std={"%0.2f"%np.std(all_messages)}, median={"%0.2f"%np.median(all_messages)}, min={np.min(all_messages)}, max={np.max(all_messages)}")


# statistics: avg.duration and exchange messages of conversations
if __name__ == "__main__":
    datapath = "conversation_data/"
    for group_name in group_time_gap_dict:
        print(group_name)
        group_conversations = get_group_conversations(datapath, group_name)
        get_avg_duration_and_messages(group_conversations)
        print("\n")












