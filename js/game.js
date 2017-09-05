var background_color = '#DDDDDD';
var WIDTH = 40;
var DIM = 20;
var WIDTH2 = WIDTH / 2;
var tick_rate = 5;
var step = 0;
var bzm = null;
var buzz = null;
var bus = null;
var crowd = null;
var ANIMATION_STATE = 0;

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
var frontier_points = solved_game['frontier_points'];

function line_grid(x1, y1, x2, y2) {
    line(WIDTH2 + x1 * WIDTH, WIDTH2 + y1 * WIDTH,
            WIDTH2 + x2 * WIDTH, WIDTH2 + y2 * WIDTH);
}

function image_grid(img, x, y) {
    image(img, x * WIDTH, y * WIDTH, WIDTH, WIDTH);
}

function draw_world(step) {
    //reset frame
    background(background_color);
    image_grid(buzz, goal[1], goal[0]);
    
    strokeWeight(10);
    if (step > 0) {
        //draw path to current point
        for (var i = 1; i < step; i++) {
            stroke(66, 134, 244);
            line_grid(path[i - 1][1], path[i - 1][0], path[i][1], path[i][0]);
        }
        line_grid(path[step - 1][1], path[step - 1][0], current[1], current[0]);
    }
    strokeWeight(1);

    //draw world obstacles
    fill(0);
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
}

function draw_bzm(step) {
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

function draw_frontier(step) {
    var point = frontier_points[step];
    rect(point[1] * WIDTH, point[0] * WIDTH, WIDTH, WIDTH);
}

function preload() {
    bzm = loadImage('js/buzzmobile.png');
    buzz = loadImage('js/buzz.png');
    bus = loadImage('js/bus.jpeg');
    crowd = loadImage('js/crowd.jpeg');
}

function setup() {
    createCanvas(WIDTH * DIM, WIDTH * DIM);
    background(background_color);
    frameRate(30);
    draw_world(0);
    fill('#717e93');
}

function draw() {
    if (ANIMATION_STATE == 0) {
        if (frameCount % 2 == 0) {
            //draw world state from step 0
            //animate frontier rollout
            draw_frontier(step);
            step += 1;
        }
        if (step == frontier_points.length) {
            step = 1;
            ANIMATION_STATE = 1;
        }
    } else if (ANIMATION_STATE == 1) {
        if (frameCount % tick_rate == 0 && step < path.length) {
            current = path[step].slice();
            step += 1;
        }

        if (step < path.length) {
            draw_world(step);
            draw_bzm(step);
        }
    }
}

