$(function(){

    var files = "../datafiles.json"
    var promises = [];
    d3.json(files).then(function(file){
        promises.push(file)
        return Promise.all(promises).then(function(data){
            list_data=[]
            data.forEach(function(d){
                list_dat.push(d)
            })
            app_data = [].concat.apply([],list_data)
            console.log('App Data', app_data)
            return app_data
        }).then(function(app_data){
            setTimeout(function(){
                app_data("#application",app_data)
            },50);
            return app_data
        })
    })
})