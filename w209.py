from flask import Flask, render_template, request, jsonify
import altair as alt
import pandas as pd
import random
import json
from os import path
from elasticsearch import Elasticsearch
from altair import Chart, X, Y, Data

from collections import Counter
client = Elasticsearch(
  "https://527db13b131f4f1b90590b6f6c0039f6.us-central1.gcp.cloud.es.io:443",
  api_key=""
)

#convert elsatic search to dataframe

docs = client.search(index='search-spotify-dataset-visualizer', body={"query": {"match_all": {}}})
spotifyresults = [hit['_source']['doc'] for hit in docs['hits']['hits']]
spotify_df = pd.json_normalize(spotifyresults)

app = Flask(__name__)


root_path = path.dirname(__file__)
with open(root_path + "/visualization_data/publisher/publisher.json") as fp:
    publisher_data = json.load(fp)

with open(root_path + "/visualization_data/show/show.json") as fp:
    show_data = json.load(fp)

with open(root_path + "/visualization_data/episode/episode.json") as fp:
    episode_data = json.load(fp)

def get_chart():
    data = pd.DataFrame({
        'a': list('CCCDDDEEE'),
        'b': [random.randint(1, 100) for _ in range(9)]
    })

    # Altair chart
    chart = alt.Chart(data).mark_bar().encode(
        x='a',
        y='b'
    )
    return chart
    

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/publisher')
def publisher():
    return render_template('publisher.html', publishers=list(publisher_data.keys()))

@app.route('/shows')
def shows():
    return render_template('shows.html', shows=list(show_data.keys()))

@app.route('/episodes')
def episodes():
    return render_template('episodes.html', episodes=list(episode_data.keys()))

@app.route('/general')
def general():
    return render_template('general_insights.html')

@app.route('/search')
def search():
    return render_template('search.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/get-publisher-visualization', methods=['POST'])
def get_publisher_visualization():
    publisher_name = request.json.get('publisher_name')
    selected_publisher_data = publisher_data[publisher_name]

    return jsonify(selected_publisher_data)


@app.route('/get-show-visualization', methods=['POST'])
def get_show_visualization():
    show_name = request.json.get('show_name')
    selected_show_data = show_data[show_name]
    print("return show data")
    return jsonify(selected_show_data)

@app.route('/get-episode-visualization', methods=['POST'])
def get_episode_visualization():
    episode_name = request.json.get('episode_name')
    selected_episode_data = episode_data[episode_name]

    return jsonify(selected_episode_data)

@app.route('/spotify-elasticsearch', methods=['POST'])
def get_spotify_data_from_elasticsearch():

    query_phrase = request.json.get("query_phrase")

    es_query = {
        "size": 200,
        "query": {
            "bool": {
            "must": {
                "multi_match": {
                "query": query_phrase,
                "fields": ["doc.show_name", "doc.show_description", "doc.episode_name", "doc.episode_description", "doc.publisher"],
                "type": "best_fields",
                "operator": "or"
                }
            }
            }
        }
    }
    filters = request.json.get("filters")

    res = client.search(index='search-spotify-dataset-visualizer', body=es_query)


    print(filters)
    show_filter = []
    publisher_filter = []

    for k,v in filters['show_filters'].items():
        if v:
            show_filter.append(k)

    for k,v in filters['publisher_filters'].items():
        if v:
            publisher_filter.append(k)

    results = [hit['_source']['doc'] for hit in res['hits']['hits']]
    # at some point we need to turn these results into a dataframe to make the visualizations
    ## build filters and types

    results1, results2 = [], []
    # apply filters
    if publisher_filter:
        results1 = list(filter(lambda x: x['publisher'] in publisher_filter, results))

    # apply filters
    if show_filter:
        results2 = list(filter(lambda x: x['show_name'] in show_filter, results))


    if not publisher_filter and not show_filter:

        avg_duration = sum([x['duration'] for x in results]) / len(results)

        # aggregate topic count
        # print(results[0]['topics'])
        list_of_counters = [Counter(x['topics']) for x in results]
        summed_counter = sum(list_of_counters, Counter())

        top_three_keys = [key for key, _ in summed_counter.most_common(3)]


        return jsonify(
            {
                'rows':results[:50],
                'average_duration': round(avg_duration),
                'top_topics': top_three_keys
            }
        )
    else:

        new_result = results1 + results2
        avg_duration = sum([x['duration'] for x in new_result]) / len(new_result)

        list_of_counters = [Counter(x['topics']) for x in new_result]
        summed_counter = sum(list_of_counters, Counter())

        top_three_keys = [key for key, _ in summed_counter.most_common(3)]
        return jsonify({
            'rows': results1 + results2,
            'average_duration': round(avg_duration),
            'top_topics': top_three_keys
        })
    
#put altair code to generate charts here
@app.route("/gen")
def gen():
    chart = Chart(spotify_df, title = 'Average duration by publisher').mark_bar(color='red').encode(
            X(f'publisher').title("Publisher Name"),
            Y('mean(duration)').title("Average Duration"),
            tooltip=['mean(duration)']
    )
    return chart.to_json()

if __name__ == '__main__':
    # app.jinja_env.auto_reload = True
    # app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True)
