var katana = {
    sidebar: {
        toggleSidebar: function ($elem) {
            var $parent = $elem.closest('.page-content');
            $parent.toggleClass('expanded collapsed');
        }
    }
};