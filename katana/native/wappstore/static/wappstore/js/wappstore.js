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
    },

    installApp: function() {
        var $elem = $(this);
        $.ajax({
                type: 'GET',
                url: 'wappstore/install_app/',
                data: {"app-name": $elem.attr('app-name')}
            }).done(function(data){
                if(data.status) {
                    setTimeout(function () {
                        katana.refreshLandingPage();
                        katana.openAlert({"alert_type": "success", "heading": "Installation successful", "text": "App has been installed"})
                        $elem.html("Installed")
                    }, 2500);
                } else {
                    setTimeout(function () {
                        katana.openAlert({"alert_type": "error", "heading": "A Problem Occurred", "text": data.message})
                    }, 2500);
                }
        });
    },

    navigate : {
        _scrollRight: function(){
            $(this).prev().scrollLeft($(this).prev().scrollLeft() + 200);
        },

        _scrollLeft: function(){
            $(this).next().scrollLeft($(this).prev().scrollLeft() - 200);
        }
    }
};