var projects = {

    mappings: {
        /* titles from drawers */
        newStep: {
            title: "New Suite" //drawer title for when new step is being edited
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
            title: "Edit Project" //drawer title for when existing step is being edited
        }
    },

    invert: function () {
        var toolbarButtons = katana.$activeTab.find('.tool-bar').find('button');
        for (var i = 0; i < toolbarButtons.length; i++) {
            if ($(toolbarButtons[i]).is(":hidden")) {
                $(toolbarButtons[i]).show();
            } else {
                $(toolbarButtons[i]).hide();
            }
        }
        var divs = katana.$activeTab.find('#body-div').children();
        for (i = 0; i < divs.length; i++) {
            if ($(divs[i]).is(":hidden")) {
                $(divs[i]).show();
            } else {
                $(divs[i]).hide();
            }
        }
    },

    drawer: {

        openCaseFile: function () {
            /* This function opens the datafile in the datafile editor*/
            var $elem = $(this);
            var $inputElem = $elem.parent().prev().children('input');
            var tsPath = katana.$activeTab.find('#main-div').attr("current-file");
            if ($inputElem.val().trim() !== "") {
                var tcPath = katana.utils.getAbsoluteFilepath(tsPath, $inputElem.val().trim(), true);
                $.ajax({
                    headers: {
                        'X-CSRFToken': katana.$activeTab.find('input[name="csrfmiddlewaretoken"]').attr('value')
                    },
                    type: 'POST',
                    url: 'check_if_file_exists/',
                    data: {"path": tcPath}
                }).done(function(data){
                    if (data.exists) {
                        katana.templateAPI.load('/katana/cases/', '/static/cases/js/cases.js, /static/cases/js/generateJson.js,',
                            null, 'Cases', function(){
                                $.ajax({
                                    type: 'GET',
                                    url: 'cases/get_file/',
                                    headers: {'X-CSRFToken': katana.$activeTab.find('input[name="csrfmiddlewaretoken"]').attr('value')},
                                    data:  {"path": tcPath}
                                }).done(function(caseData) {
                                    if(caseData.status){
                                        cases.invert();
                                        katana.$activeTab.find('#main-div').attr("current-file", caseData.filepath);
                                        katana.$activeTab.find('.tool-bar').find('.title').html(caseData.filename);
                                        katana.$activeTab.find('#main-div').html(caseData.html_data);
                                        cases.mappings.newStep.drivers = caseData.drivers;
                                    } else {
                                        katana.openAlert({"alert_type": "danger",
                                            "heading": "Could not open file",
                                            "text": "Errors: " + caseData.message,
                                            "show_cancel_btn": false})
                                    }
                                })
                            }, null)
                    } else {
                        katana.openAlert({
                            "alert_type": "danger",
                            "heading": "Problem Opening " + $inputElem.val(),
                            "text": "It seems like the file may not be available for viewing.",
                            "show_cancel_btn": false
                        });
                    }
                });
            }
        },

        openDatafile: function () {
            /* This function opens the datafile in the datafile editor*/
            var $elem = $(this);
            var $inputElem = $elem.parent().prev().children('input');
            var tsPath = katana.$activeTab.find('#main-div').attr("current-file");
            if ($inputElem.val().trim() !== "") {
                var idfPath = katana.utils.getAbsoluteFilepath(tsPath, $inputElem.val().trim(), true);
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
            }
        },

        openClosedDrawer: function (title) {
            /* This function opens the closed side Drawer*/
            var $drawerClosedDiv = katana.$activeTab.find('#main-div').find('.suites-side-drawer-closed');
            var $drawerOpenDiv = $drawerClosedDiv.siblings('.suites-side-drawer-open');
            $drawerClosedDiv.hide();
            $drawerOpenDiv.show();
            $drawerOpenDiv.find('.suites-drawer-open-header').find('h4').html(title);
        },

        closeOpenedDrawer: function () {
            /* This function closes the opened side Drawer*/
            var $drawerClosedDiv = katana.$activeTab.find('#main-div').find('.suites-side-drawer-closed');
            var $drawerOpenDiv = $drawerClosedDiv.siblings('.suites-side-drawer-open');
            $drawerClosedDiv.show();
            $drawerOpenDiv.hide();
        },

        open: {
            highlightSidebar: function (childIndex) {
                /* This function highlights the icon in the drawer sidebar */
                var $sidebarIcons = $(katana.$activeTab.find('.suites-drawer-open-body').find('.sidebar').children('div'));
                for (var i = 0; i < $sidebarIcons.length; i++) {
                    $($sidebarIcons[i]).removeClass('suites-icon-bg-color').addClass('suites-sidebar-disabled-icon');
                }
                $($sidebarIcons[childIndex]).addClass('suites-icon-bg-color').removeClass('suites-sidebar-disabled-icon');
            },

            switchView: {

                details: function ($container, data) {
                    $container.attr("id", "current_details_editor").show();
                    projects.generateDetailsDisplayHtmlBlock($container, data);
                    katana.$activeTab.find('#details_drawer_template').parent().prepend(projects.proofDetailsContainer($container));
                },

                // requirements: function($container, data, current) {
                //     /* This function generates the reqs html for the drawer and attaches it to the drawer */
                //     $container.attr("id", "current_reqs_editor").show();
                //     if (data) {
                //         $container.attr('current', current);
                //         $container.find('input[key="Requirement"]').attr('value', data).val(data);
                //     }
                //     katana.$activeTab.find('#reqs_drawer_template').parent().prepend($container);
                // },

                steps: function($container, data, stepNum) {
                    /* This function generates the step html for the drawer and attaches it to the drawer */
                    $container.attr("id", "current_steps_editor").show();
                    if (data) {
                        $container = projects.generateStepsHtmlBlock($container, data);
                    }else {
                        $container = projects.addTsToStepsHtmlBlock($container, stepNum);
                    }
                   
                    katana.$activeTab.find('#steps_drawer_template').parent().prepend(projects.proofStepsContainer($container));
                }
            },

            saveContents: function () {
                /* This function calls specific functions internally that save information on the frontend */
                var $elem = $(this);
                var saved = false;
                var $openDrawer = $elem.closest('.suites-side-drawer-open');
                var $switchElem = $openDrawer.find('.suites-drawer-open-body').find('.sidebar').find('.suites-icon-bg-color').children('i');
                if ($switchElem) {
                    var reference = $switchElem.attr('ref');
                    if (reference === "editDetails") {
                        saved = projects.drawer.open._saveContents.details($openDrawer.find('.content').find('#current_details_editor'));
                    } 
                    else if (reference === "newStep") {
                        saved = projects.drawer.open._saveContents.steps($openDrawer.find('.content').find('#current_steps_editor'));
                    }
                    if (saved) {
                        $openDrawer.find('.suites-drawer-open-body').find('.content').find('[id^="current"]').remove();
                        projects.drawer.closeOpenedDrawer();
                    }
                }
            },

            _saveContents: {
                
                details: function ($container) {

                    /* This function collects details data from the drawer and adds it to the displayed details block*/
                    if (katana.validationAPI.init($container)) {
                        var data = projects.generateJson.generateDetails($container);
                        var displayContent = projects.generateDetailsDisplayHtmlBlock(katana.$activeTab.find('#suites-display-template').clone(), data);
                        
                        katana.$activeTab.find('#suites-display-template').replaceWith(displayContent);
                        return true;
                    } else {
                        return false;
                    }
                },

                // requirements: function ($container) {
                //     /* This function collects reqs data from the drawer and adds it to the displayed reqs block*/
                //     if (katana.validationAPI.init($container)) {
                //         var data = projects.generateJson.generateRequirements(katana.$activeTab.find('#suites-requirements-template'));
                //         var temp = projects.generateJson.generateRequirements($container);
                //         var index = $container.attr('current') ? $container.attr('current') : data.Requirements.Requirement.length;
                //         data.Requirements.Requirement.splice(index, 1, temp.Requirements.Requirement[0]);
                //         var displayContent = projects.generateRequirementsHtmlBlock(katana.$activeTab.find('#suites-requirements-template').clone(), data);
                //         katana.$activeTab.find('#suites-requirements-template').replaceWith(displayContent);
                //         return true;
                //     } else {
                //         return false;
                //     }
                // },

                steps: function ($container) {
                    /* This function collects step data from the drawer and adds it to the displayed step block*/
                    if (katana.validationAPI.init($container)) {
                        var data = projects.generateJson.generateStep($container);
                        var displayContent = projects.generateStepsDisplayHtmlBlock(katana.$activeTab.find('#step-row-template').clone().attr('id', ''), data);
                        var stepType = $container.attr('step-type') === "edit";
                        var index = parseInt($container.attr('index'));
                        var $allTrs = katana.$activeTab.find('#suites-steps-template').find('tbody').find('tr');
                        if (stepType && index < $allTrs.length) {
                            $allTrs[index].remove();
                        }
                        if (index === 0) {
                            katana.$activeTab.find('#suites-steps-template').find('tbody').prepend(displayContent);
                            //displayContent.insertAfter($($allTrs[index-1]));
                            projects.redoStepNums();
                        } else {
                            displayContent.insertAfter($($allTrs[index-1]));
                            projects.redoStepNums();
                        }
                        return true;
                    } else {
                        return false;
                    }
                }
            },

            discardContents: function() {
                /* This function deletes contents from the drawer */
                var $elem = $(this);
                var $openDrawer = $elem.closest('.suites-side-drawer-open');
                katana.openAlert({
                    "alert_type": "warning",
                    "heading": "All changes will be discarded",
                    "text": "This action will discard all changes, are you sure you want to continue?"
                    }, function () {
                        $openDrawer.find('.suites-drawer-open-body').find('.content').find('[id^="current"]').remove();
                        projects.drawer.closeOpenedDrawer();
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
                projects.drawer.openFileExplorer.logsOrResultsDir(true, $(this));
            }
        }
    },

    header: {
        toggleContents: function () {
            /* This function toggles the content when up/down font-awesomes are clicked */
            var $elem = $(this);
            if ($elem.attr('collapsed') === 'false') {
                $elem.attr('collapsed', 'true');
                $elem.removeClass('fa-chevron-circle-up');
                $elem.addClass('fa-chevron-circle-down');
                $elem.closest('.suites-header').next().hide()
            } else {
                $elem.attr('collapsed', 'false');
                $elem.removeClass('fa-chevron-circle-down');
                $elem.addClass('fa-chevron-circle-up');
                $elem.closest('.suites-header').next().show()
            }
        },

        editDetails: function () {
            /* This function gets data from displayed details block and
            creates the details block in the side drawer*/
            var $elem = $(this);
            var data = projects.generateJson.generateDetails($elem.closest('#main-div').find('#detail-block'));
            projects.drawer.openClosedDrawer(projects.mappings.editDetails.title);
            projects.drawer.open.highlightSidebar(0);
            projects.drawer.open.switchView.details($elem.closest('#main-div').find('#details_drawer_template').clone(), data);
        },

        // newReq: function() {
        //     /* This function creates a new requirements block in the side drawer*/
        //     var $elem = $(this);
        //     projects.drawer.openClosedDrawer(projects.mappings.newReq.title);
        //     projects.drawer.open.highlightSidebar(1);
        //     projects.drawer.open.switchView.requirements($elem.closest('#main-div').find('#reqs_drawer_template').clone());
        // },

        newStep: function() {
            /* This function creates a new case-step block in the side drawer*/
            var $elem = $(this);

            projects.drawer.openClosedDrawer(projects.mappings.newStep.title);
            projects.drawer.open.highlightSidebar(2);
            var $container = $elem.closest('#main-div').find('#steps_drawer_template').clone().attr('step-type', 'edit').attr('index', projects.getLastStepNum());
            projects.drawer.open.switchView.steps($container, false, projects.getLastStepNum() + 1);
        }

    },

    landing: {
        init: function () {
            /* This function get the list of suite files, displays them, and
            attaches click event on each suite file */
            $.ajax({
                type: 'GET',
                url: 'projects/get_list_of_suites/'
            }).done(function (data) {
                katana.jsTreeAPI.createJstree(katana.$activeTab.find('#tree-div'), data.data);
                katana.$activeTab.find('#tree-div').on("select_node.jstree", function (e, data) {
                    if (data["node"]["icon"] === "jstree-file") {
                        $.ajax({
                            headers: {
                                'X-CSRFToken': katana.$activeTab.find('.csrf-container').html()
                            },
                            type: 'GET',
                            url: 'projects/get_file/',
                            data: {"path": data["node"]["li_attr"]["data-path"]}
                        }).done(function (data) {
                            if(data.status){
                                projects.invert();
                                katana.$activeTab.find('#main-div').attr("current-file", data.filepath);
                                katana.$activeTab.find('.tool-bar').find('.title').html(data.filename);
                                katana.$activeTab.find('#main-div').html(data.html_data);
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

        openNewFile: function () {
            $.ajax({
                headers: {
                    'X-CSRFToken': katana.$activeTab.find('.csrf-container').html()
                },
                type: 'GET',
                url: 'projects/get_file/',
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
                    projects.invert();
                    katana.$activeTab.find('#main-div').attr("current-file", data.filepath);
                    katana.$activeTab.find('.tool-bar').find('.title').html(data.filename);
                    katana.$activeTab.find('#main-div').html(data.html_data);
                    projects.mappings.newStep.drivers = data.drivers;
                } else {
                    katana.openAlert({"alert_type": "danger",
                        "heading": "Could not open file",
                        "text": "Errors: " + data.message,
                        "show_cancel_btn": false})
                }
            });
        }
    },

    suiteViewer: {
        close: function () {
            /* This function closes the suite */
            katana.$activeTab.find('#main-div').html("");
            katana.$activeTab.find('.tool-bar').find('.title').html("");
            projects.invert();
        },

        save: function () {
            /* This function collects data from each displayed block and saves the suite */
            var final_json = {"Project": {}};
            var filepath = katana.$activeTab.find('#main-div').attr("current-file");
            var filename = katana.$activeTab.find('.tool-bar').find('.title').html();
            $.extend(true, final_json.Project, projects.generateJson.generateDetails(katana.$activeTab.find('#detail-block')));
            // $.extend(true, final_json.Project, projects.generateJson.generateRequirements(katana.$activeTab.find('#req-block')));
            $.extend(true, final_json.Project, projects.generateJson.generateStep(katana.$activeTab.find('#step-block')));

            var callBack_on_accept = function(inputValue) {
                $.ajax({
                    headers: {
                        'X-CSRFToken': katana.$activeTab.find('input[name="csrfmiddlewaretoken"]').attr('value')
                    },
                    type: 'POST',
                    url: 'projects/save_file/',
                    data: {"data": JSON.stringify(final_json), "directory": filepath, "filename": inputValue, "extension": ".xml"}
                }).done(function(data){
                    if (data.status) {

                        katana.openAlert({
                            "alert_type": "success",
                            "heading": "File Saved",
                            "text": inputValue + " has been saved successfully",
                            "show_cancel_btn": false
                        });
                        projects.suiteViewer.close();
                        window.setTimeout(function(){window.location.reload()}, 1000);
                    } else {
                        katana.openAlert({
                            "alert_type": "danger",
                            "heading": "File Not Saved",
                            "text": "Please fill all the medatory details: " + inputValue,
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

    generateJson: {
        generateDetails: function ($container) {
            /* This function creates details json out of an HTML block */
            var finalJson = {Details: {}};
            var $allKeys = $container.find('[key]');
            var value = false;
            for (var i = 0; i < $allKeys.length; i++) {
                value = $($allKeys[i]).val() ? $($allKeys[i]).val().trim() : $($allKeys[i]).html().trim();
                $.extend(true, finalJson.Details, projects.generateJson._updateJson($($allKeys[i]).attr("key").trim(), value));
            }
            return finalJson;
        },

        // generateRequirements: function ($container) {
        //     /* This function creates requirements json out of an HTML block */
        //     var finalJson = {Requirements: { Requirement: []}};
        //     var $allKeys = $container.find('[key]');
        //     var value = false;
        //     for (var i=0; i <$allKeys.length; i++) {
        //         value = $($allKeys[i]).val() ? $($allKeys[i]).val().trim() : $($allKeys[i]).html().trim();
        //         finalJson.Requirements.Requirement.push(value);
        //     }
        //     return finalJson;
        // },

        generateStep: function ($container) {
            /* This function creates case-steps json out of an HTML block */
            var finalJson = {Testsuites: { Testsuite: []}};
            var $allTcs = $container.attr('key') === 'Testsuite'? [$container] : $container.find('[key="Testsuite"]');
            var $allKeys = false;
            var partialData = false;
  

            for (var i=0; i <$allTcs.length; i++) {
                $allKeys = $($allTcs[i]).find('[key]').not('[key*="Execute.Rule"]');
                partialData = {};
                for (var j=0; j<$allKeys.length; j++) {
                    var key = $($allKeys[j]).attr("key").trim();

                    var value = $($allKeys[j]).val() ? $($allKeys[j]).val().trim() : $($allKeys[j]).html().trim();
                    $.extend(true, partialData, projects.generateJson._updateJson(key, value));
                }
                $.extend(true, partialData, projects.generateJson.generateExecuteRules($($allTcs[i]).find('[key="Execute.Rule"]')));
                finalJson.Testsuites.Testsuite.push(partialData);
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
                    $.extend(true, partialData, projects.generateJson._updateJson(key, value));
                }
                finalJson.Execute.Rule.push(Object.assign({}, partialData.Execute.Rule));
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
                data[key] = projects.generateJson._updateJson(remaining_key, value)
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
            return projects.getValueFromJson(data[key], remaining_key)
        }

        return data[key]
    },


    generateDetailsDisplayHtmlBlock: function ($container, data) {
        /* This function generates the details block out of an HTML block and json data */
        var $allKeys = $container.find('[key]');

        for (var i = 0; i < $allKeys.length; i++) {
            if ($($allKeys[i]).prop('type') === 'text') {
                $($allKeys[i]).attr('value', projects.getValueFromJson(data.Details, $($allKeys[i]).attr('key')));
            } else if ($($allKeys[i]).prop('type') === 'select-one') {
                $($allKeys[i]).attr('value', projects.getValueFromJson(data.Details, $($allKeys[i]).attr('key')));
                var value = projects.getValueFromJson(data.Details, $($allKeys[i]).attr('key'));
                var $allOptions = $($allKeys[i]).children();
                for (var j = 0; j < $allOptions.length; j++) {
                    if ($($allOptions[j]).text() === value) {
                        $($allOptions[j]).prop('selected', true);
                        break;
                    }
                }
            } else {
                $($allKeys[i]).html(projects.getValueFromJson(data.Details, $($allKeys[i]).attr('key')));
            }
        }
        return $container
    },

    // generateRequirementsHtmlBlock: function ($container, data) {
    //     /* This function generates the requirements block out of an HTML block and json data */
    //     var $constantTemplate = $container.find('#req-table-template').clone().attr('id', "").show();
    //     var start = 0;
    //     var mid = Math.floor((data.Requirements.Requirement.length + 1) /2);
    //     var end = data.Requirements.Requirement.length;
    //     var $tableTemplateLeft = projects._generateReqTable(data, start, mid, $constantTemplate, $constantTemplate.clone());
    //     var $tableTemplateRight = projects._generateReqTable(data, mid, end, $constantTemplate, $constantTemplate.clone());
    //     $($container.find('.suites-internal-space')[0]).html($tableTemplateLeft);
    //     $($container.find('.suites-internal-space')[1]).html($tableTemplateRight);
    //     return $container;
    // },

    // _generateReqTable: function (data, start, end, $constantTemplate, $container) {
    //     /* This function is called by generateRequirementsHtmlBlock which creates the req block */
    //     var $trTemplate = false;
    //     $container.find('tr').remove();
    //     for (var i=start; i<end; i++) {
    //         $trTemplate = $constantTemplate.find('tr').clone();
    //         $trTemplate.attr('req-number', i+1);
    //         $trTemplate.find('th').html(i+1);
    //         $($trTemplate.find('td').children('div')[0]).attr('key', 'Requirement').html(data.Requirements.Requirement[i]);
    //         $container.find('tbody').append($trTemplate);
    //     }
    //     return $container;
    // },

    generateStepsHtmlBlock: function ($container, data) {
        /* This function generates the case-steps block (side-drawer) out of an HTML block and json data */
        var $allKeys = $container.find('[key]').not('[key*="Execute"]').not('[key*="Arguments"]');
        for (var i=0; i<$allKeys.length; i++) {
            if ($($allKeys[i]).prop('type') === 'text') {
                $($allKeys[i]).attr('value', projects.getValueFromJson(data.Testsuites.Testsuite[0], $($allKeys[i]).attr('key')));
            } else if ($($allKeys[i]).prop('type') === 'select-one') {
                $($allKeys[i]).attr('value', projects.getValueFromJson(data.Testsuites.Testsuite[0], $($allKeys[i]).attr('key')));
                var value = projects.getValueFromJson(data.Testsuites.Testsuite[0], $($allKeys[i]).attr('key'));
                var $allOptions = $($allKeys[i]).children();
                for (var j=0; j<$allOptions.length; j++) {
                    if ($($allOptions[j]).text() === value) {
                        $($allOptions[j]).prop('selected', true);
                        break;
                    }
                }
            } else {
                $($allKeys[i]).html(projects.getValueFromJson(data.Testsuites.Testsuite[0], $($allKeys[i]).attr('key')));
            }
        }
        $container = projects._addExecuteBlock($container, data);
        return $container
    },

    _addExecuteBlock: function ($container, data) {
        /* This function generates the execute block (side-drawer) out of an HTML block and json data.
        This function should not be called independently */
        var $execTypeBlock = $container.find('[key="Execute.@ExecType"]');
        $execTypeBlock.attr('current-value', projects.getValueFromJson(data.Testsuites.Testsuite[0], $execTypeBlock.attr('key')));
        projects._selectOption($execTypeBlock, $execTypeBlock.attr('current-value'));

        var $ruleBlock = $execTypeBlock.closest('.row').next().find('#rule-template');
        for (var k=0; k<data.Testsuites.Testsuite[0].Execute.Rule.length; k++) {
            var $currentRuleBlock = $ruleBlock.clone().attr('id', '').attr('key', 'Execute.Rule').show();
            var $allKeys = $currentRuleBlock.find('[key]');
            for (var i=0; i<$allKeys.length; i++) {
                var value = projects.getValueFromJson({"Execute" : {"Rule": data.Testsuites.Testsuite[0].Execute.Rule[k]}}, $($allKeys[i]).attr('key'));
                $($allKeys[i]).attr('value', value);
                if ($($allKeys[i]).prop('type') === 'select-one') {
                    projects._selectOption($($allKeys[i]), value);
                }
            }
            projects.stepEditor.updateRuleElseValue($currentRuleBlock.find('[key="Execute.Rule.@Else"]'));
            $ruleBlock.parent().append($currentRuleBlock);
            $execTypeBlock.closest('.row').next().show();
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


    generateStepsDisplayHtmlBlock: function ($container, data) {
        
        /* This function generates the steps block (main page) out of an HTML block and json data */
        $container = $($container.html());
        var $allKeys = $container.find('[key]').not('[key*="Execute.Rule"]');
        for (var i=0; i<$allKeys.length; i++) {
            if ($($allKeys[i]).prop('type') === 'text') {
                $($allKeys[i]).attr('value', projects.getValueFromJson(data.Testsuites.Testsuite[0], $($allKeys[i]).attr('key')));
            } else if ($($allKeys[i]).prop('type') === 'select-one') {
                $($allKeys[i]).attr('value', projects.getValueFromJson(data.Testsuites.Testsuite[0], $($allKeys[i]).attr('key')));
                var value = projects.getValueFromJson(data.Testsuites.Testsuite[0], $($allKeys[i]).attr('key'));
                var $allOptions = $($allKeys[i]).children();
                for (var j=0; j<$allOptions.length; j++) {
                    if ($($allOptions[j]).text() === value) {
                        $($allOptions[j]).prop('selected', true);
                        break;
                    }
                }
            } else {
                $($allKeys[i]).html(projects.getValueFromJson(data.Testsuites.Testsuite[0], $($allKeys[i]).attr('key')));
            }
        }
        // $container = projects.evaluateDisplayRunmode($container);
        $container = projects.evaluateDisplayOnError($container);
        $container = projects.evaluateDisplayExecute($container, data);
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

    evaluateDisplayExecute: function ($container, data) {
        
        /* This function hides/shows the execute block (main page).
        This function should not be called independently */
        var $templateExecRule = $container.find('[key="Execute.Rule"]').clone();
        $container.find('[key="Execute.Rule"]').next().remove();
        $container.find('[key="Execute.Rule"]').remove();
        for (var i=0; i<data.Testsuites.Testsuite[0].Execute.Rule.length; i++) {
            var $currentTemplate = $templateExecRule.clone();
            var $allKeys = $currentTemplate.find('[key]');
            for (var j=0; j<$allKeys.length; j++) {
                $($allKeys[j]).html(projects.getValueFromJson({"Execute": {"Rule": data.Testsuites.Testsuite[0].Execute.Rule[i]}}, $($allKeys[j]).attr('key')));
            }
            $container.find('[key="Execute.@ExecType"]').parent().append($currentTemplate);
            $container.find('[key="Execute.@ExecType"]').parent().append('<br>');
        }
        return $container
    },

    proofDetailsContainer: function ($container) {
        /* This function verifies if the all the correct fields are shown/hidden in the details (side-drawer) block */
        projects.detailsEditor.updateDefaultOnError($container.find('[key="default_onError.@action"]'));
        projects.detailsEditor.updateExecutionType($container.find('[key="type.@exectype"]'));
        return $container;
    },

    proofStepsContainer: function ($container) {
        /* This function verifies if the all the correct fields are shown/hidden in the case-step (side-drawer) block */
        projects.stepEditor.updateRules($container.find('[key="Execute.@ExecType"]'));
        projects.stepEditor.updateRunmode($container.find('[key="runmode.@type"]'));
        projects.stepEditor.updateOnErrorValue($container.find('[key="onError.@action"]'));
        return $container
    },

    getLastStepNum: function () {
        /* This function gets the last case-step number */
        return katana.$activeTab.find('#main-div').find('#suites-steps-template').find('tbody').children('tr').length;
    },

    redoStepNums: function(){

        /* This function re-numbers all the case-steps in the display table */
        var $tbodyElem = katana.$activeTab.find('#step-block').find('table').find('tbody');
        var $allTrElems = $tbodyElem.children('tr');
        for (var i=0; i<$allTrElems.length; i++){
            $($($allTrElems[i]).children('td')[0]).html(i+1);
        }
    },

    addTsToStepsHtmlBlock: function ($container, stepNum) {
        /* This function adds the step number to the case-step (side-drawer) block */

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
            projects._updateCommonOnError($elem);
        },

        updateExecutionType: function ($elem) {
            /* This function changes the key attribute of type.@Number_Attempts/type/@max_Attempts in the
            details_display_template and the step_template whenever the type.@exectype in details_template is updated */
            $elem = $elem ? $elem : $(this);
            var value = $elem.find(':selected').text().trim();
            var $nextElem = $elem.closest('.row').next();
            var $displayElem = $elem.closest('#main-div').find('#suites-display-template').find('[key="type.@exectype"]').parent().next().children('td');
            var $templateElem = $elem.closest('.content').find('#details_drawer_template').find('[key="type.@exectype"]').closest('.row').next().find('input');
            var keyValue = 'type.@Number_Attempts';
            if (value === "Run Until Fail" || value === "Run Until Pass") {
                keyValue = 'type.@Max_Attempts';
                $nextElem.show();
            } else if (value === "Run Multiple Times") {
                $nextElem.show();
            } else {
                $nextElem.find('input').attr('value', '').val('');
                $nextElem.hide();
            }
            $nextElem.find('input').attr('key', keyValue);
            $displayElem.attr('key', keyValue);
            $templateElem.attr('key', keyValue);
        }
    },

    // reqSection: {
    //     deleteReq: function () {
    //         /* This function deletes a req */
    //         var $elem = $(this);
    //         var $tdParent = $elem.closest('td');
    //         var reqNumber = $tdParent.siblings('th').html();
    //         var $toBeDeleted = $elem.closest('tr');
    //         var $topLevel = $elem.closest('#suites-requirements-template');
    //         katana.openAlert({
    //             "alert_type": "danger",
    //             "heading": "Delete Requirement " + reqNumber + "?",
    //             "text": "Are you sure you want to delete the requirement? This cannot be undone."
    //         }, function(){
    //             $toBeDeleted.remove();
    //             // var data = projects.generateJson.generateRequirements($topLevel);
    //             // var displayContent = projects.generateRequirementsHtmlBlock($topLevel.clone(), data);
    //             $topLevel.replaceWith(displayContent);
    //         });
    //     },

    //     editReq: function () {
    //         /* This function opens a req in the req editor*/
    //         var $elem = $(this);
    //         var data = $($elem.closest('.suites-req').children('div')[0]).html().trim();
    //         projects.drawer.openClosedDrawer(projects.mappings.editReq.title);
    //         projects.drawer.open.highlightSidebar(1);
    //         projects.drawer.open.switchView.requirements($elem.closest('#main-div').find('#reqs_drawer_template').clone(), data, $elem.closest('tr').attr('req-number')-1);
    //     }
    // },

    stepSection: {
        selectStep: function () {
            /* This function selects a case-step */
            var $elem = $(this);
            var $allTrElems = $elem.parent().children('tr');
            if ($elem.attr('marked') === 'true') {
                $elem.attr('marked', 'false');
                $elem.css('background-color', '');
            } else {
                var multiselect = katana.$activeTab.find('.suites-step-toolbar').find('.fa-th-list').attr('multiselect');
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
                /* This function de/activates the multiselect functionality for a case-step */
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
                /* This function deletes a case-step */
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
                            projects.redoStepNums();
                        })
                }
            },

            insertStep: function () {
                /* This function opens a new case-step in the step editor and inserts it into a specific spot when saved */
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
                console.log($($allTrElems[0]).index())

                projects.drawer.openClosedDrawer(projects.mappings.newStep.title);
                projects.drawer.open.highlightSidebar(2);
                var $container = $elem.closest('#main-div').find('#steps_drawer_template').clone().attr("step-type", "insert").attr("index", insertAtIndex);
                projects.drawer.open.switchView.steps($container, false, insertAtIndex+1);
            },

            editStep: function () {
                /* This function opens the case-step in the step editor and replaces the existing case-step when saved */
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
                    var data = projects.generateJson.generateStep($($allTrElems[0]));
                    projects.drawer.openClosedDrawer(projects.mappings.editStep.title);
                    projects.drawer.open.highlightSidebar(2);
                    var $container = $elem.closest('#main-div').find('#steps_drawer_template').clone().attr('step-type', 'edit').attr('index', $($allTrElems[0]).index());
                    projects.drawer.open.switchView.steps($container, data);
                }
            }
        }
    },

    stepEditor: {
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
            projects._updateCommonOnError($elem);
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
            projects._updateCommonOnError($elem);
        }
    },

    validations: {

        checkIfEmpty: function() {
            /* This function checks if fields is empty and throws a validation error */
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
            /* This function checks if fields is empty and/or not a number and throws a validation error */
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
