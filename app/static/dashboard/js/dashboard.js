function application(selector,dataset){
    var data = dataset;


    console.log('Data', data);
    var cf = crossfilter(data),
        all = cf.groupAll();

    dc.dataCount(".dc-data-count")
        .dimension(cf)
        .group(all);

     //--------- STYLES -----------------
    var pixels_per_row = 22;
    var label_offset = -10;

    build_app_card('artist','',['num_sort','alpha_sort','refresh','searchbar'])



    var data_dict = {};
    data_dict = dim_grp__artists(cf,data_dict,'artist')



    dc.renderAll();
}