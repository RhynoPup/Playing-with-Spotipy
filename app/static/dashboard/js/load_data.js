$(function(){

    var datafile = "static/datafiles.json" //Direct Call
    var promises = [];
    d3.json(datafile).then(function(contents){
        // console.log(contents)
        contents.forEach(function(item){
            promises.push(d3.json(item))
        })
        
        return Promise.all(promises).then(function(data){
            
            list_data=[];
            data.forEach(function(d){
                list_data.push(d)
            })
            app_data = [].concat.apply([],list_data.slice(0,4))
            console.log('App Data', app_data)
            return app_data
        }).then(function(app_data){
            setTimeout(function(){
                application("#application",app_data)
            },50);
            return app_data
        })
    })
})