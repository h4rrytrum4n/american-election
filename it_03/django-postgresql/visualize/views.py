from django.views import generic
from django.shortcuts import render
from visualize.models import Hashtag
from django.http import HttpResponse
from collections import Counter
from django.core.serializers.json import DjangoJSONEncoder
import json, re
# Create your views here.


# Triggered by url /index
def index(request):
  return render(request, "index.html")

# Generates a dictionary with nodes and edges
# Passes it finally to the template for further processing
# Triggered by url /network
def network(request):
  query = Hashtag.objects.raw("""select * from Hashtag where tweet_id in 
    (select tweet_id from Hashtag group by tweet_id 
    having count(*)>1 order by tweet_id asc);""")
  nodes, edges = [], []
  dict, used_nodes = {}, {}
  for n in query:
    if not n.tweet_id in dict:
      dict[n.tweet_id] = [n.hash_id, n.text]
    else:
      edge = {"id": n.hash_id, "source": n.text, "target": dict[n.tweet_id][1], "color": '#00f' }
      if n.text not in used_nodes:
        source_node = {"id" : n.text, "label": n.text}
        nodes.append(source_node);
        used_nodes[n.text] = 1
      if dict[n.tweet_id][1] not in used_nodes:
        target_node = {"id" : dict[n.tweet_id][1], "label": dict[n.tweet_id][1]}
        used_nodes[dict[n.tweet_id][1]] = 1
        nodes.append(target_node);
      edges.append(edge); 
  #ct = json.dumps({'nodes': nodes, 'edges': edges}); 
  #Write data to json
  # data = open('static/data.json', 'w')
  # data.write(ct)
  # data.close()
  context = {'c': {'nodes': nodes, 'edges': edges}}
  return render(request, "network.html",context)

# Triggered by url /network
def cluster(request):
  return render(request, "cluster.html")

# Generates a dictionary with dates and occurences of #
# Passes it finally to the tempalte as context
def timeline(request):
  query = Hashtag.objects.raw("""select hash_id, text, time from Hashtag H,
   Tweet T where H.tweet_id = T.tweet_id order by time asc;""")
  data= []
  traces = dict()

  # Iterate through the query and collect all hashtags
  # Save every occurence timestamp in a dictionary
  for h in query:
    time = re.match('\d{4}-\d{2}-\d{2}', str(h.time)).group()
    if h.text not in traces:
      traces[h.text] = [time]
    else:
      traces[h.text].append(time)

  # Count same day occurences
  # Build a dictionary structure for further processing
  for h in traces:
    traces[h] = dict(Counter(traces[h]))
    trace = {"x": list(traces[h].keys()), "y": list(traces[h].values()), "name": h, "type": 'bar'}
    data.append(trace)
  
  # Convert dict to JSON
  data = json.dumps(data, cls=DjangoJSONEncoder)
  context = {'d': data}
  return render(request, "timeline.html", context)