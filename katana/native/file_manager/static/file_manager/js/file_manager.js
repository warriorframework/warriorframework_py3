var file_manager = {

    landing: {
        init: function() {
            $.ajax({
                type: 'GET',
                url: 'file_manager/list_files/'
            }).done(function(data){
                  katana.jsTreeAPI.createJstree(katana.$activeTab.find('#tree-div'), data.data, true);
            })
        },

       refresh: function() {
            $.ajax({
                type: 'GET',
                url: 'file_manager/list_files/'
            }).done(function(data){
                  katana.$activeTab.find("#tree-div").jstree("destroy")
                  katana.jsTreeAPI.createJstree(katana.$activeTab.find('#tree-div'), data.data, true);
                  katana.$activeTab.find("#tree-div").jstree("refresh");
            })
       },

       rename: function () {
            var node_selected = katana.$activeTab.find("#tree-div").jstree('get_selected', true);
            var temp;
            var paths_selected = [];
            var files_name = [];
            for (temp = 0; temp < node_selected.length; temp++) {
                    paths_selected.push(node_selected[temp]["li_attr"]["data-path"])
                    files_name.push(node_selected[temp]["text"])
            }
            if (files_name.length > 1) {
                    katana.openAlert({'heading': 'Rename Error',
                            'text': "Can rename only one file at a time"});
            }
            else if (files_name.length == 1) {
                katana.openAlert({'heading': 'Rename',
                            'text': "'" + files_name[0] + "'" + ' to',
                            'prompt': 'true',
                            'accept_btn_text': 'Rename'}, function(input) {
                    $.ajax({
                        type: 'GET',
                        url: 'file_manager/rename_files/',
                        data: {"path" : paths_selected[0],
                            "file_name" : files_name[0],
                             "new_name" : input
                             }
                    }).done(function(data){
                          katana.$activeTab.find("#tree-div").jstree("destroy")
                          katana.jsTreeAPI.createJstree(katana.$activeTab.find('#tree-div'), data.data, true);
                          katana.$activeTab.find("#tree-div").jstree("refresh");
                          katana.openAlert({'heading': 'Rename Result',
                                'text': data.result});
                    })
                });
            }
       },

       delete_file: function() {
            var node_selected = katana.$activeTab.find("#tree-div").jstree('get_selected', true);
            var temp;
            var path_selected = [];
            for (temp = 0; temp < node_selected.length; temp++) {
                path_selected.push(node_selected[temp]["li_attr"]["data-path"])
            }
            $.ajax({
                type: 'GET',
                url: 'file_manager/delete_files/',
                data: {"path" : path_selected }
            }).done(function(data){
                    katana.$activeTab.find("#tree-div").jstree("destroy")
                    katana.jsTreeAPI.createJstree(katana.$activeTab.find('#tree-div'), data.data, true);
                    katana.$activeTab.find("#tree-div").jstree("refresh");
            })
       },

       transfer: function() {
            katana.$activeTab.find("#input-div").show()
            $.ajax({
                        type: 'GET',
                        url: 'file_manager/cache_list/',

                    }).done(function(data){
                        var $elem = katana.$activeTab.find('#user_profile');
                        var temp;
                        if (data.cache_list !== 'error'){
                            $elem.html('<option value=None>None</option>');
                            for(temp = 0; temp < data.cache_list.length; temp++ ) {
                                $elem.append('<option value=' + data.cache_list[temp] + '>' + data.cache_list[temp] + '</option>');
                            }
                        } else {
                            console.log("No cached user profile available currently")
                            $elem.html('<option value=None>None</option>');
                        }
                    })

       }
    },

    transfer_files: {

       close: function() {
            katana.$activeTab.find("#input-div").hide();
       },

       help: function() {
        help_info = "FTP:<p></p>Please create a user profile along with the directory permissions in the FTP Server." +
                    "<p></p>The Destination Directory must be from the Root Directory set up in the FTP Server" +
                    "<p></p>Some OS (Windows) are 'Case Insensitive': If the directory or " +
                    "file already exists in the destination, then FTP of a directory or file with same name, " +
                    "irrespective of the case, to that location might not be possible." +
                    "<p></p>Avoid sending broken tree files: Do not select a parent folder and just " +
                    "it's grand children. The grand children's parent must also be selected" +
                    "<p></p>SCP:" +
                    "<p></p>Please have an SSH server installed and running in your machine as SCP uses underlying " +
                    "SSH connection<p></p>Partial Folder Selection: Can not send a folder with partially selected" +
                    " files. The whole folder gets transferred<p></p><p></p>Files with same name will get overwritten" +
                    " the destination machine"
        katana.openAlert({'heading': 'Info',
                       'text': help_info});
       },


       FTP_to_backend: function(paths_selected, all_paths_selected, files_name, username, pwd, host, port, destdir) {
                $.ajax({
                        type: 'GET',
                        url: 'file_manager/ftp_files/',
                        data: {"path" : paths_selected,
                            "all_path": all_paths_selected,
                            "file_name" : files_name,
                            "username" : username,
                            "password" : pwd,
                            "host" : host,
                            "port" : port,
                            "destdir" : destdir
                        }
                    }).done(function(data){
                    console.log(data)
                    var result = JSON.stringify(data)
                    if (result.includes('530 Login or password incorrect')){
                        katana.openAlert({'heading': 'File Transfer Result',
                                'text': "Login or password incorrect!"});
                   }
                   else if (result.includes('426 Connection closed')){
                        katana.openAlert({'heading': 'File Transfer Result',
                                'text': "Connection Closed. Transfer Aborted!"});
                   }
                   else if (result.includes('Connection refused')){
                        katana.openAlert({'heading': 'File Transfer Result',
                                'text': "Connection Refused! FTP Server might not be up on the Destination"});
                   }
                   else if (result.includes("Could Not Change to Destination Directory Successfully")) {
                        katana.openAlert({'heading': 'File Transfer Result',
                            'text': "Failed to change to Destination Directory. Such a directory might not exist"});
                   }
                   else if (result.includes("broken tree file")) {
                        katana.openAlert({'heading': 'File Transfer Result',
                            'text': "Failed to transfer the Broken Tree Files"});
                            if (result.includes('Success')){
                                katana.openAlert({'heading': 'File Transfer Result',
                                'text': "Transferred other files Successfully!"});
                            }
                    }
                   else if (result.includes('Such a Folder already exists')) {
                        katana.openAlert({'heading': 'File Transfer Result',
                            'text': "Failed to create the directory in the target as a directory with the same name exists"});

                            if (result.includes('Success')){
                                katana.openAlert({'heading': 'File Transfer Result',
                                'text': "Transferred other files Successfully!"});
                                }
                   }
                   else if (result.includes('Could not transfer the file')) {
                        katana.openAlert({'heading': 'File Transfer Result',
                            'text': "Failed to transfer some files"});
                   }
                   else if (result.includes('Success')){
                        katana.openAlert({'heading': 'File Transfer Result',
                                'text': "Success!"});
                   }
                })

       },

        SCP_to_backend: function(paths_selected, all_paths_selected, files_name, username, pwd, host, port, destdir) {
                $.ajax({
                        type: 'GET',
                        url: 'file_manager/scp_files/',
                        data: {"path" : paths_selected,
//                            "all_path": all_paths_selected,
                            "file_name" : files_name,
                            "username" : username,
                            "password" : pwd,
                            "host" : host,
                            "port" : port,
                            "destdir" : destdir
                        }
                    }).done(function(data){
                    console.log(data)
                    var result = data.result
                    var result_error;
                    if (result.includes('Authentication failed')){
                        katana.openAlert({'heading': 'File Transfer Result',
                                'text': "Login or password incorrect!"});
                   }
                   else if (result.includes('Error in Changing Destination')){
                        katana.openAlert({'heading': 'File Transfer Result',
                                'text': "Could Not Create Destination Directory!"});
                   }
                   else if (result.includes('Transfer Error')){
                        for (temp = 0; temp < result.length; temp++) {
                            if (result[temp].includes('Transfer Error')) {
                                 result_error = result_error + '\n' +result[temp];
                            }
                        }
                        katana.openAlert({'heading': 'File Transfer Result',
                                'text': result_error});
                   }
                   else if (result.includes('Connection refused')){
                        katana.openAlert({'heading': 'File Transfer Result',
                                'text': "Connection Refused! SSH might not be up and running on the Destination"});
                   }
                   else
                        katana.openAlert({'heading': 'File Transfer Result',
                                'text': 'Success!'});
                })

       },

       send: function() {
            var $elem = $(this);
            var $parent = $elem.closest('#input-div');
            if (katana.validationAPI.init($parent)) {
                var host = katana.$activeTab.find("#host").val()
                console.log(host)
                var port = katana.$activeTab.find("#port").val()
                console.log(port)
                var username = katana.$activeTab.find("#username").val()
                console.log(username)
                var pwd = katana.$activeTab.find("#password:password").val()
                console.log(pwd)
                var destdir = katana.$activeTab.find("#destdir").val()
                console.log(destdir)
                var transfer_method = katana.$activeTab.find("#dropdown").val()
                console.log(transfer_method)
                var node_selected = katana.$activeTab.find("#tree-div").jstree('get_top_selected', true);
                var all_node_selected = katana.$activeTab.find("#tree-div").jstree('get_selected', true);
                var temp;
                var paths_selected = [];
                var all_paths_selected = [];
                var files_name = [];
                for (temp = 0; temp < node_selected.length; temp++) {
                    paths_selected.push(node_selected[temp]["li_attr"]["data-path"])
                    files_name.push(node_selected[temp]["text"])
                }
                for (temp = 0; temp < all_node_selected.length; temp++) {
                    all_paths_selected.push(all_node_selected[temp]["li_attr"]["data-path"])
                }

                if (transfer_method === 'FTP'){
                    file_manager.transfer_files.FTP_to_backend(paths_selected, all_paths_selected, files_name, username, pwd, host, port, destdir)
                }
                if (transfer_method === 'SCP'){
                        file_manager.transfer_files.SCP_to_backend(paths_selected, all_paths_selected, files_name, username, pwd, host, port, destdir)
                    }
            }
       },

       input_show: function() {
            var user_profile = katana.$activeTab.find("#user_profile").val()
            if (user_profile === "None") {
                katana.$activeTab.find("#username").val("")
                katana.$activeTab.find("#host").val("")
                katana.$activeTab.find("#port").val("")
                katana.$activeTab.find("#dropdown").val("")
                katana.$activeTab.find("#destdir").val("")
            } else {
            try {
                $.ajax({
                        type: 'GET',
                        url: 'file_manager/read_cache/',
                        data: {"cache_name" : user_profile}

                    }).done(function(data){
                    console.log(data.result)
                        var username = data.result[0];
                        var host = data.result[1];
                        var port = data.result[2];
                        var transfer_method = data.result[3];
                        try {
                        var destdir = data.result[4];
                        } catch (err) {}
                        katana.$activeTab.find("#username").val(username)
                        katana.$activeTab.find("#host").val(host)
                        katana.$activeTab.find("#port").val(Number(port))
                        katana.$activeTab.find("#dropdown").val(transfer_method)
                        try {
                        katana.$activeTab.find("#destdir").val(destdir)
                        } catch (err) {
                            katana.$activeTab.find("#destdir").val("")
                        }
                    })

            } catch (err) {

            }
            }
       },

       save: function() {
                var host = katana.$activeTab.find("#host").val()
                var port = katana.$activeTab.find("#port").val()
                var username = katana.$activeTab.find("#username").val()
                var destdir = katana.$activeTab.find("#destdir").val()
                var transfer_method = katana.$activeTab.find("#dropdown").val()

               katana.openAlert({'heading': 'Save',
                            'text': 'The Input data filled out will be cached. Once saved, you can use the same input values through the User Profile Dropdown. <p></p>Enter Input Filename: ',
                            'prompt': 'true',
                            'accept_btn_text': 'Save'}, function(input) {
                    $.ajax({
                        type: 'GET',
                        url: 'file_manager/save/',
                        data: {"username" : username,
                             "host" : host,
                             "port" : port,
                             "destdir" : destdir,
                             "transfer_protocol" : transfer_method,
                             "file_name" : input
                             }
                    }).done(function(data){
                        if (!data.result.includes('error')) {
                            katana.openAlert({'heading': 'User Profile Result',
                                'text': 'Success. Please Click on the Refresh Button'});
                            var $elem = katana.$activeTab.find('#user_profile');
                            var temp;
                            $elem.html('<option value=None>None</option>');
                            for(temp = 0; temp < data.result.length; temp++ ) {
                                $elem.append('<option value=' + data.result[temp] + '>' + data.result[temp] + '</option>');
                            }

                        }

                    })
                });
       }

    },

    validations: {

        validateName: function() {
            if($(this).val().trim() === ""){
                katana.validationAPI.addFlag($(this), 'Name cannot be empty');
            } else if(!(/^[a-zA-Z0-9]+$/).test($(this).val())) {
                katana.validationAPI.addFlag( $(this), 'A name cannot contain special characters or spaces');
            }
        },

        validateIP: function() {
            if($(this).val().trim() === ""){
                katana.validationAPI.addFlag($(this), 'IP cannot be empty');
            } else if(!(/^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/.test($(this).val()))){
                katana.validationAPI.addFlag($(this), 'IP is invalid');
            }
        },

        validatePort: function() {
            if($(this).val().trim() === ""){
                katana.validationAPI.addFlag($(this), 'Port cannot be empty');
            } else if(!(/^[0-9]+$/.test($(this).val()))){
                katana.validationAPI.addFlag($(this), 'Port can contain only numerals');
            }
        },

        validateIfEmpty: function() {
            if($(this).val().trim() === ""){
                katana.validationAPI.addFlag($(this), 'Cannot be empty');
            }
        }
    }

}