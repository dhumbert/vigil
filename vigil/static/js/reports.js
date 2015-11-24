$(document).ready(function(){
    var ctx = $('#burns').get(0).getContext("2d");

    $.get(ajaxUrls['burns'], function(data) {
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
                    data: data
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
                console.log(this.scale.xScaleRange.min);

                //var unitY = this.datasets[0].points[1].y - this.datasets[0].points[0].y;
                //console.log(unitY);
                //var yTop = this.scale.startPoint;
                //var yHeight = this.scale.endPoint - this.scale.startPoint;
                var xStart = this.datasets[0].points[0].x;
                var xEnd = this.chart.width;
                var yUnit = this.scale.yScaleRange.stepValue;
                var yMax = this.scale.yScaleRange.max;
                var goodThreshold = 5;

                this.chart.ctx.fillStyle = 'rgba(0,255,0,0.1)';
                this.chart.ctx.fillRect(this.datasets[0].points[0].x, (yMax - goodThreshold) * yUnit, xEnd, -5.5 * yUnit);


                //// write TODAY
                // this.chart.ctx.fillStyle = 'rgba(0,255,0,1)';
                //this.chart.ctx.textAlign = 'center';
                //this.chart.ctx.fillText("TODAY", this.datasets[0].points[0].x, (yMax - goodThreshold) * yUnit);
            }
        });


        var myNewChart = new Chart(ctx).ScatterWithLines(data, {
            scaleType: "date",
            useUtc: false,
            showScale: false,
            scaleShowGridLines: false,
			responsive: true,
            scaleDateTimeFormat: "ddd d mmm"
		});
    });
});