
$(function() {
    calculateSIP();
});
function calculateSIP() {
    sipAmount = $('#txtmonthlysip').val();
    sipMonth = $('#txttimehorizon').val() * 12;
    rateofReturn = $('#txtexpectedret').val();

    if (sipAmount >= 1000 && parseInt(sipAmount)) {
    } else {
        alert('Please enter a value greater than or equal to 1000.');
        return false;
    }
    sipAmount = parseInt(sipAmount);
    sipMonth = parseInt(sipMonth);
    rateofReturn = parseFloat(rateofReturn, 10);
    var value1 = (rateofReturn / 100) / 12;
    var value3 = 1 + value1;
    var value4 = Math.pow((value3), (sipMonth + 1));
    var amount1 = (value4 - 1);
    var amount2 = amount1 / value1;
    var final_amount = (sipAmount * amount2) - sipAmount;
    final_amount = Math.round(final_amount);
    var invest_amount = sipAmount * sipMonth;
    var interest_total = final_amount - invest_amount;
    $("#totalInvested").html(numbersWithComma(invest_amount));
    $("#expectedAmount").html(numbersWithComma(final_amount));

    PieGraphSIP("sipgraphpie",invest_amount, interest_total);
   var d = new Date();
    var current_year = d.getFullYear();
    var current_month = d.getMonth();
    barChartValuesPrepare(current_year, current_month);
//    showfutureVal(current_year, current_month);
}
function numbersWithComma(x) {
    x = x.toString();
    var afterPoint = '';
    if (x.indexOf('.') > 0)
        afterPoint = x.substring(x.indexOf('.'), x.length);
    x = Math.floor(x);
    x = x.toString();
    var lastThree = x.substring(x.length - 3);
    var otherNumbers = x.substring(0, x.length - 3);
    if (otherNumbers != '')
        lastThree = ',' + lastThree;
    var res = otherNumbers.replace(/\B(?=(\d{2})+(?!\d))/g, ",") + lastThree + afterPoint;
    return res;
}
var sipAmount = 0;
var rateofReturn = 0;
var sipMonth = 0;

