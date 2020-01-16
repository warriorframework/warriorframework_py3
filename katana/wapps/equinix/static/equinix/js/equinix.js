window.error_flag = "false";
var equinix = {
   set_func: function(){
    console.log("setting values...!")
    $(".set_result").val("");
    data = $(".set_data").val()
    console.log(data)
    // try {
    //     JSON.parse(data);
    // } catch (e) {
    //    error_flag = "true"
    // }
    // if (error_flag == "true"){
    //     console.log("invalid");
    // }
    // else{
    //     console.log("valid");
    // }
    if (data.trim() === ""){
        $(".set_data").css("border-color", "red");
    }
    else{
        $(".set_data").css("border-color", "#b1b6bd");
        if($(".set-result").css("display") == "none"){
        $(".set-result").css("display", "block");
        }
        if($(".set_loader").css("display") == "none"){
            $(".set_loader").css("display", "block");
            }
        $('.set-measure-btn').attr('disabled',true);
        $.ajax({
            headers: {
                'X-CSRFToken': katana.$activeTab.find('input[name="csrfmiddlewaretoken"]').attr('value')
            },
            type: 'POST',
            url: 'equinix/set/',
            dataType: "json",
            async:false,
            data: {"json_data": data}
        }).done(function(data){
            $(".set_result").val("Script status: "+data["script_status"]);
            $('.set-measure-btn').attr('disabled',false);
            $(".set_loader").css("display", "none");
        })
    }
   },

   measure_func: function(){
    console.log("measuring values...!");
    $(".measure_result").val("");
    data = $(".measure_data").val();
    if (data.trim() === ""){
        $(".measure_data").css("border-color", "red");

    }
    else{
        console.log(data);
        $(".measure_data").css("border-color", "#b1b6bd");
        if($(".measure-result").css("display") == "none"){
        $(".measure-result").css("display", "block");
        }
        if($(".measure_loader").css("display") == "none"){
            $(".measure_loader").css("display", "block");
            }
        $('.set-measure-btn').attr('disabled',true);
        $.ajax({
            headers: {
                'X-CSRFToken': katana.$activeTab.find('input[name="csrfmiddlewaretoken"]').attr('value')
            },
            type: 'POST',
            url: 'equinix/measure/',
            dataType: "json",
            async:false,
            data: {"json_data": data}
        }).done(function(data){
            $(".measure_result").val("Script status: "+data["script_status"]);
            $('.set-measure-btn').attr('disabled',false);
            $(".measure_loader").css("display", "none");
        })
    }
   },
}