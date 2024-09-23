import requests

# Access token and user id (you must replace with your own)
access_token = "EAAHE670kfakBO1JaCzyHNUrYAkJ61GgJZCDCJ2ABeU8CqBx6F8VPXh0dGWWkEuc0GOt0mxIP78XUg2u58ZB5lzmlDEhMmPCb0S054Tl5gVgrf1etZCskQ7OvoetkxZAkZAftZCdfjTg8IsMGOoB6DJo52W8KQlHLfqV1OZASNLBORDe6V23gBZCSonAGNOXhzzvtGrtGRUVnDsVpDZAgjdp6p3fo44wZDZD"
user_id = "497991746354601"

# URL for posting a thread
url = f"https://graph.threads.net/v1.0/{user_id}/threads"

# Data for the post (you can modify this to suit your needs)
post_data = {
    "message": "This is my first post using the Threads API!"
}

# Headers including the access token for authorization
headers = {
    "Authorization": f"Bearer {access_token}"
}

# Make the API request to post the thread
response = requests.post(url, json=post_data, headers=headers)

# Check the response
if response.status_code == 200:
    print("Thread posted successfully:", response.json())
else:
    print("Failed to post thread:", response.status_code, response.text)
