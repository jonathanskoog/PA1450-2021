@app.route("/")
    def home():
        df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2014_apple_stock.csv')
        labels = [row[0] for row in df]
        values = [row[1] for row in df]

        return render_template("index.html", labels=labels, values=values)


 render_template


<canvas id="lineChart" width="900" height="400"></canvas>
  <script>
    var ctx = document.getElementById("lineChart").getContext("2d");
    var lineChart = new Chart(ctx, {
      type: "line",
      data: {
        labels: {{ labels | safe }},
        datasets: [
          {
            label: "Data points",
            data: {{ values | safe }},
            fill: false,
            borderColor: "rgb(75, 192, 192)",
            lineTension: 0.1
          }
        ]
      },
      options: {
        responsive: false
      }
    });
  </script>


  <script src="https://cdn.jsdelivr.net/npm/chart.js@2.9.4/dist/Chart.min.js"> </script>
