var background_color = '#DDDDDD';
var WIDTH = 40;
var WIDTH2 = WIDTH / 2;
var tick_rate = 5;
var step = 1;
var bzm = null;
var buzz = null;
var bus = null;
var crowd = null;

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
var world = solved_game['world'];
var goal = solved_game['end'];

function line_grid(x1, y1, x2, y2) {
    line(WIDTH2 + x1 * WIDTH, WIDTH2 + y1 * WIDTH,
            WIDTH2 + x2 * WIDTH, WIDTH2 + y2 * WIDTH);
}

function image_grid(img, x, y) {
    image(img, x * WIDTH, y * WIDTH, WIDTH, WIDTH);
}

function draw_state(step) {
    //reset frame
    background(background_color);
    image_grid(buzz, goal[1], goal[0]);

    //draw path to current point
    for (var i = 1; i < step; i++) {
        stroke(66, 134, 244);
        line_grid(path[i - 1][1], path[i - 1][0], path[i][1], path[i][0]);
    }
    line_grid(path[step - 1][1], path[step - 1][0], current[1], current[0]);

    //draw world obstacles
    for (var i = 0; i < obstacles.length; i++) {
        stroke(0);
        var r = obstacles[i][0];
        var c = obstacles[i][1];
        if (world[r][c] == 0) {
            image_grid(bus, c, r);
        } else if (world[r][c] == 1) {
            image_grid(crowd, c, r);
        } else if (world[r][c] > 1) {
            rect(obstacles[i][1] * WIDTH, obstacles[i][0] * WIDTH, WIDTH, WIDTH);
        }

    }

    //move bzm
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

    //draw!
    image_grid(bzm, current[1], current[0]);
}

function setup() {
    createCanvas(600, 600);
    background(background_color);
    frameRate(30);
    bzm = loadImage('js/buzzmobile.png');
    buzz = loadImage('js/buzz.png');
    bus = loadImage('js/bus.jpeg');
    crowd = loadImage('js/crowd.jpeg');
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

