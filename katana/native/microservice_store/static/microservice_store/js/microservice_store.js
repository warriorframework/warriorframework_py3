var microservice = {
    MATCH_ANY_REGEX: /.*/,
    IP_REGEX: /^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/,
    URL_REGEX: /^\S*$/,
    PORT_REGEX: /^\d*$/,
    POD_NAME_REGEX: /^[^:\s]*$/,
    IMAGE_NAME_REGEX: /^[^:\s]*$/,
    IGNORE_KEY_REGEX: /^--/,

    showSection: function(section){
        s = $(this).attr("section");
        if(typeof section !== "undefined") {
            s = section;
        }
        $(".microservice.section").each(function(){
            if($(this).attr("class").indexOf(s) > 0){
                $(this).show();
            }else{
                $(this).hide();
            }
        });
        $(".microservice.options div").each(function(){
            $(this).removeClass("selected");
        });
        $(".microservice.options div[section='"+s+"']").addClass("selected");
    },

    deploy: function(){
        data = microservice.are_fields_valid();
        if(data == false){
            return;
        }
        microservice.maximize();
        var csrf = katana.$activeTab.find('.csrf-container input').val();
        var url = 'microservice_store/deploy';
        var console_div = $(".microservice-console");
        $.ajax({
            xhr: function(){
                var xhr = new window.XMLHttpRequest();
                //Download progress
                xhr.addEventListener("progress", function(evt){
                    console_div.html(evt.currentTarget.response);
                    var page_content_inner = console_div;
                    var scroll_height = page_content_inner.prop("scrollHeight");
                    page_content_inner.scrollTop(scroll_height);
                }, false);
                return xhr;
            },
            url : url,
            dataType : 'html',
            type : 'GET',
            data : { data: JSON.stringify(data) },
            success : function(data){
                //console.log('success');
            },
            error : function(xhr,errmsg,err) {
                // provide a bit more info about the error to the console
                //console.log(xhr.status + ": " + xhr.responseText);
            }
        });
    },

    load: function(){
        var csrf = katana.$activeTab.find('.csrf-container input').val();
        katana.templateAPI.post('microservice_store/get_dir_path', csrf, '', function( dirPath ){
            katana.fileExplorerAPI.openFileExplorer("Select a settings file to import", dirPath.data, csrf, false, function(str){
                katana.templateAPI.post('microservice_store/load', csrf, str, function(data){
                    katana.$activeTab.find(".microservice.main").html(data);
                }, function(data){
                    katana.openAlert({
                        "alert_type": "danger",
                        "heading": "Failed to Load",
                        "text": str,
                        "show_cancel_btn": false,
                    });
                });
            });
        });
    },

    save: function(){
        var csrf = katana.$activeTab.find('.csrf-container input').val();
        data = microservice.are_fields_valid();
        if(data == false){
            return;
        }
        katana.templateAPI.post('microservice_store/get_dir_path', csrf, '', function( dirPath ){
            katana.openAlert({
                "alert_type": "light",
                "heading": "Filename",
                "text": "",
                "prompt": "true",
                "prompt_default": "settings.dat"
                }, function(inputValue){
                    data.file = {'directory':dirPath.data, 'filename':inputValue};
                    katana.templateAPI.post('microservice_store/save', csrf, JSON.stringify(data), function(response){
                        if (response.status) {
                            katana.openAlert({
                                "alert_type": "success",
                                "heading": "Saved",
                                "text": response.file,
                                "show_cancel_btn": false,
                            });
                        } else {
                            katana.openAlert({
                                "alert_type": "danger",
                                "heading": "Failed to Save",
                                "text": response.file,
                                "show_cancel_btn": false,
                            });
                        }
                    });
                }
            );
        });
    },

    resizable: function(){
        $(".microservice-operations").resizableCustom({
            handleSelector: ".microservice-tools",
            resizeWidth: false
        });
    },

    minimize: function(){
        $(".microservice-console").css({height: "0px"});
        $(".microservice-operations").css({height: "calc(100% - 37px)"});
    },

    maximize: function(){
        $(".microservice-console").css({height: "calc(50% - 37px)"});
        $(".microservice-operations").css({height: "50%"});
    },

    deployment_details: function(){
        if($(this).val() == "docker"){
            $(".microservice.kubernetes_deployment_details").hide();
            $(".microservice.docker_deployment_details").show();
        }else if($(this).val() == "kubernetes"){
            $(".microservice.kubernetes_deployment_details").show();
            $(".microservice.docker_deployment_details").hide();
        }
    },

    get_fields: function(){
        data = {status: true};
        $(".microservice [key]").each(function(){
            s = $(this).closest("[section]").attr("section");
            k = $(this).attr("key");
            v = $.trim($(this).val());
            if(data[s] == null){
                data[s] = {};
            }
            if (!k.match(microservice.IGNORE_KEY_REGEX)) {
                data[s][k] = v;
            }
        });
        return data;
    },

    FIELD_VALIDATION: {
        "registry":{
            "address":{
                "required": true,
                "heading":"Registry Address",
                "if_missing_text": "Registry Address is empty",
                "form": ["URL_REGEX", "IP_REGEX"],
                "if_invalid_form_text": "Registry Address is not a valid URL or IP address",
            },
            "image_name":{
                "required": true,
                "heading": "Image Name",
                "if_missing_text": "Image Name Is empty",
                "form": ["IMAGE_NAME_REGEX"],
                "if_invalid_form_text": "Image Name is not a valid image name",
            },
            "port":{
                "required": false,
                "heading": "Registry Port",
                "form": ["PORT_REGEX"],
                "if_invalid_form_text": "Registry Port is not a valid port number",
            },
        },
        "host":{
            "address":{
                "required": true,
                "heading":"Host Address",
                 "if_missing_text": "Host Address Is empty",
                "form": ["URL_REGEX", "IP_REGEX"],
                "if_invalid_form_text": "Host Address is not a valid URL or IP address",
            },
            "port":{
                "required": true,
                "heading":"Host Port",
                "if_missing_text": "Host Port Is Empty",
                "form": ["PORT_REGEX"],
                "if_invalid_form_text": "Host Port is not a valid port number",
            },
            "username":{
                "required": true,
                "heading":"Host Username",
                "if_missing_text": "Host Username Is Empty",
            },
            "password":{
                "required": true,
                "heading":"Host Password",
                "if_missing_text": "Host Password Is Empty",
            },
            "end_prompt":{
                "required": true,
                "heading":"Host End Prompt",
                "if_missing_text": "Host End Prompt Is Empty",
            },
            "deployment_environment":{
                "required": true,
                "heading":"Host Deployment Environment",
                "if_missing_text": "Host Deployment Environment Is Empty",
            },
            "pod_name":{
                "required": true,
                "optional_if":{"deployment_environment":"docker"},
                "heading":"Pod Name",
                "if_missing_text":"Pod Name Is Empty",
                "form": ["POD_NAME_REGEX"],
                "if_invalid_form_text": "Pod Name is not a valid name",
            }
        }
    },

    are_fields_valid: function(){
        data = microservice.get_fields();
        for (var s in microservice.FIELD_VALIDATION) {
            for (var k in microservice.FIELD_VALIDATION[s]) {
                var required = microservice.FIELD_VALIDATION[s][k].required;
                var optional_if = microservice.FIELD_VALIDATION[s][k].optional_if;
                for (var o in optional_if) {
                    if (data[s][o] == optional_if[o]) {
                        required = false;
                        break;
                    }
                }
                var valid = false;
                var form = microservice.FIELD_VALIDATION[s][k].form;
                if ($.isEmptyObject(form)) {
                    valid = true;
                } else {
                    for (var f in form) {
                        if (data[s][k].match(microservice[form[f]])) {
                            valid = true;
                            break;
                        } else {
                        }
                    }
                }
                if (required && microservice.isEmpty(data[s][k])) {
                    katana.openAlert({"alert_type": "warning",
                        "heading": microservice.FIELD_VALIDATION[s][k].heading,
                        "text": microservice.FIELD_VALIDATION[s][k].if_missing_text,
                        "show_cancel_btn": false
                    }, function(data){
                        microservice.showSection(s);
                    }, function(data){
                        microservice.showSection(s);
                    });
                    data = {status: false};
                    return false;
                }
                if (!microservice.isEmpty(data[s][k]) && !valid) {
                    katana.openAlert({"alert_type": "warning",
                        "heading": microservice.FIELD_VALIDATION[s][k].heading,
                        "text": microservice.FIELD_VALIDATION[s][k].if_invalid_form_text,
                        "show_cancel_btn": false
                    }, function(data){
                        microservice.showSection(s);
                    }, function(data){
                        microservice.showSection(s);
                    });
                    data = {status: false};
                    return false;
                }
            }
        }
        if(data["status"] == false) return false;
        delete data["status"];
        return data;
    },

    isEmpty(v){
        return v.trim() == "";
    },

    put_flags: function(){
        var flags = "";
        $("tr.microservice.flag input").each(function(){
            k = $(this).attr("key")
            v = $(this).val()
            ev = v.split(",")
            for (var i = 0; i < ev.length; i++) {
                if(ev[i].trim() != ""){
                    flags = flags + " " + k + " " + ev[i]
                }
            }
        })
        $(".textarea.flag").val(flags)
    },

    get_flags: function(){
        return $(".textarea.flag").val();
    },

    get_flag: function(flag){
        var flags = $(".textarea.flag").val();
        vv = ""
        while(flags.indexOf(flag) != -1){
            flags = flags.substring(flags.indexOf(flag) + flag.length);
            var v = "";
            for (var i = 0; i < flags.length; i++) {
                v += flags.charAt(i);
                if(flags.charAt(i+1) == "-" && flags.charAt(i+2) == "-") break;
            }
            v = v.trim();
            if(vv == ""){
                vv = v;
            }else{
                vv = vv + "," + v;
            }
        }
        return vv;
    },

    show_options_box: function(){
        var box = $("<div></div>");
        var head = $("<div>Options</div>");
        var close = $("<div class='fa fa-remove'></div>");
        $(close).css({
            "float": "right",
            "right": "25px",
            "cursor": "pointer"
        })
        $(head).css({
            "height": "40px",
            "border-bottom": "1px solid grey",
            "color" : "#696969",
            "padding-left": "15px",
            "padding-right": "15px",
            "padding-top": "10px",
            "padding-bottom": "10px",
            "font-weight": "bold",
            "position": "sticky",
            "top": "0px",
            "background": "white",
            "zIndex": "99"
        })
        $(box).css({
            "zIndex": "99",
            "margin": "100px auto",
            "position": "relative",
            "border-radius": "0px",
            "width": "80%",
            "height": "70%",
            "overflow": "auto",
            "background": "rgba(255, 255, 255, 0.9)",
            "box-shadow": "10px 10px 50px 10px rgba(0, 0, 0, 0.2), -10px -10px 50px 10px rgba(0, 0, 0, 0.19), -10px 10px 50px 10px rgba(0, 0, 0, 0.19), 10px -10px 50px 10px rgba(0, 0, 0, 0.19)"

        })
        $(head).append(close);
        $(box).append(head);
        cl = $(".docker_flag_section").clone();
        cl.show();
        $(box).append("<center>" + cl[0].outerHTML + "</center>");
        $(box).find("tr.microservice.flag input").each(function(){
            v = microservice.get_flag($(this).attr("key"));
            $(this).val(v);
        });
        $(close).on("click", function(){$(box).remove()});
        $(document.body).append(box);
        $("tr.microservice.flag input").keyup(function(){microservice.put_flags()});
    },

    registry_address_select: function() {
        var addr = $(".microservice [section='registry']").find("[key='address']");
        addr.val($(".microservice [key='address_select']").val());
        if ($(this).val()) {
            $(".microservice.registry_address_advanced").hide();
        } else {
            $(".microservice.registry_address_advanced").show();
        }
    },
}