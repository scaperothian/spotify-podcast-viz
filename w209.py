from flask import Flask, render_template, request, jsonify
import altair as alt
import pandas as pd
import random
import json

app = Flask(__name__)

with open("visualization_data/publisher/publisher.json") as fp:
    publisher_data = json.load(fp)

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
    return render_template('shows.html', chart={})

@app.route('/episodes')
def episodes():
    return render_template('episodes.html', chart={})

@app.route('/general')
def general():
    return render_template('general_insights.html')

@app.route('/get-publisher-visualization', methods=['POST'])
def get_publisher_visualization():
    publisher_name = request.json.get('publisher_name')
    selected_publisher_data = publisher_data[publisher_name]

    return jsonify(selected_publisher_data)

if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True)