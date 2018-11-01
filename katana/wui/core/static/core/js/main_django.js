var katana = {
    sidebar: {
        toggleSidebar: function ($elem) {
            var $parent = $elem.closest('.page-content');
            $parent.toggleClass('expanded collapsed');
        },

        toggleSubMenu: function ($elem) {
            var $page = $('body');
            $page.find('#' + $elem.attr('target')).toggleClass('hidden');
            $elem.toggleClass('fa-chevron-down fa-chevron-up');
        }
    }
};