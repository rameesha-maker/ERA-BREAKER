let socket = null;
const connection = document.getElementById("connection");
const era = document.getElementById("era");
const playerX = document.getElementById("player-x");
const playerY = document.getElementById("player-y");
const challenges = document.getElementById("challenges");
const copter = document.getElementById("copter");
const timeMachine = document.getElementById("time-machine");

function connect(){
    socket = new WebSocket("ws://localhost:8765");
    socket.onopen = function (){connection.textContent = "CONNECTED";};
    socket.onclose = function (){connection.textContent = "DISCONNECTED";};
    socket.onerror = function(){connection.textContent = "ERROR";};
    socket.onmessage = function(event){const state = JSON.parse(event.data);
        updateDashboard(state);};
    }
function updateDashboard(state){era.textContent}