var equinix = {

    measure_func: function () {
        $(".result").val("")
        if ($(".api_res").css("display") == "none") {
            $(".api_res").css("display", "block");
        }
        if ($(".loader").css("display") == "none") {
            $(".loader").show();
        }
        $(".set_btn").attr("disabled", true);
        $(".msr_btn").attr("disabled", true);
        $odi = $(".msr_odi").val()
        $msr_pr_type = $(".msr_pr_type").find(":selected").text()
        $port = $(".msr_port").val()
        $group = $(".msr_grp_name").find(":selected").text()
        $.ajax({
            headers: {
                'X-CSRFToken': katana.$activeTab.find('input[name="csrfmiddlewaretoken"]').attr('value')
            },
            type: 'GET',
            url: 'equinix/measure/',
            dataType: "json",
            async: false,
            data: { "odi": $odi, "pr_type": $msr_pr_type, "msr_port":$port, "msr_group":$group }
        }).done(function (data) {
            $(".loader").css("display", "none");
            $(".result").val(JSON.stringify(data, null, 4));
            $(".set_btn").attr("disabled", false);
            $(".msr_btn").attr("disabled", false);

        })
    },

    set_func: function () {
        $(".result").val("")
        if ($(".api_res").css("display") == "none") {
            $(".api_res").css("display", "block");
        }
        if ($(".loader").css("display") == "none") {
            $(".loader").show();
        }
        $(".set_btn").attr("disabled", true);
        $(".msr_btn").attr("disabled", true);
        $odi = $(".set_odi").val()
        $set_pr_type = $(".set_pr_type").find(":selected").text()
        $port = $(".set_port").val()
        $set_grp = $(".set_grp_name").find(":selected").text()
        $.ajax({
            headers: {
                'X-CSRFToken': katana.$activeTab.find('input[name="csrfmiddlewaretoken"]').attr('value')
            },
            type: 'GET',
            url: 'equinix/set/',
            dataType: "json",
            async: false,
            data: { "odi": $odi, "pr_type": $set_pr_type, "set_port":$port, "set_group":$set_grp }
        }).done(function (data) {
            $(".loader").css("display", "none");
            $(".result").val(JSON.stringify(data, null, 4));
            $(".set_btn").attr("disabled", false);
            $(".msr_btn").attr("disabled", false);

        })
    },
    openaddgroupform: function () {
        $("#space-for-device-edit").html("<p></p>")
        $(".transponder-block").hide()
        $(".ops-block").hide()
        $(".modal-title").text("Add new group")
        $(".show-hide :input").prop("disabled", false)
        $.ajax({
            headers: {
                'X-CSRFToken': katana.$activeTab.find('input[name="csrfmiddlewaretoken"]').attr('value')
            },
            type: 'POST',
            url: 'equinix/get_list_of_transponders/',
            async: false,
            data: {}
        }).done(function (data) {
            data = data.replace(/'/g, '"');
            data = JSON.parse(data)
            transoptions = "<option>None</option>"
            if (data.length) {
                for (grp = 0; grp < data.length; grp++) {
                    transoptions += "<option>" + String(data[grp]) + "</option>"
                }
            }
        })
        $.ajax({
            headers: {
                'X-CSRFToken': katana.$activeTab.find('input[name="csrfmiddlewaretoken"]').attr('value')
            },
            type: 'POST',
            url: 'equinix/get_list_of_ops/',
            async: false,
            data: {}
        }).done(function (data) {
            data = data.replace(/'/g, '"');
            data = JSON.parse(data)
            opsoptions = "<option>None</option>"
            if (data.length) {
                for (grp = 0; grp < data.length; grp++) {
                    opsoptions += "<option>" + String(data[grp]) + "</option>"
                }
            }
        })
        $("#toggle-for-add-edit").html("<p></p>")
        grp = '<div class="input-field"><label>Group name:<span style="color: red; font-size: 24px;">*</span></label><input class="groupname" type="text"></div><br>'
        trans = '<label>Select transponder:</label><select class="selected_trans" style="margin:0;">' + transoptions + '</select><br><br>'
        ops = '<label>Select OPS:</label><select class="selected_ops" style="margin:0;">' + opsoptions + '</select>'
        $("#toggle-for-add-edit").html(grp + trans + ops)
        $(".show-hide :input").val("");
        $(".modal-footer").html("<p></p>")
        btns = '<button type="button" class="btn btn-default" id="add_close" data-dismiss="modal">Close</button><button type="button" action-type="addsave" class="btn btn-default" onclick="equinix.save(this)">Save</button>'
        $(".modal-footer").html(btns)
    },

    openaddeviceform: function () {
        $("#space-for-device-edit").html("<p></p>")
        $(".transponder-block").hide()
        $(".ops-block").hide()
        $(".ops-block :input").prop("disabled", false)
        $(".transponder-block :input").prop("disabled", false)
        $(".modal-title").text("Add new device")
        $(".show-hide :input").prop("disabled", false)
        $("#toggle-for-add-edit").html("<p></p>")
        devices = '<label>Select device type:</label><select class="selected_device" style="margin:0;" onchange="equinix.opendevicesubform()"><option>None</option><option>T600</option><option>OPS</option></select>'
        $("#toggle-for-add-edit").html(devices)
        $(".show-hide :input").val("");
        $(".modal-footer").html("<p></p>")
        btns = '<button type="button" class="btn btn-default" id="add_close" data-dismiss="modal">Close</button><button type="button" action-type="adddevicesave" class="btn btn-default" onclick="equinix.save(this)">Save</button>'
        $(".modal-footer").html(btns)
    },

    opendevicesubform: function () {
        $(".transponder-block :input").val("");
        $(".ops-block :input").val("");
        $("#space-for-device-edit").html("<p></p>")
        if ($(".selected_device").find(":selected").text() == "None") {
            $(".transponder-block").hide()
            $(".ops-block").hide()
        }
        if ($(".selected_device").find(":selected").text() == "T600") {
            $(".transponder-block").show()
            $(".ops-block").hide()
        }
        else if ($(".selected_device").find(":selected").text() == "OPS") {
            $(".transponder-block").hide()
            $(".ops-block").show()
        }
    },

    openeditgroupform: function () {
        $(".transponder-block").hide()
        $(".ops-block").hide()
        $("#space-for-device-edit").html("<p></p>")
        $(".modal-title").text("Edit group")
        $(".show-hide :input").prop("disabled", false)
        label = '<label>Select group name:</label>'
        $.ajax({
            headers: {
                'X-CSRFToken': katana.$activeTab.find('input[name="csrfmiddlewaretoken"]').attr('value')
            },
            type: 'POST',
            url: 'equinix/get_group_list/',
            async: false,
            data: {}
        }).done(function (data) {
            data = data.replace(/'/g, '"');
            data = JSON.parse(data)
            options = "<option>None</option>"
            if (data.length) {
                for (grp = 0; grp < data.length; grp++) {
                    options += "<option>" + String(data[grp]) + "</option>"
                }
            }
            groups_list = '<select class="selected_group" style="margin:0;" mode="edit" onchange="equinix.fetch_group_details(this)">' + options + '</select>'
            $("#toggle-for-add-edit").html("<p></p>")
            $("#toggle-for-add-edit").html(label + groups_list)
        });
        $(".modal-footer").html("<p></p>")
        btns = '<button type="button" class="btn btn-default" id="edit_close" data-dismiss="modal">Close</button><button type="button" action-type="editsave" class="btn btn-default" onclick="equinix.save(this)">Save</button>'
        $(".modal-footer").html(btns)
    },
    openviewgroupform: function () {
        $(".transponder-block").hide()
        $(".ops-block").hide()
        $("#space-for-device-edit").html("<p></p>")
        $(".modal-title").text("View")
        $(".transponder-block :input").val("");
        $(".ops-block :input").val("");
        label = '<label>Select group name:</label>'
        $.ajax({
            headers: {
                'X-CSRFToken': katana.$activeTab.find('input[name="csrfmiddlewaretoken"]').attr('value')
            },
            type: 'POST',
            url: 'equinix/get_group_list/',
            // dataType: "json",
            async: false,
            data: {}
        }).done(function (data) {
            data = data.replace(/'/g, '"');
            data = JSON.parse(data)
            options = "<option>None</option>"
            if (data.length) {
                for (grp = 0; grp < data.length; grp++) {
                    options += "<option>" + String(data[grp]) + "</option>"
                }
            }
            groups_list = '<select class="selected_group" style="margin:0;" mode="view" onchange="equinix.fetch_group_details(this)">' + options + '</select>'
            $("#toggle-for-add-edit").html("<p></p>")
            $("#toggle-for-add-edit").html(label + groups_list)

        });
        $(".modal-footer").html("<p></p>")
        btns = '<button type="button" class="btn btn-default" data-dismiss="modal">Close</button>'
        $(".modal-footer").html(btns)
    },

    save: function (e) {
        save_type = $(e).attr("action-type")
        grpname = $(".groupname").val()
        tsname = $(".selected_trans").find(":selected").text()
        opsname = $(".selected_ops").find(":selected").text()

        if (save_type == "addsave") {
            $.ajax({
                headers: {
                    'X-CSRFToken': katana.$activeTab.find('input[name="csrfmiddlewaretoken"]').attr('value')
                },
                type: 'POST',
                url: 'equinix/add_new_group/',
                // dataType: "json",
                async: false,
                data: { "groupname": grpname, "transpondername": tsname, "opsname": opsname }
            }).done(function (data) {
                if (data == "success") {
                    equinix.success_alert("Success!", "Succesfully added a group.", "success")
                    $("#add_close").trigger("click");
                }
                else if (data == "duplicate") {
                    equinix.success_alert("Error!", "Group name already exists.", "error")
                }
                else {
                    equinix.success_alert("Error!", "Failed to add a group.", "error")
                }
            });
        }
        else if (save_type == "editsave") {
            selgrpname = $(".selected_group").find(":selected").text()
            $.ajax({
                headers: {
                    'X-CSRFToken': katana.$activeTab.find('input[name="csrfmiddlewaretoken"]').attr('value')
                },
                type: 'POST',
                url: 'equinix/edit_group/',
                async: false,
                data: { "selgrpname": selgrpname, "groupname": grpname, "transpondername": tsname, "opsname": opsname }
            }).done(function (data) {
                if (data == "success") {
                    equinix.success_alert("Success!", "Succesfully added a group.", "success")
                    $("#edit_close").trigger("click");
                }
                else if (data == "duplicate") {
                    equinix.success_alert("Error!", "Group name already exists.", "error")
                }
                else {
                    equinix.success_alert("Error!", "Failed to add a group.", "error")
                }
            });
        }
        else if (save_type == "adddevicesave") {
            seldevname = $(".selected_device").find(":selected").text()
            if (seldevname == "T600") {
                transpondername = $(".tsname").val()
                transponderip = $(".tsip").val()
                transponderusername = $(".tsuname").val()
                transponderpassword = $(".tspassword").val()
                $.ajax({
                    headers: {
                        'X-CSRFToken': katana.$activeTab.find('input[name="csrfmiddlewaretoken"]').attr('value')
                    },
                    type: 'POST',
                    url: 'equinix/add_transponder/',
                    async: false,
                    data: { "transpondername": transpondername, "transponderip": transponderip, "transponderusername": transponderusername, "transponderpassword": transponderpassword }
                }).done(function (data) {
                    if (data == "success") {
                        equinix.success_alert("Success!", "Succesfully added a device.", "success")
                        $("#add_close").trigger("click");
                    }
                    else if (data == "duplicate") {
                        equinix.success_alert("Error!", "device name already exists.", "error")
                    }
                    else {
                        equinix.success_alert("Error!", "Failed to add a device.", "error")
                    }
                });
            }
            else if (seldevname == "OPS") {
                opsname = $(".opsname").val()
                opsip = $(".opsip").val()
                opsusername = $(".opsuname").val()
                opspassword = $(".opspassword").val()
                $.ajax({
                    headers: {
                        'X-CSRFToken': katana.$activeTab.find('input[name="csrfmiddlewaretoken"]').attr('value')
                    },
                    type: 'POST',
                    url: 'equinix/add_ops/',
                    async: false,
                    data: { "opsname": opsname, "opsip": opsip, "opsusername": opsusername, "opspassword": opspassword }
                }).done(function (data) {
                    if (data == "success") {
                        equinix.success_alert("Success!", "Succesfully added a device.", "success")
                        $("#add_close").trigger("click");
                    }
                    else if (data == "duplicate") {
                        equinix.success_alert("Error!", "device name already exists.", "error")
                    }
                    else {
                        equinix.success_alert("Error!", "Failed to add a device.", "error")
                    }
                });

            }
        }
        else if (save_type == "editdevicesave") {
            seldevtype = $(".selected_device").find(":selected").text()
            seldevname = $(".selected_device_edit").find(":selected").text()
            if (seldevtype == "T600") {
                transpondername = $(".tsname").val()
                transponderip = $(".tsip").val()
                transponderusername = $(".tsuname").val()
                transponderpassword = $(".tspassword").val()
                $.ajax({
                    headers: {
                        'X-CSRFToken': katana.$activeTab.find('input[name="csrfmiddlewaretoken"]').attr('value')
                    },
                    type: 'POST',
                    url: 'equinix/edit_transponder/',
                    async: false,
                    data: { "seldevname": seldevname, "transpondername": transpondername, "transponderip": transponderip, "transponderusername": transponderusername, "transponderpassword": transponderpassword }
                }).done(function (data) {
                    if (data == "success") {
                        equinix.success_alert("Success!", "Succesfully added a device.", "success")
                        $("#edit_close").trigger("click");
                    }
                    else if (data == "duplicate") {
                        equinix.success_alert("Error!", "device name already exists.", "error")
                    }
                    else {
                        equinix.success_alert("Error!", "Failed to add a device.", "error")
                    }
                });
            }
            else if (seldevtype == "OPS") {
                opsname = $(".opsname").val()
                opsip = $(".opsip").val()
                opsusername = $(".opsuname").val()
                opspassword = $(".opspassword").val()
                $.ajax({
                    headers: {
                        'X-CSRFToken': katana.$activeTab.find('input[name="csrfmiddlewaretoken"]').attr('value')
                    },
                    type: 'POST',
                    url: 'equinix/edit_ops/',
                    async: false,
                    data: { "seldevname": seldevname, "opsname": opsname, "opsip": opsip, "opsusername": opsusername, "opspassword": opspassword }
                }).done(function (data) {
                    if (data == "success") {
                        equinix.success_alert("Success!", "Succesfully added a device.", "success")
                        $("#edit_close").trigger("click");
                    }
                    else if (data == "duplicate") {
                        equinix.success_alert("Error!", "device name already exists.", "error")
                    }
                    else {
                        equinix.success_alert("Error!", "Failed to add a device.", "error")
                    }
                });

            }
        }
    },

    success_alert: function (header, message, message_type) {
        swal.fire(
            header,
            message,
            message_type
        )
    },

    fetch_group_details: function (e) {
        groupname = $(".selected_group").find(":selected").text()
        mode = $(e).attr("mode")
        if (groupname == "None") {
            $(".transponder-block").hide()
            $(".ops-block").hide()
            $("#space-for-device-edit").hide()
        }
        else {
            $("#space-for-device-edit").html("<p></p>")
            $("#space-for-device-edit").show()
            $(".ops-block").hide()
            $(".transponder-block").hide()
            $.ajax({
                headers: {
                    'X-CSRFToken': katana.$activeTab.find('input[name="csrfmiddlewaretoken"]').attr('value')
                },
                type: 'POST',
                url: 'equinix/get_list_of_transponders/',
                async: false,
                data: {}
            }).done(function (data) {
                data = data.replace(/'/g, '"');
                data = JSON.parse(data)
                transoptions = "<option>None</option>"
                if (data.length) {
                    for (grp = 0; grp < data.length; grp++) {
                        transoptions += "<option>" + String(data[grp]) + "</option>"
                    }
                }
            })
            $.ajax({
                headers: {
                    'X-CSRFToken': katana.$activeTab.find('input[name="csrfmiddlewaretoken"]').attr('value')
                },
                type: 'POST',
                url: 'equinix/get_list_of_ops/',
                async: false,
                data: {}
            }).done(function (data) {
                data = data.replace(/'/g, '"');
                data = JSON.parse(data)
                opsoptions = "<option>None</option>"
                if (data.length) {
                    for (grp = 0; grp < data.length; grp++) {
                        opsoptions += "<option>" + String(data[grp]) + "</option>"
                    }
                }
            })

            $("#space-for-device-edit").html("<p></p>")
            grp = '<div class="input-field"><label>Group name:<span style="color: red; font-size: 24px;">*</span></label><input class="groupname" type="text"></div><br>'
            trans = '<label>Select transponder:</label><select class="selected_trans" style="margin:0;">' + transoptions + '</select><br><br>'
            ops = '<label>Select OPS:</label><select class="selected_ops" style="margin:0;">' + opsoptions + '</select>'
            $("#space-for-device-edit").html(grp + trans + ops)

            $.ajax({
                headers: {
                    'X-CSRFToken': katana.$activeTab.find('input[name="csrfmiddlewaretoken"]').attr('value')
                },
                type: 'POST',
                url: 'equinix/fetch_group_details/',
                async: false,
                data: { "groupname": groupname }
            }).done(function (data) {
                opsoptions = "<option>None</option>"
                $(".groupname").val(data["groupname"])
                $(".selected_trans").val(data["transpondername"])
                $(".selected_ops").val(data["opsname"])
            })

            if(mode =="view"){
                $('#space-for-device-edit').find('input, select').attr('disabled',true);

            }
            else{
                $('#space-for-device-edit').find('input, select').attr('disabled',false);  
            }
        }
    },

    openeditdeviceform: function () {
        $(".transponder-block").hide()
        $(".ops-block").hide()
        $(".ops-block :input").prop("disabled", false)
        $(".transponder-block :input").prop("disabled", false)
        $("#space-for-device-edit").html("<p></p>")
        $(".modal-title").text("Edit device")
        $("#toggle-for-add-edit").html("<p></p>")
        devices = '<label>Select device type:</label><select class="selected_device" style="margin:0;" onchange="equinix.fetch_devices()"><option>None</option><option>T600</option><option>OPS</option></select>'
        $("#toggle-for-add-edit").html(devices)
        $(".modal-footer").html("<p></p>")
        btns = '<button type="button" class="btn btn-default" id="edit_close" data-dismiss="modal">Close</button><button type="button" action-type="editdevicesave" class="btn btn-default" onclick="equinix.save(this)">Save</button>'
        $(".modal-footer").html(btns)
    },

    fetch_devices: function () {
        $("#space-for-device-edit").hide()
        $(".transponder-block").hide()
        $(".ops-block").hide()
        device_type = $(".selected_device").find(":selected").text()
        $.ajax({
            headers: {
                'X-CSRFToken': katana.$activeTab.find('input[name="csrfmiddlewaretoken"]').attr('value')
            },
            type: 'POST',
            url: 'equinix/fetch_devices/',
            async: false,
            data: { "device_type": device_type }
        }).done(function (data) {
            data = data.replace(/'/g, '"');
            data = JSON.parse(data)
            options = "<option>None</option>"
            if (data.length) {
                for (grp = 0; grp < data.length; grp++) {
                    options += "<option>" + String(data[grp]) + "</option>"
                }
            }
            $("#space-for-device-edit").show()
            $("#space-for-device-edit").html("<p></p>")
            devices = '<br><label>Select device:</label><select class="selected_device_edit" style="margin:0;" onchange="equinix.get_device_details()" >' + options + '</select>'
            $("#space-for-device-edit").html(devices)
        })
    },

    get_device_details: function () {
        device_type = $(".selected_device").find(":selected").text()
        if (device_type == "T600") {
            $(".transponder-block").show()
            $(".ops-block").hide()

        }
        else if (device_type == "OPS") {
            $(".transponder-block").hide()
            $(".ops-block").show()
        }
        selected_device = $(".selected_device_edit").find(":selected").text()
        if (selected_device == "None") {
            $(".transponder-block").hide()
            $(".ops-block").hide()
        }
        if (selected_device != "None") {
            $.ajax({
                headers: {
                    'X-CSRFToken': katana.$activeTab.find('input[name="csrfmiddlewaretoken"]').attr('value')
                },
                type: 'POST',
                url: 'equinix/get_device_details/',
                async: false,
                data: { "device_type": device_type, "selected_device": selected_device }
            }).done(function (data) {
                if (device_type == "T600") {
                    $(".tsname").val(data["transpondername"])
                    $(".tsip").val(data["transponderip"])
                    $(".tsuname").val(data["transponderusername"])
                    $(".tspassword").val(data["transponderpassword"])
                }
                else if (device_type == "OPS") {
                    $(".opsname").val(data["opsname"])
                    $(".opsip").val(data["opsip"])
                    $(".opsuname").val(data["opsusername"])
                    $(".opspassword").val(data["opspassword"])
                }
            })
        }
    },

    openviewdeviceform: function () {
        $(".transponder-block").hide()
        $(".ops-block").hide()
        $("#space-for-device-edit").html("<p></p>")
        $(".modal-title").text("View device")
        $("#toggle-for-add-edit").html("<p></p>")
        devices = '<label>Select device type:</label><select class="selected_device" style="margin:0;" onchange="equinix.fetch_devices()"><option>None</option><option>T600</option><option>OPS</option></select>'
        $("#toggle-for-add-edit").html(devices)
        $(".ops-block :input").prop("disabled", true)
        $(".transponder-block :input").prop("disabled", true)
        $(".modal-footer").html("<p></p>")
        btns = '<button type="button" class="btn btn-default" id="edit_close" data-dismiss="modal">Close</button>'
        $(".modal-footer").html(btns)
    }
}