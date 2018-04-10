var wappstore = {

    expandWapp: function() {
        $.ajax({
                type: 'GET',
                url: 'wappstore/expand_wapp/',
                data: {"name": $(this).attr("name")}
            }).done(function(data){

        });
    },

    collapseSubSidebar: function () {
        var $elem = $(this);
        var $subBar = $elem.closest('.wappstore-main-bar').next();
        if ($elem.find('i').hasClass('fa-chevron-circle-up')){
            $subBar.hide();
            $elem.find('i').removeClass('fa-chevron-circle-up').addClass('fa-chevron-circle-down');
        } else {
            $subBar.show();
            $elem.find('i').removeClass('fa-chevron-circle-down').addClass('fa-chevron-circle-up');
        }
    }
};