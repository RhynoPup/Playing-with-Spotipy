function toTitleCase(str) {
    return str.replace(/\w\S*/g, function (txt) {
        return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
    });
}

function replaceAll(str, find, replace) {
if (typeof str == 'undefined' || str == null ) {
    return str
} else {
return str.toString().replace(new RegExp(escapeRegExp(find), 'g'), replace);
}
}

function escapeRegExp(str) {
    return str.replace(/([.*+?^=!:${}()|\[\]\/\\])/g, "\\$1");
}

function remove_from_subkeywords(source_group, target_chart) {
    return {
        all: function () {
            return source_group.all().filter(function (d) {
                return ( d.key != "-1" & d.key != 'others' & (target_chart.filters().indexOf(d.key) == -1));
            });
        }
    };
}

function build_app_card(div,title,icons){
    var entity = d3.select('#'+div + '.app_card');
    console.log(d3.select('#'+div ))
    var card = entity.append('div').attr('class','card-light');
    var card_title = card.append('div').attr('class','card-title');
    var card_subtitle = card.append('div').attr('class','card-subtitle');
    var card_body = card.append('div').attr('class','card-text chart');
    var title_options = card_title.append('div').attr('class','row').style('display','flex').style("flex-direction",'row');
    var title_left = title_options.append('div').attr('class','left').style('flex','1');
    title_left.append('h5').text(title);
    var title_right = title_options.append('div').attr('class','right').style('float','right');
    if (icons.indexOf('num_sort')!==-1){
        title_right.append('i').attr('class','zmdi zmdi-sort-amount-asc')
    }
    if (icons.indexOf('alpha_sort')!==-1){
        title_right.append('i').attr('class','zmdi zmdi-sort-asc')
    }
    if (icons.indexOf('refresh')!==-1){
        title_right.append('i').attr('class','zmdi zmdi-refresh-sync')
    }
    if (icons.indexOf('searchbar')!==-1){
        title_left
                .append('div').style('display', 'inline-block').style('padding-left', '10px')
                .append('input').attr('class', 'form-control')
                    .attr('id', 'search_bar')
                    .attr("type", 'text')
                    .attr('placeholder', 'Search...')
                    .attr('aria-label', 'Search');
        var search_overlay = title_left.append('div')
                .attr('class', 'col-lg-12 ' + div +'_search_overlay search_overlay')
                    .style('position', 'absolute')
                    .style('top', '65px')
                    .style('height', '75%')
                    .style('overflow', 'auto')
                    .style('background', 'whitesmoke')
                    .style('visibility', 'hidden')
                    .style('z-index', '999');
        search_overlay
                .append('div').style('padding-bottom','20px').append('i').attr('class', 'zmdi zmdi-close reset chart-reset')
    }

    d3.selectAll('.search_overlay i')
        .on('mouseover', function () {
            d3.select(this).style("font-weight", "bold").style('cursor', 'pointer')
        })
        .on('mouseout', function () {
            d3.select(this).style("font-weight", "normal").style('cursor', 'auto')
        })
        .on('click', function () {
            d3.select(this.parentNode).selectAll('text').remove();
            d3.select(this.parentNode.parentNode).style('height', 0 + 'px').style('visibility','hidden');


            //Add Code to Clear Search Bar on X Click
        });
}