function barChartValuesPrepare(current_year, current_month) {
var chartdata=[];
    years = sipMonth;
    var yearArr = new Array();
    var principalArr = new Array();
    var interestArr = new Array();
    var balanceArr = new Array();
    if (years > 120) {
        var years = sipMonth / 12;
        var mon = 12;
        if (years > 20) {
            var labels = {
                rotation: 45,
                step: 1,
                style: {
                    fontSize: '13px',
                    fontFamily: "var(--regular)"
                }
            };
        } else {
            var labels = {
                step: 1,
                style: {
                    fontSize: '13px',
                    fontFamily: "var(--regular)"
                }
            };
        }
        for (var k = 1; k <= years; k++) {
            yearArr.push(current_year);
            var value1 = (rateofReturn / 100) / 12;
            var value3 = 1 + value1;
            var value4 = Math.pow((value3), (mon + 1));
            var amount1 = (value4 - 1);
            var amount2 = amount1 / value1;
            var final_amount = (sipAmount * amount2) - sipAmount;
            final_amount = Math.round(final_amount);
            var invest_amount = sipAmount * mon;
            var interest_total = final_amount - invest_amount;
            principalArr.push(invest_amount);
            interestArr.push(interest_total);
            balanceArr.push(final_amount);
            current_year = current_year + 1;
            mon = mon + 12;
            chartdata.push({ "year": current_year, "amount": invest_amount,"amountsip": final_amount });
        }
    } else {
        var years = sipMonth;
        var mon = 1;
        var k = 1;
        var allMonths = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
        var labels = {
            rotation: 45,
            step: 1,
            style: {
                fontSize: '13px',
                fontFamily:"var(--regular)"
            }
        };
        while (k <= years) {
            var actualDate = new Date();
            // convert to actual date
            if (k != 1) {
                var actualDate = new Date(actualDate.getFullYear(),actualDate.getMonth(),actualDate.getDate() + 30 * k);
                var month = allMonths[((actualDate.getMonth()))];
            } else {
                var actualDate = new Date(actualDate.getFullYear(),actualDate.getMonth() + 1,actualDate.getDate());
                var month = allMonths[((actualDate.getMonth()))];
            }
            // make date 2 digits
            if (month == 0 || month == undefined) {
                month = 'Jan';
            }
            var date = ('0' + actualDate.getDate()).slice(-2);
            // get 4 digit year
            var year = actualDate.getFullYear();
            var string = "'" + year + "'";
            year = string.substring(3, 5);
            // concatenate into desired arrangement
            var shortDate = month + '/' + year;
            yearArr.push(shortDate);
            var value1 = (rateofReturn / 100) / 12;
            var value3 = 1 + value1;
            var value4 = Math.pow((value3), (mon + 1));
            var amount1 = (value4 - 1);
            var amount2 = amount1 / value1;
            var invest_amount = sipAmount * k;
            var final_amount = (sipAmount * amount2) - sipAmount;
            final_amount = Math.round(final_amount);
            var interest_total = final_amount - invest_amount;
            principalArr.push(invest_amount);
            interestArr.push(interest_total);
            balanceArr.push(final_amount);
            chartdata.push({ "year": shortDate, "amount": invest_amount,"amountsip": final_amount });

            if (years == 300 || years == 360 || years == 420) {
                k = k + 12;
                mon = mon + 12;
            } else if (years > 120) {
                if (k == 1) {
                    k = k + 11;
                    mon = mon + 11;
                } else {
                    k = k + 12;
                    mon = mon + 12;
                }
            } else {
                if (k == 1) {
                    k = k + 3;
                    mon = mon + 3;
                } else {
                    k = k + 4;
                    mon = mon + 4;
                }
            }
        }
    }
    var chartfields = ["year", "amount", "amountsip"];
    PieGraphLinechart(chartdata,chartfields);
    //renderBarChart(yearArr, principalArr, interestArr, balanceArr, labels);
}
function showfutureVal(current_year, current_month) {
    var years = 35;
    var mon = 12;
    currentyear = current_year;
    var yearArr = new Array();
    var principalArr = new Array();
    var interestArr = new Array();
    var balanceArr = new Array();
    for (var k = 1; k <= years; k++) {
        yearArr.push(current_year);
        var value1 = (rateofReturn / 100) / 12;
        var value3 = 1 + value1;
        var value4 = Math.pow((value3), (mon + 1));
        var amount1 = (value4 - 1);
        var amount2 = amount1 / value1;
        var final_amount = (sipAmount * amount2) - sipAmount;
        final_amount = Math.round(final_amount);
        var invest_amount = sipAmount * mon;
        var interest_total = final_amount - invest_amount;
        principalArr.push(invest_amount);
        interestArr.push(interest_total);
        balanceArr.push(final_amount);
        current_year = current_year + 1;
        mon = mon + 12;
    }
    displayFuture(yearArr, balanceArr, currentyear);
}
    function PieGraphSIP(id,invest_amount, interest_total) {
        var data = [{ "title": "SIP Invested Amt", "value":invest_amount  }, { "title": "Growth Amount", "value": interest_total}];
        var chart = AmCharts.makeChart(id, {
            "type": "pie",
            "dataProvider": data,
            "balloonText": "[[title]]<br><span><b>[[value]]</b> ([[percents]]%)</span>",
            "fontFamily":"var(--regular)",
            "color":"#fff",
            "labelRadius": "-12%",
            "innerRadius": "55%",
            "labelText": "[[percents]]",
            "startAngle": 340,
            "colors": ["var(--orange)","var(--yellow)"],
            "labelsEnabled": true,
            "titleField": "title",
            "valueField": "value",
            "allLabels": [],
            "balloon": {},
            "legend": {
                "enabled": true,
                "align": "center",
                "markerType": "circle",
                "maxColumns": 2,
                "valueText": ""
            },
            "titles": []
        });
    }
 function PieGraphLinechart(data, chartfields) {
        chart = new AmCharts.AmSerialChart();
        chart.type = "serial";
        chart.dataProvider = data;
        chart.colors = ["var(--yellow)","var(--orange)", "#002f43"];
        chart.categoryField = chartfields[0];
        chart.color = "#8d8d8d";
        chart.height = "100%";
        chart.fontFamily = "var(--regular)";
        chart.fontSize = 13;
        chart.autoGridCount = true;
        chart.autoMargins = false;
        chart.marginRight = 100;
        chart.marginLeft = 50;
        chart.marginBottom = 50;
        var categoryAxis = chart.categoryAxis;
        categoryAxis.position = "bottom";
        categoryAxis.startOnAxis = true;
        categoryAxis.gridAlpha = 0;
        categoryAxis.axisAlpha = 1;
        categoryAxis.gridPosition = "start";
        categoryAxis.axisColor = "#fff";
        var valueAxis = new AmCharts.ValueAxis();
      //  valueAxis.title = "GROWTH VALUE";
        valueAxis.titleRotation = 90;
        valueAxis.titleFontSize = 12;
        valueAxis.axisAlpha = 1;
        valueAxis.position = "right";
        valueAxis.gridAlpha = 1;
        valueAxis.gridColor = "#afafaf";
        valueAxis.axisColor = "#afafaf";
        chart.addValueAxis(valueAxis);
        var graph1 = new AmCharts.AmGraph();
        graph1.valueField = "amountsip";
        graph1.lineThickness = 2;
        graph1.balloonText = "[[amountsip]]";
        graph1.fillAlphas =1;
        graph1.lineAlpha = 0.8;
        graph1.title = "Future Value";
        chart.addGraph(graph1);

        var graph2 = new AmCharts.AmGraph();
        graph2.valueField = "amount";
        graph2.lineThickness = 2;
        graph2.balloonText = "[[amount]]";
        graph2.fillAlphas = 1;
        graph2.title = "Invested Amount";
        chart.addGraph(graph2);

        var legend = new AmCharts.AmLegend();
        legend.markerType="circle";
       
        chart.addLegend(legend, "sipgraphlinelegend");

        var chartCursor = new AmCharts.ChartCursor();
        chartCursor.cursorPosition = "mouse";
        chartCursor.categoryBalloonColor = "#000000"; //bottom line color
        chartCursor.cursorColor = "#000"; //bottom line color
        chart.addChartCursor(chartCursor);
        chart.write("sipgraphline");

    }
