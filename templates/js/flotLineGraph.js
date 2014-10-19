//Flot Line Chart
$(document).ready(function() {
    var offset = 0;
    plot();

    function plot() {

        var options = {
            series: {
                lines: {
                    show: true
                },
                points: {
                    show: true
                }
            },
            grid: {
                hoverable: true //IMPORTANT! this is needed for tooltip to work
            },
            yaxis: {
                min: 0,
                max: 300
            },
            tooltip: true,
            tooltipOpts: {
                content: "'%s' of %x.1 is %y.4",
                shifts: {
                    x: -60,
                    y: 25
                }
            }
        };

        var plotObj = $.plot($("#flot-line-chart"), [
            {
                data: [{% for key,value in data.items %}["{{ key }}", {{ value }}], {% endfor %}],
                label: "Test Data"
            }],
            options);
    }
});