function test_search(full_grp,limited_grp,chart, q,div) {
var pixels_per_row = 25;
var pattern = '.*q.*';
pattern = pattern.replace('q',q);
var re = new RegExp(pattern,"i");

if (q != '' & q.length>2) {
  var filtered = full_grp.all().filter(function (d) {
                    return 0 == d.key.search(re);
                })
      .sort(function (a, b) {
        return (b.value - a.value);
    });

  d3.select('.'+div+'_search_overlay').selectAll('text').remove();
  if (filtered.length>0) {
      var filtered_height = Math.min(Math.max((pixels_per_row*.9) * filtered.length,150),250);
      d3.select('.'+div+'_search_overlay').style('height', filtered_height + 'px').style('visibility','visible');
      d3.select('.'+div+'_search_overlay').append('text').attr('class', 'keysearch').style('font-size','12px').style('line-height','14px').html(function(d){
          var html_text = "";
          filtered.forEach(function (d) {
          html_text+="<p class='keysearch' style='margin:5px;padding:5px;' value='"+d.key+","+d.value+"'>(" + d.value + ")  " + d.key + "</p>"
            });
          return html_text
      });

      d3.selectAll('p.keysearch')
          .style('background',function(d){
            var append_key = d3.select(this).attr('value').split(',')[0];
            return chart.filters().indexOf(append_key)!=-1 ? 'lightblue' : 'whitesmoke'})
          .on('click',function(d){
              console.log('clicked')

            var append_length = d3.select(this).attr('value').split(',').length
            var append_value = parseInt(d3.select(this).attr('value').split(',')[append_length-1]);
            var append_key = d3.select(this).attr('value').split(',').slice(0,append_length-1).join(',');
            console.log(d3.select(this).attr('value').split(',').length,append_value,append_key)

            var curr_filters = chart.filters();

            //Add to Keywords Group if not already there
            if (limited_grp.all().filter(function(e){return e.key==append_key}).length==0){
                limited_grp = group_append(limited_grp,{'key':append_key,'value':append_value})}
            console.log('original filters',curr_filters,limited_grp.all().length,limited_grp.all() );

            chart.group(limited_grp);
            chart.filter(append_key);

             //Toggle highlighting if selected
            d3.select(this).classed("selected", d3.select(this).classed("selected") ? false : true);
            d3.select(this).style("background", chart.filters().indexOf(append_key)!=-1 ? 'lightblue' : 'whitesmoke');
            dc.redrawAll();



      })
          .on('mouseover',function(d){
              d3.select(this).style('color','blue').style("font-weight", "bold").style('cursor','pointer')
              //d3.select(this).style("background", chart.filters().indexOf(append_key)!=-1 ? 'lightblue' : 'whitesmoke');
          })
        .on('mouseout',function(d){
              d3.select(this).style('color','black').style("font-weight", "normal").style('cursor','normal')
           // d3.select(this).style("background", d3.select(this).classed("selected") ? 'lightblue' : 'whitesmoke');
          })
  }
  else{
      d3.select('.'+div+'_search_overlay').selectAll('text').remove();
      d3.select('.'+div+'_search_overlay').style('height', 0 + 'px').style('visibility','hidden');
  }

} else {
  d3.select('.'+div+'_search_overlay').selectAll('text').remove();
  d3.select('.'+div+'_search_overlay').style('height', 0 + 'px').style('visibility','hidden');
}
}



function minimize_card(div){
    d3.select(div).select('.header-icon').append('i').attr('class','zmdi zmdi-window-minimize')
    var minimize_height = 100;
    d3.select(div).select('.header-icon i.zmdi').on('click',function(){

        if (d3.select(div).select('.header-icon i').classed('zmdi-window-minimize')===true){
            d3.select(div).select('.header-icon i').classed('zmdi-window-minimize',false)
            d3.select(div).select('.header-icon i').classed('zmdi-window-maximize',true)

            $(div+' .row').toggle();
            d3.select(div).style('height',minimize_height+'px')
        }
        else{
            d3.select(div).select('.header-icon i').classed('zmdi-window-minimize',true)
            d3.select(div).select('.header-icon i').classed('zmdi-window-maximize',false)
            $(div+' .row').toggle();
            d3.select(div).style('height','auto')

        }
    })
}

function icon_interactivity(data_dict,div){
if (Object.keys(data_dict[div]).indexOf('row_chart')!==-1){
    d3.select('#'+div+' .card-title i.zmdi-sort-amount-asc').on('click',function(){
        data_dict[div]['row_chart'].ordering(function(d){return -d.value});
        data_dict[div]['row_chart'].redraw();
    });
    d3.select('#'+div+' .card-title i.zmdi-sort-asc').on('click',function(){
        data_dict[div]['row_chart'].ordering(function(d){return d.key});
        data_dict[div]['row_chart'].redraw();
    });
    d3.select('#'+div+' .card-title i.zmdi-refresh-sync').on('click',function(){
        console.log('REFRESH')
        data_dict[div]['row_chart'].filterAll();
        dc.redrawAll();
    });

}
if (Object.keys(data_dict[div]).indexOf('bar_chart')!==-1){

    d3.select('#'+div+' .card-title i.zmdi-refresh-sync').on('click',function(){
        data_dict[div]['bar_chart'].filterAll();
        dc.redrawAll();
    });

}
}