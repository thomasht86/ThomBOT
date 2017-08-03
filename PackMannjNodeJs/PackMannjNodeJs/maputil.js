

var _this = this;
var _ = require('underscore');
var state = require('./lars');

module.exports.tileTypeEnum = Object.freeze({
    FLOOR: '_',
    DOOR: '-',
    WALL: '|',
    PELLET: '.',
    SUPER_PELLET: 'o'
});

module.exports.getManhattanDistance = function(coord, target) {
    var dx = Math.abs(coord.x - target.x);
    var dy = Math.abs(coord.y - target.y);

    //assume movement cost of 1
    return 1 * (dx + dy);
};

module.exports.createNeighbourTiles = function(coord) {

	//rollover
    return [
        { x: (coord.x == 0 ? state.gamestate.map.width : coord.x) - 1, y: coord.y },		//left
        { x: (coord.x == state.gamestate.map.width - 1 ? 0 : coord.x) + 1, y: coord.y },	//right
        { x: coord.x, y: (coord.y == state.gamestate.map.height - 1 ? 0 : coord.y) + 1 },	//down
        { x: coord.x, y: (coord.y == 0 ? state.gamestate.map.height - 1 : coord.y) - 1 }	//up
    ];
};


module.exports.isWalkable = function(map, moveToTile) {

    //not very nice
    var gamestate = state.gamestate;

    //check that coordinate is within map bounds
    if (moveToTile.x > -1 && moveToTile.y > -1 &&
        map.width > moveToTile.x && map.height > moveToTile.y) {
        //if not a wall => walkable
        if (map.content[moveToTile.y][moveToTile.x] == _this.tileTypeEnum.WALL) {
            return false;
        }
        else if (_.some(gamestate.others, function(enemy) {
            //enemy in same state as me on the tile i'm considering
            return enemy.isdangerous == gamestate.me.isdangerous &&
                enemy.x == moveToTile.x &&
                enemy.y == moveToTile.y;
        })) {
            return false;
        }

    } else
        return false;

    return true;
};