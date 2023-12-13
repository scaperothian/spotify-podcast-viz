(function(vegaEmbed) {
    var spec = {"config": {"view": {"continuousWidth": 300, "continuousHeight": 300}, "axis": {"labelFontSize": 15, "titleFont": "Arial", "titleFontSize": 20}}, "data": {"name": "data-02220c6aba4dc67fcaa6064a95b2bc4d"}, "mark": {"type": "bar", "color": "black"}, "encoding": {"size": {"value": 30}, "x": {"axis": {"labelLimit": 300, "titlePadding": 10}, "field": "total_shows", "title": "Count of All Shows", "type": "quantitative"}, "y": {"axis": {"titlePadding": 20}, "field": "category", "sort": {"field": "total_episodes", "order": "descending"}, "title": "Podcast Categories", "type": "ordinal"}}, "height": 200, "width": 300, "$schema": "https://vega.github.io/schema/vega-lite/v5.16.3.json", "datasets": {"data-02220c6aba4dc67fcaa6064a95b2bc4d": [{"category": "Sports", "total_shows": 9005}, {"category": "Comedy", "total_shows": 8059}, {"category": "Health & Fitness", "total_shows": 7680}, {"category": "Education", "total_shows": 6679}, {"category": "Business", "total_shows": 5384}]}};
    var embedOpt = {"mode": "vega-lite"};

    function showError(el, error){
        el.innerHTML = ('<div style="color:red;">'
                        + '<p>JavaScript Error: ' + error.message + '</p>'
                        + "<p>This usually means there's a typo in your chart specification. "
                        + "See the javascript console for the full traceback.</p>"
                        + '</div>');
        throw error;
    }
    const el = document.getElementById('vis');
    vegaEmbed("#bar-chart-2", spec, embedOpt)
      .catch(error => showError(el, error));
  })(vegaEmbed);