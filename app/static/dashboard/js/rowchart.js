
function build_simple_rowchart(div, dim, grp, pixel_per_row, label_offset, titlecase){
    var rowchart = dc.rowChart(" " + div);

    rowchart
        .width($(" " + div).width())
        .height(grp.all().length > 10  ? grp.all().length * pixel_per_row : pixel_per_row*10)
        .gap(1)
        .margins(grp.all().length > 5 ? {top: 0, right: 15, bottom: 50, left: 0} : {
            top: 0,
            right: 0,
            bottom: 25,
            left: 10
        })
        .labelOffsetX(-label_offset)
        .label(function (d) {
            if (titlecase === true) {
                return '(' + d.value + ')  ' + toTitleCase(d.key)
            } else {
                return '(' + d.value + ')  ' + d.key
            }
        })
        .elasticX(true)
        .dimension(dim)
        .group(grp)
        .ordering(function (d) {
            return -d.value
        })
        .colors(function (d) {
            return "#6baed6"
        })
        .on('pretransition',function(){
            d3.selectAll(div+ ' g text').style('font-size','12px').style('fill','black')
        })
        .xAxis().ticks(5)

    if (grp.all().length<10){
            rowchart.height(grp.all().length * pixel_per_row +25)
        }
    return rowchart
}