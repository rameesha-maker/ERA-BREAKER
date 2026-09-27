
/*==era breaker mission control - SCRIPT.JS==*/
/*==game data ==*/
let fuel = 100;
let charges = 3;
let progress = 0;
let playerX = 0;
let playerY = 0;
let playerStatus = "online";
let currentEra = "FEIDAL JAPAN";

let isMoving = false;
let currentDirection = "STOP";

/* python pygame connection */
const socket = new WebSocket("ws://127.0.0.1:8765");

socket.onopen = () => {
    console.log("connected to ERA BREAKER");

    document.getElementById("connectionStatus").textContent = "CONNECTED";
};
socket.onmessage = (event) => {
    const state = JSON.parse(event.data);
    updateDashboard(state);
};
socket.onclose = () => {
    console.log("Disconnected from game");
    document.getElementById("connectionStatus").textContent = "DISCONNECTED";
}; 

function sendCommand(command) {
    if (socket.readyState === WebSocket.OPEN) {
        socket.send(JSON.stringify({
            command: command
        }));
        console.log("Sent to Python:", command);
    }
}

/*-- get html elements --*/
const eraDisplay = document.getElementById("era");
const eraDescription = document.getElementById("eraDescription");
const playerStatusDisplay = document.getElementById("playerStatus");

const playerPositionDisplay = document.getElementById("playerPosition");
const progressFIll = document.getElementById("progressFill");

const progressText = document.getElementById("progressText");
const fuelFill = document.getElementById("fuel-bar");
const fuelText = document.getElementById("fuelText");

const chargesDisplay = document.getElementById("charges");

const connectionStatus = document.getElementById("connectionStatus");

/*--updatefuel--*/
function updateFuel() {
    fuelFill.style.width = fuel + "%";
    fuelText.textContent = fuel + "%";


/*--change appearance when fuel is low--*/

if (fuel <= 20) {
    fuelFill.style.background = "#ff5864";
    fuelFill.style.boxShadow = "0 0 12px #ff5864"
    fuelText.style.color = "#ff5864";
} 
else { 
    fuelFill.style.background = "#42ff9e";

    fuelFill.style.boxShadow = "0 0 12px #42ff9e";

    fuelText.style.color = "#42ff9e";
}
}
/*-- update time machine charges --*/
 function updateCharges() {
    chargesDisplay.textContent = charges;
 }

 /*--update game progress--*/
 function updateProgress() {
    progressFill.style.width =
    progress + "%";
 } 

 /*--update play position--*/

 function updatePlayerPosition() {
    playerPositionDisplay.textContent = 
    playerX + "," + playerY;
 }

 /*--update player status __*/

 function updatePlayerStatus(status) {
    playerStatus = status;
    playerStatusDisplay.textContent = status;

    if (status === "ONLINE") {
        playerStatusDisplay.style.color = "#42ff9e";
    } 
    else if (status === "MOVING") {
        playerStatusDisplay.style.color = "#00d9ff";
    }
    else if (status === "STOPPED" ) {
        playerStatusDisplay.style.color = "#ffcf40";
    }
    else if (status === "OFFLINE") {
        playerStatusDisplay.style.color = "#ff5864";
    }
 }
 /*--change era--*/
 function changeEra(era) {
    currentEra = era;
    eraDisplay.textContent = era;
    if (era === "FEUDAL JAPAN") {
        eraDescription.textContent = 
        "Historical era detected";

        document.body.className = "feudal";
    }
    else if (era === "MODERN TOKYO") {
        eraDescription.textContent = "Modern era detected";
        
        document.body.className = "modern";
    }
    else if (era === "future city") {
        eraDescription.textContent = 
        "Future era detected";
        document.body.className = "future";
    }

    /*--small visual effect--*/
    eraDisplay.style.transform = 
    "scale(1.1)";
    setTimeout(function () {
        eraDisplay.style.transform = 
        "scale(1)";
    }, 250);
 }

 /*--move left--*/
 function moveLeft() {
    playerX -= 10;
    currentDirection = "LEFT";
    isMoving = true;
    updatePlayerPosition();
    updatePlayerStatus("MOVING");
    console.log("MOVE LEFT");

    sendCommand("MOVE_LEFT");

 }

 /*--move right--*/ 
 function moveRight() {
    playerX += 10;
    currentDirection = "RIGHT";
    isMoving = true;
    updatePlayerPosition();
    updatePlayerStatus("MOVING");
    console.log("MOVE RIGHT");
    sendCommand("MOVE_RIGHT");
 }

 /*--JUMP--*/
 function jump() {
    currentDirection = "JUMP";
    updatePlayerStatus("MOVING");
    console.log("jump");
    sendCommand("JUMP");
    /* visual feedback*/
    document.querySelector("#jumpBtn").style.transform =
    "translateY(-8px)";

    setTimeout(function() {
        document.querySelector ("#jumpBtn").style.transform = "translateY(0)";
    }, 200);
 }

 /*--stop player--*/
 function stopPlayer() {
    isMoving = false;
    currentDirection = "STOP";
    updatePlayerStatus("STOPPED");
    console.log("STOP");
    sendCommand("STOP");
 }

 /*-- bamboo copter --*/
 function activateCopter() {
    /*dont activate if no fuel*/
    if (fuel <= 0) {
        alert("BAMBOO COPTER: NO FUEL");
        return;
    }
    /*use fuel*/
    fuel -= 10;

    if (fuel < 0) {
        fuel = 0;
    }
    updateFuel();
    console.log("BAMBOO COPTER ACTIVATED");
    sendCommand("ACTIVATE_COPTER");
    updatePlayerStatus("MOVING");
 }
 /*--rewind time--*/
 function rewindTime() {
    /*check charges*/
    if (charges <= 0) {
        alert("TIME MACHINE: NO CHARGES");
        return;
    }

    /*use one charge*/
    charges--;
    updateCharges();
    console.log("time machine activated");
    sendCommand("REWIND");

    /*rewind progress*/
    progress -= 10;
    if (progress < 0) {
        progress = 0;
    }
    updateProgress();
    /*rewind visual effect*/
    document.body.style.filter =
    "brightness(2)"; 
    
    setTimeout(function () {
    document.body.style.filter =
    "brightness(1)";
    }, 200);
    updatePlayerStatus("MOVING")
 }
 /*BUTTON EVENTS*/

 /*left*/
 document
 .getElementById("leftBtn")
 .addEventListener("click",function() {
    moveLeft();
 });

 /*rightt*/
 document
 .getElementById("rightBtn")
 .addEventListener("click", function()
{
    moveRight();
});


