'use strict';

//self-invoking function - avoid polluting global namespace
(function _lars() {

	var _commander = require('commander');

	var _client = require('./client.js');
	var _astar = require('./astar.js');
	var _navigator = require('./navigator');

	_commander
		.version('0.0.1')
		.usage('[options]')
		.option('-s, --server [ip:port]', 'Server address (ip:port)', '127.0.0.1:54321')
		.option('-n, --nick [name]', 'Bot nick', 'L.A.R.S.')
		.parse(process.argv);

	var address = _commander.server.split(':');
	if (address.length != 2)
	{
		console.log('invalid argument: server. must be on the form adress:port (e.g 127:0.0.1:54321)');
		return;
	}

	var client = new _client(address[0], address[1], _commander.nick);
	var astar = new _astar();
	var navigator = new _navigator();

	var currentTarget;

	//helper method used for both 'welcome' and 'stateupdate' events
	function sendNextMove() {

		//get the tile to move to using a*-algorithm
		var nextTile = astar.getNextTile(exports.gamestate);

		var nextMove;
		if (nextTile !== undefined)
		{
			//translate to move command (up, down, left, right)
			nextMove = navigator.translateToMoveCommand(exports.gamestate.me, nextTile);
		}
		else {
			console.log('sendNextMove: unable to determine next tile! choosing direction at random!');
            nextMove = navigator.getRandomValidMove(exports.gamestate.map, exports.gamestate.me);
		}

		client.sendString(nextMove);
	}

	client.on('welcome', function (data) {
		console.time('process welcome');
		navigator.updateTargets(data.map);

		var gamestate = {
			map: data.map,
			me: data.you,
			others: data.others
		};

		currentTarget = navigator.pickTarget(gamestate);
        gamestate.target = currentTarget;

        module.exports.gamestate = gamestate;

		sendNextMove();

		console.timeEnd('process welcome');
	});

	client.on('stateupdate', function (data) {
		console.time('process update');

        navigator.updateTargets(data.gamestate.map);

        module.exports.gamestate = {
            map: data.gamestate.map,
            me: data.gamestate.you,
            others: data.gamestate.others,
            target: currentTarget
        };;
		
        currentTarget = navigator.pickTarget(exports.gamestate);

		sendNextMove();

		console.timeEnd('process update');
    });


    client.on('dead', function() {
        console.log('RIP');
    });

})();