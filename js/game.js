function get_json(url) {
    var req = new XMLHttpRequest();
    req.open("GET", url, false);
    req.send();
    return JSON.parse(req.responseText);
}

function draw_state(state) {
    for (var r = 0; r < 3; r++) {
        for (var c = 0; c < 3; c++) {
            if (state[r][c] != 0) {
                if (state[r][c] == 1) {
                    fill(255, 0, 0); 
                } else {
                    fill(0, 0, 255); 
                }
                ellipse(100 + 200 * c, 100 + 200 * r, 100);
            }
        }
    }
}

function setup() {
    createCanvas(600, 600);
    background('#DDDDDD');
    draw_state(get_json('/state'));
}

//function draw() {

//}
function mouseClicked() {
    draw_state(get_json('/next'));
}

