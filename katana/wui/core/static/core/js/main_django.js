var katana = {
    sidebar: {
        toggleSidebar: function ($elem) {
            var $parent = $elem.closest('.page-content');
            $parent.toggleClass('expanded collapsed');
        },

        toggleSubMenu: function ($elem) {
            var $pageContent = $elem.closest('.page-content');
            if($pageContent.hasClass('collapsed')) {
                $pageContent.toggleClass('collapsed expanded');
            }
            var $page = $('body');
            $page.find('#' + $elem.attr('target')).toggleClass('hidden');
            $elem.find('.toggle-this').toggleClass('fa-chevron-down fa-chevron-up');
        },

        openApp: function ($elem) {
            var url = $elem.attr("url");
            if (url.startsWith('/katana')) {
                localStorage.setItem("load_url", url);
                window.location.href = '/katana';
            } else {
                window.location.href = url;
            }
        }
    }
};