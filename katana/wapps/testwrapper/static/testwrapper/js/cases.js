var setupcases = {

    mappings: {
        newStep: {
            drivers: false, //stores all drivers and actions' information
            repos: false, //stores all the repos and actions information
            title:  "New Step" //drawer title for when new step is being edited
        },
        newReq: {
            title: "New Requirement" //drawer title for when new req is being edited
        },
        editDetails: {
            title: "Edit Details" //drawer title for when details are being edited
        },
        editReq: {
            title: "Edit Requirement" //drawer title for when existing req is being edited
        },
        editStep: {
            title: "Edit Step" //drawer title for when existing step is being edited
        }
    },

    header: {
        toggleContents: function() {
            /* This function toggles the content when up/down font-awesomes are clicked */
            var $elem = $(this);
            if ($elem.attr('collapsed') === 'false') {
                $elem.attr('collapsed', 'true');
                $elem.removeClass('fa-chevron-circle-up');
                $elem.addClass('fa-chevron-circle-down');
                $elem.closest('.cases-header').next().hide()
            } else {
                $elem.attr('collapsed', 'false');
                $elem.removeClass('fa-chevron-circle-down');
                $elem.addClass('fa-chevron-circle-up');
                $elem.closest('.cases-header').next().show()
            }
        },

        editDetails: function() {
                document.getElementById("hiddingsecond").style.display="none";
               document.getElementById("hiddingfirst").style.display="none";
               document.getElementById("hiddingthird").style.display="none";

               document.getElementById("editfirst").style.display="none";
               document.getElementById("editthird").style.display="none";
               document.getElementById("editsecond").style.display="none";

                document.getElementById("editDetails").style.display="block";
            /* This function gets data from displayed details block and
            creates the details block in the side drawer*/
            var $elem = $(this);
            var data = setupcases.generateJson.generateDetails($elem.closest('#main-div').find('#detail-block'));
            setupcases.drawer.openClosedDrawer(setupcases.mappings.editDetails.title);
            setupcases.drawer.open.highlightSidebar(0);
            setupcases.drawer.open.switchView.details($elem.closest('#main-div').find('#details_drawer_template').clone(), data);
        },

        newReq: function() {
            /* This function creates a new requirements block in the side drawer*/
            var $elem = $(this);
            setupcases.drawer.openClosedDrawer(setupcases.mappings.newReq.title);
            setupcases.drawer.open.highlightSidebar(1);
            setupcases.drawer.open.switchView.requirements($elem.closest('#main-div').find('#reqs_drawer_template').clone());
        },

        newStep: function() {
            /* This function creates a new step block in the side drawer*/
               document.getElementById("hiddingsecond").style.display="none";
               document.getElementById("hiddingfirst").style.display="block";
               document.getElementById("hiddingthird").style.display="none";

               document.getElementById("editfirst").style.display="none";
               document.getElementById("editthird").style.display="none";
               document.getElementById("editsecond").style.display="none";

               document.getElementById("editDetails").style.display="none";
            var $elem = $(this);
            setupcases.drawer.openClosedDrawer(setupcases.mappings.newStep.title);
            setupcases.drawer.open.highlightSidebar(2);
            var $container = $elem.closest('#main-div').find('#steps_drawer_template').clone().attr('step-type', 'edit').attr('index', setupcases.getLastStepNum());
            setupcases.drawer.open.switchView.steps($container, false, setupcases.getLastStepNum() + 1);
        }
    },

    drawer: {

        openDatafile: function () {
            /* This function opens the datafile in the datafile editor*/
            var $elem = $(this);
            var $inputElem = $elem.parent().prev().children('input');
            var tcPath = katana.$activeTab.find('#main-div').attr("current-file");
            var idfPath = katana.utils.getAbsoluteFilepath(tcPath, $inputElem.val(), true);
            $.ajax({
                headers: {
                    'X-CSRFToken': katana.$activeTab.find('input[name="csrfmiddlewaretoken"]').attr('value')
                },
                type: 'POST',
                url: 'check_if_file_exists/',
                data: {"path": idfPath}
            }).done(function(data){
                var pd = { type: 'POST',
                    headers: {'X-CSRFToken': katana.$activeTab.find('input[name="csrfmiddlewaretoken"]').attr('value')},
                    data:  {"path": idfPath}};
                if (data.exists) {
                    katana.templateAPI.load('/katana/wdf/index/', '/static/wdf_edit/js/main.js,',
                        null, 'WDF Editor', null, pd)
                } else {
                    katana.openAlert({
                        "alert_type": "danger",
                        "heading": "Problem Opening " + $inputElem.val(),
                        "text": "It seems like the file may not be available for viewing.",
                        "show_cancel_btn": false
                    });
                }
            });
        },

        openClosedDrawer: function (title) {
            /* This function opens the closed side Drawer*/
            var $drawerClosedDiv = katana.$activeTab.find('#main-div').find('.cases-side-drawer-closed');
            var $drawerOpenDiv = $drawerClosedDiv.siblings('.cases-side-drawer-open');
            $drawerClosedDiv.hide();
            $drawerOpenDiv.show();
            $drawerOpenDiv.find('.cases-drawer-open-header').find('h4').html(title);
        },

        closeOpenedDrawer: function () {
            /* This function closes the opened side Drawer*/
            var $drawerClosedDiv = katana.$activeTab.find('#main-div').find('.cases-side-drawer-closed');
            var $drawerOpenDiv = $drawerClosedDiv.siblings('.cases-side-drawer-open');
            $drawerClosedDiv.show();
            $drawerOpenDiv.hide();
        },

        open: {

            highlightSidebar: function (childIndex) {
                /* This function highlights the icon in the drawer sidebar */
                var $sidebarIcons = $(katana.$activeTab.find('.cases-drawer-open-body').find('.sidebar').children('div'));
                for (var i=0; i<$sidebarIcons.length; i++){
                    $($sidebarIcons[i]).removeClass('cases-icon-bg-color').addClass('cases-sidebar-disabled-icon');
                }
                $($sidebarIcons[childIndex]).addClass('cases-icon-bg-color').removeClass('cases-sidebar-disabled-icon');
            },

            switchView: {

                details: function($container, data) {
                    /* This function generates the details html for the drawer and attaches it to the drawer */
                    $container.attr("id", "current_details_editor").show();
                    setupcases.generateDetailsDisplayHtmlBlock($container, data);
                    katana.$activeTab.find('#details_drawer_template').parent().prepend(setupcases.proofDetailsContainer($container));
                },

                requirements: function($container, data, current) {
                    /* This function generates the reqs html for the drawer and attaches it to the drawer */
                    $container.attr("id", "current_reqs_editor").show();
                    if (data) {
                        $container.attr('current', current);
                        $container.find('input[key="Requirement"]').attr('value', data).val(data);
                    }
                    katana.$activeTab.find('#reqs_drawer_template').parent().prepend($container);
                },

                steps: function($container, data, stepNum) {
                    /* This function generates the step html for the drawer and attaches it to the drawer */
                    $container.attr("id", "current_steps_editor").show();
                    if (data) {
                        $container = setupcases.generateStepsHtmlBlock($container, data);
                    } else {
                        $container = setupcases.addTsToStepsHtmlBlock($container, stepNum);
                    }
                    katana.$activeTab.find('#steps_drawer_template').parent().prepend(setupcases.proofStepsContainer($container));
                }

            },

            saveContents: function () {
                /* This function calls specific functions internally that save information on the frontend */
                var $elem = $(this);
                var saved = false;
                var $openDrawer = $elem.closest('.cases-side-drawer-open');
                var $switchElem = $openDrawer.find('.cases-drawer-open-body').find('.sidebar').find('.cases-icon-bg-color').children('i');
                if ($switchElem) {
                    var reference = $switchElem.attr('ref');
                    if (reference === "editDetails") {
                        saved = setupcases.drawer.open._saveContents.details($openDrawer.find('.content').find('#current_details_editor'));
                    } else if (reference === "newReq") {
                        saved = setupcases.drawer.open._saveContents.requirements($openDrawer.find('.content').find('#current_reqs_editor'));
                    } else if (reference === "newStep") {
                        saved = setupcases.drawer.open._saveContents.steps($openDrawer.find('.content').find('#current_steps_editor'));
                    }
                    if (saved) {
                        $openDrawer.find('.cases-drawer-open-body').find('.content').find('[id^="current"]').remove();
                        setupcases.drawer.closeOpenedDrawer();
                    }
                }
            },

            _saveContents: {

                details: function ($container) {
                    /* This function collects details data from the drawer and adds it to the displayed details block*/
                    if (katana.validationAPI.init($container)) {
                        var data = setupcases.generateJson.generateDetails($container);
                        var displayContent = setupcases.generateDetailsDisplayHtmlBlock(katana.$activeTab.find('#cases-display-template').clone(), data);
                        katana.$activeTab.find('#cases-display-template').replaceWith(displayContent);
                        return true;
                    } else {
                        return false;
                    }
                },

                requirements: function ($container) {
                    /* This function collects reqs data from the drawer and adds it to the displayed reqs block*/
                    if (katana.validationAPI.init($container)) {
                        var data = setupcases.generateJson.generateRequirements(katana.$activeTab.find('#cases-requirements-template'));
                        var temp = setupcases.generateJson.generateRequirements($container);
                        var index = $container.attr('current') ? $container.attr('current') : data.Requirements.Requirement.length;
                        data.Requirements.Requirement.splice(index, 1, temp.Requirements.Requirement[0]);
                        var displayContent = setupcases.generateRequirementsHtmlBlock(katana.$activeTab.find('#cases-requirements-template').clone(), data);
                        katana.$activeTab.find('#cases-requirements-template').replaceWith(displayContent);
                        return true;
                    } else {
                        return false;
                    }
                },

                steps: function ($container) {
                    /* This function collects step data from the drawer and adds it to the displayed step block*/
                    if (katana.validationAPI.init($container)) {
                        var data = setupcases.generateJson.generateStep($container);
                        var filteredArgs = [];
                        for (var i=0; i<data.Setup.step[0].Arguments.argument.length; i++) {
                            if (data.Setup.step[0].Arguments.argument[i]["@value"] !== "") {
                                filteredArgs.push(Object.assign({}, data.Setup.step[0].Arguments.argument[i]));
                            }
                        }
                        data.Setup.step[0].Arguments.argument = filteredArgs;
                        var displayContent = setupcases.generateStepsDisplayHtmlBlock(katana.$activeTab.find('#step-row-template').clone().attr('id', ''), data);
                        var stepType = $container.attr('step-type') === "edit";
                        var index = parseInt($container.attr('index'));
                        var $allTrs = katana.$activeTab.find('#cases-steps-template').find('tbody').find('tr');
                        if (stepType && index < $allTrs.length) {
                            $allTrs[index].remove();
                        }
                        if (index === 0) {
                            katana.$activeTab.find('#cases-steps-template').find('tbody').prepend(displayContent);
                            setupcases.redoStepNums();
                        } else {
                            displayContent.insertAfter($($allTrs[index-1]));
                            setupcases.redoStepNums();
                        }
                        return true;
                    } else {
                        return false;
                    }
                }
            },

            discardContents: function () {
                /* This function deletes contents from the drawer */
                var $elem = $(this);
                var $openDrawer = $elem.closest('.cases-side-drawer-open');
                katana.openAlert({
                    "alert_type": "warning",
                    "heading": "All changes will be discarded",
                    "text": "This action will discard all changes, are you sure you want to continue?"
                    }, function () {
                        $openDrawer.find('.cases-drawer-open-body').find('.content').find('[id^="current"]').remove();
                        setupcases.drawer.closeOpenedDrawer();
                    })
            }
        },

        openFileExplorer: {

            logsOrResultsDir: function (relative, $elem) {
                /* This common function gets filepath from the fileexplorer and ataches it to the correct input field*/
                $elem = $elem ? $elem : $(this);
                var $inputElem = $elem.parent().prev().children('input');
                relative = !!relative;
                katana.fileExplorerAPI.openFileExplorer("Select a Path", false,
                    katana.$activeTab.find('input[name="csrfmiddlewaretoken"]').attr('value'), false,
                    function (inputValue){
                        if (relative) {
                            var tcPath = katana.$activeTab.find('#main-div').attr("current-file");
                            inputValue = katana.utils.getRelativeFilepath(tcPath, inputValue, true);
                        }
                        $inputElem.val(inputValue);
                        $inputElem.attr('value', inputValue);
                    },
                    false)
            },

            inputDataFile: function () {
                /* This function calls logsOrResultsDir with relative as true so that relative path is created. */
                setupcases.drawer.openFileExplorer.logsOrResultsDir(true, $(this));
            }
        }
    },

    invert: function(){
        /* This function switches between the testcase files view and the actual testcase */
        var toolbarButtons = katana.$activeTab.find('.tool-bar').find('button');
        for(var i=0; i<toolbarButtons.length; i++){
            if($(toolbarButtons[i]).is(":hidden")){
                $(toolbarButtons[i]).show();
            } else {
                $(toolbarButtons[i]).hide();
            }
        }
        var divs = katana.$activeTab.find('#body-div').children();
        for(i=0; i<divs.length; i++){
            if($(divs[i]).is(":hidden")){
                $(divs[i]).show();
            } else {
                $(divs[i]).hide();
            }
        }
    },

    landing: {
        init: function(){
            /* This function get the list of testcase files, displays them, and
            attaches click event on each testcase file */
            $.ajax({
                type: 'GET',
                url: 'testwrapper/get_list_of_testwrappers/'
            }).done(function(data){
                katana.jsTreeAPI.createJstree(katana.$activeTab.find('#tree-div'), data.data);
                katana.$activeTab.find('#tree-div').on("select_node.jstree", function (e, data){
                    if (data["node"]["icon"] === "jstree-file") {
                        $.ajax({
                            headers: {
                                'X-CSRFToken': katana.$activeTab.find('.csrf-container').html()
                            },
                            type: 'GET',
                            url: 'testwrapper/get_file/',
                            data: {"path": data["node"]["li_attr"]["data-path"]}
                        }).done(function(data){
                            if(data.status){
                               setupcases.invert();
                                katana.$activeTab.find('#main-div').attr("current-file", data.filepath);
                                 katana.$activeTab.find('.tool-bar').find('.title').html(data.filename);
                                katana.$activeTab.find('#main-div').html(data.html_data);
                                 setupcases.mappings.newStep.drivers = data.drivers;
                            } else {
                                katana.openAlert({"alert_type": "danger",
                                    "heading": "Could not open file",
                                    "text": "Errors: " + data.message,
                                    "show_cancel_btn": false})
                            }
                        });
                    }
                });
            })
        },

        openNewFile: function(){
            /* This function opens a new testcase */
            $.ajax({
                headers: {
                    'X-CSRFToken': katana.$activeTab.find('.csrf-container').html()
                },
                type: 'GET',
                url: 'testwrapper/get_file/',
                data: {"path": false}
            }).done(function(data){
                if (data.filepath==''){
                    katana.openAlert({"alert_type": "danger",
                    "heading": "Please setup the path in warrior settings",
                    "text": "Errors: " + 'Path is not provided',
                    "show_cancel_btn": false});
                    return;
                }
                if(data.status){
                    setupcases.invert();
                    katana.$activeTab.find('#main-div').attr("current-file", data.filepath);
                    katana.$activeTab.find('.tool-bar').find('.title').html(data.filename);
                    katana.$activeTab.find('#main-div').html(data.html_data);
                    setupcases.mappings.newStep.drivers = data.drivers;
                } else {
                    katana.openAlert({"alert_type": "danger",
                        "heading": "Could not open file",
                        "text": "Errors: " + data.message,
                        "show_cancel_btn": false})
                }

            });
        }

    },

    caseViewer:  {
        close: function () {
            /* This function closes the testcase */
            katana.$activeTab.find('#main-div').html("");
            katana.$activeTab.find('.tool-bar').find('.title').html("");
            setupcases.invert();
        },

        save: function () {
            /* This function collects data from each displayed block and saves the testcase */
            var final_json = {"TestWrapper": {}};
            var filepath = katana.$activeTab.find('#main-div').attr("current-file");
            var filename = katana.$activeTab.find('.tool-bar').find('.title').html();
            $.extend(true, final_json.TestWrapper, setupcases.generateJson.generateDetails(katana.$activeTab.find('#detail-block')));
            $.extend(true, final_json.TestWrapper, setupcases.generateJson.generateRequirements(katana.$activeTab.find('#req-block')));
            $.extend(true, final_json.TestWrapper, setupcases.generateJson.generateStep(katana.$activeTab.find('#step-block')));
            $.extend(true, final_json.TestWrapper, cleanupcases.generateJson.generateStep(katana.$activeTab.find('#step-block-cleanup')));
            $.extend(true, final_json.TestWrapper, debugcases.generateJson.generateStep(katana.$activeTab.find('#step-block-debug')));


            var callBack_on_accept = function(inputValue) {
                $.ajax({
                    headers: {
                        'X-CSRFToken': katana.$activeTab.find('input[name="csrfmiddlewaretoken"]').attr('value')
                    },
                    type: 'POST',
                    url: 'testwrapper/save_file/',
                    data: {"data": JSON.stringify(final_json), "directory": filepath, "filename": inputValue, "extension": ".xml"}
                }).done(function(data){
                    if (data.status) {
                        katana.openAlert({
                            "alert_type": "success",
                            "heading": "File Saved",
                            "text": inputValue + " has been saved successfully",
                            "show_cancel_btn": false
                        });
                        setupcases.caseViewer.close();
                        window.setTimeout(function(){window.location.reload()}, 2000)
                    } else {
                        katana.openAlert({
                            "alert_type": "danger",
                            "heading": "File Not Saved",
                            "text": "Some problem occurred while saving the file: " + inputValue,
                            "show_cancel_btn": false
                        })
                    }
                });
            };

            katana.openAlert({
                "alert_type": "light",
                "heading": "Name for the file",
                "text": "",
                "prompt": "true",
                "prompt_default": filename
                },
                function(inputValue){
                $.ajax({
                    headers: {
                        'X-CSRFToken': katana.$activeTab.find('input[name="csrfmiddlewaretoken"]').attr('value')
                    },
                    type: 'POST',
                    url: 'check_if_file_exists/',
                    data: {"filename": inputValue, "directory": filepath, "extension": ".xml"}
                }).done(function(data){
                     if(data.exists){
                        katana.openAlert({
                            "alert_type": "warning",
                            "heading": "File Exists",
                            "text": "A file with the name " + inputValue + " already exists; do you want to overwrite it?",
                            "accept_btn_text": "Yes",
                            "cancel_btn_text": "No"
                            }, function() {
                            callBack_on_accept(inputValue)}
                            )
                     } else {
                        callBack_on_accept(inputValue);
                     }
                });
            });
        }
    },

    reqSection: {
        deleteReq: function () {
            /* This function deletes a req */
            var $elem = $(this);
            var $tdParent = $elem.closest('td');
            var reqNumber = $tdParent.siblings('th').html();
            var $toBeDeleted = $elem.closest('tr');
            var $topLevel = $elem.closest('#cases-requirements-template');
            katana.openAlert({
                "alert_type": "danger",
                "heading": "Delete Requirement " + reqNumber + "?",
                "text": "Are you sure you want to delete the requirement? This cannot be undone."
            }, function(){
                $toBeDeleted.remove();
                var data = setupcases.generateJson.generateRequirements($topLevel);
                var displayContent = setupcases.generateRequirementsHtmlBlock($topLevel.clone(), data);
                $topLevel.replaceWith(displayContent);
            });
        },

        editReq: function () {
            /* This function opens a req in the req editor*/
            var $elem = $(this);
            var data = $($elem.closest('.cases-req').children('div')[0]).html().trim();
            setupcases.drawer.openClosedDrawer(cases.mappings.editReq.title);
            setupcases.drawer.open.highlightSidebar(1);
            setupcases.drawer.open.switchView.requirements($elem.closest('#main-div').find('#reqs_drawer_template').clone(), data, $elem.closest('tr').attr('req-number')-1);
        }
    },

    stepSection: {
        selectStep: function () {
            /* This function selects a step */
            var $elem = $(this);
            var $allTrElems = $elem.parent().children('tr');
            if ($elem.attr('marked') === 'true') {
                $elem.attr('marked', 'false');
                $elem.css('background-color', '');
            } else {
                var multiselect = katana.$activeTab.find('.cases-step-toolbar').find('.fa-th-list').attr('multiselect');
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
                /* This function de/activates the multiselect functionality for a step */
                var $elem = $(this);
                var $iconElem = $elem.children('i');
                if ($iconElem.attr('multiselect') === 'on'){
                    $iconElem.attr('multiselect', 'off');
                    $iconElem.removeClass('badged');
                    $iconElem.children('i').hide();
                    var $allTrElems = katana.$activeTab.find('#step-block').find('tbody').children('tr');
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
                /* This function deletes a step */
                var $tbodyElem = katana.$activeTab.find('#step-block').find('tbody');
                var $allTrElems = $tbodyElem.children('tr[marked="true"]');
                if ($allTrElems.length === 0) {
                    katana.openAlert({"alert_type": "danger",
                        "heading": "No step selected for deletion",
                        "text": "Please select at least one step to delete",
                        "show_cancel_btn": "false"})
                } else {
                    var stepNumbers = "";
                    for (var i=0; i<$allTrElems.length; i++){
                        stepNumbers += ($($allTrElems[i]).index() + 1).toString() + ", "
                    }
                    stepNumbers = stepNumbers.slice(0, -2);
                    katana.openAlert({"alert_type": "warning",
                        "heading": "This would delete Steps " + stepNumbers,
                        "text": "Are you sure you want to delete these steps?"},
                        function () {
                            for (var i=0; i<$allTrElems.length; i++){
                                $($allTrElems[i]).remove();
                            }
                            setupcases.redoStepNums();
                        })
                }
            },

            insertStep: function () {
                document.getElementById("hiddingsecond").style.display="none";
               document.getElementById("hiddingfirst").style.display="block";
               document.getElementById("hiddingthird").style.display="none";
               
               document.getElementById("editfirst").style.display="none";
               document.getElementById("editsecond").style.display="none";
               document.getElementById("editthird").style.display="none";

               document.getElementById("editDetails").style.display="none";
//                    document.getElementById("hiddingfirst").style.display="none";
                /* This function opens a new step in the step editor and inserts it into a speific spot when saved */
                var $elem = $(this);
                var $tbodyElem = katana.$activeTab.find('#step-block').find('tbody');
                var $allTrElems = $tbodyElem.children('tr[marked="true"]');
                if ($allTrElems.length === 0) {
                    var insertAtIndex = $tbodyElem.children('tr').length;
                } else if ($allTrElems.length > 1) {
                    katana.openAlert({
                        "alert_type": "danger",
                        "heading": "Multiple Steps Selected",
                        "text": "Only one step can be inserted at a time. Please select only one " +
                        "step above which you want to insert another step.",
                        "show_cancel_btn": false
                    });
                    return;
                } else {
                    insertAtIndex = $($allTrElems[0]).index();
                }

                setupcases.drawer.openClosedDrawer(setupcases.mappings.newStep.title);
                setupcases.drawer.open.highlightSidebar(2);
                var $container = $elem.closest('#main-div').find('#steps_drawer_template').clone().attr("step-type", "insert").attr("index", insertAtIndex);
                setupcases.drawer.open.switchView.steps($container, false, insertAtIndex+1);

            },

            editStep: function () {
                /* This function opens the step in the step editor and replaces the existing step when saved */
                document.getElementById("hiddingsecond").style.display="none";
               document.getElementById("hiddingfirst").style.display="none";
               document.getElementById("hiddingthird").style.display="none";

               document.getElementById("editfirst").style.display="block";
               document.getElementById("editsecond").style.display="none";
               document.getElementById("editthird").style.display="none";

               document.getElementById("editDetails").style.display="none";
                var $elem = $(this);
                var $tbodyElem = katana.$activeTab.find('#step-block').find('tbody');
                var $allTrElems = $tbodyElem.children('tr[marked="true"]');
                if ($allTrElems.length === 0) {
                    katana.openAlert({
                        "alert_type": "danger",
                        "heading": "No Step Selected",
                        "text": "Please select a step to edit.",
                        "show_cancel_btn": false
                    });
                } else if ($allTrElems.length > 1) {
                    katana.openAlert({
                        "alert_type": "danger",
                        "heading": "Multiple Steps Selected",
                        "text": "Only one step can be edited at a time. Please select only one " +
                        "step to edit.",
                        "show_cancel_btn": false
                    });
                } else {
                    var data = setupcases.generateJson.generateStep($($allTrElems[0]));
                    setupcases.drawer.openClosedDrawer(setupcases.mappings.editStep.title);
                    setupcases.drawer.open.highlightSidebar(2);
                    var $container = $elem.closest('#main-div').find('#steps_drawer_template').clone().attr('step-type', 'edit').attr('index', $($allTrElems[0]).index());
                    setupcases.drawer.open.switchView.steps($container, data);
                }
            }
        }
    },

    generateJson: {

        generateDetails: function ($container) {
            /* This function creates details json out of an HTML block */
            var finalJson = {Details: {}};
            var $allKeys = $container.find('[key]');
            var value = false;
            for (var i=0; i <$allKeys.length; i++) {
                value = $($allKeys[i]).val() ? $($allKeys[i]).val().trim() : $($allKeys[i]).html().trim();
                $.extend(true, finalJson.Details, setupcases.generateJson._updateJson($($allKeys[i]).attr("key").trim(), value));
            }
            return finalJson;
        },

        generateRequirements: function ($container) {
            /* This function creates requirements json out of an HTML block */
            var finalJson = {Requirements: { Requirement: []}};
            var $allKeys = $container.find('[key]');
            var value = false;
            for (var i=0; i <$allKeys.length; i++) {
                value = $($allKeys[i]).val() ? $($allKeys[i]).val().trim() : $($allKeys[i]).html().trim();

            }
            return ;
        },

        generateStep: function ($container) {
            /* This function creates steps json out of an HTML block */
            var finalJson = {Setup: { step: []}};
            var $allSteps = $container.attr('key') === 'step'? [$container] : $container.find('[key="step"]');
            var $allKeys = false;
            var partialData = false;
            for (var i=0; i <$allSteps.length; i++) {
                $allKeys = $($allSteps[i]).find('[key]').not('[key*="Execute.Rule"]').not('[key*="Arguments"]');
                partialData = {};
                for (var j=0; j<$allKeys.length; j++) {
                    var key = $($allKeys[j]).attr("key").trim();
                    var value = $($allKeys[j]).val() ? $($allKeys[j]).val().trim() : $($allKeys[j]).html().trim();
                    $.extend(true, partialData, setupcases.generateJson._updateJson(key, value));
                }
                $.extend(true, partialData, setupcases.generateJson.generateArguments($($allSteps[i]).find('[key="Arguments.argument"]')));
                $.extend(true, partialData, setupcases.generateJson.generateExecuteRules($($allSteps[i]).find('[key="Execute.Rule"]')));
                finalJson.Setup.step.push(partialData);
            }
            return finalJson
        },

        generateExecuteRules: function ($container){
            /* This function creates execute (rules) json out of an HTML block. Typically this function should
            never be called independently. */
            var finalJson = {Execute: {Rule: []}};
            var partialData = false;
            var $ruleBlock = false;
            for (var i=0; i<$container.length; i++) {
                $ruleBlock = $($container[i]).find('[key]');
                partialData = {};
                for (var j=0; j<$ruleBlock.length; j++) {
                    var key = $($ruleBlock[j]).attr("key").trim();
                    var val = $($ruleBlock[j]).val() ? $($ruleBlock[j]).val().trim() : $($ruleBlock[j]).attr('value');
                    var value = val ? val.trim() : $($ruleBlock[j]).html().trim();
                    $.extend(true, partialData, setupcases.generateJson._updateJson(key, value));
                }
                finalJson.Execute.Rule.push(Object.assign({}, partialData.Execute.Rule));
            }
            return finalJson;
        },

        generateArguments: function ($container){
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
                    $.extend(true, partialData, setupcases.generateJson._updateJson(key, value));
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
                data[key] = setupcases.generateJson._updateJson(remaining_key, value)
            } else {
                data[unrefined_key] = value;
            }
            return data;
        }
    },

    getValueFromJson: function (data, unrefined_key) {
        /* This function iterates through a json recursively and gets the value for the given key.
        This function should never be called independently */
        var key = unrefined_key.split(/\.(.+)/)[0];
        var remaining_key = unrefined_key.split(/\.(.+)/)[1];
        if (key !== undefined && remaining_key !== undefined) {
            return setupcases.getValueFromJson(data[key], remaining_key)
        }
        return data[key]
    },

    generateDetailsDisplayHtmlBlock: function ($container, data) {
        /* This function generates the details block out of an HTML block and json data */
        var $allKeys = $container.find('[key]');
        for (var i=0; i<$allKeys.length; i++) {
            if ($($allKeys[i]).prop('type') === 'text') {
                $($allKeys[i]).attr('value', setupcases.getValueFromJson(data.Details, $($allKeys[i]).attr('key')));
            } else if ($($allKeys[i]).prop('type') === 'select-one') {
                $($allKeys[i]).attr('value', setupcases.getValueFromJson(data.Details, $($allKeys[i]).attr('key')));
                var value = setupcases.getValueFromJson(data.Details, $($allKeys[i]).attr('key'));
                var $allOptions = $($allKeys[i]).children();
                for (var j=0; j<$allOptions.length; j++) {
                    if ($($allOptions[j]).text() === value) {
                        $($allOptions[j]).prop('selected', true);
                        break;
                    }
                }
            } else {
                $($allKeys[i]).html(setupcases.getValueFromJson(data.Details, $($allKeys[i]).attr('key')));
            }
        }
        return $container
    },

    generateRequirementsHtmlBlock: function ($container, data) {
        /* This function generates the requirements block out of an HTML block and json data */
        var $constantTemplate = $container.find('#req-table-template').clone().attr('id', "").show();
        var start = 0;
        var mid = Math.floor((data.Requirements.Requirement.length + 1) /2);
        var end = data.Requirements.Requirement.length;
        var $tableTemplateLeft = setupcases._generateReqTable(data, start, mid, $constantTemplate, $constantTemplate.clone());
        var $tableTemplateRight = setupcases._generateReqTable(data, mid, end, $constantTemplate, $constantTemplate.clone());
        $($container.find('.cases-internal-space')[0]).html($tableTemplateLeft);
        $($container.find('.cases-internal-space')[1]).html($tableTemplateRight);
        return $container;
    },

    _generateReqTable: function (data, start, end, $constantTemplate, $container) {
        /* This function is called by generateRequirementsHtmlBlock which creates the req block */
        var $trTemplate = false;
        $container.find('tr').remove();
        for (var i=start; i<end; i++) {
            $trTemplate = $constantTemplate.find('tr').clone();
            $trTemplate.attr('req-number', i+1);
            $trTemplate.find('th').html(i+1);
            $($trTemplate.find('td').children('div')[0]).attr('key', 'Requirement').html(data.Requirements.Requirement[i]);
            $container.find('tbody').append($trTemplate);
        }
        return $container;
    },

    generateStepsHtmlBlock: function ($container, data) {
        /* This function generates the steps block (side-drawer) out of an HTML block and json data */
        var $allKeys = $container.find('[key]').not('[key*="Execute"]').not('[key*="Arguments"]');
        for (var i=0; i<$allKeys.length; i++) {
            if ($($allKeys[i]).prop('type') === 'text') {
                $($allKeys[i]).attr('value', setupcases.getValueFromJson(data.Setup.step[0], $($allKeys[i]).attr('key')));
            } else if ($($allKeys[i]).prop('type') === 'select-one') {
                $($allKeys[i]).attr('value', setupcases.getValueFromJson(data.Setup.step[0], $($allKeys[i]).attr('key')));
                var value = setupcases.getValueFromJson(data.Setup.step[0], $($allKeys[i]).attr('key'));
                var $allOptions = $($allKeys[i]).children();
                for (var j=0; j<$allOptions.length; j++) {
                    if ($($allOptions[j]).text() === value) {
                        $($allOptions[j]).prop('selected', true);
                        break;
                    }
                }
            } else {
                $($allKeys[i]).html(setupcases.getValueFromJson(data.Setup.step[0], $($allKeys[i]).attr('key')));
            }
        }
        $container = setupcases._addExecuteBlock($container, data);
        $container = setupcases._addArgumentsEtcBlock($container, data);
        return $container
    },

    _addExecuteBlock: function ($container, data) {
        /* This function generates the execute block (side-drawer) out of an HTML block and json data.
        This function should not be called independently */
        var $execTypeBlock = $container.find('[key="Execute.@ExecType"]');
        $execTypeBlock.attr('current-value', setupcases.getValueFromJson(data.Setup.step[0], $execTypeBlock.attr('key')));
        setupcases._selectOption($execTypeBlock, $execTypeBlock.attr('current-value'));

        var $ruleBlock = $execTypeBlock.closest('.row').next().find('#rule-template');
        for (var k=0; k<data.Setup.step[0].Execute.Rule.length; k++) {
            var $currentRuleBlock = $ruleBlock.clone().attr('id', '').attr('key', 'Execute.Rule').show();
            var $allKeys = $currentRuleBlock.find('[key]');
            for (var i=0; i<$allKeys.length; i++) {
                var value = setupcases.getValueFromJson({"Execute" : {"Rule": data.Setup.step[0].Execute.Rule[k]}}, $($allKeys[i]).attr('key'));
                $($allKeys[i]).attr('value', value);
                if ($($allKeys[i]).prop('type') === 'select-one') {
                    setupcases._selectOption($($allKeys[i]), value);
                }
            }
            setupcases.stepEditor.updateRuleElseValue($currentRuleBlock.find('[key="Execute.Rule.@Else"]'));
            $ruleBlock.parent().append($currentRuleBlock);
            $execTypeBlock.closest('.row').next().show();
        }

        return $container
    },

    _addArgumentsEtcBlock: function ($container, data) {
        /* This function generates the arguments block (side-drawer) out of an HTML block and json data.
        This function should not be called independently */
        setupcases.stepEditor.getDrivers($container.find('[key="@Repo"]'), $container.find('[key="@Driver"]').val());
        setupcases.stepEditor.getKeywords($container.find('[key="@Driver"]'), $container.find('[key="@Keyword"]').val());
        var $allArgs = $container.find('[key="Arguments.argument"]');
        for (var i=0 ; i<$allArgs.length; i++) {
            var currentArg = $($allArgs[i]).find('.cases-label').text();
            for (var j=0; j<data.Setup.step[0].Arguments.argument.length; j++) {
                if (data.Setup.step[0].Arguments.argument[j]["@name"] === currentArg) {
                    $($allArgs[i]).find('[key="Arguments.argument.@value"]').attr('value', data.Setup.step[0].Arguments.argument[j]["@value"]);
                    break;
                }
            }
        }
        return $container;
    },

    generateStepsDisplayHtmlBlock: function ($container, data) {
        /* This function generates the steps block (main page) out of an HTML block and json data */
        $container = $($container.html());
        var $allKeys = $container.find('[key]').not('[key*="Execute.Rule"]').not('[key*="Arguments"]');
        for (var i=0; i<$allKeys.length; i++) {
            if ($($allKeys[i]).prop('type') === 'text') {
                $($allKeys[i]).attr('value', setupcases.getValueFromJson(data.Setup.step[0], $($allKeys[i]).attr('key')));
            } else if ($($allKeys[i]).prop('type') === 'select-one') {
                $($allKeys[i]).attr('value', setupcases.getValueFromJson(data.Setup.step[0], $($allKeys[i]).attr('key')));
                var value = setupcases.getValueFromJson(data.Setup.step[0], $($allKeys[i]).attr('key'));
                var $allOptions = $($allKeys[i]).children();
                for (var j=0; j<$allOptions.length; j++) {
                    if ($($allOptions[j]).text() === value) {
                        $($allOptions[j]).prop('selected', true);
                        break;
                    }
                }
            } else {
                $($allKeys[i]).html(setupcases.getValueFromJson(data.Setup.step[0], $($allKeys[i]).attr('key')));
            }
        }
        $container = setupcases.evaluateDisplayRunmode($container);
        $container = setupcases.evaluateDisplayOnError($container);
        $container = setupcases.evaluateDisplayArguments($container, data);
        $container = setupcases.evaluateDisplayExecute($container, data);
        return $container;
    },

    evaluateDisplayRunmode: function ($container) {
        /* This function hides/shows the runmode block (main page).
        This function should not be called independently */
        if($container.find('[key="runmode.@type"]').html().trim() === "Standard") {
            $container.find('[key="runmode.@type"]').next().next().remove();
            $container.find('[key="runmode.@type"]').next().remove();
        }
        return $container;
    },

    evaluateDisplayOnError: function ($container) {
        /* This function hides/shows the onerror block (main page).
        This function should not be called independently */
        if($container.find('[key="onError.@action"]').html().trim() !== "Go To") {
            $container.find('[key="onError.@action"]').next().next().remove();
            $container.find('[key="onError.@action"]').next().remove();
        }
        return $container;
    },

    evaluateDisplayArguments: function ($container, data) {
        /* This function hides/shows the argument block (main page).
        This function should not be called independently */
        var $templateArg = $container.find('[key="Arguments.argument"]').clone();
        var $argBlock = $container.find('[key="Arguments"]').empty();
        for (var i=0; i<data.Setup.step[0].Arguments.argument.length; i++) {
            var $currentArgBlock = $templateArg.clone();
            $currentArgBlock.find('[key="Arguments.argument.@name"]').html(data.Setup.step[0].Arguments.argument[i]["@name"]);
            $currentArgBlock.find('[key="Arguments.argument.@value"]').html(data.Setup.step[0].Arguments.argument[i]["@value"]);
            $argBlock.append($currentArgBlock);
        }
        return $container
    },

    evaluateDisplayExecute: function ($container, data) {
        /* This function hides/shows the execute block (main page).
        This function should not be called independently */
        var $templateExecRule = $container.find('[key="Execute.Rule"]').clone();
        $container.find('[key="Execute.Rule"]').next().remove();
        $container.find('[key="Execute.Rule"]').remove();
        for (var i=0; i<data.Setup.step[0].Execute.Rule.length; i++) {
            var $currentTemplate = $templateExecRule.clone();
            var $allKeys = $currentTemplate.find('[key]');
            for (var j=0; j<$allKeys.length; j++) {
                $($allKeys[j]).html(setupcases.getValueFromJson({"Execute": {"Rule": data.Setup.step[0].Execute.Rule[i]}}, $($allKeys[j]).attr('key')));
            }
            $container.find('[key="Execute.@ExecType"]').parent().append($currentTemplate);
            $container.find('[key="Execute.@ExecType"]').parent().append('<br>');
        }
        return $container
    },

    _selectOption: function ($elem, value) {
        /* This function selects an "option" in a <select> tag.
        This function should not be called independently */
        var $allOptions = $elem.children();
        for (var j=0; j<$allOptions.length; j++) {
            if ($($allOptions[j]).text().trim() === value) {
                $($allOptions[j]).prop('selected', true);
                break;
            }
        }
    },

    proofDetailsContainer: function ($container) {
        /* This function verifies if the all the correct fields are shown/hidden in the details (side-drawer) block */
        setupcases.detailsEditor.updateDefaultOnError($container.find('[key="default_onError.@action"]'));
        setupcases.detailsEditor.updateIterationTypeStepTmpl($container.find('[key="Datatype"]'));
        return $container;
    },

    proofStepsContainer: function ($container) {
        /* This function verifies if the all the correct fields are shown/hidden in the step (side-drawer) block */
        setupcases.stepEditor.updateRules($container.find('[key="Execute.@ExecType"]'));
        setupcases.stepEditor.updateRunmode($container.find('[key="runmode.@type"]'));
        setupcases.stepEditor.updateOnErrorValue($container.find('[key="onError.@action"]'));
        return $container
    },

    getLastStepNum: function () {
        /* This function gets the last step number */
        return katana.$activeTab.find('#main-div').find('#cases-steps-template').find('tbody').children('tr').length;
    },

    redoStepNums: function(){
        var $tbodyElem = katana.$activeTab.find('#step-block').find('table').find('tbody');
        var $allTrElems = $tbodyElem.children('tr');
        for (var i=0; i<$allTrElems.length; i++){
            $($($allTrElems[i]).children('td')[0]).html(i+1);
        }
    },

    addTsToStepsHtmlBlock: function ($container, stepNum) {
        /* This function adds the step number to the step (side-drawer) block */
        $container.find('[key="@TS"]').attr('value', stepNum).val(stepNum);
        return $container
    },

    _updateCommonOnError: function ($elem) {
        /* This common function hides/shows  the corresponding "goto value" field for the onerror "goto" */
        var value = $elem.find(':selected').text().trim();
        if (value === "Go To") {
            $elem.closest('.row').next().show();
        } else {
            $elem.closest('.row').next().find('input').attr('value', '').val('');
            $elem.closest('.row').next().hide();
        }
        $elem.attr('value', value);
    },

    detailsEditor: {

        updateDefaultOnError: function ($elem) {
            /* This function hides/shows  the corresponding "goto value" field for the onerror "goto".
            Internally calls the _updateCommonOnError function */
            $elem = $elem ? $elem : $(this);
            setupcases._updateCommonOnError($elem);
        },

        updateIterationTypeStepTmpl: function ($elem) {
            /* This function disables/enables the step-level "Iteration Type" field for any change in the details
              level datatype field change */
            $elem = $elem ? $elem : $(this);
            var value = $elem.find(':selected').text().trim();
            var $parent = $elem.closest('.content').length > 0 ? $elem.closest('.content') : katana.$activeTab.find('#main-div');
            var $iterationTypeElem = $parent.find('#steps_drawer_template').find('[key="Iteration_type.@type"]');
            if (value === "Hybrid") {
                $iterationTypeElem.prop('disabled', false);
            } else {
                $iterationTypeElem.find(':selected').prop('selected', false);
                $iterationTypeElem.find('option:contains("Standard")').prop('selected', true);
                $iterationTypeElem.prop('disabled', true);
            }
        }
    },

    stepEditor: {
        getDrivers: function ($elem, driverName) {
            /* This function internally calls the getArgumentsEtc function for updating related fields on driver change */
            $elem = $elem ? $elem : $(this);
            driverName = driverName ? driverName : "";
            var repoName = $elem.val();
            var $driverRow = $elem.closest('.row').next();
            $driverRow.find('input').attr("value", driverName).val(driverName);
            $elem.attr("value", repoName);
            $driverRow.find('#drivers').html("");
            for (driver in setupcases.mappings.newStep.drivers[repoName]) {
                        $driverRow.find('#drivers').append('<option>' + driver + '</option>');
                    }
                },

        getKeywords: function ($elem, kwName) {
            /* This function internally calls the getArgumentsEtc function for updating related fields on driver change */
            $elem = $elem ? $elem : $(this);
            kwName = kwName ? kwName : "";
            var driverName = $elem.val();
            var $repoRow = $elem.closest('.row').prev();
            var $kwRow = $elem.closest('.row').next();
            var repo = $repoRow.find('input').attr("value");
            $kwRow.find('input').attr("value", kwName).val(kwName);
            $kwRow.find('#keywords').html("");
            for (keyword in setupcases.mappings.newStep.drivers[repo][driverName].actions){
                $kwRow.find('#keywords').append('<option>' + keyword + '</option>');
            }
            setupcases.stepEditor.getArgumentsEtc($kwRow.find('input'));
        },

        getArgumentsEtc: function ($elem, data) {
            /* This function internally calls the _setSignature, _setArguments, _setWDescription, _setComments
            functions for upadting those fields on kw name change */
            $elem = $elem ? $elem : $(this);
            var kwName = $elem.val();
            var driverName = $elem.closest('.row').prev().find('input').val();
            $DriverRow = $elem.closest('.row').prev();
            Repo=$DriverRow.closest('.row').prev().find('input').attr("value");
            data = data ? data : false;

            if (driverName in setupcases.mappings.newStep.drivers[Repo]) {
                if (kwName in setupcases.mappings.newStep.drivers[Repo][driverName].actions) {
                    data = setupcases.mappings.newStep.drivers[Repo][driverName].actions[kwName]
                }
            }

            setupcases.stepEditor._setSignature($elem.closest('.row').next(), data);
            setupcases.stepEditor._setArguments($elem.closest('.row').next().next(), data);
            setupcases.stepEditor._setWDescription($elem.closest('.row').next().next().next(), data);
            setupcases.stepEditor._setComments($elem.closest('.row').next().next().next().next(), data);
        },

        _setSignature: function ($topLevelSignRow, data) {
            /* This function hides/shows corresponding function signature */
            $topLevelSignRow.hide();
            $topLevelSignRow.find('input').attr('value', '');
            if (data) {
                $topLevelSignRow.find('textarea').html(data.signature);
                $topLevelSignRow.show();
            }
        },

        _setArguments: function ($topLevelArgRow, data) {
            /* This function hides/shows corresponding arguments */
            var $argRow = $topLevelArgRow.find('#arg-template').clone().attr('key', 'Arguments.argument').show();
            var $argContainer = $topLevelArgRow.find('.container-fluid');
            $argContainer.children().slice(1).remove();
            $topLevelArgRow.hide();
            var temp = false;

            if (data) {
                for (var i=0; i<data.arguments.length; i++){
                    temp = $argRow.clone();
                    temp.find('.cases-label').html(data.arguments[i]);
                    $argContainer.append(temp.clone());
                    $topLevelArgRow.show();
                }
            }
        },

        _setWDescription: function ($topLevelWDescRow, data) {
            /* This function hides/shows corresponding description */
            $topLevelWDescRow.find('input').attr('value', '');
            $topLevelWDescRow.hide();
            if (data) {
                $topLevelWDescRow.find('textarea').html(data.wdesc);
                $topLevelWDescRow.show();
            }
        },

        _setComments: function ($topLevelCommentsRow, data) {
            /* This function hides/shows corresponding comments */
            $topLevelCommentsRow.find('textarea').html('');
            $topLevelCommentsRow.hide();
            if (data) {
                $topLevelCommentsRow.find('textarea').html(data.comments);
                $topLevelCommentsRow.show();
            }
        },

        updateRules: function ($elem) {
            /* This function hides/shows  the corresponding "rules" block for the execute type field */
            $elem = $elem ? $elem : $(this);
            var currentValue = $elem.attr('current-value');
            var newValue = $elem.find(':selected').text().trim();
            $elem.attr('current-value', newValue);
            var $rulesBlock = $elem.closest('.row').next();
            var $rulesBlockContainer = $rulesBlock.find('.container-fluid');

            if (currentValue === "Yes" || currentValue === "No") {
                if (newValue === "If" || newValue === "If Not") {
                    $rulesBlock.find('.col-sm-9').append($rulesBlockContainer.clone().attr('id', '').attr('key', 'Execute.Rule').show());
                    $rulesBlock.show();
                }
            } else {
                if (newValue === "Yes" || newValue === "No") {
                    $rulesBlockContainer.slice(1).remove();
                    $rulesBlock.hide();
                }
            }
        },

        updateRuleElseValue: function ($elem) {
            /* This function hides/shows  the corresponding "goto value" field for the onerror "goto".
            Internally calls the _updateCommonOnError function */
            $elem = $elem ? $elem : $(this);
            setupcases._updateCommonOnError($elem);
        },

        updateRunmode: function ($elem) {
            /* This function hides/shows  the corresponding "runmode value" field for the runmode type field */
            $elem = $elem ? $elem : $(this);
            var value =  $elem.find(':selected').text().trim();
            if (value !== "Standard") {
                $elem.closest('.row').next().show();
            } else {
                $elem.closest('.row').next().find('input').attr('value', '').val('');
                $elem.closest('.row').next().hide();
            }
        },

        updateOnErrorValue: function ($elem) {
            /* This function hides/shows  the corresponding "goto value" field for the onerror "goto".
            Internally calls the _updateCommonOnError function */
            $elem = $elem ? $elem : $(this);
            setupcases._updateCommonOnError($elem);
        }
    },

    validations: {

        checkIfEmpty: function() {
            var $elem = $(this);
            var parentDisplay = $elem.attr('display-parent') === 'true';
            var parentVisible = parentDisplay ? $elem.closest('.row').closest('.row').is(':visible') : false;
            if (parentDisplay === parentVisible) {
                if ($elem.val().trim() === "") {
                    katana.validationAPI.addFlag( $elem, 'Cannot be Empty');
                }
            }
        },

        checkIfEmptyOrNaN: function () {
            var $elem = $(this);
            var parentDisplay = $elem.attr('display-parent') === 'true';
            var parentVisible = $elem.closest('.row').closest('.row').is(':visible');
            if (parentDisplay === parentVisible) {
                if ($elem.val().trim() === "") {
                    katana.validationAPI.addFlag( $elem, 'Cannot be Empty');
                } else if (isNaN($elem.val().trim())) {
                    katana.validationAPI.addFlag( $elem, 'Has to be a valid numerical');
                }
            }
        }

    }

};

