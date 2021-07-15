const first_name_input_element = document.getElementById('first_name');
const last_name_input_element = document.getElementById('last_name');
const middle_name_input_element = document.getElementById('middle_name');
const email_input_element = document.getElementById('email');
const password_input_element = document.getElementById('password');
const confirm_password_input_element = document.getElementById('confirm_password');
const span_elements = document.getElementsByClassName('error');
const form_element = document.getElementById('form');
form_element.addEventListener('submit', (e) =>{
    // Calling form validation function if user try to submit form and then the return value of form_validation
    // will be assigned to const validation_result.
    const validation_result = form_validation();
    // If in form validation occurs any error the const validation_result will be greater than 0 and form submition
    // will be stoped and show error to the user
    if( validation_result > 0){
        e.preventDefault();
    }
})

// form validation
const form_validation = () => {
    // Now before any validation the below if statement checks if there is flask form error
    // element on the web page and removes it in order to start a new validation check. 
    if(span_elements[0]){
        for(let error = 0; error < span_elements.length; error++){
            span_elements[error].remove();
        };
    }

    // Here by default if there is no error, number_of_errors = 0
    let number_of_errors = 0;
    // Validating first_name, if any error occurs, number_of_error += 1
    if(first_name_input_element.value === ''){
        number_of_errors += 1; 
        throw_error_for(first_name_input_element,"You must fillout this field!",'error-1');
    } else if(first_name_input_element.value.length >= 25){
        number_of_errors += 1;
        throw_error_for(first_name_input_element,"Your name must be less than 25 characters!",'error-1');
    }else{
        remove_error_for('error-1'); 
    }

    // Validating last_name, if any error occurs, number_of_error += 1
    if(last_name_input_element.value === ''){
        number_of_errors += 1;
        throw_error_for(last_name_input_element,"You must fillout this field!",'error-2');
    } else if(last_name_input_element.value.length >= 25){
        number_of_errors += 1;
        throw_error_for(last_name_input_element,"Your name must be less than 25 characters!",'error-2');
    } else{
        remove_error_for('error-2');
    }

    // Validating middle_name, if any error occurs, number_of_error += 1
    if(middle_name_input_element.value.length >= 15){
        number_of_errors += 1;
        throw_error_for(middle_name_input_element,"Your name must be less than 15 characters!",'error-3'); 
    } else{
        remove_error_for('error-3');
    }

    // Validating email, if any error occurs, number_of_error += 1
    if(email_input_element.value === ''){
        number_of_errors += 1;
        throw_error_for(email_input_element,"You must fillout this field!",'error-4');
    }else if(valid_email(email_input_element.value) === false){
        number_of_errors += 1;
        throw_error_for(email_input_element,"Your email is not valid!",'error-4');
    }else if(email_input_element.value.length >= 321){
        number_of_errors += 1;
        throw_error_for(email_input_element,"your email must be less than 321 characters!",'error-4');
    } else{
        remove_error_for('error-4');
    }

    // Validating password, if any error occurs, number_of_error += 1
    if(password_input_element.value === ''){
        number_of_errors += 1;
        throw_error_for(password_input_element,"You must fillout this field!",'error-5');
    } else if(password_input_element.value.length <= 5){
        number_of_errors += 1;
        throw_error_for(password_input_element,"Your password must be greater than 5 characters",'error-5')
    } else{
        remove_error_for('error-5');
    }

    // Validating confirm_password, if any error occurs, number_of_error += 1
    if(confirm_password_input_element.value === ''){
        number_of_errors += 1;
        throw_error_for(confirm_password_input_element,"You must fillout this field!",'error-6');
    } else if(password_input_element.value !== confirm_password_input_element.value){
        number_of_errors += 1;
        throw_error_for(confirm_password_input_element,"Your passwords does not match!",'error-6');
    } else{
        remove_error_for('error-6');
    }
    // Now here the return statement will show us number_of_errors in our form 
    // at where form validation function is called
    return number_of_errors


};
// This function get three argument
// input_name, error message, input_id
const throw_error_for = (input_element,message,error_id) => {
    if(document.getElementById(error_id)){
        const span = document.getElementById(error_id);
        span.innerText = message;
    }else{
        const parent_element = input_element.parentElement;
        const span = document.createElement("span");
        span.innerText = message;
        span.style.color = 'red';
        span.id = error_id;
        parent_element.appendChild(span);
    }
}

// This function remove error element if no error found but
// there is a previous error shown to the user
const remove_error_for = (error_id) =>{
    if(document.getElementById(error_id)){
     const error = document.getElementById(error_id);
     error.remove(); 
    }
}

// Validating if it is real email from https://www.w3resource.com/javascript/form/email-validation.php
const valid_email = (email) =>{
    return /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/.test(email);
}
