var questions = document.getElementById("questions");
function attempt_btn_click() {
    alert("You can asses the quiz now..")
    for(let i=0;i<questions.children.length;i++){
        var sub_parent = questions.children.item(i);
        for(let j=0;j<sub_parent.children.length;j++){
            sub_parent.children.item(j).disabled = false;
        }
    }
    document.getElementById("attempt_btn").disabled = true;
}

function submit_btn() {
    var quiz = document.getElementById("quiz_id");
    var csrf = questions.children.item(0);
    var answers = new FormData();
    var answers_selected = 0;
    const xhr = new XMLHttpRequest();
    xhr.onload = function() {
        if (xhr.status == 200 && xhr.readyState == 4){
            responses = JSON.parse(xhr.response);
            answer_key = responses["answer_key"];
            console.log(answer_key);
            alert("Congratulations, you have " + responses["correct answers"] + " correct answers");
            for (let index in answer_key) {
                if (answer_key.hasOwnProperty(index)) {
                    mark_right_or_wrong(index, answer_key[index]);
                }
            }
        }        
        else {
            console.error(xhr.response);
        }
    }
    for(let i=0;i<questions.children.length;i++){
        var sub_parent = questions.children.item(i);
        for(let j=0;j<sub_parent.children.length;j++){
            checked_item = sub_parent.children.item(j);
            if(checked_item.checked) {
                answers.append(String(sub_parent.id), checked_item.value);
                answers_selected=answers_selected+1;
            }
        }
    }
    if (answers_selected===questions.children.length-1){
        xhr.open("POST", "/qms/quizzes/"+quiz.value);
        xhr.setRequestHeader('X-CSRFToken', csrf.value);
        xhr.setRequestHeader('content_type', "application/json");
        xhr.send(answers);
        document.getElementById("submit_btn").disabled =true;
    }
    else{
        alert("You must answer all the questions..");
    }
}

function mark_right_or_wrong(question_id, right) {
    var division = document.getElementsByClassName("question_"+question_id);
    var question = division[0];
    console.log(question);
    if (right){question.style = "background-color:green;";}
    else {question.style = "background-color:orange;"}
}
