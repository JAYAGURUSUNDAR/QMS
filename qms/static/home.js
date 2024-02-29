function on_click(){
    var sub = document.getElementById('sub-content');
    var is_element = sub.querySelector('h4');
    if(!is_element){
        var heading1 = document.createElement("h4");
        heading1.style = "color:blue;"
        heading1.innerText = "A comprehensive Management System for creating and assessing the quiz. Mainly useful for schools students"
        sub.appendChild(heading1);
    }
    else{
        sub.removeChild(is_element);
    }
}