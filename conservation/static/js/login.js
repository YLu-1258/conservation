var inputs = document.querySelectorAll('.form-field');
var submit_button = document.getElementById("submit-button")
console.log(submit_button);
var isAllFilled = false;
function check_if_all_filled() {
    for (var i = 0; i < inputs.length; i++) {
        if (inputs[i].value === '') {
            submit_button.classList.remove('filled');
            submit_button.setAttribute("disabled", "true")
            return;
        }
                
    }
    submit_button.removeAttribute("disabled")
    submit_button.classList.add('filled');
            
}

document.addEventListener('DOMContentLoaded', function() {
    for (var i = 0; i < inputs.length; i++) {
        inputs[i].addEventListener('focus', function() {
            this.parentNode.classList.add('focused');
        });

        inputs[i].addEventListener('blur', function() {
            var inputValue = this.value;
            if (inputValue === '') {
                this.classList.remove('filled');
                this.parentNode.classList.remove('focused');
                check_if_all_filled();
            } else {
                this.classList.add('filled');
                check_if_all_filled();
            }
        });
    }
});