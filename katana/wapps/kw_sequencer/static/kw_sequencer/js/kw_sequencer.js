'use strict';

var kwSequencer = {

    actionFilePath: "",
    drivers: false,

    init: function() {
        /* This function get the warrior source dir from 'settings -> General settings' and
        lists all the valid action files using jstree */
        var $currentPage = katana.$activeTab;
        var $newBtn = $currentPage.find('[katana-click="kwSequencer.newKeyword"]');
        var $closeBtn = $currentPage.find('[katana-click="kwSequencer.closeKeyword"]');
        var $saveBtn = $currentPage.find('[katana-click="kwSequencer.saveKeyword"]');
        var $displayFilesDiv = $currentPage.find('#display-files');
        var $displayErrorMsgDiv = $currentPage.find('#display-error-message');
        var $createKwDiv = $currentPage.find('#create-keyword');
        kwSequencer.actionFilePath = "";
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
                    data = kwSequencer.removeNonActionFiles([data])[0];
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
                        kwSequencer.actionFilePath = data.instance.get_path(data.node, '/');
                    });
                });
            }
        });
    },

    newKeyword: function() {
        /* This function opens a new wrapper keyword */
        var isActionFile = false;
        if (kwSequencer.actionFilePath) {
            var actionFileName = kwSequencer.actionFilePath.split('\\').pop().split('/').pop();
            var actionFileExtn = actionFileName.split('.').pop();
            if (actionFileName != '__init__.py' && actionFileExtn == 'py') {
                isActionFile = true;
            }
        }

        if (isActionFile) {
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
                $createKwDiv.html(data);
                $currentPage.find("#wrapperActionFile").val(actionFileName.split('.')[0]);
                $toolBarDiv.find('.title').html("Katana Wrapper Keyword Editor");
            });
        } else {
            katana.openAlert({"alert_type": "warning",
                               "heading": "Action file required!",
                               "text": "Please choose a Warrior Action File and click 'New' to create a Keyword.",
                               "accept_btn_text": "Ok", "show_cancel_btn": false})
        }

    },

    closeKeyword: function() {
        /* This function closes the wrapper keyword */
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

    saveKeyword: function() {
        /* This function saves the wrapper keyword in the corresponding warrior action file */
        var $currentPage = katana.$activeTab;
        var $wrappeKwDetailsDiv = $currentPage.find('#wrapper-keyword-details-div');
        if (katana.validationAPI.init($wrappeKwDetailsDiv)){
            var $newSubKwDiv = $currentPage.find('#new-sub-keyword-div');
            if ($newSubKwDiv.css('display') != 'none') {
                katana.openAlert({
                    "alert_type": "danger",
                    "heading": "SubKeyword is not saved!",
                    "text": "Either save or discard the Subkeyword before saving the Wrapper Keyword.",
                    "show_cancel_btn": false
                });
                return;
            }
            var tableLength = $currentPage.find('#sub-keywords-table').find('tbody').children('tr').length
            if (tableLength == 0) {
                katana.openAlert({
                    "alert_type": "danger",
                    "heading": "No SubKeywords added!",
                    "text": "Please add at least one SubKeyword before saving Wrapper Keyword.",
                    "show_cancel_btn": false
                });
                return;
            }
            var wrapperKwDetails = kwSequencer.getWrapperKwDetails($currentPage.find('#wrapper-keyword-details-div'));
            var subKeywordDetails = kwSequencer.getSubKeywordDetails($currentPage.find('#display-sub-keywords-div'));
            wrapperKwDetails['@subKeywords'] = JSON.stringify(subKeywordDetails)
            wrapperKwDetails['@actionFile']= kwSequencer.actionFilePath

            $.ajax({
                headers: {
                    'X-CSRFToken': $currentPage.find('input[name="csrfmiddlewaretoken"]').attr('value')
                },
                type: 'POST',
                url: 'kw_sequencer/save_wrapper_kw/',
                data: wrapperKwDetails
            }).done(function(output) {
                var callbackOnSuccess = function(){
                    $currentPage.find('[katana-click="kwSequencer.newKeyword"]').show();
                    $currentPage.find('[katana-click="kwSequencer.closeKeyword"]').hide();
                    $currentPage.find('[katana-click="kwSequencer.saveKeyword"]').hide();
                    $currentPage.find('#create-keyword').hide();
                    $currentPage.find('#display-files').show();
                    var $toolBarDiv = $currentPage.find('.tool-bar');
                    $toolBarDiv.find('.title').html("Create New Keyword");
                }
                if (output.status) {
                    katana.openAlert({
                        "alert_type": "success",
                        "heading": "Wrapper Keyword Saved",
                        "text": output.message,
                        "show_cancel_btn": false
                    }, callbackOnSuccess);
                } else {
                    katana.openAlert({
                        "alert_type": "danger",
                        "heading": "Wrapper Keyword Not Saved",
                        "text": output.message,
                        "show_cancel_btn": false
                    })
                }
            });
        }
    },

    newSubKeyword: function(insertAtIndex) {
        /* This function opens new sub keyword */
        $.ajax({
            type: 'GET',
            url: 'kw_sequencer/create_new_subkw/'
        }).done(function(data) {
            var $currentPage = katana.$activeTab;
            var $newSubKwDiv = $currentPage.find('#new-sub-keyword-div');
            $newSubKwDiv.html(data.html_data);
            $newSubKwDiv.show();
            var $newSubKwButton = $currentPage.find('#newSubKwButton');
            $newSubKwButton.hide();
            kwSequencer.drivers = data.drivers;
            if (insertAtIndex !== undefined) {
                $newSubKwDiv.attr('index', insertAtIndex);
            } else {
                $newSubKwDiv.attr('index', kwSequencer.getLastSubKwNum());
            }
        });
    },

    cancelSubKeyword: function() {
        /* This function closes already opened sub keyword block */
        var $currentPage = katana.$activeTab;
        $currentPage.find('#new-sub-keyword-div').hide();
        var $newSubKwButton = $currentPage.find('#newSubKwButton');
        $newSubKwButton.show();
    },

    saveSubKeyword: function() {
        /* This function saves current subkeyword block to wrapper keyword */
        var $currentPage = katana.$activeTab;
        var $newSubKwDiv = $currentPage.find('#new-sub-keyword-div');
        if (katana.validationAPI.init($newSubKwDiv)){
            var data = kwSequencer.generateSubKw($newSubKwDiv);
            var filteredArgs = [];
            // Remove arguments with empty values
            for (var i=0; i<data.SubKws.subKw[0].Arguments.argument.length; i++) {
                if (data.SubKws.subKw[0].Arguments.argument[i]["@value"] !== "") {
                    filteredArgs.push(Object.assign({}, data.SubKws.subKw[0].Arguments.argument[i]));
                }
            }
            data.SubKws.subKw[0].Arguments.argument = filteredArgs;
            var displayContent = kwSequencer.generateSubKeywordsDisplayHtmlBlock($currentPage.find('#kw-row-template').clone().attr('id', ''), data);
            var stepType = $newSubKwDiv.attr('sub-keyword-type') === "edit";
            var index = parseInt($newSubKwDiv.attr('index'))
            displayContent.find('[key="@SubKwStep"]').html(index+1)
            var $allTrs = $currentPage.find('#sub-keywords-table').find('tbody').find('tr');
            if (stepType && index < $allTrs.length) {
                $allTrs[index].remove();
            }
            if (index === 0 ) {
                $currentPage.find('#sub-keywords-table').find('tbody').prepend(displayContent);
            } else {
                displayContent.insertAfter($($allTrs[index-1]));
            }
            kwSequencer.redoStepNums();
            $currentPage.find('#new-sub-keyword-div').hide();
            var $newSubKwButton = $currentPage.find('#newSubKwButton');
            $newSubKwButton.show();
            var tableLength = $currentPage.find('#sub-keywords-table').find('tbody').find('tr').length;
            if (tableLength > 0) {
                $currentPage.find('#display-sub-keywords-div').show();
            }
        }
    },

    generateSubKeywordsDisplayHtmlBlock: function($container, data) {
        /* This function is to generate step data(for dispaly section) by cloning kw-row-template */
        $container = $($container.html());
        var $allKeys = $container.find('[key]').not('[key*="Arguments"]');
        for (var i=0; i<$allKeys.length; i++) {
            $($allKeys[i]).html(kwSequencer.getValueFromJson(data.SubKws.subKw[0], $($allKeys[i]).attr('key')));
        }
        $container = kwSequencer.evaluateDisplayArguments($container, data);
        return $container;
    },

    evaluateDisplayArguments: function ($container, data) {
        /* This function hides/shows the argument block (main page).
        This function should not be called independently */
        var $templateArg = $container.find('[key="Arguments.argument"]').clone();
        var $argBlock = $container.find('[key="Arguments"]').empty();
        for (var i=0; i<data.SubKws.subKw[0].Arguments.argument.length; i++) {
            var $currentArgBlock = $templateArg.clone();
            $currentArgBlock.find('[key="Arguments.argument.@name"]').html(data.SubKws.subKw[0].Arguments.argument[i]["@name"]);
            $currentArgBlock.find('[key="Arguments.argument.@value"]').html(data.SubKws.subKw[0].Arguments.argument[i]["@value"]);
            $argBlock.append($currentArgBlock);
        }
        return $container;
    },

    generateSubKw: function($container) {
        /* This function generates json data from subkeyword block */
        // TODO: See if partialData can be directly assigned to 'finalJson.SubKws.subKw' instead of pushing into an array
        var finalJson = {SubKws: { subKw: []}};
        var $allSubKws = $container.attr('key') === 'subKw'? [$container] : $container.find('[key="subKw"]');
        var $allKeys = false;
        var partialData = false;
        for (var i=0; i <$allSubKws.length; i++) {
            $allKeys = $($allSubKws[i]).find('[key]').not('[key*="Arguments"]');
            partialData = {};
            for (var j=0; j<$allKeys.length; j++) {
                var key = $($allKeys[j]).attr("key").trim();
                var value = $($allKeys[j]).val() ? $($allKeys[j]).val().trim() : $($allKeys[j]).html().trim();
                $.extend(true, partialData, kwSequencer._updateJson(key, value));
            }
            $.extend(true, partialData, kwSequencer.generateArguments($($allSubKws[i]).find('[key="Arguments.argument"]')));
            finalJson.SubKws.subKw.push(partialData);
        }
        return finalJson;
    },

    generateArguments: function ($container) {
        /* This function creates arguments json out of an HTML block. Typically this function should
        never be called independently. */
        var finalJson = {Arguments: {argument: []}};
        var partialData = false;
        var $argBlock = false;
        for (var i=0; i<$container.length; i++) {
            $argBlock = $($container[i]).find('[key]');
            partialData = {};
            for (var j=0; j<$argBlock.length; j++) {
                var key = $($argBlock[j]).attr("key").trim();
                var val = $($argBlock[j]).val() ? $($argBlock[j]).val().trim() : $($argBlock[j]).attr('value');
                var value = val ? val.trim() : $($argBlock[j]).html().trim();
                $.extend(true, partialData, kwSequencer._updateJson(key, value));
            }
            finalJson.Arguments.argument.push(Object.assign({}, partialData.Arguments.argument));
        }
        return finalJson;
    },

    _updateJson: function (unrefined_key, value) {
        /* This function iterates through a json recursively and inserts the value for the given key at the correct place.
         * This function should never be called independently */
        var data = {};
        var key = unrefined_key.split(/\.(.+)/)[0];
        var remaining_key = unrefined_key.split(/\.(.+)/)[1];
        if (key !== undefined && remaining_key !== undefined) {
            data[key] = kwSequencer._updateJson(remaining_key, value)
        } else {
            data[unrefined_key] = value;
        }
        return data;
    },

    getValueFromJson: function (data, unrefined_key) {
        /* This function iterates through a json recursively and gets the value for the given key.
        This function should never be called independently */
        var key = unrefined_key.split(/\.(.+)/)[0];
        var remaining_key = unrefined_key.split(/\.(.+)/)[1];
        if (key !== undefined && remaining_key !== undefined) {
            return cases.getValueFromJson(data[key], remaining_key)
        }
        return data[key];
    },

    getDriverKeywords: function($elem, kwName) {
        /* This function is to update/add all available keywords to 'Keywords'
        option of sub keyword block */
        $elem = $elem ? $elem : $(this);
        kwName = kwName ? kwName : "";
        var driverName = $elem.val();
        var $kwRow = $elem.closest('.row').next();
        $kwRow.find('#stepKeyword').html("<option selected disabled hidden>Select Keyword</option>");
        if ((kwSequencer.drivers) && (driverName in kwSequencer.drivers)) {
            for (var key in kwSequencer.drivers[driverName].actions){
                if (kwSequencer.drivers[driverName].actions.hasOwnProperty(key)){
                    if (key === kwName) {
                        $kwRow.find('#stepKeyword').append('<option selected>' + key + '</option>');
                    } else {
                        $kwRow.find('#stepKeyword').append('<option>' + key + '</option>');
                    }
                }
            }
        }
        // To reset Siganture/Arguemnts/wDescription/Comments blocks
        kwSequencer.getArgumentsEtc($kwRow.find('#stepKeyword'));
    },

    getArgumentsEtc: function($elem) {
        /* This function internally calls the _setSignature, _setArguments, _setWDescription, _setComments
        functions for upadting those fields on kw name change */
        $elem = $elem ? $elem : $(this);
        var kwName = $elem.val();
        var driverName = $elem.closest('.row').prev().find('#stepDriver').val();
        var data = false;

        if ((kwSequencer.drivers) && (driverName in kwSequencer.drivers)) {
            if (kwName in kwSequencer.drivers[driverName].actions) {
                data = kwSequencer.drivers[driverName].actions[kwName]
            }
        }
        kwSequencer._setSignature($elem.closest('.row').next(), data);
        kwSequencer._setArguments($elem.closest('.row').next().next(), data);
        kwSequencer._setWDescription($elem.closest('.row').next().next().next(), data);
        kwSequencer._setComments($elem.closest('.row').next().next().next().next(), data);
    },

    _setSignature: function ($topLevelSignRow, data) {
        /* This function hides/shows corresponding function signature */
        $topLevelSignRow.hide();
        if (data) {
            $topLevelSignRow.find('textarea').html(data.signature);
            $topLevelSignRow.show();
        }
    },

    _setArguments: function ($topLevelArgRow, data) {
        /* This function hides/shows corresponding arguments */
        var $argRow = $topLevelArgRow.find('#arg-template').attr('key', 'Arguments.argument').clone().show();
        var $argContainer = $topLevelArgRow.find('.container-fluid');
        //$topLevelArgRow.find('#arg-template').remove();
        $argContainer.children().slice(1).remove();
        $topLevelArgRow.hide();
        var temp = false;

        if (data) {
            for (var i=0; i<data.arguments.length; i++){
                temp = $argRow.clone();
                temp.find('.subkw-label').attr('for', data.arguments[i]);
                temp.find('.subkw-label').html(data.arguments[i]);
                temp.find('.subkw-text').find('input').attr('id', data.arguments[i]);
                $argContainer.append(temp.clone());
                $topLevelArgRow.show();
            }
        }
    },

    _setWDescription: function ($topLevelWDescRow, data) {
        /* This function hides/shows corresponding description */
        $topLevelWDescRow.hide();
        if (data) {
            $topLevelWDescRow.find('textarea').html(data.wdesc);
            $topLevelWDescRow.show();
        }
    },

    _setComments: function ($topLevelCommentsRow, data) {
        /* This function hides/shows corresponding comments */
        $topLevelCommentsRow.hide();
        if (data) {
            $topLevelCommentsRow.find('textarea').html(data.comments);
            $topLevelCommentsRow.show();
        }
    },

    getLastSubKwNum: function () {
        /* This function gets the last sub-keyword number */
        return katana.$activeTab.find('#sub-keywords-table').find('tbody').children('tr').length;
    },

    redoStepNums: function() {
        /* This fucntion is to redo step numbers after insert/edit/delete operations */
        var $tbodyElem = katana.$activeTab.find('#display-sub-keywords-div').find('table').find('tbody');
        var $allTrElems = $tbodyElem.children('tr');
        for (var i=0; i<$allTrElems.length; i++){
            $($($allTrElems[i]).children('td')[0]).html(i+1);
        }
    },

    stepSection: {
        selectStep: function () {
            /* This function selects a sub-keyword */
            var $elem = $(this);
            var $allTrElems = $elem.parent().children('tr');
            if ($elem.attr('marked') === 'true') {
                $elem.attr('marked', 'false');
                $elem.css('background-color', '');
            } else {
                var multiselect = katana.$activeTab.find('.kwsequencer-subkw-toolbar').find('.fa-th-list').attr('multiselect');
                if (multiselect === 'off'){
                    for (var i=0; i<$allTrElems.length; i++){
                        $($allTrElems[i]).attr('marked', 'false');
                        $($allTrElems[i]).css('background-color', '');
                    }
                }
                $elem.attr('marked', 'true');
                $elem.css('background-color', 'khaki');
            }
        },

        toolbar: {
            multiselect: function() {
                /* This function de/activates the multiselect functionality for a sub-keyword */
                var $elem = $(this);
                var $iconElem = $elem.children('i');
                if ($iconElem.attr('multiselect') === 'on'){
                    $iconElem.attr('multiselect', 'off');
                    $iconElem.removeClass('badged');
                    $iconElem.children('i').hide();
                    var $allTrElems = katana.$activeTab.find('#display-sub-keywords-div').find('tbody').children('tr');
                    for (var i=0; i<$allTrElems.length; i++){
                        $($allTrElems[i]).attr('marked', 'false');
                        $($allTrElems[i]).css('background-color', 'white');
                    }
                } else {
                    $iconElem.attr('multiselect', 'on');
                    $iconElem.addClass('badged');
                    $iconElem.children('i').show()
                }
            },

            deleteStep: function () {
                /* This function deletes a sub-keyword */
                var $tbodyElem = katana.$activeTab.find('#display-sub-keywords-div').find('tbody');
                var $allTrElems = $tbodyElem.children('tr[marked="true"]');
                if ($allTrElems.length === 0) {
                    katana.openAlert({"alert_type": "danger",
                        "heading": "No keyword selected for deletion",
                        "text": "Please select at least one keyword to delete",
                        "show_cancel_btn": "false"})
                } else {
                    var stepNumbers = "";
                    for (var i=0; i<$allTrElems.length; i++){
                        stepNumbers += ($($allTrElems[i]).index() + 1).toString() + ", "
                    }
                    stepNumbers = stepNumbers.slice(0, -2);
                    katana.openAlert({"alert_type": "warning",
                        "heading": "This would delete keyword(s) " + stepNumbers,
                        "text": "Are you sure you want to delete these keyword(s)?"},
                        function () {
                            for (var i=0; i<$allTrElems.length; i++){
                                $($allTrElems[i]).remove();
                            }
                            kwSequencer.redoStepNums();
                            var tableLength = katana.$activeTab.find('#sub-keywords-table').find('tbody').find('tr').length;
                            if (tableLength == 0) {
                                katana.$activeTab.find('#display-sub-keywords-div').hide();
                            }
                            kwSequencer.cancelSubKeyword();
                        })
                }

            },

            insertStep: function () {
                /* This function opens a new sub-keyword and inserts it into a speific spot when saved */
                var $elem = $(this);
                var $tbodyElem = katana.$activeTab.find('#display-sub-keywords-div').find('tbody');
                var $allTrElems = $tbodyElem.children('tr[marked="true"]');
                if ($allTrElems.length === 0) {
                    var insertAtIndex = $tbodyElem.children('tr').length;
                } else if ($allTrElems.length > 1) {
                    katana.openAlert({
                        "alert_type": "danger",
                        "heading": "Multiple keywords selected",
                        "text": "Only one keyword can be inserted at a time. Please select only one " +
                        "keyword above which you want to insert another keyword.",
                        "show_cancel_btn": false
                    });
                    return;
                } else {
                    insertAtIndex = $($allTrElems[0]).index();
                }
                katana.$activeTab.find('#new-sub-keyword-div').attr('sub-keyword-type', 'insert')
                kwSequencer.newSubKeyword(insertAtIndex);
            },

            editStep: function () {
                /* This function opens the step in the step editor and replaces the existing step when saved */
                var $elem = $(this);
                var $tbodyElem = katana.$activeTab.find('#display-sub-keywords-div').find('tbody');
                var $allTrElems = $tbodyElem.children('tr[marked="true"]');
                if ($allTrElems.length === 0) {
                    katana.openAlert({
                        "alert_type": "danger",
                        "heading": "No keyword selected",
                        "text": "Please select a keyword to edit.",
                        "show_cancel_btn": false
                    });
                } else if ($allTrElems.length > 1) {
                    katana.openAlert({
                        "alert_type": "danger",
                        "heading": "Multiple keywords selected",
                        "text": "Only one keyword can be edited at a time. Please select only one " +
                        "keyword to edit.",
                        "show_cancel_btn": false
                    });
                } else {
                    var data = kwSequencer.generateSubKw($($allTrElems[0]));
                    var $container = katana.$activeTab.find('#new-sub-keyword-div').show().attr('sub-keyword-type', 'edit').attr('index', $($allTrElems[0]).index());
                    $container = kwSequencer.editSubKeywordHtmlBlock($container, data);
                    var $newSubKwButton = katana.$activeTab.find('#newSubKwButton');
                    $newSubKwButton.hide();
                }
            }
        }
    },

    editSubKeywordHtmlBlock: function ($container, data) {
        /* This function edits the sub keyword block based on json data */
        var $driver = $container.find('[key="@Driver"]');
        var driverName = kwSequencer.getValueFromJson(data.SubKws.subKw[0], "@Driver");
        var kwName = kwSequencer.getValueFromJson(data.SubKws.subKw[0], "@Keyword");
        var $allOptions = $($driver).children();
        for (var i=0; i<$allOptions.length; i++) {
            if ($($allOptions[i]).text() === driverName) {
                $($allOptions[i]).prop('selected', true);
                kwSequencer.getDriverKeywords($driver, kwName);
                break;
            }
        }
        var $allArgs = $container.find('[key="Arguments.argument"]');
        for (var i=0 ; i<$allArgs.length; i++) {
            var currentArg = $($allArgs[i]).find('label').text();
            for (var j=0; j<data.SubKws.subKw[0].Arguments.argument.length; j++) {
                if (data.SubKws.subKw[0].Arguments.argument[j]["@name"] === currentArg) {
                    $($allArgs[i]).find('[key="Arguments.argument.@value"]').attr('value', data.SubKws.subKw[0].Arguments.argument[j]["@value"]);
                    break;
                }
            }
        }
        return $container;
    },

    validations: {
        checkIfEmpty: function() {
            /* This fucntion to validate a field to check if it is empty */
            var $elem = $(this);
            if ($elem.val() == null || $elem.val().trim() === "") {
                katana.validationAPI.addFlag( $elem, 'Required field');
            }
        },
    },

    getWrapperKwDetails: function($container) {
        /* This fucntion is to get the Wrapper keyword details */
        var $allValues = $container.find('[key]');
        var result = {};
        for (var i=0; i<$allValues.length; i++) {
            var key = $($allValues[i]).attr("key").trim();
            var value = $($allValues[i]).val() ? $($allValues[i]).val().trim() : $($allValues[i]).html().trim();
            result[key] = value
        }
        return result;
    },

    getSubKeywordDetails: function($container) {
        /* This function is to get all subkeyword details from table */
        var $allTrElems = $container.find('tbody').children('tr');
        var result = [];
        for (var i=0; i<$allTrElems.length; i++) {
            var data = kwSequencer.generateSubKw($($allTrElems[i]));
            result.push(data.SubKws.subKw[0]);
        }
        return result;
    },

    removeNonActionFiles: function(children) {
        /* This function is to remove nonAction files from jsontree json
        Input for this method : Output(s) of navigator_util.get_dir_tree_json method in array */
        // Add new nonActions files to nonActionFiles array if required
        var nonActionFiles = ["__init__.py", "__pycache__"];
        var new_children = [];
        for (var i = 0; i < children.length; i++) {
            var child = children[i];
            var new_child = {};
            if (!(nonActionFiles.indexOf(child['text']) > -1)) {
                for (var val in child) {
                    if (val == "children") {
                        new_child['children'] = kwSequencer.removeNonActionFiles(child['children']);
                    } else {
                        new_child[val] = child[val];
                    }
                }
                new_children.push(new_child);
            }
        }
        return new_children;
    },
};
