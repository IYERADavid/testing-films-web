let global_id;
let get_video_info = (id_as_string, video_id, video_name, status, upload_time) => {
    global_id = id_as_string;
    document.getElementById('video_id').innerHTML = video_id;
    document.getElementById('video_name').innerHTML = video_name;
    document.getElementById('video_description').innerHTML = status;
    document.getElementById('upload_time').innerHTML = upload_time;
    let video_element = document.getElementById(id_as_string);
    let video_place = document.getElementById('modal_video');
    let video_navigation_btn = document.getElementsByClassName(id_as_string)[0];
    let video_navigation_btn_place = document.getElementById("navigation_btn");
    video_element.setAttribute('class','block video_on');
    video_navigation_btn.setAttribute('id', 'button_on');
    video_place.appendChild(video_element);
    video_navigation_btn_place.appendChild(video_navigation_btn)
}

remove_data = () =>{
    let id_as_string = global_id
    let id = parseInt(id_as_string);
    id = id-1;
    document.getElementById('video_id').innerHTML = "";
    document.getElementById('video_name').innerHTML = "";
    document.getElementById('video_description').innerHTML = "";
    document.getElementById('upload_time').innerHTML = "";
    let video_element = document.getElementsByClassName('block video_on')[0];
    let video_navigation_btn = document.getElementById('button_on');
    let video_place = document.getElementsByClassName('video_hidden_tag')[id];
    let video_navigation_btn_place = document.getElementsByClassName('video_btn_tag')[id];
    video_element.setAttribute('class','block');
    video_navigation_btn.setAttribute('id','button');
    setTimeout(() => {
        video_place.appendChild(video_element);
        video_navigation_btn_place.appendChild(video_navigation_btn);
    },300);
}

