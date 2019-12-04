window.inc = 0;
window.current_context="";
window.$preipf="";
window.nul_flag=0;
var settings = {

    openFileExplorer: {

            logsOrResultsDir: function (relative, $elem) {
                /* This common function gets filepath from the fileexplorer and ataches it to the correct input field*/
                $elem = $elem ? $elem : $(this);
                var $inputElem = $elem.parent().children('input');
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
                        $("#saveButton").removeClass("saved");
                    },
                    false)
            },

            inputDataFile: function () {
                /* This function calls logsOrResultsDir with relative as true so that relative path is created. */
                settings.openFileExplorer.logsOrResultsDir(true, $(this));
            },

        },

    closeSetting: function () {
        if (this.parent().find('.saved').length)
            katana.closeSubApp();
        else
            katana.openDialog('Are you sure you would like to close this page?', 'Confirm', true, katana.closeSubApp);
    },

    encryption: {
        save: function () {
            var $elem = this;
            $elem.addClass('loading');
            katana.templateAPI.post(katana.$activeTab.find('.to-save').attr('post-url'), null,
                katana.$activeTab.find('.to-save').find('input:not([name="csrfmiddlewaretoken"]),textarea').serializeArray(), function(data){
                    $elem.removeClass('loading').addClass('saved');
                }, null);
        }
    },

    profile: {
        init: function () {
            settings.changeDetection.call(this);
            this.find('.profile-image').insertAfter(this.find('.field-block .title'));
            this.find('[key="lastName"], [key="firstName"]').closest('.field').insertAfter(this.find('.profile-image:last'));
        },

        selectProfileImage: function () {
            var $elem = this;
            $elem.parent().find('input').click();
        },

        encodeImage: function () {
            var $elem = this;
            var element = this.get(0);
            var toplevel = $elem.parent();
            var file = element.files[0];
            var preview = toplevel.find('.image');
            var reader = new FileReader();
            preview.addClass('loading');
            reader.onloadend = function () {
                var result = reader.result;
                toplevel.find('input[name="image"]').val(result);
                preview.css('background-image', 'url(' + result + ')');
                preview.removeClass('loading');
            }
            reader.readAsDataURL(file);
        },

        save: function () {
            settings.save.call(this);
            var bgImage = this.closest('.page').find('input[key="bgImage"]').val() ? this.closest('.page').find('input[key="bgImage"]').val() : '';
            var profileImage = this.closest('.page').find('input[key="Base64image"]').val() ? this.closest('.page').find('input[key="Base64image"]').val() : '';
            if (bgImage != "")
                $('#bg-style').html('.page{ background-image: url(' + bgImage + ')}');
            else
                $('#bg-style').html('');

            katana.$view.find('.quick-user .profile-image').css('background-image', 'url(' + profileImage + ')');
        },

        clearImage: function () {
            var topLevel = this.closest('.profile-image');
            topLevel.find('.image').css('background-image', 'none');
            topLevel.find('input').val('');
        }

    },

    mail: {
        init: function () {
            settings.changeDetection.call(this);
            settings.mail.changeFrequency(this);
        },

        changeFrequency: function ($elem) {
            katana.multiSelect($elem, $elem.find('[key="@mail_on"]'));
        }
    },

    jira: {
        boolHandler: function ($elem) {
            var button = $elem.closest('.field-block').find('.relative-tool-bar [key="' + $elem.attr('key') + '"]');
            $elem.val() == 'true' && button.addClass('active');
            $elem.closest('.field').remove();
        },

        password: function () {
            this.attr('type', 'password');
        },

        default: function () {
            settings.jira.boolHandler($(this));
        },

        append_log: function () {
            settings.jira.boolHandler($(this));
        },

        defaultClick: function () {
            this.closest('.page-content').find('[key="@default"]').not(this).removeClass('active');
            katana.toggleActive.call(this);
        },

        issue_type: function () {
            var $elem = this;
            var data = JSON.parse($elem.val());
            data = Array.isArray(data) ? data : [data];
            var fieldContainer = $elem.closest('.field-block > .to-scroll');
            $.each(data, function () {
                settings.jira.buildSubForms(this, $elem);
            });
            $elem.closest('.field').remove();
        },

        buildSubForms: function (objs, $elem) {
            var container = settings.jira.addIssueType($elem);
            $.each(Object.keys(objs), function () {
                container.find('[key=' + this + ']').val(objs[this]);
            });
        },

        addIssueType: function ($elem) {
            $elem = $elem ? $elem : this;
            var $template = $($elem.closest('.to-save').find('#issue_type').html());
            var fieldContainer = $elem.closest('.field-block').find('.to-scroll');
            $elem == this && fieldContainer.find('input:first').trigger('change');
            return $template.clone().appendTo(fieldContainer);

        },

        deleteBlock: function () {
            var fieldBlock = this.closest('.field-block');
            fieldBlock.find('input').trigger('change');
            fieldBlock.remove();
        },

        addBlock: function () {
            var $elem = this;
            var feildBlock = $elem.closest('.field-block');
            feildBlock.find('input:first').trigger('change');
            feildBlock.clone().insertAfter(feildBlock);
        }
    },

    addSystem: function () {
        var page = this.closest('.page-content');
        var template = $(page.find('#block-template').html()).appendTo(page.find('.to-save'));
        template.find('input:first').trigger('change');
    },

    changeDetection: function () {
        var $elem = this;
        $elem.on('change', 'input, select, textarea', function () {
            $elem.closest('.page-content').find('.saved').removeClass('saved');
        });
    },

     validatedir: function(paths) {
        $.ajax({
                headers: {
                    'X-CSRFToken': katana.$activeTab.find('input[name="csrfmiddlewaretoken"]').attr('value')
                },
                type: 'POST',
                url: 'settings/validate_repo/',
                data: {"paths": JSON.stringify(paths)}
            }).done(function(data){
                if(data==1){
                nul_flag=1;
                }
                else{
                nul_flag=0;
                }
            });
             return nul_flag;
   },

    save: function () {
        nul_flag=0;
        var $elem = this;
        // $elem.removeClass('saved').addClass('loading');
        inc =$('#get_count_of_ip input').length;
        inc -= 13;
        var ipfarray=[];
        ipfarray[0]=$ippref=$("#get_count_of_ip").find("input"+"[key=userreposdir]").val();
        if (inc){
        var ipfarray = $("input[category='repo']")
              .map(function(){return $(this).val();}).get();
    }
    function find_duplicate_in_array(ipfarray) {
            var object = {};
            var result = [];
            ipfarray.forEach(function (item) {
              if(!object[item])
                  object[item] = 0;
                object[item] += 1;
            })
            for (var prop in object) {
               if(object[prop] >= 2) {
                   result.push(prop);
               }
            }
            return result;
        }
    fresult = find_duplicate_in_array(ipfarray);
    null_flag = settings.validatedir(ipfarray);
    if(null_flag || fresult.length){
        ipfarray.forEach(function (i) {
            $ippreff=$("#get_count_of_ip").find("input[value='"+i+"']");
            $ippreff.css({"border-color":"#dcdcdc"});
            
          })
        fresult.forEach(function (item) {
            $ippref=$("#get_count_of_ip").find("input[category=repo]").filter("[value='"+item+"']");
            $ippref.css({"border-color":"red"});
          })

          katana.openAlert({
            "alert_type": "danger",
            "heading": "Invalid Repo path(s)",
            "text": "It seems like the entered Repo path may be empty or not valid.",
            "show_cancel_btn": false
        });
    
       }
       else{
        $("#get_count_of_ip").find("input").css({"border-color":"#dcdcdc"});
        katana.templateAPI.post.call(katana.$activeTab.find('.to-save'), null, null, katana.toJSON(), function (data) {
            ipfarray.forEach(function (i) {
                $ippreff=$("#get_count_of_ip").find("input[value='"+i+"']");
                $ippreff.css({"border-color":"#dcdcdc"});
                
              })
            $elem.removeClass('loading').addClass('saved');
        });
    }
    },

    prerequisites: {

        init: function () {
        },

        installDependency: function () {
            var $elem = $(this);
            if ($elem.attr('status') === 'install' || $elem.attr('status') === 'upgrade') {
                $elem.attr('aria-selected', 'true');
                var $parent = $elem.parent();
                $elem.hide();
                $parent.find('br').hide();
                $parent.find('hr').hide();
                $parent.find('.card').show();
            }
        },

        cancelDependencyInstallation: function ($elem) {
            if ($elem === undefined) {
                $elem = $(this);
            }
            var $parent = $elem.closest('.card');
            var $installBtn = $parent.siblings('button[katana-click="settings.prerequisites.installDependency"]');
            $installBtn.attr('aria-selected', 'false');
            $parent.hide();
            $installBtn.siblings('br').show();
            $installBtn.siblings('hr').show();
            $installBtn.show();
        },

        installDependencyAsAdmin: function () {
            var $elem = $(this);
            var $parentDiv = $elem.closest('.card');
            var $installBtn = $parentDiv.siblings('button[katana-click="settings.prerequisites.installDependency"]');
            var data = {
                "name": $installBtn.attr('prerequisite-name'),
                "version": $installBtn.attr('version'),
                "admin": true
            };
            $.when(settings.prerequisites.setInstallBtn($installBtn))
                .then(settings.prerequisites.cancelDependencyInstallation($elem))
                .then(settings.prerequisites.install(data, $installBtn));
        },

        installDependencyAsUser: function () {
            var $elem = $(this);
            var $parentDiv = $elem.closest('.card');
            var $installBtn = $parentDiv.siblings('button[katana-click="settings.prerequisites.installDependency"]');
            var data = {
                "name": $installBtn.attr('prerequisite-name'),
                "version": $installBtn.attr('version'),
                "admin": false
            };
            $.when(settings.prerequisites.setInstallBtn($installBtn))
                .then(settings.prerequisites.cancelDependencyInstallation($elem))
                .then(settings.prerequisites.install(data, $installBtn));
        },

        install: function (data, $installBtn) {
            $.ajax({
                headers: {
                    'X-CSRFToken': katana.$activeTab.find('input[name="csrfmiddlewaretoken"]').attr('value')
                },
                type: 'POST',
                url: 'settings/install_prerequisite/',
                data: data,
            }).done(function(resp_data){
                if(resp_data.status){
                    $installBtn.html('Installed' + '&nbsp;<i class="fa fa-check-circle skyblue" aria-hidden="true"></i>');
                    $installBtn.attr('status', 'installed');
                    $installBtn.attr('aria-selected', 'false');
                    $installBtn.prev().prev().html('Available Version: ' + data.version);
                    katana.openAlert({"alert_type": "success",
                        "heading": "Installation Successful",
                        "text": "Name: " + data.name + "<br>" +
                                "Version: " + data.version + "<br>" +
                                "Exit Status: " + resp_data.return_code + "<br><br>" +
                                "Full Output: <br>" + resp_data.output + "<br><br>" +
                                "Errors/Warnings (if any): <br>" + resp_data.errors,
                        "show_cancel_btn": false
                    })
                } else {
                    $installBtn.html('Install Again' + '&nbsp;<i class="fa fa-exclamation-circle red" aria-hidden="true"></i>');
                    $installBtn.attr('status', 'install');
                    $installBtn.attr('aria-selected', 'false');
                    katana.openAlert({"alert_type": "danger",
                        "heading": "Installation Unsuccessful",
                        "text": "Name: " + data.name + "<br>" +
                                "Version: " + data.version + "<br>" +
                                "Exit Status: " + resp_data.return_code + "<br><br>" +
                                "Errors: <br>" + resp_data.errors + "<br><br>" +
                                "Full Output: <br>" + resp_data.output + "<br>",
                        "show_cancel_btn": false
                    })
                }
            });
        },

        setInstallBtn: function ($installBtn) {
            $installBtn.attr('status', 'installing');
            $installBtn.attr('aria-selected', 'true');
            $installBtn.html('Installing' + '&nbsp;<i class="fa fa-spinner fa-spin green" aria-hidden="true"></i>&nbsp;');
        },
    },
    incrementfnc: function(){
    $("#removebtn").find(".fa-minus-circle").remove();
    inc =$('#get_count_of_ip input').length;
    inc -= 13;
    inc += 1;
    $(".incrementfnc").append("<div katana-click='settings.onselect' class='field'><input category='repo' key="+"userreposdir"+inc+" type='text' {% if v %} value='' {% endif %} placeholder=''><div class='file-explorer-launcher' katana-click='settings.openFileExplorer.logsOrResultsDir'></div>");
    $("#saveButton").removeClass("saved");
   },

   set_context:function(context){
   current_context=context;
   },

   removerepo: function(){
    fieldname=$(this).attr("key");
    inputfd = current_context.parent().remove();
    inputfd.remove();
    $("#saveButton").removeClass("saved");
    $("#removebtn").find(".fa-minus-circle").remove();
   },

  onselect:function(){
      elem=$(this).children();
      field=$(this).children().attr("key");
      settings.set_context(elem);
      $("#removebtn").find(".fa-minus-circle").remove();
      $("<i class='fa fa-minus-circle' key='"+field+"' style='margin-left: 10px;' katana-click='settings.removerepo'></i>").insertAfter(".fa-plus-circle");
      $("#saveButton").removeClass("saved");
},

  deselect: function(){
      $("#removebtn").find(".fa-minus-circle").remove();
 },

};