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