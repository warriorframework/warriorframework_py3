var equinix = {

measure_func: function(){
    $(".result").val("")
    if($(".api_res").css("display") == "none"){
        $(".api_res").css("display", "block");
    }
    if($(".loader").css("display") == "none"){
        $(".loader").show();
    }
    $(".set_btn").attr("disabled", true);
    $(".msr_btn").attr("disabled", true);
   $odi = $(".msr_odi").val()
   $msr_pr_type = $(".msr_pr_type").find(":selected").text()
   console.log($odi, $msr_pr_type)
   $.ajax({
    headers: {
        'X-CSRFToken': katana.$activeTab.find('input[name="csrfmiddlewaretoken"]').attr('value')
    },
    type: 'GET',
    url: 'equinix/measure/',
    dataType: "json",
    async:false,
    data: {"odi": $odi, "pr_type":$msr_pr_type}
}).done(function(data){
    $(".loader").css("display", "none");
    $(".result").val(JSON.stringify(data, null, 4));
    $(".set_btn").attr("disabled", false);
    $(".msr_btn").attr("disabled", false);

})
},

set_func: function(){
    $(".result").val("")
    if($(".api_res").css("display") == "none"){
        $(".api_res").css("display", "block");
    }
    if($(".loader").css("display") == "none"){
        $(".loader").show();
    }
    $(".set_btn").attr("disabled", true);
    $(".msr_btn").attr("disabled", true);
   $odi = $(".set_odi").val()
   $set_pr_type = $(".set_pr_type").find(":selected").text()
   console.log($odi, $set_pr_type)
   $.ajax({
    headers: {
        'X-CSRFToken': katana.$activeTab.find('input[name="csrfmiddlewaretoken"]').attr('value')
    },
    type: 'GET',
    url: 'equinix/set/',
    dataType: "json",
    async:false,
    data: {"odi": $odi, "pr_type":$set_pr_type}
}).done(function(data){
    $(".loader").css("display", "none");
    $(".result").val(JSON.stringify(data, null, 4));
    $(".set_btn").attr("disabled", false);
    $(".msr_btn").attr("disabled", false);

})
}

}