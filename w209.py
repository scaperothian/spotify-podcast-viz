from flask import Flask, render_template, request, jsonify
import altair as alt
import pandas as pd
import random
import json

app = Flask(__name__)

with open("visualization_data/publisher/publisher.json") as fp:
    publisher_data = json.load(fp)

with open("visualization_data/show/show.json") as fp:
    show_data = json.load(fp)

with open("visualization_data/episode/episode.json") as fp:
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

if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True)