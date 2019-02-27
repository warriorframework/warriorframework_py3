var katana = {
    sidebar: {
        /* Contains all functions pertaining to the main sidebar */

        toggleSidebar: function ($elem) {
            /* This function toggles the css classes "expanded" and "collapsed" on the main sidebar.*/
            var $parent = $elem.closest('.page-content');
            $parent.toggleClass('expanded collapsed');
        },

        toggleSubMenu: function ($elem) {
            /* This function toggles the submenu bar on the main sidebar. Associated submenu can be tracked by
            adding a "target" attribute on the "clicked" menu item that contains the id of the target submenu */
            var $pageContent = $elem.closest('.page-content');
            if($pageContent.hasClass('collapsed')) {
                $pageContent.toggleClass('collapsed expanded');
            }
            var $page = $('body');
            $page.find('#' + $elem.attr('target')).toggleClass('hidden');
            $elem.find('.toggle-this').toggleClass('fa-chevron-down fa-chevron-up');
        },

        openApp: function ($elem) {
            /* Function exists purely to move back and forth between the old Katana API and new
            on the framework level. This can deprecated once all apps are moved to new API */
            var url = $elem.attr("url");
            var pureDjango = $elem.attr('pure-django').toLowerCase() === "true";
            if ( !pureDjango ) {
                localStorage.setItem("load_url", url);
                window.location.href = '/katana';
            } else {
                window.location.href = url;
            }
        }
    }
};