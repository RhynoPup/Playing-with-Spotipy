
function dim_grp__artists(cf, data_dict,div) {
    data_dict[div] = {
        'format': 'string',
        'div': div,
        'display_title': 'Artists',
        'type':'simple'

    };

    data_dict[div]['dim'] = cf.dimension(function (d) {
        if (typeof d['artists'] == "undefined") return "";
        var artist_name = []
        d['artists'].forEach(function(artist){
            artist_name.push(artist['name'])
        })
        return artist_name
    }, true);

    data_dict[div]['grp'] = data_dict[div]['dim'].group();
    data_dict[div]['grp_n'] = remove_empty_text_bins(group_top_n(data_dict[div]['grp'],50));

    console.log(div, data_dict[div]['grp'].all())
    console.log(div, data_dict[div]['grp_n'].all())

    return data_dict
}

function dim_grp__album(cf, data_dict,div) {
    data_dict[div] = {
        'format': 'string',
        'div': div,
        'display_title': 'Album',
        'type':'simple'

    };

    data_dict[div]['dim'] = cf.dimension(function (d) {
        if (typeof d['album'] == "undefined") return "";
        
        return d['album']['name']
    }, false);

    data_dict[div]['grp'] = data_dict[div]['dim'].group();
    data_dict[div]['grp_n'] = remove_empty_text_bins(group_top_n(data_dict[div]['grp'],50));

    console.log(div, data_dict[div]['grp'].all())
    console.log(div, data_dict[div]['grp_n'].all())

    return data_dict
}


// Extra Grp Functions
function remove_empty_text_bins(source_group) {
    return {
        all: function () {
            return source_group.all().filter(function (d) {
                return d.key !== "" && d.key !== null;
            });
        }
    };
}


function group_top_n(source_group,n) {
    return {
        all: function () {
            return source_group.top(n).filter(function (d) {
                return ( d.key != "-1" & d.key!='others');
            });
        }
    };
}