var cleanupcases = {

    mappings: {
        newStep: {
            drivers: false, //stores all drivers and actions' information
            repos:false, //stores all the repos and actions information
            title:  "New Step" //drawer title for when new step is being edited
        },
        newReq: {
            title: "New Requirement" //drawer title for when new req is being edited
        },
        editDetails: {
            title: "Edit Details" //drawer title for when details are being edited
        },
        editReq: {
            title: "Edit Requirement" //drawer title for when existing req is being edited
        },
        editStep: {
            title: "Edit Step" //drawer title for when existing step is being edited
        }
    },

    header: {
        toggleContents: function() {
            /* This function toggles the content when up/down font-awesomes are clicked */
            var $elem = $(this);
            if ($elem.attr('collapsed') === 'false') {
                $elem.attr('collapsed', 'true');
                $elem.removeClass('fa-chevron-circle-up');
                $elem.addClass('fa-chevron-circle-down');
                $elem.closest('.cases-header').next().hide()
            } else {
                $elem.attr('collapsed', 'false');
                $elem.removeClass('fa-chevron-circle-down');
                $elem.addClass('fa-chevron-circle-up');
                $elem.closest('.cases-header').next().show()
            }
        },

        editDetails: function() {
            /* This function gets data from displayed details block and
            creates the details block in the side drawer*/
            var $elem = $(this);
            var data = cleanupcases.generateJson.generateDetails($elem.closest('#main-div').find('#detail-block'));
            cleanupcases.drawer.openClosedDrawer(cleanupcases.mappings.editDetails.title);
            cleanupcases.drawer.open.highlightSidebar(0);
            cleanupcases.drawer.open.switchView.details($elem.closest('#main-div').find('#details_drawer_template').clone(), data);
        },

        newReq: function() {
            /* This function creates a new requirements block in the side drawer*/
            var $elem = $(this);
            cleanupcases.drawer.openClosedDrawer(cleanupcases.mappings.newReq.title);
            cleanupcases.drawer.open.highlightSidebar(1);
            cleanupcases.drawer.open.switchView.requirements($elem.closest('#main-div').find('#reqs_drawer_template').clone());
        },

        newStep: function() {
            /* This function creates a new step block in the side drawer*/
               document.getElementById("hiddingsecond").style.display="block";
               document.getElementById("hiddingfirst").style.display="none";
               document.getElementById("hiddingthird").style.display="none";

               document.getElementById("editfirst").style.display="none";
               document.getElementById("editthird").style.display="none";
               document.getElementById("editsecond").style.display="none";

               document.getElementById("editDetails").style.display="none";
            var $elem = $(this);
            cleanupcases.drawer.openClosedDrawer(cleanupcases.mappings.newStep.title);
            cleanupcases.drawer.open.highlightSidebar(2);
            var $container = $elem.closest('#main-div').find('#steps_drawer_template').clone().attr('step-type', 'edit').attr('index', cleanupcases.getLastStepNum());
            cleanupcases.drawer.open.switchView.steps($container, false, cleanupcases.getLastStepNum() + 1);
        }
    },

    drawer: {

        openDatafile: function () {
            /* This function opens the datafile in the datafile editor*/
            var $elem = $(this);
            var $inputElem = $elem.parent().prev().children('input');
            var tcPath = katana.$activeTab.find('#main-div').attr("current-file");
            var idfPath = katana.utils.getAbsoluteFilepath(tcPath, $inputElem.val(), true);
            $.ajax({
                headers: {
                    'X-CSRFToken': katana.$activeTab.find('input[name="csrfmiddlewaretoken"]').attr('value')
                },
                type: 'POST',
                url: 'check_if_file_exists/',
                data: {"path": idfPath}
            }).done(function(data){
                var pd = { type: 'POST',
                    headers: {'X-CSRFToken': katana.$activeTab.find('input[name="csrfmiddlewaretoken"]').attr('value')},
                    data:  {"path": idfPath}};
                if (data.exists) {
                    katana.templateAPI.load('/katana/wdf/index/', '/static/wdf_edit/js/main.js,',
                        null, 'WDF Editor', null, pd)
                } else {
                    katana.openAlert({
                        "alert_type": "danger",
                        "heading": "Problem Opening " + $inputElem.val(),
                        "text": "It seems like the file may not be available for viewing.",
                        "show_cancel_btn": false
                    });
                }
            });
        },

        openClosedDrawer: function (title) {
            /* This function opens the closed side Drawer*/
            var $drawerClosedDiv = katana.$activeTab.find('#main-div').find('.cases-side-drawer-closed');
            var $drawerOpenDiv = $drawerClosedDiv.siblings('.cases-side-drawer-open');
            $drawerClosedDiv.hide();
            $drawerOpenDiv.show();
            $drawerOpenDiv.find('.cases-drawer-open-header').find('h4').html(title);
        },

        closeOpenedDrawer: function () {
            /* This function closes the opened side Drawer*/
            var $drawerClosedDiv = katana.$activeTab.find('#main-div').find('.cases-side-drawer-closed');
            var $drawerOpenDiv = $drawerClosedDiv.siblings('.cases-side-drawer-open');
            $drawerClosedDiv.show();
            $drawerOpenDiv.hide();
        },

        open: {


            highlightSidebar: function (childIndex) {
                /* This function highlights the icon in the drawer sidebar */
                var $sidebarIcons = $(katana.$activeTab.find('.cases-drawer-open-body').find('.sidebar').children('div'));
                for (var i=0; i<$sidebarIcons.length; i++){
                    $($sidebarIcons[i]).removeClass('cases-icon-bg-color').addClass('cases-sidebar-disabled-icon');
                }
                $($sidebarIcons[childIndex]).addClass('cases-icon-bg-color').removeClass('cases-sidebar-disabled-icon');
            },

            switchView: {

                details: function($container, data) {
                    /* This function generates the details html for the drawer and attaches it to the drawer */
                    $container.attr("id", "current_details_editor").show();
                    cleanupcases.generateDetailsDisplayHtmlBlock($container, data);
                    katana.$activeTab.find('#details_drawer_template').parent().prepend(cleanupcases.proofDetailsContainer($container));
                },

                requirements: function($container, data, current) {
                    /* This function generates the reqs html for the drawer and attaches it to the drawer */
                    $container.attr("id", "current_reqs_editor").show();
                    if (data) {
                        $container.attr('current', current);
                        $container.find('input[key="Requirement"]').attr('value', data).val(data);
                    }
                    katana.$activeTab.find('#reqs_drawer_template').parent().prepend($container);
                },

                steps: function($container, data, stepNum) {
                    /* This function generates the step html for the drawer and attaches it to the drawer */
                    $container.attr("id", "current_steps_editor").show();
                    if (data) {
                        $container = cleanupcases.generateStepsHtmlBlock($container, data);
                    } else {
                        $container = cleanupcases.addTsToStepsHtmlBlock($container, stepNum);
                    }
                    katana.$activeTab.find('#steps_drawer_template').parent().prepend(cleanupcases.proofStepsContainer($container));
                }

            },

            saveContents: function () {
                /* This function calls specific functions internally that save information on the frontend */
                var $elem = $(this);
                var saved = false;
                var $openDrawer = $elem.closest('.cases-side-drawer-open');
                var $switchElem = $openDrawer.find('.cases-drawer-open-body').find('.sidebar').find('.cases-icon-bg-color').children('i');
                if ($switchElem) {
                    var reference = $switchElem.attr('ref');
                    if (reference === "editDetails") {
                        saved = cleanupcases.drawer.open._saveContents.details($openDrawer.find('.content').find('#current_details_editor'));
                    } else if (reference === "newReq") {
                        saved = cleanupcases.drawer.open._saveContents.requirements($openDrawer.find('.content').find('#current_reqs_editor'));
                    } else if (reference === "newStep") {
                        saved = cleanupcases.drawer.open._saveContents.steps($openDrawer.find('.content').find('#current_steps_editor'));
                    }
                    if (saved) {
                        $openDrawer.find('.cases-drawer-open-body').find('.content').find('[id^="current"]').remove();
                        cleanupcases.drawer.closeOpenedDrawer();
                    }
                }
            },

            _saveContents: {

                details: function ($container) {
                    /* This function collects details data from the drawer and adds it to the displayed details block*/
                    if (katana.validationAPI.init($container)) {
                        var data = cleanupcases.generateJson.generateDetails($container);
                        var displayContent = cleanupcases.generateDetailsDisplayHtmlBlock(katana.$activeTab.find('#cases-display-template').clone(), data);
                        katana.$activeTab.find('#cases-display-template').replaceWith(displayContent);
                        return true;
                    } else {
                        return false;
                    }
                },

                requirements: function ($container) {
                    /* This function collects reqs data from the drawer and adds it to the displayed reqs block*/
                    if (katana.validationAPI.init($container)) {
                        var data = cleanupcases.generateJson.generateRequirements(katana.$activeTab.find('#cases-requirements-template'));
                        var temp = cleanupcases.generateJson.generateRequirements($container);
                        var index = $container.attr('current') ? $container.attr('current') : data.Requirements.Requirement.length;
                        data.Requirements.Requirement.splice(index, 1, temp.Requirements.Requirement[0]);
                        var displayContent = cleanupcases.generateRequirementsHtmlBlock(katana.$activeTab.find('#cases-requirements-template').clone(), data);
                        katana.$activeTab.find('#cases-requirements-template').replaceWith(displayContent);
                        return true;
                    } else {
                        return false;
                    }
                },

                steps: function ($container) {
                    /* This function collects step data from the drawer and adds it to the displayed step block*/
                    if (katana.validationAPI.init($container)) {
                        var data = cleanupcases.generateJson.generateStep($container);
                        var filteredArgs = [];
                        for (var i=0; i<data.Cleanup.step[0].Arguments.argument.length; i++) {
                            if (data.Cleanup.step[0].Arguments.argument[i]["@value"] !== "") {
                                filteredArgs.push(Object.assign({}, data.Cleanup.step[0].Arguments.argument[i]));
                            }
                        }
                        data.Cleanup.step[0].Arguments.argument = filteredArgs;
                        var displayContent = cleanupcases.generateStepsDisplayHtmlBlock(katana.$activeTab.find('#step-row-template-cleanup').clone().attr('id', ''), data);
                        var stepType = $container.attr('step-type') === "edit";
                        var index = parseInt($container.attr('index'));
                        var $allTrs = katana.$activeTab.find('#cases-steps-template-cleanup').find('tbody').find('tr');
                        if (stepType && index < $allTrs.length) {
                            $allTrs[index].remove();
                        }
                        if (index === 0) {
                            katana.$activeTab.find('#cases-steps-template-cleanup').find('tbody').prepend(displayContent);
                            cleanupcases.redoStepNums();
                        } else {
                            displayContent.insertAfter($($allTrs[index-1]));
                            cleanupcases.redoStepNums();
                        }
                        return true;
                    } else {
                        return false;
                    }
                }
            },

            discardContents: function () {
                /* This function deletes contents from the drawer */
                var $elem = $(this);
                var $openDrawer = $elem.closest('.cases-side-drawer-open');
                katana.openAlert({
                    "alert_type": "warning",
                    "heading": "All changes will be discarded",
                    "text": "This action will discard all changes, are you sure you want to continue?"
                    }, function () {
                        $openDrawer.find('.cases-drawer-open-body').find('.content').find('[id^="current"]').remove();
                        cleanupcases.drawer.closeOpenedDrawer();
                    })
            }
        },

        openFileExplorer: {

            logsOrResultsDir: function (relative, $elem) {
                /* This common function gets filepath from the fileexplorer and ataches it to the correct input field*/
                $elem = $elem ? $elem : $(this);
                var $inputElem = $elem.parent().prev().children('input');
                relative = !!relative;
                katana.fileExplorerAPI.openFileExplorer("Select a Path", false,
                    katana.$activeTab.find('input[name="csrfmiddlewaretoken"]').attr('value'), false,
                    function (inputValue){
                        if (relative) {
                            var tcPath = katana.$activeTab.find('#main-div').attr("current-file");
                            inputValue = katana.utils.getRelativeFilepath(tcPath, inputValue, true);
                        }
                        $inputElem.val(inputValue);
                        $inputElem.attr('value', inputValue);
                    },
                    false)
            },

            inputDataFile: function () {
                /* This function calls logsOrResultsDir with relative as true so that relative path is created. */
                cleanupcases.drawer.openFileExplorer.logsOrResultsDir(true, $(this));
            }
        }
    },

    invert: function(){
        /* This function switches between the testcase files view and the actual testcase */
        var toolbarButtons = katana.$activeTab.find('.tool-bar').find('button');
        for(var i=0; i<toolbarButtons.length; i++){
            if($(toolbarButtons[i]).is(":hidden")){
                $(toolbarButtons[i]).show();
            } else {
                $(toolbarButtons[i]).hide();
            }
        }
        var divs = katana.$activeTab.find('#body-div').children();
        for(i=0; i<divs.length; i++){
            if($(divs[i]).is(":hidden")){
                $(divs[i]).show();
            } else {
                $(divs[i]).hide();
            }
        }
    },

    landing: {
        init: function(){
            /* This function get the list of testcase files, displays them, and
            attaches click event on each testcase file */
            $.ajax({
                type: 'GET',
                url: 'testwrapper/get_list_of_testwrappers/'
            }).done(function(data){
                katana.jsTreeAPI.createJstree(katana.$activeTab.find('#tree-div'), data.data);
                katana.$activeTab.find('#tree-div').on("select_node.jstree", function (e, data){
                    if (data["node"]["icon"] === "jstree-file") {
                        $.ajax({
                            headers: {
                                'X-CSRFToken': katana.$activeTab.find('.csrf-container').html()
                            },
                            type: 'GET',
                            url: 'testwrapper/get_file/',
                            data: {"path": data["node"]["li_attr"]["data-path"]}
                        }).done(function(data){
                            if(data.status){
                                cleanupcases.invert();
                                katana.$activeTab.find('#main-div').attr("current-file", data.filepath);
                                katana.$activeTab.find('.tool-bar').find('.title').html(data.filename);
                                katana.$activeTab.find('#main-div').html(data.html_data);
                                cleanupcases.mappings.newStep.drivers = data.drivers;
                            } else {
                                katana.openAlert({"alert_type": "danger",
                                    "heading": "Could not open file",
                                    "text": "Errors: " + data.message,
                                    "show_cancel_btn": false})
                            }
                        });
                    }
                });
            })
        },

        openNewFile: function(){
            /* This function opens a new testcase */
            $.ajax({
                headers: {
                    'X-CSRFToken': katana.$activeTab.find('.csrf-container').html()
                },
                type: 'GET',
                url: 'testwrapper/get_file/',
                data: {"path": false}
            }).done(function(data){
                if(data.status){
                    cleanupcases.invert();
                    katana.$activeTab.find('#main-div').attr("current-file", data.filepath);
                    katana.$activeTab.find('.tool-bar').find('.title').html(data.filename);
                    katana.$activeTab.find('#main-div').html(data.html_data);
                    cleanupcases.mappings.newStep.drivers = data.drivers;
                } else {
                    katana.openAlert({"alert_type": "danger",
                        "heading": "Could not open file",
                        "text": "Errors: " + data.message,
                        "show_cancel_btn": false})
                }
            });
        }
    },

    caseViewer:  {
        close: function () {
            /* This function closes the testcase */
            katana.$activeTab.find('#main-div').html("");
            katana.$activeTab.find('.tool-bar').find('.title').html("");
            cleanupcases.invert();
        },

        save: function () {
            /* This function collects data from each displayed block and saves the testcase */
            var final_json = {"TestWrapper": {}};
            var filepath = katana.$activeTab.find('#main-div').attr("current-file");
            var filename = katana.$activeTab.find('.tool-bar').find('.title').html();
            $.extend(true, final_json.Testcase, cleanupcases.generateJson.generateDetails(katana.$activeTab.find('#detail-block')));
//            $.extend(true, final_json.Testcase, cleanupcases.generateJson.generateRequirements(katana.$activeTab.find('#req-block')));
            $.extend(true, final_json.Testcase, cleanupcases.generateJson.generateStep(katana.$activeTab.find('#step-block-cleanup')));


            var callBack_on_accept = function(inputValue) {
                $.ajax({
                    headers: {
                        'X-CSRFToken': katana.$activeTab.find('input[name="csrfmiddlewaretoken"]').attr('value')
                    },
                    type: 'POST',
                    url: 'testwrapper/save_file/',
                    data: {"data": JSON.stringify(final_json), "directory": filepath, "filename": inputValue, "extension": ".xml"}
                }).done(function(data){
                    if (data.status) {
                        katana.openAlert({
                            "alert_type": "success",
                            "heading": "File Saved",
                            "text": inputValue + " has been saved successfully",
                            "show_cancel_btn": false
                        });
                        cleanupcases.caseViewer.close();
                    } else {
                        katana.openAlert({
                            "alert_type": "danger",
                            "heading": "File Not Saved",
                            "text": "Some problem occurred while saving the file: " + inputValue,
                            "show_cancel_btn": false
                        })
                    }
                });
            };

            katana.openAlert({
                "alert_type": "light",
                "heading": "Name for the file",
                "text": "",
                "prompt": "true",
                "prompt_default": filename
                },
                function(inputValue){
                $.ajax({
                    headers: {
                        'X-CSRFToken': katana.$activeTab.find('input[name="csrfmiddlewaretoken"]').attr('value')
                    },
                    type: 'POST',
                    url: 'check_if_file_exists/',
                    data: {"filename": inputValue, "directory": filepath, "extension": ".xml"}
                }).done(function(data){
                     if(data.exists){
                        katana.openAlert({
                            "alert_type": "warning",
                            "heading": "File Exists",
                            "text": "A file with the name " + inputValue + " already exists; do you want to overwrite it?",
                            "accept_btn_text": "Yes",
                            "cancel_btn_text": "No"
                            }, function() {
                            callBack_on_accept(inputValue)}
                            )
                     } else {
                        callBack_on_accept(inputValue);
                     }
                });
            });
        }
    },

    reqSection: {
        deleteReq: function () {
            /* This function deletes a req */
            var $elem = $(this);
            var $tdParent = $elem.closest('td');
            var reqNumber = $tdParent.siblings('th').html();
            var $toBeDeleted = $elem.closest('tr');
            var $topLevel = $elem.closest('#cases-requirements-template');
            katana.openAlert({
                "alert_type": "danger",
                "heading": "Delete Requirement " + reqNumber + "?",
                "text": "Are you sure you want to delete the requirement? This cannot be undone."
            }, function(){
                $toBeDeleted.remove();
                var data = cleanupcases.generateJson.generateRequirements($topLevel);
                var displayContent = cleanupcases.generateRequirementsHtmlBlock($topLevel.clone(), data);
                $topLevel.replaceWith(displayContent);
            });
        },

        editReq: function () {
            /* This function opens a req in the req editor*/
            var $elem = $(this);
            var data = $($elem.closest('.cases-req').children('div')[0]).html().trim();
            cleanupcases.drawer.openClosedDrawer(cleanupcases.mappings.editReq.title);
            cleanupcases.drawer.open.highlightSidebar(1);
            cleanupcases.drawer.open.switchView.requirements($elem.closest('#main-div').find('#reqs_drawer_template').clone(), data, $elem.closest('tr').attr('req-number')-1);
        }
    },

    stepSection: {
        selectStep: function () {
            /* This function selects a step */
            var $elem = $(this);
            var $allTrElems = $elem.parent().children('tr');
            if ($elem.attr('marked') === 'true') {
                $elem.attr('marked', 'false');
                $elem.css('background-color', '');
            } else {
                var multiselect = katana.$activeTab.find('.cases-step-toolbar').find('.fa-th-list').attr('multiselect');
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
                /* This function de/activates the multiselect functionality for a step */
                var $elem = $(this);
                var $iconElem = $elem.children('i');
                if ($iconElem.attr('multiselect') === 'on'){
                    $iconElem.attr('multiselect', 'off');
                    $iconElem.removeClass('badged');
                    $iconElem.children('i').hide();
                    var $allTrElems = katana.$activeTab.find('#step-block-cleanup').find('tbody').children('tr');
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
                /* This function deletes a step */
                var $tbodyElem = katana.$activeTab.find('#step-block-cleanup').find('tbody');
                var $allTrElems = $tbodyElem.children('tr[marked="true"]');
                if ($allTrElems.length === 0) {
                    katana.openAlert({"alert_type": "danger",
                        "heading": "No step selected for deletion",
                        "text": "Please select at least one step to delete",
                        "show_cancel_btn": "false"})
                } else {
                    var stepNumbers = "";
                    for (var i=0; i<$allTrElems.length; i++){
                        stepNumbers += ($($allTrElems[i]).index() + 1).toString() + ", "
                    }
                    stepNumbers = stepNumbers.slice(0, -2);
                    katana.openAlert({"alert_type": "warning",
                        "heading": "This would delete Steps " + stepNumbers,
                        "text": "Are you sure you want to delete these steps?"},
                        function () {
                            for (var i=0; i<$allTrElems.length; i++){
                                $($allTrElems[i]).remove();
                            }
                            cleanupcases.redoStepNums();
                        })
                }
            },

            insertStep: function () {
            document.getElementById("hiddingfirst").style.display="none";
            document.getElementById("hiddingsecond").style.display="block";
            document.getElementById("hiddingthird").style.display="none";

            document.getElementById("editfirst").style.display="none";
            document.getElementById("editthird").style.display="none";
               document.getElementById("editsecond").style.display="none";

               document.getElementById("editDetails").style.display="none";
//                document.getElementById("hiddingfirst").style.display="none ";
                /* This function opens a new step in the step editor and inserts it into a speific spot when saved */
                var $elem = $(this);
                var $tbodyElem = katana.$activeTab.find('#step-block-cleanup').find('tbody');
                var $allTrElems = $tbodyElem.children('tr[marked="true"]');
                if ($allTrElems.length === 0) {
                    var insertAtIndex = $tbodyElem.children('tr').length;
                } else if ($allTrElems.length > 1) {
                    katana.openAlert({
                        "alert_type": "danger",
                        "heading": "Multiple Steps Selected",
                        "text": "Only one step can be inserted at a time. Please select only one " +
                        "step above which you want to insert another step.",
                        "show_cancel_btn": false
                    });
                    return;
                } else {
                    insertAtIndex = $($allTrElems[0]).index();
                }

                cleanupcases.drawer.openClosedDrawer(cleanupcases.mappings.newStep.title);
                cleanupcases.drawer.open.highlightSidebar(2);
                var $container = $elem.closest('#main-div').find('#steps_drawer_template').clone().attr("step-type", "insert").attr("index", insertAtIndex);
                cleanupcases.drawer.open.switchView.steps($container, false, insertAtIndex+1);

            },

            editStep: function () {
             document.getElementById("hiddingfirst").style.display="none";
            document.getElementById("hiddingsecond").style.display="none";
            document.getElementById("hiddingthird").style.display="none";

            document.getElementById("editfirst").style.display="none";
            document.getElementById("editthird").style.display="none";
               document.getElementById("editsecond").style.display="block";

               document.getElementById("editDetails").style.display="none";
                /* This function opens the step in the step editor and replaces the existing step when saved */
                var $elem = $(this);
                var $tbodyElem = katana.$activeTab.find('#step-block-cleanup').find('tbody');
                var $allTrElems = $tbodyElem.children('tr[marked="true"]');
                if ($allTrElems.length === 0) {
                    katana.openAlert({
                        "alert_type": "danger",
                        "heading": "No Step Selected",
                        "text": "Please select a step to edit.",
                        "show_cancel_btn": false
                    });
                } else if ($allTrElems.length > 1) {
                    katana.openAlert({
                        "alert_type": "danger",
                        "heading": "Multiple Steps Selected",
                        "text": "Only one step can be edited at a time. Please select only one " +
                        "step to edit.",
                        "show_cancel_btn": false
                    });
                } else {
                    var data = setupcases.generateJson.generateStep($($allTrElems[0]));
                    setupcases.drawer.openClosedDrawer(setupcases.mappings.editStep.title);
                    setupcases.drawer.open.highlightSidebar(2);
                    var $container = $elem.closest('#main-div').find('#steps_drawer_template').clone().attr('step-type', 'edit').attr('index', $($allTrElems[0]).index());
                    setupcases.drawer.open.switchView.steps($container, data);
                }
            }
        }
    },

    generateJson: {

        generateDetails: function ($container) {
            /* This function creates details json out of an HTML block */
            var finalJson = {Details: {}};
            var $allKeys = $container.find('[key]');
            var value = false;
            for (var i=0; i <$allKeys.length; i++) {
                value = $($allKeys[i]).val() ? $($allKeys[i]).val().trim() : $($allKeys[i]).html().trim();
                $.extend(true, finalJson.Details, cleanupcases.generateJson._updateJson($($allKeys[i]).attr("key").trim(), value));
            }
            return finalJson;
        },

        generateRequirements: function ($container) {
            /* This function creates requirements json out of an HTML block */
            var finalJson = {Requirements: { Requirement: []}};
            var $allKeys = $container.find('[key]');
            var value = false;
            for (var i=0; i <$allKeys.length; i++) {
                value = $($allKeys[i]).val() ? $($allKeys[i]).val().trim() : $($allKeys[i]).html().trim();

            }
            return ;
        },

        generateStep: function ($container) {
            /* This function creates steps json out of an HTML block */
            var finalJson = {Cleanup: { step: []}};
            var $allSteps = $container.attr('key') === 'step'? [$container] : $container.find('[key="step"]');
            var $allKeys = false;
            var partialData = false;
            for (var i=0; i <$allSteps.length; i++) {
                $allKeys = $($allSteps[i]).find('[key]').not('[key*="Execute.Rule"]').not('[key*="Arguments"]');
                partialData = {};
                for (var j=0; j<$allKeys.length; j++) {
                    var key = $($allKeys[j]).attr("key").trim();
                    var value = $($allKeys[j]).val() ? $($allKeys[j]).val().trim() : $($allKeys[j]).html().trim();
                    $.extend(true, partialData, cleanupcases.generateJson._updateJson(key, value));
                }
                $.extend(true, partialData, cleanupcases.generateJson.generateArguments($($allSteps[i]).find('[key="Arguments.argument"]')));
                $.extend(true, partialData, cleanupcases.generateJson.generateExecuteRules($($allSteps[i]).find('[key="Execute.Rule"]')));
                finalJson.Cleanup.step.push(partialData);
            }
            return finalJson
        },

        generateExecuteRules: function ($container){
            /* This function creates execute (rules) json out of an HTML block. Typically this function should
            never be called independently. */
            var finalJson = {Execute: {Rule: []}};
            var partialData = false;
            var $ruleBlock = false;
            for (var i=0; i<$container.length; i++) {
                $ruleBlock = $($container[i]).find('[key]');
                partialData = {};
                for (var j=0; j<$ruleBlock.length; j++) {
                    var key = $($ruleBlock[j]).attr("key").trim();
                    var val = $($ruleBlock[j]).val() ? $($ruleBlock[j]).val().trim() : $($ruleBlock[j]).attr('value');
                    var value = val ? val.trim() : $($ruleBlock[j]).html().trim();
                    $.extend(true, partialData, cleanupcases.generateJson._updateJson(key, value));
                }
                finalJson.Execute.Rule.push(Object.assign({}, partialData.Execute.Rule));
            }
            return finalJson;
        },

        generateArguments: function ($container){
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
                    $.extend(true, partialData, cleanupcases.generateJson._updateJson(key, value));
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
                data[key] = cleanupcases.generateJson._updateJson(remaining_key, value)
            } else {
                data[unrefined_key] = value;
            }
            return data;
        }
    },

    getValueFromJson: function (data, unrefined_key) {
        /* This function iterates through a json recursively and gets the value for the given key.
        This function should never be called independently */
        var key = unrefined_key.split(/\.(.+)/)[0];
        var remaining_key = unrefined_key.split(/\.(.+)/)[1];
        if (key !== undefined && remaining_key !== undefined) {
            return cleanupcases.getValueFromJson(data[key], remaining_key)
        }
        return data[key]
    },

    generateDetailsDisplayHtmlBlock: function ($container, data) {
        /* This function generates the details block out of an HTML block and json data */
        var $allKeys = $container.find('[key]');
        for (var i=0; i<$allKeys.length; i++) {
            if ($($allKeys[i]).prop('type') === 'text') {
                $($allKeys[i]).attr('value', cleanupcases.getValueFromJson(data.Details, $($allKeys[i]).attr('key')));
            } else if ($($allKeys[i]).prop('type') === 'select-one') {
                $($allKeys[i]).attr('value', cleanupcases.getValueFromJson(data.Details, $($allKeys[i]).attr('key')));
                var value = cleanupcases.getValueFromJson(data.Details, $($allKeys[i]).attr('key'));
                var $allOptions = $($allKeys[i]).children();
                for (var j=0; j<$allOptions.length; j++) {
                    if ($($allOptions[j]).text() === value) {
                        $($allOptions[j]).prop('selected', true);
                        break;
                    }
                }
            } else {
                $($allKeys[i]).html(cleanupcases.getValueFromJson(data.Details, $($allKeys[i]).attr('key')));
            }
        }
        return $container
    },

    generateRequirementsHtmlBlock: function ($container, data) {
        /* This function generates the requirements block out of an HTML block and json data */
        var $constantTemplate = $container.find('#req-table-template').clone().attr('id', "").show();
        var start = 0;
        var mid = Math.floor((data.Requirements.Requirement.length + 1) /2);
        var end = data.Requirements.Requirement.length;
        var $tableTemplateLeft = cleanupcases._generateReqTable(data, start, mid, $constantTemplate, $constantTemplate.clone());
        var $tableTemplateRight = cleanupcases._generateReqTable(data, mid, end, $constantTemplate, $constantTemplate.clone());
        $($container.find('.cases-internal-space')[0]).html($tableTemplateLeft);
        $($container.find('.cases-internal-space')[1]).html($tableTemplateRight);
        return $container;
    },

    _generateReqTable: function (data, start, end, $constantTemplate, $container) {
        /* This function is called by generateRequirementsHtmlBlock which creates the req block */
        var $trTemplate = false;
        $container.find('tr').remove();
        for (var i=start; i<end; i++) {
            $trTemplate = $constantTemplate.find('tr').clone();
            $trTemplate.attr('req-number', i+1);
            $trTemplate.find('th').html(i+1);
            $($trTemplate.find('td').children('div')[0]).attr('key', 'Requirement').html(data.Requirements.Requirement[i]);
            $container.find('tbody').append($trTemplate);
        }
        return $container;
    },

    generateStepsHtmlBlock: function ($container, data) {
        /* This function generates the steps block (side-drawer) out of an HTML block and json data */
        var $allKeys = $container.find('[key]').not('[key*="Execute"]').not('[key*="Arguments"]');
        for (var i=0; i<$allKeys.length; i++) {
            if ($($allKeys[i]).prop('type') === 'text') {
                $($allKeys[i]).attr('value', cleanupcases.getValueFromJson(data.Cleanup.step[0], $($allKeys[i]).attr('key')));
            } else if ($($allKeys[i]).prop('type') === 'select-one') {
                $($allKeys[i]).attr('value', cleanupcases.getValueFromJson(data.Cleanup.step[0], $($allKeys[i]).attr('key')));
                var value = cleanupcases.getValueFromJson(data.Cleanup.step[0], $($allKeys[i]).attr('key'));
                var $allOptions = $($allKeys[i]).children();
                for (var j=0; j<$allOptions.length; j++) {
                    if ($($allOptions[j]).text() === value) {
                        $($allOptions[j]).prop('selected', true);
                        break;
                    }
                }
            } else {
                $($allKeys[i]).html(cleanupcases.getValueFromJson(data.Cleanup.step[0], $($allKeys[i]).attr('key')));
            }
        }
        $container = cleanupcases._addExecuteBlock($container, data);
        $container = cleanupcases._addArgumentsEtcBlock($container, data);
        return $container
    },

    _addExecuteBlock: function ($container, data) {
        /* This function generates the execute block (side-drawer) out of an HTML block and json data.
        This function should not be called independently */
        var $execTypeBlock = $container.find('[key="Execute.@ExecType"]');
        $execTypeBlock.attr('current-value', cleanupcases.getValueFromJson(data.Cleanup.step[0], $execTypeBlock.attr('key')));
        cleanupcases._selectOption($execTypeBlock, $execTypeBlock.attr('current-value'));

        var $ruleBlock = $execTypeBlock.closest('.row').next().find('#rule-template');
        for (var k=0; k<data.Cleanup.step[0].Execute.Rule.length; k++) {
            var $currentRuleBlock = $ruleBlock.clone().attr('id', '').attr('key', 'Execute.Rule').show();
            var $allKeys = $currentRuleBlock.find('[key]');
            for (var i=0; i<$allKeys.length; i++) {
                var value = cleanupcases.getValueFromJson({"Execute" : {"Rule": data.Cleanup.step[0].Execute.Rule[k]}}, $($allKeys[i]).attr('key'));
                $($allKeys[i]).attr('value', value);
                if ($($allKeys[i]).prop('type') === 'select-one') {
                    cleanupcases._selectOption($($allKeys[i]), value);
                }
            }
            cleanupcases.stepEditor.updateRuleElseValue($currentRuleBlock.find('[key="Execute.Rule.@Else"]'));
            $ruleBlock.parent().append($currentRuleBlock);
            $execTypeBlock.closest('.row').next().show();
        }

        return $container
    },

    _addArgumentsEtcBlock: function ($container, data) {
        /* This function generates the arguments block (side-drawer) out of an HTML block and json data.
        This function should not be called independently */
        cleanupcases.stepEditor.getDrivers($container.find('[key="@Repo"]'), $container.find('[key="@Driver"]').val());
        cleanupcases.stepEditor.getKeywords($container.find('[key="@Driver"]'), $container.find('[key="@Keyword"]').val());
        var $allArgs = $container.find('[key="Arguments.argument"]');
        for (var i=0 ; i<$allArgs.length; i++) {
            var currentArg = $($allArgs[i]).find('.cases-label').text();
            for (var j=0; j<data.Cleanup.step[0].Arguments.argument.length; j++) {
                if (data.Cleanup.step[0].Arguments.argument[j]["@name"] === currentArg) {
                    $($allArgs[i]).find('[key="Arguments.argument.@value"]').attr('value', data.Cleanup.step[0].Arguments.argument[j]["@value"]);
                    break;
                }
            }
        }
        return $container;
    },

    generateStepsDisplayHtmlBlock: function ($container, data) {
        /* This function generates the steps block (main page) out of an HTML block and json data */
        $container = $($container.html());
        var $allKeys = $container.find('[key]').not('[key*="Execute.Rule"]').not('[key*="Arguments"]');
        for (var i=0; i<$allKeys.length; i++) {
            if ($($allKeys[i]).prop('type') === 'text') {
                $($allKeys[i]).attr('value', cleanupcases.getValueFromJson(data.Cleanup.step[0], $($allKeys[i]).attr('key')));
            } else if ($($allKeys[i]).prop('type') === 'select-one') {
                $($allKeys[i]).attr('value', cleanupcases.getValueFromJson(data.Cleanup.step[0], $($allKeys[i]).attr('key')));
                var value = cleanupcases.getValueFromJson(data.Cleanup.step[0], $($allKeys[i]).attr('key'));
                var $allOptions = $($allKeys[i]).children();
                for (var j=0; j<$allOptions.length; j++) {
                    if ($($allOptions[j]).text() === value) {
                        $($allOptions[j]).prop('selected', true);
                        break;
                    }
                }
            } else {
                $($allKeys[i]).html(cleanupcases.getValueFromJson(data.Cleanup.step[0], $($allKeys[i]).attr('key')));
            }
        }
        $container = cleanupcases.evaluateDisplayRunmode($container);
        $container = cleanupcases.evaluateDisplayOnError($container);
        $container = cleanupcases.evaluateDisplayArguments($container, data);
        $container = cleanupcases.evaluateDisplayExecute($container, data);
        return $container;
    },

    evaluateDisplayRunmode: function ($container) {
        /* This function hides/shows the runmode block (main page).
        This function should not be called independently */
        if($container.find('[key="runmode.@type"]').html().trim() === "Standard") {
            $container.find('[key="runmode.@type"]').next().next().remove();
            $container.find('[key="runmode.@type"]').next().remove();
        }
        return $container;
    },

    evaluateDisplayOnError: function ($container) {
        /* This function hides/shows the onerror block (main page).
        This function should not be called independently */
        if($container.find('[key="onError.@action"]').html().trim() !== "Go To") {
            $container.find('[key="onError.@action"]').next().next().remove();
            $container.find('[key="onError.@action"]').next().remove();
        }
        return $container;
    },

    evaluateDisplayArguments: function ($container, data) {
        /* This function hides/shows the argument block (main page).
        This function should not be called independently */
        var $templateArg = $container.find('[key="Arguments.argument"]').clone();
        var $argBlock = $container.find('[key="Arguments"]').empty();
        for (var i=0; i<data.Cleanup.step[0].Arguments.argument.length; i++) {
            var $currentArgBlock = $templateArg.clone();
            $currentArgBlock.find('[key="Arguments.argument.@name"]').html(data.Cleanup.step[0].Arguments.argument[i]["@name"]);
            $currentArgBlock.find('[key="Arguments.argument.@value"]').html(data.Cleanup.step[0].Arguments.argument[i]["@value"]);
            $argBlock.append($currentArgBlock);
        }
        return $container
    },

    evaluateDisplayExecute: function ($container, data) {
        /* This function hides/shows the execute block (main page).
        This function should not be called independently */
        var $templateExecRule = $container.find('[key="Execute.Rule"]').clone();
        $container.find('[key="Execute.Rule"]').next().remove();
        $container.find('[key="Execute.Rule"]').remove();
        for (var i=0; i<data.Cleanup.step[0].Execute.Rule.length; i++) {
            var $currentTemplate = $templateExecRule.clone();
            var $allKeys = $currentTemplate.find('[key]');
            for (var j=0; j<$allKeys.length; j++) {
                $($allKeys[j]).html(cleanupcases.getValueFromJson({"Execute": {"Rule": data.Cleanup.step[0].Execute.Rule[i]}}, $($allKeys[j]).attr('key')));
            }
            $container.find('[key="Execute.@ExecType"]').parent().append($currentTemplate);
            $container.find('[key="Execute.@ExecType"]').parent().append('<br>');
        }
        return $container
    },

    _selectOption: function ($elem, value) {
        /* This function selects an "option" in a <select> tag.
        This function should not be called independently */
        var $allOptions = $elem.children();
        for (var j=0; j<$allOptions.length; j++) {
            if ($($allOptions[j]).text().trim() === value) {
                $($allOptions[j]).prop('selected', true);
                break;
            }
        }
    },

    proofDetailsContainer: function ($container) {
        /* This function verifies if the all the correct fields are shown/hidden in the details (side-drawer) block */
        cleanupcases.detailsEditor.updateDefaultOnError($container.find('[key="default_onError.@action"]'));
        cleanupcases.detailsEditor.updateIterationTypeStepTmpl($container.find('[key="Datatype"]'));
        return $container;
    },

    proofStepsContainer: function ($container) {
        /* This function verifies if the all the correct fields are shown/hidden in the step (side-drawer) block */
        cleanupcases.stepEditor.updateRules($container.find('[key="Execute.@ExecType"]'));
        cleanupcases.stepEditor.updateRunmode($container.find('[key="runmode.@type"]'));
        cleanupcases.stepEditor.updateOnErrorValue($container.find('[key="onError.@action"]'));
        return $container
    },

    getLastStepNum: function () {
        /* This function gets the last step number */
        return katana.$activeTab.find('#main-div').find('#cases-steps-template-cleanup').find('tbody').children('tr').length;
    },

    redoStepNums: function(){
        var $tbodyElem = katana.$activeTab.find('#step-block-cleanup').find('table').find('tbody');
        var $allTrElems = $tbodyElem.children('tr');
        for (var i=0; i<$allTrElems.length; i++){
            $($($allTrElems[i]).children('td')[0]).html(i+1);
        }
    },

    addTsToStepsHtmlBlock: function ($container, stepNum) {
        /* This function adds the step number to the step (side-drawer) block */
        $container.find('[key="@TS"]').attr('value', stepNum).val(stepNum);
        return $container
    },

    _updateCommonOnError: function ($elem) {
        /* This common function hides/shows  the corresponding "goto value" field for the onerror "goto" */
        var value = $elem.find(':selected').text().trim();
        if (value === "Go To") {
            $elem.closest('.row').next().show();
        } else {
            $elem.closest('.row').next().find('input').attr('value', '').val('');
            $elem.closest('.row').next().hide();
        }
        $elem.attr('value', value);
    },

    detailsEditor: {

        updateDefaultOnError: function ($elem) {
            /* This function hides/shows  the corresponding "goto value" field for the onerror "goto".
            Internally calls the _updateCommonOnError function */
            $elem = $elem ? $elem : $(this);
            cleanupcases._updateCommonOnError($elem);
        },

        updateIterationTypeStepTmpl: function ($elem) {
            /* This function disables/enables the step-level "Iteration Type" field for any change in the details
              level datatype field change */
            $elem = $elem ? $elem : $(this);
            var value = $elem.find(':selected').text().trim();
            var $parent = $elem.closest('.content').length > 0 ? $elem.closest('.content') : katana.$activeTab.find('#main-div');
            var $iterationTypeElem = $parent.find('#steps_drawer_template').find('[key="Iteration_type.@type"]');
            if (value === "Hybrid") {
                $iterationTypeElem.prop('disabled', false);
            } else {
                $iterationTypeElem.find(':selected').prop('selected', false);
                $iterationTypeElem.find('option:contains("Standard")').prop('selected', true);
                $iterationTypeElem.prop('disabled', true);
            }
        }
    },

    stepEditor: {
        getDrivers: function ($elem, driverName) {
            /* This function internally calls the getArgumentsEtc function for updating related fields on driver change */
            $elem = $elem ? $elem : $(this);
            driverName = driverName ? driverName : "";
            var repoName = $elem.val();
            var $driverRow = $elem.closest('.row').next();
            $driverRow.find('input').attr("value", driverName).val(driverName);
            $elem.attr("value", repoName);
            $driverRow.find('#drivers').html("");
            for (driver in cases.mappings.newStep.drivers[repoName]) {
                        $driverRow.find('#drivers').append('<option>' + driver + '</option>');
                    }
                },

        getKeywords: function ($elem, kwName) {
            /* This function internally calls the getArgumentsEtc function for updating related fields on driver change */
            $elem = $elem ? $elem : $(this);

            kwName = kwName ? kwName : "";
            var driverName = $elem.val();
            var $repoRow = $elem.closest('.row').prev();
            var $kwRow = $elem.closest('.row').next();
            var repo = $repoRow.find('input').attr("value");
            $kwRow.find('input').attr("value", kwName).val(kwName);
            $kwRow.find('#keywords').html("");
            for (keyword in cleanupcases.mappings.newStep.drivers[repo][driverName].actions){
                $kwRow.find('#keywords').append('<option>' + keyword + '</option>');
            }
            cleanupcases.stepEditor.getArgumentsEtc($kwRow.find('input'));
        },

        getArgumentsEtc: function ($elem, data) {
            /* This function internally calls the _setSignature, _setArguments, _setWDescription, _setComments
            functions for upadting those fields on kw name change */
            $elem = $elem ? $elem : $(this);
            var kwName = $elem.val();
            var driverName = $elem.closest('.row').prev().find('input').val();
            $DriverRow = $elem.closest('.row').prev();
            Repo=$DriverRow.closest('.row').prev().find('input').attr("value");
            data = data ? data : false;

            if (driverName in cleanupcases.mappings.newStep.drivers[Repo]) {
                if (kwName in cleanupcases.mappings.newStep.drivers[Repo][driverName].actions) {
                    data = cleanupcases.mappings.newStep.drivers[Repo][driverName].actions[kwName]
                }
            }

            cleanupcases.stepEditor._setSignature($elem.closest('.row').next(), data);
            cleanupcases.stepEditor._setArguments($elem.closest('.row').next().next(), data);
            cleanupcases.stepEditor._setWDescription($elem.closest('.row').next().next().next(), data);
            cleanupcases.stepEditor._setComments($elem.closest('.row').next().next().next().next(), data);
        },

        _setSignature: function ($topLevelSignRow, data) {
            /* This function hides/shows corresponding function signature */
            $topLevelSignRow.hide();
            $topLevelSignRow.find('input').attr('value', '');
            if (data) {
                $topLevelSignRow.find('textarea').html(data.signature);
                $topLevelSignRow.show();
            }
        },

        _setArguments: function ($topLevelArgRow, data) {
            /* This function hides/shows corresponding arguments */
            var $argRow = $topLevelArgRow.find('#arg-template').clone().attr('key', 'Arguments.argument').show();
            var $argContainer = $topLevelArgRow.find('.container-fluid');
            $argContainer.children().slice(1).remove();
            $topLevelArgRow.hide();
            var temp = false;

            if (data) {
                for (var i=0; i<data.arguments.length; i++){
                    temp = $argRow.clone();
                    temp.find('.cases-label').html(data.arguments[i]);
                    $argContainer.append(temp.clone());
                    $topLevelArgRow.show();
                }
            }
        },

        _setWDescription: function ($topLevelWDescRow, data) {
            /* This function hides/shows corresponding description */
            $topLevelWDescRow.find('input').attr('value', '');
            $topLevelWDescRow.hide();
            if (data) {
                $topLevelWDescRow.find('textarea').html(data.wdesc);
                $topLevelWDescRow.show();
            }
        },

        _setComments: function ($topLevelCommentsRow, data) {
            /* This function hides/shows corresponding comments */
            $topLevelCommentsRow.find('textarea').html('');
            $topLevelCommentsRow.hide();
            if (data) {
                $topLevelCommentsRow.find('textarea').html(data.comments);
                $topLevelCommentsRow.show();
            }
        },

        updateRules: function ($elem) {
            /* This function hides/shows  the corresponding "rules" block for the execute type field */
            $elem = $elem ? $elem : $(this);
            var currentValue = $elem.attr('current-value');
            var newValue = $elem.find(':selected').text().trim();
            $elem.attr('current-value', newValue);
            var $rulesBlock = $elem.closest('.row').next();
            var $rulesBlockContainer = $rulesBlock.find('.container-fluid');

            if (currentValue === "Yes" || currentValue === "No") {
                if (newValue === "If" || newValue === "If Not") {
                    $rulesBlock.find('.col-sm-9').append($rulesBlockContainer.clone().attr('id', '').attr('key', 'Execute.Rule').show());
                    $rulesBlock.show();
                }
            } else {
                if (newValue === "Yes" || newValue === "No") {
                    $rulesBlockContainer.slice(1).remove();
                    $rulesBlock.hide();
                }
            }
        },

        updateRuleElseValue: function ($elem) {
            /* This function hides/shows  the corresponding "goto value" field for the onerror "goto".
            Internally calls the _updateCommonOnError function */
            $elem = $elem ? $elem : $(this);
            cleanupcases._updateCommonOnError($elem);
        },

        updateRunmode: function ($elem) {
            /* This function hides/shows  the corresponding "runmode value" field for the runmode type field */
            $elem = $elem ? $elem : $(this);
            var value =  $elem.find(':selected').text().trim();
            if (value !== "Standard") {
                $elem.closest('.row').next().show();
            } else {
                $elem.closest('.row').next().find('input').attr('value', '').val('');
                $elem.closest('.row').next().hide();
            }
        },

        updateOnErrorValue: function ($elem) {
            /* This function hides/shows  the corresponding "goto value" field for the onerror "goto".
            Internally calls the _updateCommonOnError function */
            $elem = $elem ? $elem : $(this);
            cleanupcases._updateCommonOnError($elem);
        }
    },

    validations: {

        checkIfEmpty: function() {
            var $elem = $(this);
            var parentDisplay = $elem.attr('display-parent') === 'true';
            var parentVisible = parentDisplay ? $elem.closest('.row').closest('.row').is(':visible') : false;
            if (parentDisplay === parentVisible) {
                if ($elem.val().trim() === "") {
                    katana.validationAPI.addFlag( $elem, 'Cannot be Empty');
                }
            }
        },

        checkIfEmptyOrNaN: function () {
            var $elem = $(this);
            var parentDisplay = $elem.attr('display-parent') === 'true';
            var parentVisible = $elem.closest('.row').closest('.row').is(':visible');
            if (parentDisplay === parentVisible) {
                if ($elem.val().trim() === "") {
                    katana.validationAPI.addFlag( $elem, 'Cannot be Empty');
                } else if (isNaN($elem.val().trim())) {
                    katana.validationAPI.addFlag( $elem, 'Has to be a valid numerical');
                }
            }
        }

    }

};