function renderBarChart(yearArr, principalArr, interestArr, balanceArr, labels) {
    $('#areaGraph').highcharts({
        chart: {
            type: 'area'
        },
        legend: {
            enabled: false
        },
        title: {
            text: 'Systematic Investment Plan (SIP)<br /> Growth Chart'
        },
        xAxis: {
            allowDecimals: false,
            type: 'datetime',
            categories: yearArr,
            text: 'Time Frame',
            labels: labels,
        },
        yAxis: {
            title: {
                text: 'Growth Value'
            },
            labels: {
                x: -5,
                y: 0,
                formatter: function() {
                    return '₹' + numDifferentiation(this.value);
                }
            },
            opposite: true
        },
        plotOptions: {
            area: {
                marker: {
                    enabled: false,
                    symbol: 'circle',
                    states: {
                        hover: {
                            enabled: true
                        }
                    },
                },
                animation: {
                    duration: 1200,
                    easing: 'linear'
                },
            }
        },
        legend: {
            align: 'left',
            verticalAlign: 'top',
            floating: true,
            borderWidth: 0,
            x: 0,
            y: 75
        },
        series: [
        {
            name: 'Future value',
            data: balanceArr
        }, {
            name: 'Invested Amount',
            data: principalArr
        }
        ]
    });
}
function in_array(needle, haystack) {
    var found = 0;
    for (var i = 0, len = haystack.length; i < len; i++) {
        if (haystack[i] == needle)
            return i;
        found++;
    }
    return -1;
}
function displayFuture(yearArr, balanceArr, current_year) {
    var displayYear = new Array();
    var displayBalance = new Array();
    var YearIndex = new Array();
    var balancehtml = '<td class="text-tra">Future Value</td>';
    var yearhtml = '<td class="color-td text-tra">Year</td>';
    var years = current_year + (sipMonth / 12) - 1;
    for (var i = 0; i < yearArr.length; i++) {
        if (i > 0) {
            if (yearArr.length > 14) {
                i + 5
                var check = (yearArr[i]) / 5;
            } else if (yearArr.length > 8) {
                var check = (yearArr[i]) / 2;
            } else {
                var check = (yearArr[i]);
            }
            if ((check + "").match(/^\d+$/)) {
                displayYear.push(yearArr[i]);
                YearIndex.push(i);
            }
        } else {
            displayYear.push(yearArr[i]);
            YearIndex.push(i);
        }
    }
    for (var i = 0; i < YearIndex.length; i++) {
        if (years == displayYear[i]) {
            var balancehtml = balancehtml.concat('<td class="active">' + numDifferentiation(balanceArr[YearIndex[i]]) + '</td>');
        } else {
            var balancehtml = balancehtml.concat('<td class="">' + numDifferentiation(balanceArr[YearIndex[i]]) + '</td>');
        }
    }
    for (var i = 0; i < displayYear.length; i++) {
        if (years == displayYear[i]) {
            var yearhtml = yearhtml.concat('<td class="color-td active">' + displayYear[i] + '</td>');
        } else {
            var yearhtml = yearhtml.concat('<td class="color-td">' + displayYear[i] + '</td>');
        }
    }
    $('.yearappend').html(yearhtml);
    $('.valueappend').html(balancehtml);
}
function numDifferentiation(val) {
    if (val >= 10000000)
        val = (val / 10000000).toFixed(2) + ' Cr';
    else if (val >= 100000)
        val = (val / 100000).toFixed(2) + ' Lac';
    else if (val >= 1000)
        val = (val / 1000).toFixed(2) + ' K';
    return val;
}
