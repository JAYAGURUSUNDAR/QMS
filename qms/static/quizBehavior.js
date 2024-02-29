var attempts = [];
var scores = [];
var best_attempt;

function get_data() {
    var table = document.querySelector('table');
    var tableBody = table.querySelector('tbody');
    var rows = tableBody.querySelectorAll('tr');
    for (var i = 0; i < rows.length; i++) {
        var y = rows[i].querySelector('td:nth-child(3)');
        var y_data = parseInt(y.textContent);
        attempts.push(String(i+1));
        scores.push(y_data);
    }
}

get_data();

const ctx = document.getElementById('quizBehaviorChart').getContext('2d');

const chart = new Chart(ctx, {
    type: 'line',  // Change chart type to line
    data: {
        labels: attempts,
        datasets: [{
            label: 'Score',
            data: scores,
            backgroundColor: 'rgba(255, 99, 132, 0.2)',
            borderColor: 'rgba(255, 99, 132, 1)',
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true,
                ticks: {  // Add y-axis ticks configuration
                    stepSize: 1,  // Define step size for y-axis
                },
                title: {  // Add y-axis title
                    display: true,
                    text: 'Scores'  // Specify y-axis title text
                }
            }
        }
    }
});

function get_best_attempt(){
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/api/user/" + userId + "/best_attempt");
    xhr.onload = function() {
      if (xhr.status == 200) {
          best_attempt = JSON.parse(xhr.responseText);
          show_result();
      } else {
          console.error(xhr.statusText);
      }
    };
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.setRequestHeader("X-CSRFToken", );
    xhr.send();
}

// Function to update the result on screen with the best attempt information
function show_result(){
    document.getElementById('username').innerHTML= "User: "+best_attempt['user'];
    document.getElementById('score').innerHTML="Score: "+best_attempt['score']+" / 10";
    document.getElementById('time').innerHTML="Time taken: "+best_attempt['time']+'s';
}

