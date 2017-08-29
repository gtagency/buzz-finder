//vars to request from server
//var path = [[0, 0], [0, 1], [0, 2], [0, 3],
    //[1, 3], [2, 3], [3, 3],
    //[3, 2], [3, 1], [3, 0],
    //[2, 0], [1, 0], [0, 0]]
var background_color = '#DDDDDD';
var WIDTH = 40;
var WIDTH2 = WIDTH / 2;
var tick_rate = 5;
var step = 1;
var bzm = null;
var buzz = null;
var bus = null;

function get_json(url) {
    var req = new XMLHttpRequest();
    req.open("GET", url, false);
    req.send();
    return JSON.parse(req.responseText);
}

var solved_game = get_json('/solve');
var path = solved_game['path'];
var current = solved_game['start'];
var obstacles = solved_game['obstacles'];
var goal = solved_game['end'];


function draw_state(step) {
    //reset frame
    background(background_color);
    image(buzz, goal[1] * WIDTH, goal[0] * WIDTH, WIDTH, WIDTH);
    
    //draw path to current point
    for (var i = 1; i < step; i++) {
        line(WIDTH2 + path[i - 1][1] * WIDTH, WIDTH2 + path[i - 1][0] * WIDTH,
                WIDTH2 + path[i + 0][1] * WIDTH, WIDTH2 + path[i + 0][0] * WIDTH);
    }

    line(WIDTH2 + path[step - 1][1] * WIDTH, WIDTH2 + path[step - 1][0] * WIDTH, 
            WIDTH2 + current[1] * WIDTH, WIDTH2 + current[0] * WIDTH);
    
    //draw world
    for (var i = 0; i < obstacles.length; i++) {
        //image(bus, WIDTH2 + obstacles[i][1] * WIDTH,
                //WIDTH2 + obstacles[i][0] * WIDTH, WIDTH, WIDTH);
        rect(obstacles[i][1] * WIDTH, obstacles[i][0] * WIDTH, WIDTH, WIDTH);
    }

    //move
    var dr = 0
    if (current[0] > path[step][0]) {
        dr = -1;
    } else if (current[0] < path[step][0]){
        dr = 1;
    }

    var dc = 0
    if (current[1] > path[step][1]) {
        dc = -1;
    } else if (current[1] < path[step][1]){
        dc = 1;
    }

    current[0] = current[0] + dr / tick_rate;
    current[1] = current[1] + dc / tick_rate;

    image(bzm, WIDTH * current[1], WIDTH * current[0], WIDTH, WIDTH);
}

function setup() {
    createCanvas(600, 600);
    background(background_color);
    frameRate(30);
    bzm = loadImage('js/buzzmobile.png');
    buzz = loadImage('js/buzz.png');
    bus = loadImage('js/bus.png');
    strokeWeight(10);
}

function draw() {
    if (frameCount % tick_rate == 0 && step < path.length) {
        current = path[step].slice();
        step += 1;
    }

    if (step < path.length) {
        draw_state(step);
    }
}

