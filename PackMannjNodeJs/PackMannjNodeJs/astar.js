
var _ = require('underscore');
var mapUtil = require('./maputil');

var Astar = function Astar() {

    const defaultMoveCost = 10;

    function heuristic(arg, target) {

        //handle standing on the edge, and taking a shortcut to the other side
        if (Math.abs(arg.me.x - target.x) == arg.map.width - 1 ||  //left-right shortcut
            Math.abs(arg.me.y - target.y) == arg.map.height - 1) {
            return defaultMoveCost;
        }

        return mapUtil.getManhattanDistance(arg.me, target);
    };


    function moveCost(arg, movingTo) {
        //check if tile is within "safe" distance from dangerous enemies
        //todo: consider remaining lethality ticks for both me and enemies
        if (!arg.me.isdangerous) {

            var dangerous = _.where(arg.others, { isdangerous: true });
            for (var i = 0; i < dangerous.length; i++) {
                var enemy = dangerous[i];

                //todo: manhattan er ganske sloppy, og bryr seg ikke om vegger ol.

                var distance = mapUtil.getManhattanDistance(arg.me, enemy);
                if (distance <= 2) { //too close for comfort
                    console.log('panic!');
                    return 1000 / distance; // avoid tile plz (weighted by proximity so as to enable retreat)
                }
            }
        }

        
        try {
            var type = arg.map.content[movingTo.y][movingTo.x];
            switch (type) {
                case mapUtil.tileTypeEnum.PELLET:
                case mapUtil.tileTypeEnum.SUPER_PELLET:
                    return 0;
            }
        } catch (e) {
            console.log(`moveCost: failed to determine movement cost for (${movingTo.x}, ${movingTo.y})`);
        }

        return defaultMoveCost; //default: floor, door
        
    }

    return {


        /*
 
        arg = {
            me: {}
            others: [],
            target: {},
            map: {}
        }
        */
        getNextTile: function(arg) {

            if (arg === undefined || arg === null) {
                console.log('getNextTile: arg cannot be null or undefined');
                return;
            } else if (arg.target === undefined || arg.target === null) {
                console.log('getNextTile: target cannot be null or undefined');
                return;
            }

            var coordStart = arg.me;
            var target = arg.target;
            var map = arg.map;

            //console.log(`getNextTile: find next move from (${coordStart.x}, ${coordStart.y}) to (${target.x}, ${target.y})`);

            coordStart.cost = 0;

            var frontier = [coordStart];
            var closed = [];

            var current = {};

            while (frontier.length > 0) {

                var lowestValue = frontier[0].cost;
                var ties = [frontier[0]];
                //find the x tiles with the lowest cost
                for (var i = 1; i < frontier.length; i++) {
                    if (frontier[i].cost === lowestValue)
                        ties.push(frontier[i]);
                    else
                        break;
                }

                if (ties.length === 1) {
                    current = frontier.shift();
                } else {
                    //select randomly among tiles if more than one with lowest cost
                    var rndIndex = Math.floor(Math.random() * ties.length);
                    current = frontier.splice(rndIndex, 1)[0];
                }

                if (current.x === target.x && current.y === target.y)
                    break;

                closed.push(current);


                mapUtil
                    //process neighbours
                    .createNeighbourTiles(current)
                    //check all neighbours that are not already processed
                    //must also be within map bounds and walkable
                    .filter(function(neighbour) {
                        return _.findWhere(closed, { x: neighbour.x, y: neighbour.y }) === undefined
                            && mapUtil.isWalkable(map, neighbour);
                    })
                    .forEach(function(neighbour) {
                        //total cost of moving to neighbour from starting point
                        //f(n) = g(n) + h(n)
                        var f = (current.cost + moveCost(arg, neighbour)) + heuristic(arg, neighbour);

                        var existingIndex = frontier.findIndex(function(elem) {
                            return elem.x === neighbour.x && elem.y === neighbour.y;
                        });

                        if (existingIndex > -1) {
                            if (frontier[existingIndex].cost > f) {
                                frontier[existingIndex].cost = f
                                frontier[existingIndex].parent = current;
                            }
                        } else {
                            neighbour.cost = f;
                            neighbour.parent = current;
                            frontier.push(neighbour);
                        }
                    });

                frontier.sort(function(a, b) { return a.cost - b.cost; });

            }

            var moveToTile;
            if (current.x === target.x && current.y === target.y) {
                while (current !== undefined && current.parent !== undefined) {
                    moveToTile = current;
                    current = current.parent;
                }

                //if (moveToTile !== undefined)
                //    console.log(`getNextTile: next tile (${moveToTile.x}, ${moveToTile.y})`)
            }

            return moveToTile;
        }
    }
};

module.exports = Astar;