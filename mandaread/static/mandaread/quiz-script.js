$(document).ready(function(){
    let score = 0;
    let answered_all = true
    let numOfItems = $('.card-body').length
    let wrongAnswers = []
    percentage = 0

    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    var forms = document.querySelectorAll('.needs-validation')

    // Loop over them and prevent submission
    Array.prototype.slice.call(forms)
        .forEach(function (form) {
            form.addEventListener('submit', function (event) {
                form.classList.add('was-validated')
            }, false)
        })


    $("#assessment-form").on("submit", function(e){
        answered_all = true
        score = 0
        e.preventDefault()
        
        //Check for MC and FITB fields
        $(".assessment-item").each(function(){
            //Check if current field is unanswered
            if($(this).val() == ""){
                answered_all = false
            }
            // Check if answer is correct. If yes, add 1 to score.
            else if($(this).val().toLowerCase() == $(this).siblings(".hidden-answer").val().toLowerCase()){
                score += 1;
            }
            // If answer not correct, add their IDs to array.
            else{
                let id = $(this).attr('id')
                wrongAnswers.push(id)
            }
        })

        $(".radio-group").each(function(){
            // If none of the radio buttons were checked
            if(!$(this).find(".form-check-input").is(":checked")){
                answered_all = false
            }
            else if($(this).find("input:radio[class='form-check-input']:checked").val() == $(this).siblings(".hidden-answer").val()){
                score += 1;
            }
            else{
                let id = $(this).attr('id')
                wrongAnswers.push(id)
            }
        })


        // If there were any unanswered fields
        if(answered_all == false){
            $(".submit-error").show()
            e.preventDefault()
            e.stopPropagation()
        }
        else if(answered_all){
            percentage = Math.round((score / numOfItems) * 100)

            //LOW PERCENTAGE: 0-33
            //MED PERCENTAGE: 34-67
            //HIGH PERCENTAGE: 68-100

            if(percentage >= 68 && percentage <= 100){
                $(".alert").addClass("alert-success")
                $(".score-message-span").html("Congratulations! pretty good score! Keep learning, keep striving, and stay motivated!")
            }
            else if(percentage >= 34 && percentage <= 67){
                $(".alert").addClass("alert-warning")
                $(".score-message-span").html("Not bad! But we know you can do better. Just keep up the good work.")
            }
            else if(percentage >= 0 && percentage <= 33){
                $(".alert").addClass("alert-danger")
                $(".score-message-span").html("Keep your hopes high! Re-read the lesson and have breaks once in a while. You got this!")
            }
            
            if(percentage != 100){
                $(".take-a-scroll").show()
            }

            $("#score").html(score)
            $("#total").html(numOfItems)
            $(".score-message").show()
            $(".submit-error").hide()
            $(".instructions").hide()
            window.scrollTo({ top: 0, behavior: 'smooth' });
            
            //Show wrong answers
            $.each(wrongAnswers, function(index, value){
                $(`#${value}`).siblings(".correct-answer").show()
            })

            //Disable all text fields
            $("input").each(function(){
                $(this).prop('disabled', true)
            })

            //Hide submit button
            $(".submit-assessment").hide()

            if($("#test-type").val() == "assessment")
                checkAssessmentPerfect()
            else if($("#test-type").val() == "mock")
                checkMockPerfect()
        }
    })



    // Only allow A, B, C, D inputs
    $(".type-mc").on('keypress', function(e){
        if(e.which != 65 &&
            e.which != 66 &&
            e.which != 67 &&
            e.which != 68 &&    
            e.which != 97 && 
            e.which != 98 && 
            e.which != 99 && 
            e.which != 100){
            return false
        }
    })
})