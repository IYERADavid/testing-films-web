const email_input_element = document.getElementById('email');
const password_input_element = document.getElementById('password');
const span_elements = document.getElementsByClassName('error');
const form_element = document.getElementById('form');
const user_next_url_element = document.getElementById('next_url'); 
form_element.addEventListener('submit', (e) =>{
    // calling form validation if use try to submit form and the return value of form_validation
    // will be assigned to const validation_result.
    const validation_result = form_validation();
    // if in form validation occurs any error ,validation_result > 0,stop form submition
    // and show error to the user
    if (validation_result > 0){
        e.preventDefault();
    }
});

// form validation
const form_validation = () =>{
    // Now before any validation the below if statement checks if there is flask form error
    // element on the web page and removes it in order to start a new validation check. 
    if(span_elements[0]){
        for(let error = 0; error < span_elements.length; error++){
            span_elements[error].remove();
        };
    }

    //here by default if there is no error, number_of_errors = 0
    let number_of_errors = 0;

    // validating email, if any error occurs, number_of_error += 1
    if(email_input_element.value === ''){
        number_of_errors += 1;
        throw_error_for(email_input_element,"you must fillout this field!",'error-1');
    }else if(valid_email(email_input_element.value) === false){
        number_of_errors += 1;
        throw_error_for(email_input_element,"your email is not valid!",'error-1');
    }else if(email_input_element.value.length >= 321){
        number_of_errors += 1;
        throw_error_for(email_input_element,"your email must be less than 321 characters!",'error-1');
    } else{
        remove_error_for('error-1');
    }

    // validating password, if any error occurs, number_of_error += 1
    if(password_input_element.value === ''){
        number_of_errors += 1;
        throw_error_for(password_input_element,"you must fillout this field!",'error-2');
    } else if(password_input_element.value.length <= 5){
        number_of_errors += 1;
        throw_error_for(password_input_element,"Your password must be greater than 5 characters",'error-2')
    } else{
        remove_error_for('error-2');
    }

    // Now here the return statement will show us number_of_errors in our form 
    // at where form validation function is called
    return number_of_errors;
}
/* 
On this user_next_url function we set the user_next_url_element.value to a url
where a user wiil go when he/she finish login (the reason we set this url is becouse
a user has tryed to access this url without login and this url can be used by only
logged in user so for a great service we redirect user to previous needed url which
he/she was wanting to access before login)
*/
const user_next_url = (url) =>{
    user_next_url_element.value = url;
}

// this function get three argument
// input_name, error message, input_id
const throw_error_for = (input,message,error_id) =>{
    if(document.getElementById(error_id)){
        const span = document.getElementById(error_id);
        span.innerText = message;
    }else{
        const parent_div = input.parentElement;
        const span = document.createElement("span");
        span.innerText = message;
        span.style.color = 'red';
        span.id = error_id;
        parent_div.appendChild(span);
    }
}

// this function remove error element if no error found but 
// there is a previous error shown to the user
const remove_error_for = (error_id) =>{
    if(document.getElementById(error_id)){
     const error = document.getElementById(error_id);
     error.remove(); 
    }
}

// validating if it is real email
const valid_email = (email) =>{
    return /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/.test(email);
}
