
# coding: utf-8

# # Facebook Message Analyzer

# <b> Current Features For a Given Chat: </b>
# <ul> 
#     <li> Number of Messages Sent </li> 
#     <li> Messages Sent Over Time </li> 
#     <li> Average Word Count </li>
# </ul>

# In[5]:


import os
import json
import numpy as np
import pylab as pl
import datetime

CURRENT_DIRECTORY = os.getcwd()
NUMBER_TO_ANALYZE = 20
MESSAGE_THRESHOLD = 10
MESSAGE_BOUND = 100000000
NAME = "Sheldon Tan"


# In[6]:


def get_json_data(chat):
    try:
        json_location = CURRENT_DIRECTORY + "/messages/" + chat + "/message_1.json"
        with open(json_location) as json_file:
            json_data = json.load(json_file)
            return json_data
    except IOError:
        pass # some things the directory aren't messages (DS_Store, stickers_used, etc.)


# In[7]:


chats = os.listdir(CURRENT_DIRECTORY + "/messages/")[:NUMBER_TO_ANALYZE]
sorted_chats = []
final_data_messages = {}
final_data_times = {}
final_data_words = {}
invalid_message_count = 0


# In[9]:


print('Analyzing ' + str(min(NUMBER_TO_ANALYZE, len(chats))) + ' chats...')

for chat in chats:
    url = chat + '/message_1.json'
    json_data = get_json_data(chat)
    print(chat)
    if json_data != None:
        messages = json_data["messages"]
        if len(messages) >= MESSAGE_THRESHOLD and len(messages) <= MESSAGE_BOUND:
            total = len(messages)
            message_dict = {}
            message_time_dict = {}
            time_dict = {}
            time_ratio_dict = {}
            current_time = 0
            past_time = 0
            time = 0
            word_dict = {}
            for message in messages:
                person = message["sender_name"]
                if person in message_dict:
                    message_dict[person] += 1
                else:
                    message_dict[person] = 1

                if current_time != 0:
                    past_time = current_time
                current_time = message["timestamp_ms"]
                if past_time != 0:
                    time = past_time - current_time
                if time != 0 and time < 1000 * 60 * 60 * 24 * 2:
                    if person in time_dict:
                        time_dict[person] += time
                    else:
                        time_dict[person] = time
                    if person in message_time_dict:
                        message_time_dict[person] += 1
                    else:
                        message_time_dict[person] = 1
                if "content" in message:
                    content = message["content"]
                    words = content.split()
                    for word in words:
                        lower_word = word.lower()
                        if lower_word in word_dict:
                            word_dict[lower_word] += 1
                        else:
                            word_dict[lower_word] = 1
            for person in time_dict:
                time_ratio_dict[person] = time_dict[person]/(1000 * 60 * message_time_dict[person])
# {'sender_name': 'Glen Lim', 'timestamp_ms': 1534827208419, 'content': 'I plucked Friday afternoon', 'type': 'Generic'}

                
            sorted_chats.append((total, chat, messages, message_dict, time_ratio_dict, word_dict))

sorted_chats.sort(reverse=True)

print('Finished processing chats...')


# In[10]:


for i, (total, chat, messages, message_dict, time_ratio_dict, word_dict) in enumerate(sorted_chats):
    number_messages = {}
    person_to_times = {}
    number_words = {}
    if NAME in message_dict:
        my_ratio = message_dict[NAME]*100/total
    else:
        my_ratio = 0
    if NAME in time_ratio_dict:
        my_time = time_ratio_dict[NAME]
    else:
        my_time = 0
    chat_name = ""
    for char in chat:
        if char != "_":
            chat_name += char
        else:
            break
    max_word_1 = max(word_dict, key = word_dict.get)
    max_value_1 = word_dict[max_word_1]
    temp = word_dict.pop(max_word_1)
    max_word_2 = max(word_dict, key = word_dict.get)
    max_value_2 = word_dict[max_word_2]
    temp = word_dict.pop(max_word_2)
    max_word_3 = max(word_dict, key = word_dict.get)
    max_value_3 = word_dict[max_word_3]
    temp = word_dict.pop(max_word_3)
    max_word_4 = max(word_dict, key = word_dict.get)
    max_value_4 = word_dict[max_word_4]
    temp = word_dict.pop(max_word_4)
    max_word_5 = max(word_dict, key = word_dict.get)
    max_value_5 = word_dict[max_word_5]
    temp = word_dict.pop(max_word_5)
    

    print(str(i+1) + " - " + str(chat_name) + ": " + str(total) + " messages; My message ratio: " + str(my_ratio) + "%; My average messaging delay: " + str(my_time) + "mins; 5 most frequent words used: " + str(max_word_1) + " : " + str(max_value_1) + ", " + str(max_word_2) + " : " + str(max_value_2) + ", " + str(max_word_3) + " : " + str(max_value_3) + ", " + str(max_word_4) + " : " + str(max_value_4) + ", " + str(max_word_5) + " : " + str(max_value_5) + ", ")

    for message in messages:
        try:
            name = message["sender_name"]
            time = message["timestamp_ms"]
            message_content = message["content"]

            number_messages[name] = number_messages.get(name, 0)
            number_messages[name] += 1

            person_to_times[name] = person_to_times.get(name, [])
            person_to_times[name].append(datetime.datetime.fromtimestamp(time/1000.0))

            number_words[name] = number_words.get(name, [])
            number_words[name].append(len(message_content.split()))
        except KeyError:
            # happens for special cases like users who deactivated, unfriended, blocked
            invalid_message_count += 1

    final_data_messages[i] = number_messages
    final_data_times[i] = person_to_times
    final_data_words[i] = number_words

print('Found ' + str(invalid_message_count) + ' invalid messages...')
print('Found ' + str(len(sorted_chats)) + ' chats with ' + str(MESSAGE_THRESHOLD) + ' messages or more')

def word_analysis(i, top_n_words):
    total, chat, messages, message_dict, time_ratio_dict, word_dict = sorted_chats[i]
    sorted_word_dict = sorted(word_dict.items(), key = lambda item: -item[1])
    return sorted_word_dict[:top_n_words]

print(word_analysis(1, 20))

# In[12]:


def plot_num_messages(chat_number):
    plotted_data = final_data_messages[chat_number]
    X = np.arange(len(plotted_data))
    pl.bar(X, list(plotted_data.values()), align='center', width=0.5, color = 'r', bottom = 0.3)
    pl.xticks(X, plotted_data.keys(), rotation = 90)
    pl.title('Number of Messages Sent')
    pl.tight_layout()
    pl.show()
    
def plot_histogram_time(chat_number):
    person_to_times = final_data_times[chat_number]
    pl.xlabel('Time')
    pl.ylabel('Number of Messages')
    pl.title('# of Messages Over Time')
    colors = ['b', 'r', 'c', 'm', 'y', 'k', 'w', 'g']
    for i , person in enumerate(person_to_times):
        plotted_data = person_to_times[person]
        pl.hist(plotted_data, 100, alpha=0.3, label=person, facecolor=colors[i % len(colors)])
    pl.legend()
    pl.xticks(rotation=90)
    pl.tight_layout()
    pl.show()

def plot_histogram_words(chat_number):
    temp = {}
    for person in final_data_words[chat_number]:
        temp[person] = np.average(final_data_words[chat_number][person])
    plotted_data = temp
    X = np.arange(len(plotted_data))
    pl.bar(X, list(plotted_data.values()), align='center', width=0.5, color = 'r', bottom = 0.3)
    pl.xticks(X, plotted_data.keys(), rotation = 90)
    pl.title('Average Word Count')
    pl.tight_layout()
    pl.show()
    
def plot(number1,number2):
    for chat_number in range(number1, number2):
        plot_num_messages(chat_number)
        plot_histogram_time(chat_number)
        plot_histogram_words(chat_number)

# In[ ]:
# plot(35,36)

# Insights:
# I was surprised to find that the total counts of my top individual chats were higher than those of my top group chats. This seems to imply that even though the group chats are used by more people and seemingly more frequently, the conversations I have in my top individual chats tend to be longer and in more depth, resulting in a greater count of messages.
# I also found it interesting that in almost all of my individual chats, my message ratio was less than 50%. This could be because I talk less than the people I message with, or because my messages are denser. 
# I noticed that my average messaging delay is somewhat significantly less for my top individual chats. This could be because I prioritize responding to these messages more, or simply because we often have longer conversations through messenger that result in close to immediate response times.
# I found that my most commonly used words in my messages did not really change depending on the person I was messaging or our relative message count. The most common words, throughout my chats, tended to be I, the, to, u, you, like, and, lol.
