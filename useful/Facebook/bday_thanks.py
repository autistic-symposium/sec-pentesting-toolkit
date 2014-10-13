#!/usr/bin/env python

#Dont forget to install the facebook python SDK


import facebook
import json
import os
import random
from time import sleep

FB_ACCESS_TOKEN = # you need to set this

access_token = os.getenv('FB_ACCESS_TOKEN')


# Define  message
thankyou_messages = [
    'Thank you!',
    'Thanks!',
    'Thank you! I appreciate it!!!'
]

#  "birthday" query
birthday_fql = ("SELECT post_id, actor_id, target_id, created_time, message, comments "
                "FROM stream "
                "WHERE source_id = me() "
                    "AND filter_key = 'others' "
                    "AND created_time > 1391346000 "
                    "AND actor_id != me() "
                    "AND comments.count = 0 "
                    "AND comments.can_post = 1 "
                    "AND (strpos(message, 'birthday') >= 0 "
                        "OR strpos(message, 'Birthday') >= 0 "
                        "OR strpos(message, 'happy') >= 0 "
                        "OR strpos(message, 'Happy') >= 0) "
                "LIMIT 500")

# new GraphAPI instance with our access token
graph = facebook.GraphAPI(access_token)

# birthday posts using our FQL query
query_result = graph.get_object('fql', q=birthday_fql)

# data from the response
birthday_posts = query_result['data']

# how many posts
print'Query returned: ', len(birthday_posts)

# loop through returned posts
for post in birthday_posts:
    post_id = post['post_id']
    graph.put_object(post_id, 'likes')
    rand_message = random.choice(thankyou_messages)
    graph.put_object(post_id, 'comments', message=rand_message)
    print 'The like/comment should have posted for post', post_id
    sleep(0.1) # tenth of a second

print('Done!'')