/*stop*/ 
document
.getElementById("stopBtn")
.addEventListener("click", function () {
    stopPlayer();
});

/*jump*/
document
.getElementById("jumpBtn")
.addEventListener("click", function()
{
    jump();
});

/*bamboo copter*/
document
.getElementById("copterBtn")
.addEventListener("click", function()
{
    activateCopter();
});

/*time machine*/
document
.getElementById("rewindBtn")
.addEventListener("click", function()
{
    rewindTime();
});

function updateDashboard(state) {
    if (state.era !== undefined) {
        changeEra(state.era);
    }
    if (state.playerX !== undefined) {
        playerX = state.playerX;
    }
    if(state.playerY !== undefined) {
        playerY = state.playerY;
    }
    if (state.status !== undefined) {
        playerStatus = state.status;
    }
    if (state.charges !== undefined) {
        charges = state.charges;
    }
    if (state.progress !== undefined) {
        progress = state.progress;
    }
    updatePlayerPosition();
    updatePlayerStatus(playerStatus);
    updateFuel();
    updateCharges();
    updateProgress();
}
/*keyboard controls*/
document.addEventListener("keydown", function(event)
{
    /*left*/
    if (event.key === "ArrowLeft") {
        event.preventDefault();
        moveLeft();
    }
    /*right*/
    if (event.key === "ArrowRight") {
        event.preventDefault();
        moveRight();
    }

    /*up*/
    if (event.key === "ArrowUp") {
        event.preventDefault();
        jump();
    }
    /*space*/
    if (event.code === "Space") {
        event.preventDefault();
        stopPlayer();
    }
});

/*stimulated game progress*/
/* this is for testing only*/
setInterval(function() {
    if (progress < 100 && isMoving) {
        progress++;
        updateProgress();
    }
}, 1000);
/*stimulated player movement */
/*player positions *only in testing*/

setInterval(function()
{
    if (isMoving) {
        if (currentDirection === "RIGHT") {
            playerX += 2;
        }
        else if (currentDirection === "LEFT") {
            playerX -= 2;
        }
        updatePlayerPosition();
    }
}, 500);

/*initial game state */
updateFuel();
updateCharges();
updateProgress();
updatePlayerPosition();
updatePlayerStatus("ONLINE");
changeEra("FEUDAL JAPAN");

/*test commands*/

/* i hATE BUGS */