$(document).ready(function(){
    hidden = true;

    $("#logout-btn").on("click", function(){
        if(hidden){
            $("#logout-dropdown").removeClass("d-none").addClass("d-flex");
            hidden = false
        }
        else{
            $("#logout-dropdown").removeClass("d-flex").addClass("d-none");
            hidden = true
        }
    })


    $("#cancel-logout").on('click', function(){
        $("#logout-dropdown").removeClass("d-flex").addClass("d-none");
        hidden = true
    })

    $("#dropdown-range").on('click', function(){
        $("#date-range-picker").show()
    })

    $("#filter-range").on('click', function(){
        rangeStart = $("#range-start").val()
        rangeEnd = $("#range-end").val()
        currentURL = $("#current-url").val()
        window.location.href = currentURL + "?start=" + rangeStart + "&end=" + rangeEnd
    })
})

// Date Picker
const elem = document.getElementById('range');
const dateRangePicker = new DateRangePicker(elem, {
    format: "yyyy-mm-dd"
}); 
