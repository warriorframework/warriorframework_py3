
var kwSequencer = {

    init: function(){
        var $currentPage = katana.$activeTab;
        var $newBtn = $currentPage.find('[katana-click="kwSequencer.newKeyword"]');
        var $closeBtn = $currentPage.find('[katana-click="kwSequencer.closeKeyword"]');
        var $saveBtn = $currentPage.find('[katana-click="kwSequencer.saveKeyword"]');
        var $displayFilesDiv = $currentPage.find('#display-files');
        var $displayErrorMsgDiv = $currentPage.find('#display-error-message');
        $newBtn.hide();
        $closeBtn.hide();
        $saveBtn.hide();
        $.ajax({
            type: 'GET',
            url: 'read_config_file/',
        }).done(function(config_json_data) {
            if(config_json_data["pythonsrcdir"] === ""){
                $displayErrorMsgDiv.show();
                $displayFilesDiv.hide();
            } else {
                $newBtn.show();
                $displayErrorMsgDiv.hide();
                $displayFilesDiv.show();
                $.ajax({
                    headers: {
                        'X-CSRFToken': $currentPage.find('input[name="csrfmiddlewaretoken"]').attr('value')
                    },
                    type: 'POST',
                    url: 'get_file_explorer_data/',
                    // TODO: Find a correct way to append '/Actions'
                    data: {"data": {"start_dir": config_json_data["pythonsrcdir"]+'/Actions'}}
                }).done(function(data) {
                    // TODO: Do not show __init__.py files
                    $displayFilesDiv.jstree({
                        "core": { "data": [data]},
                        "plugins": ["search", "sort"],
                        "sort": function (a, b) {
                            var nodeA = this.get_node(a);
                            var nodeB = this.get_node(b);
                            var lengthA = nodeA.children.length;
                            var lengthB = nodeB.children.length;
                            if ((lengthA == 0 && lengthB == 0) || (lengthA > 0 && lengthB > 0))
                                return this.get_text(a).toLowerCase() > this.get_text(b).toLowerCase() ? 1 : -1;
                            else
                                return lengthA > lengthB ? -1 : 1;
                        }
                    });
                    $displayFilesDiv.jstree().hide_dots();
                });
            }
        });
    }

};
