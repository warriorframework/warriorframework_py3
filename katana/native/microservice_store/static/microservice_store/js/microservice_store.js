var microservice = {

    IP_REGEX: "/^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/",
    URL_REGEX: "/(?:(?:https?|http):\/\/)?(?:(?!(?:10|127)(?:\.\d{1,3}){3})(?!(?:169\.254|192\.168)(?:\.\d{1,3}){2})(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|(?:(?:[a-z\u00a1-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)(?:\.(?:[a-z\u00a1-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)*(?:\.(?:[a-z\u00a1-\uffff]{2,})))(?::\d{2,5})?(?:\/\S*)?/",

    showSection: function(){
        s = $(this).attr("section")
        $(".microservice.section").each(function(){
            if($(this).attr("class").indexOf(s) > 0){
                $(this).show()
            }else{
                $(this).hide()
            }
        })
        $(".microservice.options div").each(function(){
            $(this).removeClass("selected")
        })
        $(".microservice.options div[section='"+s+"']").addClass("selected")
    },

    deploy: function(){
        data = microservice.are_fields_valid()
        if(data == false){
            return
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
                console.log(xhr.status + ": " + xhr.responseText);
            }
        });
    },

    resizable: function(){
        $(".microservice-operations").resizableCustom({
            handleSelector: ".microservice-tools",
            resizeWidth: false
        });
    },

    minimize: function(){
        $(".microservice-console").css({height: "0px"})
        $(".microservice-operations").css({height: "calc(100% - 37px)"})
    },

    maximize: function(){
        $(".microservice-console").css({height: "calc(50% - 37px)"})
        $(".microservice-operations").css({height: "50%"})
    },

    deployment_details: function(){
        if($(this).val() == "docker"){
            $(".microservice.kubernetes_deployment_details").hide();
        }else if($(this).val() == "kubernetes"){
            $(".microservice.kubernetes_deployment_details").show();
        }
    },

    are_fields_valid: function(){
        data = {status: true}
        $(".microservice [key]").each(function(){
            s = $(this).closest("[section]").attr("section");
            k = $(this).attr("key");
            v = $(this).val();
            if(data[s] == null){
                data[s] = {}
            }
            if(s == "registry"){
                if(k == "address"){
                    if(microservice.isEmpty(v)){
                        katana.openAlert({"alert_type": "warning",
                            "heading": "Docker Registry Address",
                            "text": "Docker Registry Address Is Empty",
                            "show_cancel_btn": false
                        })
                        data = {status: false}
                        return false
                    }
                    data[s][k] = v;
                }
                if(k == "image"){
                    if(microservice.isEmpty(v)){
                        katana.openAlert({"alert_type": "warning",
                            "heading": "Docker Image",
                            "text": "Docker Image Is Empty",
                            "show_cancel_btn": false
                        })
                        data = {status: false}
                        return false
                    }
                    data[s][k] = v;
                }
                if(k == "key"){
                    if(microservice.isEmpty(v)){
                        katana.openAlert({"alert_type": "warning",
                            "heading": "Docker Registry Key",
                            "text": "Registry Key Is Empty",
                            "show_cancel_btn": false
                        })
                        data = {status: false}
                        return false
                    }
                    data[s][k] = v;
                }
            }
            if(s == "host"){
                if(k == "address"){
                    if(microservice.isEmpty(v)){
                        katana.openAlert({"alert_type": "warning",
                            "heading": "Host Address",
                            "text": "Host Address Is Empty",
                            "show_cancel_btn": false
                        })
                        data = {status: false}
                        return false
                    }
                    data[s][k] = v;
                }
                if(k == "port"){
                    if(microservice.isEmpty(v)){
                        katana.openAlert({"alert_type": "warning",
                            "heading": "Host Port",
                            "text": "Host Port Is Empty",
                            "show_cancel_btn": false
                        })
                        data = {status: false}
                        return false
                    }
                    data[s][k] = v;
                }
                if(k == "username"){
                    if(microservice.isEmpty(v)){
                        katana.openAlert({"alert_type": "warning",
                            "heading": "Host Username",
                            "text": "Host Username Is Empty",
                            "show_cancel_btn": false
                        })
                        data = {status: false}
                        return false
                    }
                    data[s][k] = v;
                }
                if(k == "password"){
                    if(microservice.isEmpty(v)){
                        katana.openAlert({"alert_type": "warning",
                            "heading": "Host Password",
                            "text": "Host Password Is Empty",
                            "show_cancel_btn": false
                        })
                        data = {status: false}
                        return false
                    }
                    data[s][k] = v;
                }
                if(k == "end_prompt"){
                    if(microservice.isEmpty(v)){
                        katana.openAlert({"alert_type": "warning",
                            "heading": "End Prompt",
                            "text": "End Prompt Is Empty",
                            "show_cancel_btn": false
                        })
                        data = {status: false}
                        return false
                    }
                    data[s][k] = v;
                }
                if(k == "deployment_environment"){
                    if(microservice.isEmpty(v)){
                        katana.openAlert({"alert_type": "warning",
                            "heading": "Deployment Environment",
                            "text": "Deployment Environment Is Empty",
                            "show_cancel_btn": false
                        })
                        data = {status: false}
                        return false
                    }
                    data[s][k] = v;
                }
                if(k == "bind_host_interface"){
                    data[s][k] = v;
                }
                if(k == "bind_host_port"){
                    data[s][k] = v;
                }
                if(k == "pod_name"){
                    data[s][k] = v;
                }
                if(k == "replicas"){
                    data[s][k] = v;
                }
            }

        });
        if(data["status"] == false) return false
        delete data["status"]
        return data
    },

    isEmpty(v){
        return v.trim() == "";
    }

}