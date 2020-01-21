var equinix = {

measure_func: function(){
    $(".result").attr("placeholder", "fetching result...");
    if($(".api_res").css("display") == "none"){
        $(".api_res").css("display", "block");
    }
    if($(".loader").css("display") == "none"){
        $(".loader").css("display", "block");
    }
    $(".set_btn").attr("disabled", true);
    $(".msr_btn").attr("disabled", true);
   $odi = $(".msr_odi").val()
   $msr_min_freq = $(".msr_min_freq").val()
   $msr_max_freq = $(".msr_max_freq").val()
   $pr_type = $(".msr_pr_type").find(":selected").text()
   console.log($odi, $msr_min_freq, $msr_max_freq, $pr_type)
   $.ajax({
    headers: {
        'X-CSRFToken': katana.$activeTab.find('input[name="csrfmiddlewaretoken"]').attr('value')
    },
    type: 'GET',
    url: 'equinix/measure/',
    dataType: "json",
    async:false,
    data: {"odi": $odi, "msr_min_freq":$msr_min_freq, "msr_max_freq" :$msr_max_freq, "pr_type":$pr_type}
}).done(function(data){
    console.log(data)
    $(".loader").css("display", "none");
    $(".result").val(JSON.stringify(data))
    $(".set_btn").attr("disabled", false);
    $(".msr_btn").attr("disabled", false);

})
},

set_func: function(){
    $(".result").attr("placeholder", "fetching result...");
    if($(".api_res").css("display") == "none"){
        $(".api_res").css("display", "block");
    }
    if($(".loader").css("display") == "none"){
        $(".loader").css("display", "block");
    }
    $(".set_btn").attr("disabled", true);
    $(".msr_btn").attr("disabled", true);
   $odi = $(".set_odi").val()
   $set_min_freq = $(".set_min_freq").val()
   $set_max_freq = $(".set_max_freq").val()
   $set_pr_type = $(".set_pr_type").find(":selected").text()
   console.log($odi, $set_min_freq, $set_max_freq, $set_pr_type)
   $.ajax({
    headers: {
        'X-CSRFToken': katana.$activeTab.find('input[name="csrfmiddlewaretoken"]').attr('value')
    },
    type: 'GET',
    url: 'equinix/set/',
    dataType: "json",
    async:false,
    data: {"odi": $odi, "set_min_freq":$set_min_freq, "set_max_freq" :$set_max_freq, "pr_type":$set_pr_type}
}).done(function(data){
    console.log(data)
    $(".loader").css("display", "none");
    $(".result").val(JSON.stringify(data))
    $(".set_btn").attr("disabled", false);
    $(".msr_btn").attr("disabled", false);

})
}

}