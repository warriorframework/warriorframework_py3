

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
        $group1 = $(".msr_grp_name1").find(":selected").text()
        $group2 = $(".msr_grp_name2").find(":selected").text()
        $.ajax({
            headers: {
                'X-CSRFToken': katana.$activeTab.find('input[name="csrfmiddlewaretoken"]').attr('value')
            },
            type: 'GET',
            url: 'equinix/measure/',
            dataType: "json",
            async: false,
            data: { "msr_group1": $group1, "msr_group2": $group2 }
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
        $set_grp1 = $(".set_grp_name1").find(":selected").text()
        $set_grp2 = $(".set_grp_name2").find(":selected").text()
        $.ajax({
            headers: {
                'X-CSRFToken': katana.$activeTab.find('input[name="csrfmiddlewaretoken"]').attr('value')
            },
            type: 'GET',
            url: 'equinix/set/',
            dataType: "json",
            async: false,
            data: { "set_group1": $set_grp1, "set_group2": $set_grp2 }
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
        $(".equinix-group-toolbar").hide()
        $(".equinix-device-toolbar").hide()
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
            transoptions = ""
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
            opsoptions = ""
            if (data.length) {
                for (grp = 0; grp < data.length; grp++) {
                    opsoptions += "<option>" + String(data[grp]) + "</option>"
                }
            }
        })
        $("#toggle-for-add-edit").html("<p></p>")
        grp = '<div class="input-field"><label>Group name:<span style="color: red; font-size: 24px;">*</span></label><input class="groupname" type="text"></div><br>\
        <div class="input-field"><label>otsi-interface name:<span style="color: red; font-size: 24px;">*</span></label><input type="text" class="interface"></input></div><br>'
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
        $(".equinix-group-toolbar").hide()
        $(".equinix-device-toolbar").hide()
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
        $(".equinix-group-toolbar").hide()
        $(".equinix-device-toolbar").hide()
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
        $(".equinix-device-toolbar").hide()
        $("#space-for-device-edit").html("<p></p>")
        $(".modal-title").text("View group")
        $(".transponder-block :input").val("");
        $(".ops-block :input").val("");

        $.ajax({
            headers: {
                'X-CSRFToken': katana.$activeTab.find('input[name="csrfmiddlewaretoken"]').attr('value')
            },
            type: 'POST',
            url: 'equinix/fetch_all_groups/',
            async: false,
            data: {}
        }).done(function (data) {
            let tbody = ""
            for (i = 0; i < data.length; i++) {
                tbody += '<tr class="tb-items"><td class="desc" field="groupname">' + data[i][0] + '</td><td class="desc" field="interface">' + data[i][1] + '</td><td class="desc" field="trans">' + data[i][2] + '</td><td class="desc" field="ops">' + data[i][3] + '</td></tr>'
            }
            table = '<table class="table table-bordered"><thead><tr><th>Group name</th><th>otsi-interface name</th><th>Transponder</th><th>OPS</th></tr></thead>' + tbody + '</table>'
            $("#toggle-for-add-edit").html(table)
        })
        $(".equinix-group-toolbar").show()
        $(".tb-items").click(function () {
            if ($(this).css('background-color') == "rgb(255, 255, 0)") {
                $(this).css('background-color', '#ffffff');
                $(this).removeAttr("selected")
            }
            else {
                $(this).css('background-color', 'yellow');
                $(this).attr("selected", "true")
            }
        })

        $(".modal-footer").html("<p></p>")
        btns = '<button type="button" class="btn btn-default" data-dismiss="modal">Close</button>'
        $(".modal-footer").html(btns)
    },

    save: function (e) {
        save_type = $(e).attr("action-type")
        grpname = $(".groupname").val()
        interfacename = $(".interface").val()
        tsname = $(".selected_trans").find(":selected").text()
        opsname = $(".selected_ops").find(":selected").text()
        console.log(tsname, opsname)

        if (save_type == "addsave") {
            $.ajax({
                headers: {
                    'X-CSRFToken': katana.$activeTab.find('input[name="csrfmiddlewaretoken"]').attr('value')
                },
                type: 'POST',
                url: 'equinix/add_new_group/',
                // dataType: "json",
                async: false,
                data: { "groupname": grpname, "interfacename": interfacename, "transpondername": tsname, "opsname": opsname }
            }).done(function (data) {
                if (data == "success") {
                    equinix.alert("Success!", "Succesfully added a group.", "success")
                    $("#add_close").trigger("click");
                }
                else if (data == "duplicate") {
                    equinix.alert("Error!", "Group name already exists.", "error")
                }
                else {
                    equinix.alert("Error!", "Failed to add a group.", "error")
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
                data: { "selgrpname": selgrpname, "groupname": grpname, "interfacename": interfacename, "transpondername": tsname, "opsname": opsname }
            }).done(function (data) {
                if (data == "success") {
                    equinix.alert("Success!", "Succesfully added a group.", "success")
                    $("#edit_close").trigger("click");
                }
                else if (data == "duplicate") {
                    equinix.alert("Error!", "Group name already exists.", "error")
                }
                else {
                    equinix.alert("Error!", "Failed to add a group.", "error")
                }
            });
        }
        else if (save_type == "adddevicesave") {
            seldevname = $(".selected_device").find(":selected").text()
            if (seldevname == "T600") {
                transpondername = $(".tsname").val()
                transponderip = $(".tsip").val()
                transponderport = $(".tsport").val()
                transponderusername = $(".tsuname").val()
                transponderpassword = $(".tspassword").val()
                $.ajax({
                    headers: {
                        'X-CSRFToken': katana.$activeTab.find('input[name="csrfmiddlewaretoken"]').attr('value')
                    },
                    type: 'POST',
                    url: 'equinix/add_transponder/',
                    async: false,
                    data: { "transpondername": transpondername, "transponderip": transponderip, "transponderport": transponderport, "transponderusername": transponderusername, "transponderpassword": transponderpassword }
                }).done(function (data) {
                    if (data == "success") {
                        equinix.alert("Success!", "Succesfully added a device.", "success")
                        $("#add_close").trigger("click");
                    }
                    else if (data == "duplicate") {
                        equinix.alert("Error!", "device name already exists.", "error")
                    }
                    else {
                        equinix.alert("Error!", "Failed to add a device.", "error")
                    }
                });
            }
            else if (seldevname == "OPS") {
                opsname = $(".opsname").val()
                opsip = $(".opsip").val()
                opsport = $(".opsport").val()
                opsusername = $(".opsuname").val()
                opspassword = $(".opspassword").val()
                $.ajax({
                    headers: {
                        'X-CSRFToken': katana.$activeTab.find('input[name="csrfmiddlewaretoken"]').attr('value')
                    },
                    type: 'POST',
                    url: 'equinix/add_ops/',
                    async: false,
                    data: { "opsname": opsname, "opsip": opsip, "opsport": opsport, "opsusername": opsusername, "opspassword": opspassword }
                }).done(function (data) {
                    if (data == "success") {
                        equinix.alert("Success!", "Succesfully added a device.", "success")
                        $("#add_close").trigger("click");
                    }
                    else if (data == "duplicate") {
                        equinix.alert("Error!", "device name already exists.", "error")
                    }
                    else {
                        equinix.alert("Error!", "Failed to add a device.", "error")
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
                transponderport = $(".tsport").val()
                transponderusername = $(".tsuname").val()
                transponderpassword = $(".tspassword").val()
                $.ajax({
                    headers: {
                        'X-CSRFToken': katana.$activeTab.find('input[name="csrfmiddlewaretoken"]').attr('value')
                    },
                    type: 'POST',
                    url: 'equinix/edit_transponder/',
                    async: false,
                    data: { "seldevname": seldevname, "transpondername": transpondername, "transponderip": transponderip, "transponderport": transponderport, "transponderusername": transponderusername, "transponderpassword": transponderpassword }
                }).done(function (data) {
                    if (data == "success") {
                        equinix.alert("Success!", "Succesfully added a device.", "success")
                        $("#edit_close").trigger("click");
                    }
                    else if (data == "duplicate") {
                        equinix.alert("Error!", "device name already exists.", "error")
                    }
                    else {
                        equinix.alert("Error!", "Failed to add a device.", "error")
                    }
                });
            }
            else if (seldevtype == "OPS") {
                opsname = $(".opsname").val()
                opsip = $(".opsip").val()
                opsport = $(".opsport").val()
                opsusername = $(".opsuname").val()
                opspassword = $(".opspassword").val()
                $.ajax({
                    headers: {
                        'X-CSRFToken': katana.$activeTab.find('input[name="csrfmiddlewaretoken"]').attr('value')
                    },
                    type: 'POST',
                    url: 'equinix/edit_ops/',
                    async: false,
                    data: { "seldevname": seldevname, "opsname": opsname, "opsip": opsip, "opsport": opsport, "opsusername": opsusername, "opspassword": opspassword }
                }).done(function (data) {
                    if (data == "success") {
                        equinix.alert("Success!", "Succesfully added a device.", "success")
                        $("#edit_close").trigger("click");
                    }
                    else if (data == "duplicate") {
                        equinix.alert("Error!", "device name already exists.", "error")
                    }
                    else {
                        equinix.alert("Error!", "Failed to add a device.", "error")
                    }
                });

            }
        }
    },

    alert: function (header, message, message_type) {
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
                transoptions = ""
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
                opsoptions = ""
                if (data.length) {
                    for (grp = 0; grp < data.length; grp++) {
                        opsoptions += "<option>" + String(data[grp]) + "</option>"
                    }
                }
            })

            $("#space-for-device-edit").html("<p></p>")
            grp = '<div class="input-field"><label>Group name:<span style="color: red; font-size: 24px;">*</span></label><input class="groupname" type="text"></div><br>\
            <div class="input-field"><label>otsi-interface name:<span style="color: red; font-size: 24px;">*</span></label><input type="text" class="interface"></input></div><br>'
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
                $(".interface").val(data["interfacename"])
                $(".selected_trans").val(data["transpondername"])
                $(".selected_ops").val(data["opsname"])
            })

            if (mode == "view") {
                $('#space-for-device-edit').find('input, select').attr('disabled', true);

            }
            else {
                $('#space-for-device-edit').find('input, select').attr('disabled', false);
            }
        }
    },

    openeditdeviceform: function () {
        $(".transponder-block").hide()
        $(".ops-block").hide()
        $(".equinix-group-toolbar").hide()
        $(".equinix-device-toolbar").hide()
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
                    $(".tsport").val(data["transponderport"])
                    $(".tsuname").val(data["transponderusername"])
                    $(".tspassword").val(data["transponderpassword"])
                }
                else if (device_type == "OPS") {
                    $(".opsname").val(data["opsname"])
                    $(".opsip").val(data["opsip"])
                    $(".opsport").val(data["opsport"])
                    $(".opsuname").val(data["opsusername"])
                    $(".opspassword").val(data["opspassword"])
                }
            })
        }
    },

    openviewdeviceform: function () {
        $(".transponder-block").hide()
        $(".ops-block").hide()
        $(".equinix-group-toolbar").hide()
        $(".equinix-device-toolbar").hide()
        $("#space-for-device-edit").html("<p></p>")
        $(".modal-title").text("View device")
        $("#toggle-for-add-edit").html("<p></p>")
        devices = '<label>Select device type:</label><select class="selected_device" style="margin:0;" onchange="equinix.fetch_devices_for_table()"><option>None</option><option>T600</option><option>OPS</option></select>'
        $("#toggle-for-add-edit").html(devices)
        $(".ops-block :input").prop("disabled", true)
        $(".transponder-block :input").prop("disabled", true)
        $(".modal-footer").html("<p></p>")
        btns = '<button type="button" class="btn btn-default" id="edit_close" data-dismiss="modal">Close</button>'
        $(".modal-footer").html(btns)
    },

    editgroupintable: function () {
        elen = $("[selected=selected]").length
        if (elen > 1) {
            equinix.alert("Multiple selects!", "Can not edit multiple groups at a time.", "error")
        }
        else if (elen < 1) {
            equinix.alert("No group selected!", "Please select a group to edit.", "error")
        }
        else if (elen == 1) {
            console.log("editing groups...")
            $(".edit-area-template").show()
            btns = '<div style="display: inline; float: right; padding: 5px;"><button class="btn btn-default" onclick="equinix.closesidepanel()">Close</button>&nbsp;<button class="btn btn-default" onclick="equinix.saveedittable()">Save</button></div><br><br><br><br><br>'
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
                transoptions = ""
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
                opsoptions = ""
                if (data.length) {
                    for (grp = 0; grp < data.length; grp++) {
                        opsoptions += "<option>" + String(data[grp]) + "</option>"
                    }
                }
            })

            $(".edit-area-template").html("<p></p>")
            grp = '<div class="input-field"><label>Group name:<span style="color: red; font-size: 24px;">*</span></label><input class="groupnamet" type="text"></div><br>\
            <div class="input-field"><label>otsi-interface name:<span style="color: red; font-size: 24px;">*</span></label><input type="text" class="interfacet"></input></div><br>'
            trans = '<label style="width:185px">Select transponder:</label><select class="selected_transt" style="margin:0;">' + transoptions + '</select><br><br>'
            ops = '<label style="width:185px">Select OPS:</label><select class="selected_opst" style="margin:0;">' + opsoptions + '</select>'
            $(".edit-area-template").html(btns + grp + trans + ops)
            groupname = $("[selected=selected]").find("[field=groupname]").text()
            interfacename = $("[selected=selected]").find("[field=interface]").text()
            trans = $("[selected=selected]").find("[field=trans]").text()
            ops = $("[selected=selected]").find("[field=ops]").text()
            $(".groupnamet").val(groupname)
            $(".groupnamet").attr("curgrpname", groupname)
            $(".interfacet").val(interfacename)
            $(".selected_transt").val(trans)
            $(".selected_opst").val(ops)


        }

    },

    deletegroupintable: function () {
        dlen = $("[selected=selected]").length
        let sel_groups = []
        if (dlen >= 1) {
            sel_groups = $("[selected=selected]").find("[field=groupname]")
                .map(function () { return $(this).text(); }).get();
            console.log("deleting groups...", sel_groups)

            $.ajax({
                headers: {
                    'X-CSRFToken': katana.$activeTab.find('input[name="csrfmiddlewaretoken"]').attr('value')
                },
                type: 'POST',
                url: 'equinix/delete_group/',
                async: false,
                data: { "groups": String(sel_groups) }
            }).done(function (data) {
                if (data == "success") {
                    equinix.alert("Success!", "Group(s) deleted succesfully.", "success")
                    equinix.openviewgroupform()
                }
                else if (data == "fail") {
                    equinix.alert("Error!", "Unable to delete the group(s).", "error")
                }
            })

        }
        else if (dlen < 1) {
            equinix.alert("No group selected!", "Please select atleast one group to delete.", "error")
        }
    },

    closesidepanel: function () {
        $(".edit-area-template").hide()
        $('#toggle-for-add-edit').find('select').attr('disabled', false);
    },

    saveedittable: function () {
        selgrpname = $(".groupnamet").attr("curgrpname")
        grpname = $(".groupnamet").val()
        interfacename = $(".interfacet").val()
        tsname = $(".selected_transt").find(":selected").text()
        opsname = $(".selected_opst").find(":selected").text()
        console.log(selgrpname)
        $.ajax({
            headers: {
                'X-CSRFToken': katana.$activeTab.find('input[name="csrfmiddlewaretoken"]').attr('value')
            },
            type: 'POST',
            url: 'equinix/edit_group/',
            async: false,
            data: { "selgrpname": selgrpname, "groupname": grpname, "interfacename": interfacename, "transpondername": tsname, "opsname": opsname }
        }).done(function (data) {
            if (data == "success") {
                equinix.alert("Success!", "Succesfully edited a group.", "success")
                equinix.closesidepanel()
                equinix.openviewgroupform()
            }
            else if (data == "duplicate") {
                equinix.alert("Error!", "Group name already exists.", "error")
            }
            else {
                equinix.alert("Error!", "Failed to edit a group.", "error")
            }
        });
    },

    fetch_devices_for_table: function () {
        $("#space-for-device-edit").hide()
        $(".transponder-block").hide()
        $(".ops-block").hide()
        $(".equinix-device-toolbar").hide()
        $(".equinix-group-toolbar").hide()
        device_type = $(".selected_device").find(":selected").text()
        $.ajax({
            headers: {
                'X-CSRFToken': katana.$activeTab.find('input[name="csrfmiddlewaretoken"]').attr('value')
            },
            type: 'POST',
            url: 'equinix/fetch_devices_details_for_table/',
            async: false,
            data: { "device_type": device_type }
        }).done(function (data) {
            let tbody = ""
            for (i = 0; i < data.length; i++) {
                tbody += '<tr class="tb-items"><td class="desc" field="devicename">' + data[i][0] + '</td><td class="desc" field="deviceport">' + data[i][1] + '</td><td class="desc" field="deviceip">' + data[i][2] + '</td><td class="desc" field="deviceusername">' + data[i][3] + '</td><td class="desc" field="devicepassword">' + data[i][4] + '</td></tr>'
            }
            
            if (device_type == "T600") {
                table = '<br><table class="table table-bordered"><thead><tr><th>Transponder name</th><th>Transponder port</th><th>Transponder ip</th><th>Transponder username</th><th>Transponder password</th></tr></thead>' + tbody + '</table>'
                $(".equinix-device-toolbar").show()
            }
            else if (device_type == "OPS") {
                table = '<br><table class="table table-bordered"><thead><tr><th>OPS name</th><th>OPS port</th><th>OPS ip</th><th>OPS username</th><th>OPS password</th></tr></thead>' + tbody + '</table>'
                $(".equinix-device-toolbar").show()
            }
            $("#space-for-device-edit").show()
            $("#space-for-device-edit").html("<p></p>")
            $("#space-for-device-edit").html(table)
            $(".tb-items").click(function () {
                if ($(this).css('background-color') == "rgb(255, 255, 0)") {
                    $(this).css('background-color', '#ffffff');
                    $(this).removeAttr("selected")
                }
                else {
                    $(this).css('background-color', 'yellow');
                    $(this).attr("selected", "true")
                }
            })

        })
    },

    editdeviceintable: function () {
        elen = $("[selected=selected]").length
        if (elen > 1) {
            equinix.alert("Multiple selects!", "Can not edit multiple devices at a time.", "error")
        }
        else if (elen < 1) {
            equinix.alert("No device selected!", "Please select a device to edit.", "error")
        }
        else if (elen == 1) {
            console.log("editing devices...")
            $('#toggle-for-add-edit').find('select').attr('disabled', true);
            device_type = $(".selected_device").find(":selected").text()
            $(".edit-area-template").show()
            btns = '<div style="display: inline; float: right; padding: 5px;"><button class="btn btn-default" onclick="equinix.closesidepanel()">\
            Close</button>&nbsp;<button class="btn btn-default" onclick="equinix.savedeviceintable()">Save</button></div><br><br><br><br><br>'
            if (device_type == "T600") {
                form = '<div class="input-field"><label>Transponder name:<span style="color: red; font-size: 24px;">*</span></label><input \
                class="tsnamet" type="text"></div><div class="input-field"><label>Ip address:<span style="color: red; font-size: 24px;">*</span>\
                </label><input class="tsipt" type="text"></div><div class="input-field"><label>Port:<span style="color: red; font-size: 24px;">*</span>\
                </label><input class="tsportt" type="text"></div><div class="input-field"><label>Transponder username:<span style="color: red; font-size:\
                 24px;">*</span></label><input class="tsunamet" type="text"></div><div class="input-field"><label>Transponder password:<span style="color:\
                  red; font-size: 24px;">*</span></label><input class="tspasswordt" type="text"></div>'

            }
            else if (device_type == "OPS") {
                form = '<div class="input-field"><label>OPS name:<span style="color: red; font-size: 24px;">*</span></label><input class="opsnamet" type="text">\
                </div><div class="input-field"><label>Ip address:<span style="color: red; font-size: 24px;">*</span></label><input class="opsipt" type="text">\
                </div><div class="input-field"><label>Port:<span style="color: red; font-size: 24px;">*</span></label><input class="opsportt" type="text">\
                </div><div class="input-field"><label>OPS username:<span style="color: red; font-size: 24px;">*</span></label><input class="opsunamet" type="text"\
                ></div><div class="input-field"><label>OPS password:<span style="color: red; font-size: 24px;">*</span></label><input class="opspasswordt" type="text"></div>'

            }
            $(".edit-area-template").html("<p></p>")
            $(".edit-area-template").html(btns+form)
            devicename = $("[selected=selected]").find("[field=devicename]").text()
            deviceip = $("[selected=selected]").find("[field=deviceip]").text()
            deviceport = $("[selected=selected]").find("[field=deviceport]").text()
            deviceusername = $("[selected=selected]").find("[field=deviceusername]").text()
            devicepassword = $("[selected=selected]").find("[field=devicepassword]").text()
            if(device_type == "T600"){
                $(".tsnamet").val(devicename)
                $(".tsnamet").attr("curdevicename", devicename)
                $(".tsipt").val(deviceip)
                $(".tsportt").val(deviceport)
                $(".tsunamet").val(deviceusername)
                $(".tspasswordt").val(devicepassword)

            }
            else if(device_type == "OPS"){
                $(".opsnamet").val(devicename)
                $(".opsnamet").attr("curdevicename", devicename)
                $(".opsipt").val(deviceip)
                $(".opsportt").val(deviceport)
                $(".opsunamet").val(deviceusername)
                $(".opspasswordt").val(devicepassword)
            }
            


        }

    },

    savedeviceintable: function(){
        seldevtype = $(".selected_device").find(":selected").text()
            if (seldevtype == "T600") {
                transpondername = $(".tsnamet").val()
                seldevname = $(".tsnamet").attr("curdevicename")
                transponderip = $(".tsipt").val()
                transponderport = $(".tsportt").val()
                transponderusername = $(".tsunamet").val()
                transponderpassword = $(".tspasswordt").val()
                $.ajax({
                    headers: {
                        'X-CSRFToken': katana.$activeTab.find('input[name="csrfmiddlewaretoken"]').attr('value')
                    },
                    type: 'POST',
                    url: 'equinix/edit_transponder/',
                    async: false,
                    data: { "seldevname": seldevname, "transpondername": transpondername, "transponderip": transponderip, "transponderport": transponderport, "transponderusername": transponderusername, "transponderpassword": transponderpassword }
                }).done(function (data) {
                    if (data == "success") {
                        equinix.alert("Success!", "Succesfully edited a device.", "success")
                        equinix.closesidepanel()
                        equinix.fetch_devices_for_table()

                    }
                    else if (data == "duplicate") {
                        equinix.alert("Error!", "device name already exists.", "error")
                    }
                    else {
                        equinix.alert("Error!", "Failed to edit a device.", "error")
                    }
                });
            }
            else if (seldevtype == "OPS") {
                opsname = $(".opsnamet").val()
                seldevname = $(".opsnamet").attr("curdevicename")
                opsip = $(".opsipt").val()
                opsport = $(".opsportt").val()
                opsusername = $(".opsunamet").val()
                opspassword = $(".opspasswordt").val()
                $.ajax({
                    headers: {
                        'X-CSRFToken': katana.$activeTab.find('input[name="csrfmiddlewaretoken"]').attr('value')
                    },
                    type: 'POST',
                    url: 'equinix/edit_ops/',
                    async: false,
                    data: { "seldevname": seldevname, "opsname": opsname, "opsip": opsip, "opsport": opsport, "opsusername": opsusername, "opspassword": opspassword }
                }).done(function (data) {
                    if (data == "success") {
                        equinix.alert("Success!", "Succesfully edited a device.", "success")
                        equinix.closesidepanel()
                        equinix.fetch_devices_for_table()
                    }
                    else if (data == "duplicate") {
                        equinix.alert("Error!", "device name already exists.", "error")
                    }
                    else {
                        equinix.alert("Error!", "Failed to edit a device.", "error")
                    }
                });

            }
    },

    deletedeviceintable: function(){
        seldevtype = $(".selected_device").find(":selected").text()
        sel_devices = $("[selected=selected]").find("[field=devicename]")
                .map(function () { return $(this).text(); }).get();
            console.log("deleting groups...", sel_devices)
            $.ajax({
                headers: {
                    'X-CSRFToken': katana.$activeTab.find('input[name="csrfmiddlewaretoken"]').attr('value')
                },
                type: 'POST',
                url: 'equinix/delete_device/',
                async: false,
                data: { "devices": String(sel_devices), "device_type":seldevtype }
            }).done(function (data) {
                if (data == "success") {
                    equinix.alert("Success!", "Device(s) deleted succesfully.", "success")
                    equinix.fetch_devices_for_table()
                }
                else if (data == "fail") {
                    equinix.alert("Error!", "Unable to delete the device(s).", "error")
                }
            })

    },

    prompt_before_delete: function(){

        seldevtype = $(".selected_device").find(":selected").text()
        dlen = $("[selected=selected]").length
        let sel_devices = []
        if (dlen >= 1) {
            const swalWithBootstrapButtons = Swal.mixin({
                customClass: {
                  confirmButton: 'btn btn-success',
                  cancelButton: 'btn btn-danger'
                },
                buttonsStyling: false
              })
              
              swalWithBootstrapButtons.fire({
                title: 'Are you sure?',
                text: 'This action will also delete the groups, which are linked with the device(s)!',
                icon: 'warning',
                showCancelButton: true,
                confirmButtonText: 'Yes',
                cancelButtonText: 'No',
                reverseButtons: true
              }).then((result) => {
                if (result.value) {
                //   call delete function here
                equinix.deletedeviceintable()
                } 
              })

        }
        else if (dlen < 1) {
            equinix.alert("No device selected!", "Please select atleast one device to delete.", "error")
        }
    },

}

