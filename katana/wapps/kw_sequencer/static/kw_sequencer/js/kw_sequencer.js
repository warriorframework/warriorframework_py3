'use strict';

var kwSequencer = {

    action_file: "",

    init: function(){
        var $currentPage = katana.$activeTab;
        var $newBtn = $currentPage.find('[katana-click="kwSequencer.newKeyword"]');
        var $closeBtn = $currentPage.find('[katana-click="kwSequencer.closeKeyword"]');
        var $saveBtn = $currentPage.find('[katana-click="kwSequencer.saveKeyword"]');
        var $displayFilesDiv = $currentPage.find('#display-files');
        var $displayErrorMsgDiv = $currentPage.find('#display-error-message');
        var $createKwDiv = $currentPage.find('#create-keyword');
        kwSequencer.action_file = "";
        $newBtn.hide();
        $closeBtn.hide();
        $saveBtn.hide();
        $createKwDiv.hide();
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
                    $displayFilesDiv.on('changed.jstree', function (e, data) {
                        kwSequencer.action_file = data.instance.get_path(data.node,'/');
                    });
                });
            }
        });
    },

    newKeyword: function(){
        if (kwSequencer.action_file) {
            $.ajax({
               type: 'GET',
               url: 'kw_sequencer/create_new_kw/'
            }).done(function(data){
                var $currentPage = katana.$activeTab;
                var $newBtn = $currentPage.find('[katana-click="kwSequencer.newKeyword"]');
                var $closeBtn = $currentPage.find('[katana-click="kwSequencer.closeKeyword"]');
                var $saveBtn = $currentPage.find('[katana-click="kwSequencer.saveKeyword"]');
                var $displayFilesDiv = $currentPage.find('#display-files');
                var $displayErrorMsgDiv = $currentPage.find('#display-error-message');
                var $createKwDiv = $currentPage.find('#create-keyword');
                var $toolBarDiv = $currentPage.find('.tool-bar');
                $newBtn.hide();
                $closeBtn.show();
                $saveBtn.show();
                $displayFilesDiv.hide();
                $displayErrorMsgDiv.hide();
                $createKwDiv.show();
                $currentPage.find("#create-keyword").html(data);
                $toolBarDiv.find('.title').html("Katana Wrapper Keyword Editor");
            });
        } else {
            katana.openAlert({"alert_type": "warning",
                               "heading": "Action file required!",
                               "text": "Please choose an action file and click 'New' to create a Keyword.",
                               "accept_btn_text": "Ok", "show_cancel_btn": false})
        }

    },

    closeKeyword: function(){
        var $currentPage = katana.$activeTab;
        var callbackOnAccept = function(){
            $currentPage.find('[katana-click="kwSequencer.newKeyword"]').show();
            $currentPage.find('[katana-click="kwSequencer.closeKeyword"]').hide();
            $currentPage.find('[katana-click="kwSequencer.saveKeyword"]').hide();
            $currentPage.find('#create-keyword').hide();
            $currentPage.find('#display-files').show();
            var $toolBarDiv = $currentPage.find('.tool-bar');
            $toolBarDiv.find('.title').html("Create New Keyword");
        }
        katana.openAlert({"alert_type": "warning",
                           "heading": "Do You Want To Continue?",
                           "text": "All changes made would be discarded.",
                           "accept_btn_text": "Yes", "cancel_btn_text": "No"},
                           callbackOnAccept)

    },

    newSubKeyword: function(){
        console.log("newSubKeyword")
    },

};
