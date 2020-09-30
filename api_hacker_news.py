import requests
import plotly.graph_objects as go
from datetime import datetime

# make an API call & store the response
# googling: "hacker news + api" results in a GitHub page. HackerNews has parterned with FirebaseIO to provide an API solution
# API guide: https://github.com/HackerNews/API/blob/master/README.md
# it wasn't possible to open the json file and immediately determine underlying structure; a single file was assumed.  A single JSON file was found for each page which led to some confusion.

url = 'https://hacker-news.firebaseio.com/v0/topstories.json'
r = requests.get(url)
# print(r.text)
print(f"Status code: {r.status_code}")
submission_ids = r.json()
# print(submission_ids)


# Process results
submission_dicts, time = [], []
for submission_id in submission_ids[:30]:
    # make a separate API call for each of the first 30 stories submitted
    url = f"https://hacker-news.firebaseio.com/v0/item/{submission_id}.json"
    r = requests.get(url)
    print(f"ID: {submission_id}\tStatus: {r.status_code}")
    response_dict = r.json()
    print(response_dict)


    # build a dictionary for each article (with a different json file)
    try:
        submission_dict = {
            'title': response_dict['title'],
            'hn_link': f"http://news.ycombinator.com/item?id={submission_id}",
            'comments': response_dict['descendants'],
            'score': response_dict['score'],
            'time': response_dict['time'],
            'author': response_dict['by'],
        }
    except KeyError:
        print("A KeyError exception has occured.")
    else:
        submission_dict = {
            'title': response_dict['title'],
            'hn_link': f"http://news.ycombinator.com/item?id={submission_id}",
            'comments': response_dict['descendants'],
            'score': response_dict['score'],
            'time': response_dict['time'],
            'author': response_dict['by'],
        }

    dt_object = datetime.fromtimestamp(submission_dict['time'])
    time.append(dt_object)
    submission_dicts.append(submission_dict)

submission_dicts = sorted(submission_dicts, key= lambda i: i['score'], reverse=True)


for submission_dict in submission_dicts:
    print(f"\nTitle : {submission_dict['title']}")
    print(f"URL     : {submission_dict['hn_link']}")
    print(f"Comments: {submission_dict['comments']}")
    print(f"Score   : {submission_dict['score']}")
    print(f"Author   : {submission_dict['author']}")

# Make Visualization

# https://plotly.com/python/bar-charts/ used as guidance

xaxes, yaxes, hover = [], [], []
count = 0
for i in submission_dicts:
    xaxis = f"<a href='{i['hn_link']}'>{i['title']}</a>"
    xaxes.append(xaxis)
    yaxis = i['score']
    yaxes.append(yaxis)

    hover_text = f"""Title: {i['title']} 
<br /> by: {i['author']} 
<br /> Time Submitted: {time[count]}"""
    hover.append(hover_text)
    count += 1


print(xaxes, "\n")
print(yaxes, "\n")
print(hover, "\n")

x = xaxes
y = yaxes

# Use the hovertext kw argument for hover text
fig = go.Figure(data=[go.Bar(x=x, y=y, hovertext=hover)])
# fig = go.Figure(data=[go.Bar(x=x, y=y, text=y,textposi, hovertext=labels)]) #this text overlays the number of stars onto each respective bars

# Customize aspect
fig.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
                  marker_line_width=1.5, opacity=0.6)
fig.update_xaxes(title_text="News Stories")
fig.update_yaxes(title_text="Score")
fig.update_layout(title_text="HackerNews' Most Popular Current Stories")
# fig.set
fig.show()