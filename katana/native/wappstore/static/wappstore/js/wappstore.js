var wappstore = {

    expandWapp: function() {
        $.ajax({
                type: 'GET',
                url: 'wappstore/expand_wapp/',
                data: {"name": $(this).attr("name")}
            }).done(function(data){

        });
    }
};