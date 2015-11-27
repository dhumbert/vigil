$(document).ready(function(){
    var ctx = $('#top-graph').get(0).getContext("2d");

    $.get(ajaxUrls['top_graph'], function(graph_data) {
        var data = {
            datasets: [
                {
                    label: "Burns Score",
                    fillColor: "rgba(220,220,220,0.2)",
                    strokeColor: "rgba(220,220,220,1)",
                    pointColor: "rgba(220,220,220,1)",
                    pointStrokeColor: "#fff",
                    pointHighlightFill: "#fff",
                    pointHighlightStroke: "rgba(220,220,220,1)",
                    data: graph_data.burns
                }
                //,
                //{
                //    label: "My Second dataset",
                //    fillColor: "rgba(151,187,205,0.2)",
                //    strokeColor: "rgba(151,187,205,1)",
                //    pointColor: "rgba(151,187,205,1)",
                //    pointStrokeColor: "#fff",
                //    pointHighlightFill: "#fff",
                //    pointHighlightStroke: "rgba(151,187,205,1)",
                //    data: [
                //        {y: 0, x: 1447142400000}
                //    ]
                //}
            ]
        };

        for (var k in graph_data.other) {
            if (graph_data.other.hasOwnProperty(k)) {
                data.datasets.push({
                    label: k,
                    data: graph_data.other[k].data,
                    fillColor: "rgba(" + graph_data.other[k].color.red + "," + graph_data.other[k].color.green + "," + graph_data.other[k].color.blue + ",0.2)",
                    strokeColor: "rgba(" + graph_data.other[k].color.red + "," + graph_data.other[k].color.green + "," + graph_data.other[k].color.blue + ",1)",
                    pointColor: "rgba(" + graph_data.other[k].color.red + "," + graph_data.other[k].color.green + "," + graph_data.other[k].color.blue + ",1)",
                    pointStrokeColor: "#fff",
                    pointHighlightFill: "#fff",
                    pointHighlightStroke: "rgba(" + graph_data.other[k].color.red + "," + graph_data.other[k].color.green + "," + graph_data.other[k].color.blue + ",1)"
                });
            }
        }

        console.log(data.datasets);

        Chart.types.Scatter.extend({
            name: "ScatterWithLines",
            initialize: function () {
                Chart.types.Scatter.prototype.initialize.apply(this, arguments);
            },
            draw: function () {
                Chart.types.Scatter.prototype.draw.apply(this, arguments);

                var point = this.datasets[0].points[0];//[this.options.lineAtIndex];
                //console.log(point);
                var scale = this.scale;

                //var unitY = this.datasets[0].points[1].y - this.datasets[0].points[0].y;
                //console.log(unitY);
                //var yTop = this.scale.startPoint;
                //var yHeight = this.scale.endPoint - this.scale.startPoint;
                var xStart = this.datasets[0].points[0].x;
                var xEnd = this.chart.width;
                //var yUnit = this.scale.yScaleRange.stepValue;
                //var yMax = this.scale.yScaleRange.max;
                //var goodThreshold = 5;
                //
                //this.chart.ctx.fillStyle = 'rgba(0,255,0,0.1)';
                //this.chart.ctx.fillRect(this.datasets[0].points[0].x, (yMax - goodThreshold) * yUnit, xEnd, -5.5 * yUnit);

                // draw line at "good" cutoff
                var yLine = this.scale.calculateY(6); // above 5 is not good
                this.chart.ctx.beginPath();
                this.chart.ctx.moveTo(xStart, yLine);
                this.chart.ctx.strokeStyle = '#fc9d94';
                this.chart.ctx.lineTo(xEnd, yLine);
                this.chart.ctx.stroke();

                // draw line at 0
                var yLineZero = this.scale.calculateY(0);
                this.chart.ctx.beginPath();
                this.chart.ctx.moveTo(xStart, yLineZero);
                this.chart.ctx.strokeStyle = '#ccc';
                this.chart.ctx.lineTo(xEnd, yLineZero);
                this.chart.ctx.stroke();


                //// write TODAY
                // this.chart.ctx.fillStyle = 'rgba(0,255,0,1)';
                //this.chart.ctx.textAlign = 'center';
                //this.chart.ctx.fillText("TODAY", this.datasets[0].points[0].x, (yMax - goodThreshold) * yUnit);
            }
        });


        var topChart = new Chart(ctx).ScatterWithLines(data, {
            scaleType: "date",
            useUtc: false,
            showScale: false,
            scaleShowGridLines: false,
			responsive: true,
            scaleDateTimeFormat: "ddd d mmm"
            //legendTemplate: "<ul class=\"<%=name.toLowerCase()%>-legend\"><%for(var i=0;i<datasets.length;i++){%><li><span class=\"<%=name.toLowerCase()%>-legend-marker\" style=\"background-color:<%=datasets[i].strokeColor%>\"></span><%=datasets[i].label%></li><%}%></ul>"
		});

        var legend = topChart.generateLegend();
        $('#top-graph-legend').append(legend);

        $('#top-graph').hover(function(){
            $('#top-graph-legend').slideDown();
        }, function() {
            $('#top-graph-legend').slideUp();
        })
    });
});