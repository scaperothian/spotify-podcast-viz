# from flask import Flask, render_template
# app = Flask(__name__)

# @app.route("/")
# def w209():
#     file="about9.jpg"
#     return render_template("w209.html",file=file)

# if __name__ == "__main__":
#     app.run()


from flask import Flask, render_template
# from flask_bootstrap import Bootstrap
import altair as alt
import pandas as pd
import numpy as np

app = Flask(__name__)
# Bootstrap(app)
# @app.route('/')
# def index():
#     # Sample data
#     data = pd.DataFrame({
#         'a': list('CCCDDDEEE'),
#         'b': [2, 7, 4, 5, 3, 2, 7, 2, 4]
#     })

#     # Altair chart
#     chart = alt.Chart(data).mark_bar().encode(
#         x='a',
#         y='b'
#     )
#     print(chart)
#     # Convert chart to JSON

#     chart_json = chart.to_dict()
#     print(chart_json)
#     return render_template('index.html', chart=chart_json)

@app.route('/')
def index():
    return render_template('base.html')


@app.route('/publisher')
def publisher():
    # data = load_data('publisher')  # Load publisher data
    # chart = alt.Chart(data).mark_bar().encode(
    #     x='name:N',
    #     y='count:Q'
    # )

    # if metadata.tsv is not there, then run
    try:
        df = pd.read_csv('data/metadata_with_episode_dates.csv')

        # Create data frame with publishers mapped to episodes and shows....
        # TODO: create this offline and load as a json
        #
        # Publisher Data Frame for shows
        df_pub2show = df.groupby(['publisher', 'show_name']).size().reset_index()\
            .groupby('publisher').size().sort_values(ascending=False)
        df_pub2show = pd.DataFrame(df_pub2show, columns=['Number of Shows']).reset_index()
        # Calculate circle sizes based on 'Value'
        # df_pub2show['CircleSize'] = np.sqrt(df_pub2show['Number of Shows'])
        df_pub2show['Number of Shows Jitter'] = df_pub2show['Number of Shows'] + np.abs(
            np.random.normal(0, 1, (len(df_pub2show),)))

        # Publisher Data Frame for episodes
        df_pub2episode = df.groupby('publisher').size().sort_values(ascending=False)
        df_pub2episode = pd.DataFrame(df_pub2episode, columns=['Number of Episodes']).reset_index()
        # Calculate circle sizes based on 'Value'
        df_pub2episode['CircleSize'] = np.sqrt(df_pub2episode['Number of Episodes'])
        df_pub2episode['Number of Episodes Jitter'] = df_pub2episode[
                        'Number of Episodes'] + np.random.random((len(df_pub2episode),))

        data = df_pub2episode.merge(df_pub2show, on='publisher', how='left')

        # Create a scatter plot with circles to represent the categorical table
        chart = alt.Chart(data.sample(5000)).mark_circle().encode(
            x=alt.X('publisher:O', axis=alt.Axis(labels=False, title='')),
            y=alt.Y('Number of Episodes Jitter:Q', scale=alt.Scale(type='log'),
                    axis=alt.Axis(labels=False, title='')),
            size=alt.Size('CircleSize:Q', scale=alt.Scale(range=[5, 2000]), legend=None),
            # Adjust size range as needed
            #color=alt.Color('publisher:N', legend=None),
            color=alt.Color(scale=alt.Scale(scheme='blueorange-8')),
            tooltip=['publisher:N', 'Number of Episodes:Q', 'Number of Shows:Q']
            # Add a tooltip with 'Category' and 'Value'
        ).properties(
            width=500,
            height=500,
            title='Hover over Podcast Publishers (5000 Samples)'
        ).configure_title(
            fontSize=14,
            anchor='middle'
        ).configure_axis(
            grid=False  # Remove gridlines
        ).configure_axisY(
            ticks=False
        )
        print(chart)

    except Exception as e:
        data = pd.DataFrame({
            'a': list('CCCDDDEEE'),
            'b': [2, 7, 4, 5, 3, 2, 7, 2, 4]
        })

        # Altair chart
        chart = alt.Chart(data).mark_bar().encode(
            x='a',
            y='b'
        )
        print(chart)
        # Convert chart to JSON

    chart_dict = chart.to_dict()
    return render_template('publisher.html', chart=chart_dict)

@app.route('/shows')
def shows():
    # data = load_data('publisher')  # Load publisher data
    # chart = alt.Chart(data).mark_bar().encode(
    #     x='name:N',
    #     y='count:Q'
    # )
    return render_template('shows.html', chart={})

@app.route('/episodes')
def episodes():
    # data = load_data('publisher')  # Load publisher data
    # chart = alt.Chart(data).mark_bar().encode(
    #     x='name:N',
    #     y='count:Q'
    # )
    return render_template('episodes.html', chart={})

if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True)