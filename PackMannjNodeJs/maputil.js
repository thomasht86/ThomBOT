

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


module.exports.discoverShortcuts = function (map) {
	var _shortcuts = [];

	function bfs(node, target) {
		var queue = [node];
		var visited = [node];

		while (queue.length !== 0) {
			var current = queue.pop();

			//console.log(`(${current.x}, ${current.y}) -> (${target.x}, ${target.y})`)
			if (current.x == target.x && current.y == target.y)
				return true;

			if (map.content[current.y][current.x] !== _this.tileTypeEnum.WALL) {
				var neighbours = _this.createNeighbourTiles(current);
				for (var i = 0; i < neighbours.length; i++) {
					if (_.findWhere(visited, { x: neighbours[i].x, y: neighbours[i].y }) == undefined) {
						visited.push(neighbours[i]);
						queue.push(neighbours[i]);
					}
				}
			}
		}

		return false;
	};


	for (var y = 0; y < map.content.length; y++) {

		for (var x = 0; x < map.content[y].length; x++) {
			if (y == 0 || y == map.content.length - 1 || x == 0 || x == map.content[y].length - 1) {
				if (map.content[y][x] !== _this.tileTypeEnum.WALL) {
					var isReachable = bfs({ x: x, y: y }, state.gamestate.me);
					if (isReachable) {
						var shortcut = {
							entry: {
								x: x,
								y: y
							}
						};

						var exit = shortcut.entry;

						if (x == 0)
							exit.x = map.content[y].length - 1;
						else if (x == map.content[y].length - 1)
							exit.x = 0;

						if (y == 0)
							exit.y = map.content.length - 1;
						else if (y == map.content.length - 1)
							exit.y = 0;

						shortcut.exit = exit;

						_shortcuts.push(shortcut);
					}


				};
			};
		};
	};

	state.gamestate.shortcuts = _shortcuts;

};

module.exports.getManhattanDistance = function (coord, target) {


	function diff(a, b) {
		var dx = Math.abs(a.x - b.x);
		var dy = Math.abs(a.y - b.y);

		//assume movement cost of 1
		return 1 * (dx + dy);
	}

	var shortestPath = diff(coord, target);

	for (var i = 0; i < state.gamestate.shortcuts.length; i++) {

		var estimate = diff(coord, state.gamestate.shortcuts[i].entry) + diff(state.gamestate.shortcuts[i].exit, target);
		//distance from current to shortcut + other side of shortcut to target
		if (estimate < shortestPath)
			shortestPath = estimate;
	}

	return shortestPath;
};

module.exports.createNeighbourTiles = function (coord) {

	//rollover
	return [
		{ x: (coord.x == 0 ? state.gamestate.map.width : coord.x) - 1, y: coord.y },		//left
		{ x: (coord.x == state.gamestate.map.width - 1 ? 0 : coord.x) + 1, y: coord.y },	//right
		{ x: coord.x, y: (coord.y == state.gamestate.map.height - 1 ? 0 : coord.y) + 1 },	//down
		{ x: coord.x, y: (coord.y == 0 ? state.gamestate.map.height - 1 : coord.y) - 1 }	//up
	];
};


module.exports.isWalkable = function (map, moveToTile) {

	//not very nice
	var gamestate = state.gamestate;

	//check that coordinate is within map bounds
	if (moveToTile.x > -1 && moveToTile.y > -1 &&
		map.width > moveToTile.x && map.height > moveToTile.y) {
		//if not a wall => walkable
		if (map.content[moveToTile.y][moveToTile.x] == _this.tileTypeEnum.WALL) {
			return false;
		}
		else if (_.some(gamestate.others, function (enemy) {
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