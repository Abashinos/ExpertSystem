function renderStat() {
    var chartCount = 0;

    var statisticsData = $('.statistics-data')[0];

    var width = 1200;

    $(statisticsData).children('div').each(function() {
        var statisticsTitle = $(this).data('statistics-title');

        var type = $(this).data('chart-type').toLowerCase();
        if (typeof type == 'undefined') {
            type = 'bar';
        }

        var data = {};

        if (type == 'pie') {
            data = [];
            $(this).children('div').each(function(i) {
                var point = $(this).data('point');
                var count = $(this).data('number');

                data.push({
                    'value': count,
                    'color': getColor(i),
                    'label': point
                });
            });

            width = 600;
        }
        else {
            var labels = [];
            var dataset = [];

            $(this).children('div').each(function(i) {
                var point = $(this).data('point');
                var count = $(this).data('number');

                labels.push(point);
                dataset.push(count);

                data = {
                    labels: labels,
                    datasets: [
                        {
                            fillColor: "rgba(220,220,220,0.5)",
                            strokeColor: "rgba(220,220,220,1)",
                            pointColor: "rgba(220,220,220,1)",
                            pointStrokeColor: "#fff",
                            pointHighlightFill: "#fff",
                            pointHighlightStroke: "rgba(220,220,220,1)",
                            data: dataset
                        }
                    ]
                };

                width = (dataset.length > 6) ? 1200 : (dataset.length * 200);
            });
        }

        chartCount++;

        var container = $('<div class="container col-md-12"></div>');
        container.appendTo($('.chart-container'));

        container.append('<p class="statistics__title">' + statisticsTitle + '</p>');

        var chart = $('<canvas width="' + width + '" height="600"></canvas>').attr('id', 'chart' + chartCount);

        var chart_container = $('<div class="container col-md-6"></div>');
        if (type == 'pie') {
            chart_container.css('text-align', 'center');
        }
        chart_container.appendTo(container);

        chart.appendTo(chart_container);

        var options = {
            animation: false,
            scaleOverride: true,
            scaleSteps: 10,
            scaleStepWidth: Math.ceil(Math.max.apply(null, dataset) / 10),
            scaleStartValue: 0,
            legendTemplate :"<div class=\"container col-md-5\">" +
                                "<p class=\"statistics__title\">Легенда</p>" +
                                "<table class=\"<%=name.toLowerCase()%>-legend\" style=\"margin: 0 10px 0 10px; border-width: 2px; border-style:solid\">" +
                                    "<% for (var i=0; i<segments.length; i++){%>" +
                                        "<tr style=\"min-width:60px; height:20px; border-bottom:solid #ccc 2px\">" +
                                            "<td style=\"background-color:<%=segments[i].fillColor%>; min-width:30px\"></td>" +
                                            "<td style=\"min-width:30px; text-align:center\">" +
                                                "<p><%if(segments[i].label){%><%=segments[i].label%><%}%></p>" +
                                            "</td>" +
                                        "</tr>" +
                                    "<%}%>" +
                                "</table>" +
                            "</div>"
        };

        var ctx = chart.get(0).getContext("2d");
        var myNewChart = new Chart(ctx);

        if (type == 'bar') {
            myNewChart.Bar(data, options);
        } else if (type == 'line') {
            myNewChart.Line(data, options);
        } else if (type == 'pie') {
            chart = myNewChart.Pie(data, options);
            var legend = chart.generateLegend();
            container.append(legend);
        } else {
            myNewChart.Bar(data, options);
        }
    });
}

$(document).ready(function () {
    renderStat();
});
