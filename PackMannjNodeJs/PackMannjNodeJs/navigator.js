
var _ = require('underscore');
var shuffle = require('shuffle-array');
var mapUtil = require('./maputil');

var Navigator = function Navigator() {

	var targets = {
		superPellets: [],
		pellets: []
	};
	
	return {

		updateTargets: function (map) {

			targets.superPellets = [];
			targets.pellets = [];

			map.content.forEach(function (row, rowIndex) {
				for (var i = 0; i < row.length; i++) {
					if (row[i] === mapUtil.tileTypeEnum.SUPER_PELLET) {
						targets.superPellets.push(
							{
								x: i,
								y: rowIndex
							}
						);
					}
					else if (row[i] === mapUtil.tileTypeEnum.PELLET) {
						targets.pellets.push(
							{
								x: i,
								y: rowIndex
							}
						);
					}
				}
			});
		},


		/*
		expects an object in the current form:
			arg = {
				me: {
					x: 0,
					y: 0,
					score: 0,
					isdangerous: false
				},
				others = [ {...} ], //objects similar to 'me'
				target = {
					x: 0,
					y: 0
				}
			}
		*/
		pickTarget: function (arg) {

			if (arg == null || arg == undefined) {
				console.log(`pickTarget: arg cannot be null or undefined`);
				return null;
			}

			try {
				/*
					update targets if:
						- none has been set, or
						- tracking enemies (they are probably moving every tick :), or
						- target has been reached
				*/

                var updateTarget = !arg.target ||
                    arg.me.isdangerous ||
                    mapUtil.getManhattanDistance(arg.target, arg.me) == 0 ||
                    arg.map.content[arg.target.y][arg.target.x] == mapUtil.tileTypeEnum.FLOOR;

				if (!updateTarget)
					return arg.target;

				//if I am dangerous and there are non-dangerous enemies
				//todo: refine: consider distance and remaining lethality of enemies
				if (arg.me.isdangerous && _.findWhere(arg.others, { isdangerous: false }) != undefined) {

					var closestNonDangerous;
					for (var i = 0; i < arg.others.length; i++) {
						var enemy = arg.others[i];
						if (closestNonDangerous == undefined || mapUtil.getManhattanDistance(arg.me, enemy) < closestNonDangerous) {
							closestNonDangerous = enemy;
						}
					}
					return closestNonDangerous;
				}

				else if (targets.superPellets.length > 0) {
					//pick the one closest to me
					//todo: consider enemies
					var closestSuperPellet;
					for (var i = 0; i < targets.superPellets.length; i++) {
						var pellet = targets.superPellets[i];
						if (closestSuperPellet == undefined || mapUtil.getManhattanDistance(arg.me, pellet) < closestSuperPellet) {
							closestSuperPellet = pellet;
						}
					}

					return closestSuperPellet;
				}
				else if (targets.pellets.length > 0) {
                    //return targets.pellets[Math.floor(Math.random() * targets.pellets.length)];

					var furthestPellet, distanceToFurthestPellet;
						
					for (var i = 0; i < targets.pellets.length; i++) {
						var pellet = targets.pellets[i];
						var distanceToPellet = mapUtil.getManhattanDistance(arg.me, pellet);
						if (!furthestPellet || distanceToPellet > distanceToFurthestPellet) {
							furthestPellet = pellet;
							distanceToFurthestPellet = distanceToPellet;
						}
					}

					return furthestPellet;
				}
			} catch (e) {
				console.log(`pickTarget: ${e}`);
			}
			
			return null;
		},

		translateToMoveCommand: function (currentTile, targetTile) {
			if (targetTile.x > currentTile.x)
				return 'RIGHT';
			else if (targetTile.x < currentTile.x)
				return 'LEFT';
			else if (targetTile.y > currentTile.y)
				return 'DOWN';
			else if (targetTile.y < currentTile.y)
				return 'UP';
		},

		getRandomValidMove: function (map, currentTile) {
			
			var walkableNeighbours = _.filter(
				mapUtil.createNeighbourTiles(currentTile), function (elem) {
					return mapUtil.isWalkable(map, elem);
				});

			var randomNeighbour = _.first(shuffle(walkableNeighbours));

			return this.translateToMoveCommand(currentTile, randomNeighbour);
		}
	}
};

module.exports = Navigator;