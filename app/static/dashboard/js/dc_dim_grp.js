
function dim_grp__artists(cf, data_dict,div) {
    data_dict[div] = {
        'format': 'list',
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