var debugcases = {

    mappings: {
        newStep: {
            drivers: false, //stores all drivers and actions' information
            repos:false, //stores all the repos and actions information
            title:  "New Step" //drawer title for when new step is being edited
        },
        newReq: {
            title: "New Requirement" //drawer title for when new req is being edited
        },
        editDetails: {
            title: "Edit Details" //drawer title for when details are being edited
        },
        editReq: {
            title: "Edit Requirement" //drawer title for when existing req is being edited
        },
        editStep: {
            title: "Edit Step" //drawer title for when existing step is being edited
        }
    },

    header: {
        toggleContents: function() {
            /* This function toggles the content when up/down font-awesomes are clicked */
            var $elem = $(this);
            if ($elem.attr('collapsed') === 'false') {
                $elem.attr('collapsed', 'true');
                $elem.removeClass('fa-chevron-circle-up');
                $elem.addClass('fa-chevron-circle-down');
                $elem.closest('.cases-header').next().hide()
            } else {
                $elem.attr('collapsed', 'false');
                $elem.removeClass('fa-chevron-circle-down');
                $elem.addClass('fa-chevron-circle-up');
                $elem.closest('.cases-header').next().show()
            }
        },

        editDetails: function() {
            /* This function gets data from displayed details block and
            creates the details block in the side drawer*/
            var $elem = $(this);
            var data = debugcases.generateJson.generateDetails($elem.closest('#main-div').find('#detail-block'));
            debugcases.drawer.openClosedDrawer(debugcases.mappings.editDetails.title);
            debugcases.drawer.open.highlightSidebar(0);
            debugcases.drawer.open.switchView.details($elem.closest('#main-div').find('#details_drawer_template').clone(), data);
        },

        newReq: function() {
            /* This function creates a new requirements block in the side drawer*/
            var $elem = $(this);
            debugcases.drawer.openClosedDrawer(debugcases.mappings.newReq.title);
            debugcases.drawer.open.highlightSidebar(1);
            debugcases.drawer.open.switchView.requirements($elem.closest('#main-div').find('#reqs_drawer_template').clone());
        },

        newStep: function() {
            /* This function creates a new step block in the side drawer*/
               document.getElementById("hiddingthird").style.display="block";
               document.getElementById("hiddingfirst").style.display="none";
               document.getElementById("hiddingsecond").style.display="none";

               document.getElementById("editfirst").style.display="none";
               document.getElementById("editsecond").style.display="none";
               document.getElementById("editthird").style.display="none";

               document.getElementById("editDetails").style.display="none";
            var $elem = $(this);
            debugcases.drawer.openClosedDrawer(debugcases.mappings.newStep.title);
            debugcases.drawer.open.highlightSidebar(2);
            var $container = $elem.closest('#main-div').find('#steps_drawer_template').clone().attr('step-type', 'edit').attr('index', debugcases.getLastStepNum());
            debugcases.drawer.open.switchView.steps($container, false, debugcases.getLastStepNum() + 1);
        }
    },

    drawer: {

        openDatafile: function () {
            /* This function opens the datafile in the datafile editor*/
            var $elem = $(this);
            var $inputElem = $elem.parent().prev().children('input');
            var tcPath = katana.$activeTab.find('#main-div').attr("current-file");
            var idfPath = katana.utils.getAbsoluteFilepath(tcPath, $inputElem.val(), true);
            $.ajax({
                headers: {
                    'X-CSRFToken': katana.$activeTab.find('input[name="csrfmiddlewaretoken"]').attr('value')
                },
                type: 'POST',
                url: 'check_if_file_exists/',
                data: {"path": idfPath}
            }).done(function(data){
                var pd = { type: 'POST',
                    headers: {'X-CSRFToken': katana.$activeTab.find('input[name="csrfmiddlewaretoken"]').attr('value')},
                    data:  {"path": idfPath}};
                if (data.exists) {
                    katana.templateAPI.load('/katana/wdf/index/', '/static/wdf_edit/js/main.js,',
                        null, 'WDF Editor', null, pd)
                } else {
                    katana.openAlert({
                        "alert_type": "danger",
                        "heading": "Problem Opening " + $inputElem.val(),
                        "text": "It seems like the file may not be available for viewing.",
                        "show_cancel_btn": false
                    });
                }
            });
        },

        openClosedDrawer: function (title) {
            /* This function opens the closed side Drawer*/
            var $drawerClosedDiv = katana.$activeTab.find('#main-div').find('.cases-side-drawer-closed');
            var $drawerOpenDiv = $drawerClosedDiv.siblings('.cases-side-drawer-open');
            $drawerClosedDiv.hide();
            $drawerOpenDiv.show();
            $drawerOpenDiv.find('.cases-drawer-open-header').find('h4').html(title);
        },

        closeOpenedDrawer: function () {
            /* This function closes the opened side Drawer*/
            var $drawerClosedDiv = katana.$activeTab.find('#main-div').find('.cases-side-drawer-closed');
            var $drawerOpenDiv = $drawerClosedDiv.siblings('.cases-side-drawer-open');
            $drawerClosedDiv.show();
            $drawerOpenDiv.hide();
        },

        open: {


            highlightSidebar: function (childIndex) {
                /* This function highlights the icon in the drawer sidebar */
                var $sidebarIcons = $(katana.$activeTab.find('.cases-drawer-open-body').find('.sidebar').children('div'));
                for (var i=0; i<$sidebarIcons.length; i++){
                    $($sidebarIcons[i]).removeClass('cases-icon-bg-color').addClass('cases-sidebar-disabled-icon');
                }
                $($sidebarIcons[childIndex]).addClass('cases-icon-bg-color').removeClass('cases-sidebar-disabled-icon');
            },

            switchView: {

                details: function($container, data) {
                    /* This function generates the details html for the drawer and attaches it to the drawer */
                    $container.attr("id", "current_details_editor").show();
                    debugcases.generateDetailsDisplayHtmlBlock($container, data);
                    katana.$activeTab.find('#details_drawer_template').parent().prepend(debugcases.proofDetailsContainer($container));
                },

                requirements: function($container, data, current) {
                    /* This function generates the reqs html for the drawer and attaches it to the drawer */
                    $container.attr("id", "current_reqs_editor").show();
                    if (data) {
                        $container.attr('current', current);
                        $container.find('input[key="Requirement"]').attr('value', data).val(data);
                    }
                    katana.$activeTab.find('#reqs_drawer_template').parent().prepend($container);
                },

                steps: function($container, data, stepNum) {
                    /* This function generates the step html for the drawer and attaches it to the drawer */
                    $container.attr("id", "current_steps_editor").show();
                    if (data) {
                        $container = debugcases.generateStepsHtmlBlock($container, data);
                    } else {
                        $container = debugcases.addTsToStepsHtmlBlock($container, stepNum);
                    }
                    katana.$activeTab.find('#steps_drawer_template').parent().prepend(debugcases.proofStepsContainer($container));
                }

            },

            saveContents: function () {
                /* This function calls specific functions internally that save information on the frontend */
                var $elem = $(this);
                var saved = false;
                var $openDrawer = $elem.closest('.cases-side-drawer-open');
                var $switchElem = $openDrawer.find('.cases-drawer-open-body').find('.sidebar').find('.cases-icon-bg-color').children('i');
                if ($switchElem) {
                    var reference = $switchElem.attr('ref');
                    if (reference === "editDetails") {
                        saved = debugcases.drawer.open._saveContents.details($openDrawer.find('.content').find('#current_details_editor'));
                    } else if (reference === "newReq") {
                        saved = debugcases.drawer.open._saveContents.requirements($openDrawer.find('.content').find('#current_reqs_editor'));
                    } else if (reference === "newStep") {
                        saved = debugcases.drawer.open._saveContents.steps($openDrawer.find('.content').find('#current_steps_editor'));
                    }
                    if (saved) {
                        $openDrawer.find('.cases-drawer-open-body').find('.content').find('[id^="current"]').remove();
                        debugcases.drawer.closeOpenedDrawer();
                    }
                }
            },

            _saveContents: {

                details: function ($container) {
                    /* This function collects details data from the drawer and adds it to the displayed details block*/
                    if (katana.validationAPI.init($container)) {
                        var data = debugcases.generateJson.generateDetails($container);
                        var displayContent = debugcases.generateDetailsDisplayHtmlBlock(katana.$activeTab.find('#cases-display-template').clone(), data);
                        katana.$activeTab.find('#cases-display-template').replaceWith(displayContent);
                        return true;
                    } else {
                        return false;
                    }
                },

                requirements: function ($container) {
                    /* This function collects reqs data from the drawer and adds it to the displayed reqs block*/
                    if (katana.validationAPI.init($container)) {
                        var data = debugcases.generateJson.generateRequirements(katana.$activeTab.find('#cases-requirements-template'));
                        var temp = debugcases.generateJson.generateRequirements($container);
                        var index = $container.attr('current') ? $container.attr('current') : data.Requirements.Requirement.length;
                        data.Requirements.Requirement.splice(index, 1, temp.Requirements.Requirement[0]);
                        var displayContent = debugcases.generateRequirementsHtmlBlock(katana.$activeTab.find('#cases-requirements-template').clone(), data);
                        katana.$activeTab.find('#cases-requirements-template').replaceWith(displayContent);
                        return true;
                    } else {
                        return false;
                    }
                },

                steps: function ($container) {
                    /* This function collects step data from the drawer and adds it to the displayed step block*/
                    if (katana.validationAPI.init($container)) {
                        var data = debugcases.generateJson.generateStep($container);
                        var filteredArgs = [];
                        for (var i=0; i<data.Debug.step[0].Arguments.argument.length; i++) {
                            if (data.Debug.step[0].Arguments.argument[i]["@value"] !== "") {
                                filteredArgs.push(Object.assign({}, data.Debug.step[0].Arguments.argument[i]));
                            }
                        }
                        data.Debug.step[0].Arguments.argument = filteredArgs;
                        var displayContent = debugcases.generateStepsDisplayHtmlBlock(katana.$activeTab.find('#step-row-template-debug').clone().attr('id', ''), data);
                        var stepType = $container.attr('step-type') === "edit";
                        var index = parseInt($container.attr('index'));
                        var $allTrs = katana.$activeTab.find('#cases-steps-template-debug').find('tbody').find('tr');
                        if (stepType && index < $allTrs.length) {
                            $allTrs[index].remove();
                        }
                        if (index === 0) {
                            katana.$activeTab.find('#cases-steps-template-debug').find('tbody').prepend(displayContent);
                            debugcases.redoStepNums();
                        } else {
                            displayContent.insertAfter($($allTrs[index-1]));
                            debugcases.redoStepNums();
                        }
                        return true;
                    } else {
                        return false;
                    }
                }
            },

            discardContents: function () {
                /* This function deletes contents from the drawer */
                var $elem = $(this);
                var $openDrawer = $elem.closest('.cases-side-drawer-open');
                katana.openAlert({
                    "alert_type": "warning",
                    "heading": "All changes will be discarded",
                    "text": "This action will discard all changes, are you sure you want to continue?"
                    }, function () {
                        $openDrawer.find('.cases-drawer-open-body').find('.content').find('[id^="current"]').remove();
                        debugcases.drawer.closeOpenedDrawer();
                    })
            }
        },

        openFileExplorer: {

            logsOrResultsDir: function (relative, $elem) {
                /* This common function gets filepath from the fileexplorer and ataches it to the correct input field*/
                $elem = $elem ? $elem : $(this);
                var $inputElem = $elem.parent().prev().children('input');
                relative = !!relative;
                katana.fileExplorerAPI.openFileExplorer("Select a Path", false,
                    katana.$activeTab.find('input[name="csrfmiddlewaretoken"]').attr('value'), false,
                    function (inputValue){
                        if (relative) {
                            var tcPath = katana.$activeTab.find('#main-div').attr("current-file");
                            inputValue = katana.utils.getRelativeFilepath(tcPath, inputValue, true);
                        }
                        $inputElem.val(inputValue);
                        $inputElem.attr('value', inputValue);
                    },
                    false)
            },

            inputDataFile: function () {
                /* This function calls logsOrResultsDir with relative as true so that relative path is created. */
                debugcases.drawer.openFileExplorer.logsOrResultsDir(true, $(this));
            }
        }
    },

    invert: function(){
        /* This function switches between the testcase files view and the actual testcase */
        var toolbarButtons = katana.$activeTab.find('.tool-bar').find('button');
        for(var i=0; i<toolbarButtons.length; i++){
            if($(toolbarButtons[i]).is(":hidden")){
                $(toolbarButtons[i]).show();
            } else {
                $(toolbarButtons[i]).hide();
            }
        }
        var divs = katana.$activeTab.find('#body-div').children();
        for(i=0; i<divs.length; i++){
            if($(divs[i]).is(":hidden")){
                $(divs[i]).show();
            } else {
                $(divs[i]).hide();
            }
        }
    },

    landing: {
        init: function(){
            /* This function get the list of testcase files, displays them, and
            attaches click event on each testcase file */
            $.ajax({
                type: 'GET',
                url: 'testwrapper/get_list_of_testwrappers/'
            }).done(function(data){
                katana.jsTreeAPI.createJstree(katana.$activeTab.find('#tree-div'), data.data);
                katana.$activeTab.find('#tree-div').on("select_node.jstree", function (e, data){
                    if (data["node"]["icon"] === "jstree-file") {
                        $.ajax({
                            headers: {
                                'X-CSRFToken': katana.$activeTab.find('.csrf-container').html()
                            },
                            type: 'GET',
                            url: 'testwrapper/get_file/',
                            data: {"path": data["node"]["li_attr"]["data-path"]}
                        }).done(function(data){
                            if(data.status){
                                debugcases.invert();
                                katana.$activeTab.find('#main-div').attr("current-file", data.filepath);
                                katana.$activeTab.find('.tool-bar').find('.title').html(data.filename);
                                katana.$activeTab.find('#main-div').html(data.html_data);
                                debugcases.mappings.newStep.drivers = data.drivers;
                            } else {
                                katana.openAlert({"alert_type": "danger",
                                    "heading": "Could not open file",
                                    "text": "Errors: " + data.message,
                                    "show_cancel_btn": false})
                            }
                        });
                    }
                });
            })
        },

        openNewFile: function(){
            /* This function opens a new testcase */
            $.ajax({
                headers: {
                    'X-CSRFToken': katana.$activeTab.find('.csrf-container').html()
                },
                type: 'GET',
                url: 'testwrapper/get_file/',
                data: {"path": false}
            }).done(function(data){
                if(data.status){
                    debugcases.invert();
                    katana.$activeTab.find('#main-div').attr("current-file", data.filepath);
                    katana.$activeTab.find('.tool-bar').find('.title').html(data.filename);
                    katana.$activeTab.find('#main-div').html(data.html_data);
                    debugcases.mappings.newStep.drivers = data.drivers;
                } else {
                    katana.openAlert({"alert_type": "danger",
                        "heading": "Could not open file",
                        "text": "Errors: " + data.message,
                        "show_cancel_btn": false})
                }
            });
        }
    },

    caseViewer:  {
        close: function () {
            /* This function closes the testcase */
            katana.$activeTab.find('#main-div').html("");
            katana.$activeTab.find('.tool-bar').find('.title').html("");
            debugcases.invert();
        },

        save: function () {
            /* This function collects data from each displayed block and saves the testcase */
            var final_json = {"TestWrapper": {}};
            var filepath = katana.$activeTab.find('#main-div').attr("current-file");
            var filename = katana.$activeTab.find('.tool-bar').find('.title').html();
            $.extend(true, final_json.Testcase, debugcases.generateJson.generateDetails(katana.$activeTab.find('#detail-block')));
//            $.extend(true, final_json.Testcase, debugcases.generateJson.generateRequirements(katana.$activeTab.find('#req-block')));
            $.extend(true, final_json.Testcase, debugcases.generateJson.generateStep(katana.$activeTab.find('#step-block-debug')));


            var callBack_on_accept = function(inputValue) {
                $.ajax({
                    headers: {
                        'X-CSRFToken': katana.$activeTab.find('input[name="csrfmiddlewaretoken"]').attr('value')
                    },
                    type: 'POST',
                    url: 'testwrapper/save_file/',
                    data: {"data": JSON.stringify(final_json), "directory": filepath, "filename": inputValue, "extension": ".xml"}
                }).done(function(data){
                    if (data.status) {
                        katana.openAlert({
                            "alert_type": "success",
                            "heading": "File Saved",
                            "text": inputValue + " has been saved successfully",
                            "show_cancel_btn": false
                        });
                        debugcases.caseViewer.close();
                    } else {
                        katana.openAlert({
                            "alert_type": "danger",
                            "heading": "File Not Saved",
                            "text": "Some problem occurred while saving the file: " + inputValue,
                            "show_cancel_btn": false
                        })
                    }
                });
            };

            katana.openAlert({
                "alert_type": "light",
                "heading": "Name for the file",
                "text": "",
                "prompt": "true",
                "prompt_default": filename
                },
                function(inputValue){
                $.ajax({
                    headers: {
                        'X-CSRFToken': katana.$activeTab.find('input[name="csrfmiddlewaretoken"]').attr('value')
                    },
                    type: 'POST',
                    url: 'check_if_file_exists/',
                    data: {"filename": inputValue, "directory": filepath, "extension": ".xml"}
                }).done(function(data){
                     if(data.exists){
                        katana.openAlert({
                            "alert_type": "warning",
                            "heading": "File Exists",
                            "text": "A file with the name " + inputValue + " already exists; do you want to overwrite it?",
                            "accept_btn_text": "Yes",
                            "cancel_btn_text": "No"
                            }, function() {
                            callBack_on_accept(inputValue)}
                            )
                     } else {
                        callBack_on_accept(inputValue);
                     }
                });
            });
        }
    },

    reqSection: {
        deleteReq: function () {
            /* This function deletes a req */
            var $elem = $(this);
            var $tdParent = $elem.closest('td');
            var reqNumber = $tdParent.siblings('th').html();
            var $toBeDeleted = $elem.closest('tr');
            var $topLevel = $elem.closest('#cases-requirements-template');
            katana.openAlert({
                "alert_type": "danger",
                "heading": "Delete Requirement " + reqNumber + "?",
                "text": "Are you sure you want to delete the requirement? This cannot be undone."
            }, function(){
                $toBeDeleted.remove();
                var data = debugcases.generateJson.generateRequirements($topLevel);
                var displayContent = debugcases.generateRequirementsHtmlBlock($topLevel.clone(), data);
                $topLevel.replaceWith(displayContent);
            });
        },

        editReq: function () {
            /* This function opens a req in the req editor*/
            var $elem = $(this);
            var data = $($elem.closest('.cases-req').children('div')[0]).html().trim();
            debugcases.drawer.openClosedDrawer(debugcases.mappings.editReq.title);
            debugcases.drawer.open.highlightSidebar(1);
            debugcases.drawer.open.switchView.requirements($elem.closest('#main-div').find('#reqs_drawer_template').clone(), data, $elem.closest('tr').attr('req-number')-1);
        }
    },

    stepSection: {
        selectStep: function () {
            /* This function selects a step */
            var $elem = $(this);
            var $allTrElems = $elem.parent().children('tr');
            if ($elem.attr('marked') === 'true') {
                $elem.attr('marked', 'false');
                $elem.css('background-color', '');
            } else {
                var multiselect = katana.$activeTab.find('.cases-step-toolbar').find('.fa-th-list').attr('multiselect');
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
                /* This function de/activates the multiselect functionality for a step */
                var $elem = $(this);
                var $iconElem = $elem.children('i');
                if ($iconElem.attr('multiselect') === 'on'){
                    $iconElem.attr('multiselect', 'off');
                    $iconElem.removeClass('badged');
                    $iconElem.children('i').hide();
                    var $allTrElems = katana.$activeTab.find('#step-block-debug').find('tbody').children('tr');
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
                /* This function deletes a step */
                var $tbodyElem = katana.$activeTab.find('#step-block-debug').find('tbody');
                var $allTrElems = $tbodyElem.children('tr[marked="true"]');
                if ($allTrElems.length === 0) {
                    katana.openAlert({"alert_type": "danger",
                        "heading": "No step selected for deletion",
                        "text": "Please select at least one step to delete",
                        "show_cancel_btn": "false"})
                } else {
                    var stepNumbers = "";
                    for (var i=0; i<$allTrElems.length; i++){
                        stepNumbers += ($($allTrElems[i]).index() + 1).toString() + ", "
                    }
                    stepNumbers = stepNumbers.slice(0, -2);
                    katana.openAlert({"alert_type": "warning",
                        "heading": "This would delete Steps " + stepNumbers,
                        "text": "Are you sure you want to delete these steps?"},
                        function () {
                            for (var i=0; i<$allTrElems.length; i++){
                                $($allTrElems[i]).remove();
                            }
                            debugcases.redoStepNums();
                        })
                }
            },

            insertStep: function () {
            document.getElementById("hiddingfirst").style.display="none";
            document.getElementById("hiddingthird").style.display="block";
            document.getElementById("hiddingsecond").style.display="none";

            document.getElementById("editfirst").style.display="none";
            document.getElementById("editthird").style.display="none";
               document.getElementById("editsecond").style.display="none";
               

               document.getElementById("editDetails").style.display="none";
//                document.getElementById("hiddingfirst").style.display="none ";
                /* This function opens a new step in the step editor and inserts it into a speific spot when saved */
                var $elem = $(this);
                var $tbodyElem = katana.$activeTab.find('#step-block-debug').find('tbody');
                var $allTrElems = $tbodyElem.children('tr[marked="true"]');
                if ($allTrElems.length === 0) {
                    var insertAtIndex = $tbodyElem.children('tr').length;
                } else if ($allTrElems.length > 1) {
                    katana.openAlert({
                        "alert_type": "danger",
                        "heading": "Multiple Steps Selected",
                        "text": "Only one step can be inserted at a time. Please select only one " +
                        "step above which you want to insert another step.",
                        "show_cancel_btn": false
                    });
                    return;
                } else {
                    insertAtIndex = $($allTrElems[0]).index();
                }

                debugcases.drawer.openClosedDrawer(debugcases.mappings.newStep.title);
                debugcases.drawer.open.highlightSidebar(2);
                var $container = $elem.closest('#main-div').find('#steps_drawer_template').clone().attr("step-type", "insert").attr("index", insertAtIndex);
                debugcases.drawer.open.switchView.steps($container, false, insertAtIndex+1);

            },

            editStep: function () {
             document.getElementById("hiddingfirst").style.display="none";
            document.getElementById("hiddingsecond").style.display="none";
            document.getElementById("hiddingthird").style.display="none";

            document.getElementById("editfirst").style.display="none";
            document.getElementById("editsecond").style.display="none";
               document.getElementById("editthird").style.display="block";

               document.getElementById("editDetails").style.display="none";
                /* This function opens the step in the step editor and replaces the existing step when saved */
                var $elem = $(this);
                var $tbodyElem = katana.$activeTab.find('#step-block-debug').find('tbody');
                var $allTrElems = $tbodyElem.children('tr[marked="true"]');
                if ($allTrElems.length === 0) {
                    katana.openAlert({
                        "alert_type": "danger",
                        "heading": "No Step Selected",
                        "text": "Please select a step to edit.",
                        "show_cancel_btn": false
                    });
                } else if ($allTrElems.length > 1) {
                    katana.openAlert({
                        "alert_type": "danger",
                        "heading": "Multiple Steps Selected",
                        "text": "Only one step can be edited at a time. Please select only one " +
                        "step to edit.",
                        "show_cancel_btn": false
                    });
                } else {
                    var data = setupcases.generateJson.generateStep($($allTrElems[0]));
                    setupcases.drawer.openClosedDrawer(setupcases.mappings.editStep.title);
                    setupcases.drawer.open.highlightSidebar(2);
                    var $container = $elem.closest('#main-div').find('#steps_drawer_template').clone().attr('step-type', 'edit').attr('index', $($allTrElems[0]).index());
                    setupcases.drawer.open.switchView.steps($container, data);
                }
            }
        }
    },

    generateJson: {

        generateDetails: function ($container) {
            /* This function creates details json out of an HTML block */
            var finalJson = {Details: {}};
            var $allKeys = $container.find('[key]');
            var value = false;
            for (var i=0; i <$allKeys.length; i++) {
                value = $($allKeys[i]).val() ? $($allKeys[i]).val().trim() : $($allKeys[i]).html().trim();
                $.extend(true, finalJson.Details, debugcases.generateJson._updateJson($($allKeys[i]).attr("key").trim(), value));
            }
            return finalJson;
        },

        generateRequirements: function ($container) {
            /* This function creates requirements json out of an HTML block */
            var finalJson = {Requirements: { Requirement: []}};
            var $allKeys = $container.find('[key]');
            var value = false;
            for (var i=0; i <$allKeys.length; i++) {
                value = $($allKeys[i]).val() ? $($allKeys[i]).val().trim() : $($allKeys[i]).html().trim();

            }
            return ;
        },

        generateStep: function ($container) {
            /* This function creates steps json out of an HTML block */
            var finalJson = {Debug: { step: []}};
            var $allSteps = $container.attr('key') === 'step'? [$container] : $container.find('[key="step"]');
            var $allKeys = false;
            var partialData = false;
            for (var i=0; i <$allSteps.length; i++) {
                $allKeys = $($allSteps[i]).find('[key]').not('[key*="Execute.Rule"]').not('[key*="Arguments"]');
                partialData = {};
                for (var j=0; j<$allKeys.length; j++) {
                    var key = $($allKeys[j]).attr("key").trim();
                    var value = $($allKeys[j]).val() ? $($allKeys[j]).val().trim() : $($allKeys[j]).html().trim();
                    $.extend(true, partialData, debugcases.generateJson._updateJson(key, value));
                }
                $.extend(true, partialData, debugcases.generateJson.generateArguments($($allSteps[i]).find('[key="Arguments.argument"]')));
                $.extend(true, partialData, debugcases.generateJson.generateExecuteRules($($allSteps[i]).find('[key="Execute.Rule"]')));
                finalJson.Debug.step.push(partialData);
            }
            return finalJson
        },

        generateExecuteRules: function ($container){
            /* This function creates execute (rules) json out of an HTML block. Typically this function should
            never be called independently. */
            var finalJson = {Execute: {Rule: []}};
            var partialData = false;
            var $ruleBlock = false;
            for (var i=0; i<$container.length; i++) {
                $ruleBlock = $($container[i]).find('[key]');
                partialData = {};
                for (var j=0; j<$ruleBlock.length; j++) {
                    var key = $($ruleBlock[j]).attr("key").trim();
                    var val = $($ruleBlock[j]).val() ? $($ruleBlock[j]).val().trim() : $($ruleBlock[j]).attr('value');
                    var value = val ? val.trim() : $($ruleBlock[j]).html().trim();
                    $.extend(true, partialData, debugcases.generateJson._updateJson(key, value));
                }
                finalJson.Execute.Rule.push(Object.assign({}, partialData.Execute.Rule));
            }
            return finalJson;
        },

        generateArguments: function ($container){
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
                    $.extend(true, partialData, debugcases.generateJson._updateJson(key, value));
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
                data[key] = debugcases.generateJson._updateJson(remaining_key, value)
            } else {
                data[unrefined_key] = value;
            }
            return data;
        }
    },

    getValueFromJson: function (data, unrefined_key) {
        /* This function iterates through a json recursively and gets the value for the given key.
        This function should never be called independently */
        var key = unrefined_key.split(/\.(.+)/)[0];
        var remaining_key = unrefined_key.split(/\.(.+)/)[1];
        if (key !== undefined && remaining_key !== undefined) {
            return debugcases.getValueFromJson(data[key], remaining_key)
        }
        return data[key]
    },

    generateDetailsDisplayHtmlBlock: function ($container, data) {
        /* This function generates the details block out of an HTML block and json data */
        var $allKeys = $container.find('[key]');
        for (var i=0; i<$allKeys.length; i++) {
            if ($($allKeys[i]).prop('type') === 'text') {
                $($allKeys[i]).attr('value', debugcases.getValueFromJson(data.Details, $($allKeys[i]).attr('key')));
            } else if ($($allKeys[i]).prop('type') === 'select-one') {
                $($allKeys[i]).attr('value', debugcases.getValueFromJson(data.Details, $($allKeys[i]).attr('key')));
                var value = debugcases.getValueFromJson(data.Details, $($allKeys[i]).attr('key'));
                var $allOptions = $($allKeys[i]).children();
                for (var j=0; j<$allOptions.length; j++) {
                    if ($($allOptions[j]).text() === value) {
                        $($allOptions[j]).prop('selected', true);
                        break;
                    }
                }
            } else {
                $($allKeys[i]).html(debugcases.getValueFromJson(data.Details, $($allKeys[i]).attr('key')));
            }
        }
        return $container
    },

    generateRequirementsHtmlBlock: function ($container, data) {
        /* This function generates the requirements block out of an HTML block and json data */
        var $constantTemplate = $container.find('#req-table-template').clone().attr('id', "").show();
        var start = 0;
        var mid = Math.floor((data.Requirements.Requirement.length + 1) /2);
        var end = data.Requirements.Requirement.length;
        var $tableTemplateLeft = debugcases._generateReqTable(data, start, mid, $constantTemplate, $constantTemplate.clone());
        var $tableTemplateRight = debugcases._generateReqTable(data, mid, end, $constantTemplate, $constantTemplate.clone());
        $($container.find('.cases-internal-space')[0]).html($tableTemplateLeft);
        $($container.find('.cases-internal-space')[1]).html($tableTemplateRight);
        return $container;
    },

    _generateReqTable: function (data, start, end, $constantTemplate, $container) {
        /* This function is called by generateRequirementsHtmlBlock which creates the req block */
        var $trTemplate = false;
        $container.find('tr').remove();
        for (var i=start; i<end; i++) {
            $trTemplate = $constantTemplate.find('tr').clone();
            $trTemplate.attr('req-number', i+1);
            $trTemplate.find('th').html(i+1);
            $($trTemplate.find('td').children('div')[0]).attr('key', 'Requirement').html(data.Requirements.Requirement[i]);
            $container.find('tbody').append($trTemplate);
        }
        return $container;
    },

    generateStepsHtmlBlock: function ($container, data) {
        /* This function generates the steps block (side-drawer) out of an HTML block and json data */
        var $allKeys = $container.find('[key]').not('[key*="Execute"]').not('[key*="Arguments"]');
        for (var i=0; i<$allKeys.length; i++) {
            if ($($allKeys[i]).prop('type') === 'text') {
                $($allKeys[i]).attr('value', debugcases.getValueFromJson(data.Debug.step[0], $($allKeys[i]).attr('key')));
            } else if ($($allKeys[i]).prop('type') === 'select-one') {
                $($allKeys[i]).attr('value', debugcases.getValueFromJson(data.Debug.step[0], $($allKeys[i]).attr('key')));
                var value = debugcases.getValueFromJson(data.Debug.step[0], $($allKeys[i]).attr('key'));
                var $allOptions = $($allKeys[i]).children();
                for (var j=0; j<$allOptions.length; j++) {
                    if ($($allOptions[j]).text() === value) {
                        $($allOptions[j]).prop('selected', true);
                        break;
                    }
                }
            } else {
                $($allKeys[i]).html(debugcases.getValueFromJson(data.Debug.step[0], $($allKeys[i]).attr('key')));
            }
        }
        $container = debugcases._addExecuteBlock($container, data);
        $container = debugcases._addArgumentsEtcBlock($container, data);
        return $container
    },

    _addExecuteBlock: function ($container, data) {
        /* This function generates the execute block (side-drawer) out of an HTML block and json data.
        This function should not be called independently */
        var $execTypeBlock = $container.find('[key="Execute.@ExecType"]');
        $execTypeBlock.attr('current-value', debugcases.getValueFromJson(data.Debug.step[0], $execTypeBlock.attr('key')));
        debugcases._selectOption($execTypeBlock, $execTypeBlock.attr('current-value'));

        var $ruleBlock = $execTypeBlock.closest('.row').next().find('#rule-template');
        for (var k=0; k<data.Debug.step[0].Execute.Rule.length; k++) {
            var $currentRuleBlock = $ruleBlock.clone().attr('id', '').attr('key', 'Execute.Rule').show();
            var $allKeys = $currentRuleBlock.find('[key]');
            for (var i=0; i<$allKeys.length; i++) {
                var value = debugcases.getValueFromJson({"Execute" : {"Rule": data.Debug.step[0].Execute.Rule[k]}}, $($allKeys[i]).attr('key'));
                $($allKeys[i]).attr('value', value);
                if ($($allKeys[i]).prop('type') === 'select-one') {
                    debugcases._selectOption($($allKeys[i]), value);
                }
            }
            debugcases.stepEditor.updateRuleElseValue($currentRuleBlock.find('[key="Execute.Rule.@Else"]'));
            $ruleBlock.parent().append($currentRuleBlock);
            $execTypeBlock.closest('.row').next().show();
        }

        return $container
    },

    _addArgumentsEtcBlock: function ($container, data) {
        /* This function generates the arguments block (side-drawer) out of an HTML block and json data.
        This function should not be called independently */
        debugcases.stepEditor.getDrivers($container.find('[key="@Repo"]'), $container.find('[key="@Driver"]').val());
        debugcases.stepEditor.getKeywords($container.find('[key="@Driver"]'), $container.find('[key="@Keyword"]').val());
        var $allArgs = $container.find('[key="Arguments.argument"]');
        for (var i=0 ; i<$allArgs.length; i++) {
            var currentArg = $($allArgs[i]).find('.cases-label').text();
            for (var j=0; j<data.Debug.step[0].Arguments.argument.length; j++) {
                if (data.Debug.step[0].Arguments.argument[j]["@name"] === currentArg) {
                    $($allArgs[i]).find('[key="Arguments.argument.@value"]').attr('value', data.Debug.step[0].Arguments.argument[j]["@value"]);
                    break;
                }
            }
        }
        return $container;
    },

    generateStepsDisplayHtmlBlock: function ($container, data) {
        /* This function generates the steps block (main page) out of an HTML block and json data */
        $container = $($container.html());
        var $allKeys = $container.find('[key]').not('[key*="Execute.Rule"]').not('[key*="Arguments"]');
        for (var i=0; i<$allKeys.length; i++) {
            if ($($allKeys[i]).prop('type') === 'text') {
                $($allKeys[i]).attr('value', debugcases.getValueFromJson(data.Debug.step[0], $($allKeys[i]).attr('key')));
            } else if ($($allKeys[i]).prop('type') === 'select-one') {
                $($allKeys[i]).attr('value', debugcases.getValueFromJson(data.Debug.step[0], $($allKeys[i]).attr('key')));
                var value = debugcases.getValueFromJson(data.Debug.step[0], $($allKeys[i]).attr('key'));
                var $allOptions = $($allKeys[i]).children();
                for (var j=0; j<$allOptions.length; j++) {
                    if ($($allOptions[j]).text() === value) {
                        $($allOptions[j]).prop('selected', true);
                        break;
                    }
                }
            } else {
                $($allKeys[i]).html(debugcases.getValueFromJson(data.Debug.step[0], $($allKeys[i]).attr('key')));
            }
        }
        $container = debugcases.evaluateDisplayRunmode($container);
        $container = debugcases.evaluateDisplayOnError($container);
        $container = debugcases.evaluateDisplayArguments($container, data);
        $container = debugcases.evaluateDisplayExecute($container, data);
        return $container;
    },

    evaluateDisplayRunmode: function ($container) {
        /* This function hides/shows the runmode block (main page).
        This function should not be called independently */
        if($container.find('[key="runmode.@type"]').html().trim() === "Standard") {
            $container.find('[key="runmode.@type"]').next().next().remove();
            $container.find('[key="runmode.@type"]').next().remove();
        }
        return $container;
    },

    evaluateDisplayOnError: function ($container) {
        /* This function hides/shows the onerror block (main page).
        This function should not be called independently */
        if($container.find('[key="onError.@action"]').html().trim() !== "Go To") {
            $container.find('[key="onError.@action"]').next().next().remove();
            $container.find('[key="onError.@action"]').next().remove();
        }
        return $container;
    },

    evaluateDisplayArguments: function ($container, data) {
        /* This function hides/shows the argument block (main page).
        This function should not be called independently */
        var $templateArg = $container.find('[key="Arguments.argument"]').clone();
        var $argBlock = $container.find('[key="Arguments"]').empty();
        for (var i=0; i<data.Debug.step[0].Arguments.argument.length; i++) {
            var $currentArgBlock = $templateArg.clone();
            $currentArgBlock.find('[key="Arguments.argument.@name"]').html(data.Debug.step[0].Arguments.argument[i]["@name"]);
            $currentArgBlock.find('[key="Arguments.argument.@value"]').html(data.Debug.step[0].Arguments.argument[i]["@value"]);
            $argBlock.append($currentArgBlock);
        }
        return $container
    },

    evaluateDisplayExecute: function ($container, data) {
        /* This function hides/shows the execute block (main page).
        This function should not be called independently */
        var $templateExecRule = $container.find('[key="Execute.Rule"]').clone();
        $container.find('[key="Execute.Rule"]').next().remove();
        $container.find('[key="Execute.Rule"]').remove();
        for (var i=0; i<data.Debug.step[0].Execute.Rule.length; i++) {
            var $currentTemplate = $templateExecRule.clone();
            var $allKeys = $currentTemplate.find('[key]');
            for (var j=0; j<$allKeys.length; j++) {
                $($allKeys[j]).html(debugcases.getValueFromJson({"Execute": {"Rule": data.Debug.step[0].Execute.Rule[i]}}, $($allKeys[j]).attr('key')));
            }
            $container.find('[key="Execute.@ExecType"]').parent().append($currentTemplate);
            $container.find('[key="Execute.@ExecType"]').parent().append('<br>');
        }
        return $container
    },

    _selectOption: function ($elem, value) {
        /* This function selects an "option" in a <select> tag.
        This function should not be called independently */
        var $allOptions = $elem.children();
        for (var j=0; j<$allOptions.length; j++) {
            if ($($allOptions[j]).text().trim() === value) {
                $($allOptions[j]).prop('selected', true);
                break;
            }
        }
    },

    proofDetailsContainer: function ($container) {
        /* This function verifies if the all the correct fields are shown/hidden in the details (side-drawer) block */
        debugcases.detailsEditor.updateDefaultOnError($container.find('[key="default_onError.@action"]'));
        debugcases.detailsEditor.updateIterationTypeStepTmpl($container.find('[key="Datatype"]'));
        return $container;
    },

    proofStepsContainer: function ($container) {
        /* This function verifies if the all the correct fields are shown/hidden in the step (side-drawer) block */
        debugcases.stepEditor.updateRules($container.find('[key="Execute.@ExecType"]'));
        debugcases.stepEditor.updateRunmode($container.find('[key="runmode.@type"]'));
        debugcases.stepEditor.updateOnErrorValue($container.find('[key="onError.@action"]'));
        return $container
    },

    getLastStepNum: function () {
        /* This function gets the last step number */
        return katana.$activeTab.find('#main-div').find('#cases-steps-template-debug').find('tbody').children('tr').length;
    },

    redoStepNums: function(){
        var $tbodyElem = katana.$activeTab.find('#step-block-debug').find('table').find('tbody');
        var $allTrElems = $tbodyElem.children('tr');
        for (var i=0; i<$allTrElems.length; i++){
            $($($allTrElems[i]).children('td')[0]).html(i+1);
        }
    },

    addTsToStepsHtmlBlock: function ($container, stepNum) {
        /* This function adds the step number to the step (side-drawer) block */
        $container.find('[key="@TS"]').attr('value', stepNum).val(stepNum);
        return $container
    },

    _updateCommonOnError: function ($elem) {
        /* This common function hides/shows  the corresponding "goto value" field for the onerror "goto" */
        var value = $elem.find(':selected').text().trim();
        if (value === "Go To") {
            $elem.closest('.row').next().show();
        } else {
            $elem.closest('.row').next().find('input').attr('value', '').val('');
            $elem.closest('.row').next().hide();
        }
        $elem.attr('value', value);
    },

    detailsEditor: {

        updateDefaultOnError: function ($elem) {
            /* This function hides/shows  the corresponding "goto value" field for the onerror "goto".
            Internally calls the _updateCommonOnError function */
            $elem = $elem ? $elem : $(this);
            debugcases._updateCommonOnError($elem);
        },

        updateIterationTypeStepTmpl: function ($elem) {
            /* This function disables/enables the step-level "Iteration Type" field for any change in the details
              level datatype field change */
            $elem = $elem ? $elem : $(this);
            var value = $elem.find(':selected').text().trim();
            var $parent = $elem.closest('.content').length > 0 ? $elem.closest('.content') : katana.$activeTab.find('#main-div');
            var $iterationTypeElem = $parent.find('#steps_drawer_template').find('[key="Iteration_type.@type"]');
            if (value === "Hybrid") {
                $iterationTypeElem.prop('disabled', false);
            } else {
                $iterationTypeElem.find(':selected').prop('selected', false);
                $iterationTypeElem.find('option:contains("Standard")').prop('selected', true);
                $iterationTypeElem.prop('disabled', true);
            }
        }
    },

    stepEditor: {
        getDrivers: function ($elem, driverName) {
            /* This function internally calls the getArgumentsEtc function for updating related fields on driver change */
            $elem = $elem ? $elem : $(this);
            driverName = driverName ? driverName : "";
            var repoName = $elem.val();
            var $driverRow = $elem.closest('.row').next();
            $driverRow.find('input').attr("value", driverName).val(driverName);
            $elem.attr("value", repoName);
            $driverRow.find('#drivers').html("");
            for (driver in cases.mappings.newStep.drivers[repoName]) {
                        $driverRow.find('#drivers').append('<option>' + driver + '</option>');
                    }
                },

        getKeywords: function ($elem, kwName) {
            /* This function internally calls the getArgumentsEtc function for updating related fields on driver change */
            $elem = $elem ? $elem : $(this);

            kwName = kwName ? kwName : "";
            var driverName = $elem.val();
            var $repoRow = $elem.closest('.row').prev();
            var $kwRow = $elem.closest('.row').next();
            var repo = $repoRow.find('input').attr("value");
            $kwRow.find('input').attr("value", kwName).val(kwName);
            $kwRow.find('#keywords').html("");
             for (keyword in debugcases.mappings.newStep.drivers[repo][driverName].actions){
                $kwRow.find('#keywords').append('<option>' + keyword + '</option>');
            }
            debugcases.stepEditor.getArgumentsEtc($kwRow.find('input'));
        },

        getArgumentsEtc: function ($elem, data) {
            /* This function internally calls the _setSignature, _setArguments, _setWDescription, _setComments
            functions for upadting those fields on kw name change */
            $elem = $elem ? $elem : $(this);
            var kwName = $elem.val();
            var driverName = $elem.closest('.row').prev().find('input').val();
            $DriverRow = $elem.closest('.row').prev();
            Repo=$DriverRow.closest('.row').prev().find('input').attr("value");
            data = data ? data : false;

            if (driverName in debugcases.mappings.newStep.drivers[Repo]) {
                if (kwName in debugcases.mappings.newStep.drivers[Repo][driverName].actions) {
                    data = debugcases.mappings.newStep.drivers[Repo][driverName].actions[kwName]
                }
            }

            debugcases.stepEditor._setSignature($elem.closest('.row').next(), data);
            debugcases.stepEditor._setArguments($elem.closest('.row').next().next(), data);
            debugcases.stepEditor._setWDescription($elem.closest('.row').next().next().next(), data);
            debugcases.stepEditor._setComments($elem.closest('.row').next().next().next().next(), data);
        },

        _setSignature: function ($topLevelSignRow, data) {
            /* This function hides/shows corresponding function signature */
            $topLevelSignRow.hide();
            $topLevelSignRow.find('input').attr('value', '');
            if (data) {
                $topLevelSignRow.find('textarea').html(data.signature);
                $topLevelSignRow.show();
            }
        },

        _setArguments: function ($topLevelArgRow, data) {
            /* This function hides/shows corresponding arguments */
            var $argRow = $topLevelArgRow.find('#arg-template').clone().attr('key', 'Arguments.argument').show();
            var $argContainer = $topLevelArgRow.find('.container-fluid');
            $argContainer.children().slice(1).remove();
            $topLevelArgRow.hide();
            var temp = false;

            if (data) {
                for (var i=0; i<data.arguments.length; i++){
                    temp = $argRow.clone();
                    temp.find('.cases-label').html(data.arguments[i]);
                    $argContainer.append(temp.clone());
                    $topLevelArgRow.show();
                }
            }
        },

        _setWDescription: function ($topLevelWDescRow, data) {
            /* This function hides/shows corresponding description */
            $topLevelWDescRow.find('input').attr('value', '');
            $topLevelWDescRow.hide();
            if (data) {
                $topLevelWDescRow.find('textarea').html(data.wdesc);
                $topLevelWDescRow.show();
            }
        },

        _setComments: function ($topLevelCommentsRow, data) {
            /* This function hides/shows corresponding comments */
            $topLevelCommentsRow.find('textarea').html('');
            $topLevelCommentsRow.hide();
            if (data) {
                $topLevelCommentsRow.find('textarea').html(data.comments);
                $topLevelCommentsRow.show();
            }
        },

        updateRules: function ($elem) {
            /* This function hides/shows  the corresponding "rules" block for the execute type field */
            $elem = $elem ? $elem : $(this);
            var currentValue = $elem.attr('current-value');
            var newValue = $elem.find(':selected').text().trim();
            $elem.attr('current-value', newValue);
            var $rulesBlock = $elem.closest('.row').next();
            var $rulesBlockContainer = $rulesBlock.find('.container-fluid');

            if (currentValue === "Yes" || currentValue === "No") {
                if (newValue === "If" || newValue === "If Not") {
                    $rulesBlock.find('.col-sm-9').append($rulesBlockContainer.clone().attr('id', '').attr('key', 'Execute.Rule').show());
                    $rulesBlock.show();
                }
            } else {
                if (newValue === "Yes" || newValue === "No") {
                    $rulesBlockContainer.slice(1).remove();
                    $rulesBlock.hide();
                }
            }
        },

        updateRuleElseValue: function ($elem) {
            /* This function hides/shows  the corresponding "goto value" field for the onerror "goto".
            Internally calls the _updateCommonOnError function */
            $elem = $elem ? $elem : $(this);
            debugcases._updateCommonOnError($elem);
        },

        updateRunmode: function ($elem) {
            /* This function hides/shows  the corresponding "runmode value" field for the runmode type field */
            $elem = $elem ? $elem : $(this);
            var value =  $elem.find(':selected').text().trim();
            if (value !== "Standard") {
                $elem.closest('.row').next().show();
            } else {
                $elem.closest('.row').next().find('input').attr('value', '').val('');
                $elem.closest('.row').next().hide();
            }
        },

        updateOnErrorValue: function ($elem) {
            /* This function hides/shows  the corresponding "goto value" field for the onerror "goto".
            Internally calls the _updateCommonOnError function */
            $elem = $elem ? $elem : $(this);
            debugcases._updateCommonOnError($elem);
        }
    },

    validations: {

        checkIfEmpty: function() {
            var $elem = $(this);
            var parentDisplay = $elem.attr('display-parent') === 'true';
            var parentVisible = parentDisplay ? $elem.closest('.row').closest('.row').is(':visible') : false;
            if (parentDisplay === parentVisible) {
                if ($elem.val().trim() === "") {
                    katana.validationAPI.addFlag( $elem, 'Cannot be Empty');
                }
            }
        },

        checkIfEmptyOrNaN: function () {
            var $elem = $(this);
            var parentDisplay = $elem.attr('display-parent') === 'true';
            var parentVisible = $elem.closest('.row').closest('.row').is(':visible');
            if (parentDisplay === parentVisible) {
                if ($elem.val().trim() === "") {
                    katana.validationAPI.addFlag( $elem, 'Cannot be Empty');
                } else if (isNaN($elem.val().trim())) {
                    katana.validationAPI.addFlag( $elem, 'Has to be a valid numerical');
                }
            }
        }

    }

};

