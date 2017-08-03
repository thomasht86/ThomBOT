
var net = require('net'),
	eventEmitter = require('events'),
	util = require('util');


var Client = function (host, port, botName) {

	var _this = this;

	_this._client = new net.Socket();

	_this._client.connect(port, host, function () {
		_this._client.write('NAME ' + botName);
	});

	_this._client.on('data', function (buffer) {

		try {
			var data = JSON.parse(buffer.toString('utf8'));

			switch (data['messagetype']) {
				case 'welcome':
				case 'stateupdate':
				case 'dead':
				case 'endofround':
				case 'startofround':
					_this.emit(data['messagetype'], data);
					break;
				default:
					console.log('Unrecognized message type: ' + data['messagetype']);
			}
		} catch (e) {
			console.log(`unable to parse data: ${e.message}`);
		}
		
	});
};

Client.prototype.sendString = function (str) {
	this._client.write(str);
};

util.inherits(Client, eventEmitter);

module.exports = Client;

