(function(){
	var app = angular.module('userzone', []);

	app.controller('LoginController', function(){
		this.login = {};
	});

	app.controller('SignupController', function(){
		this.signup = {
			userType: '1',
		};
	});
})();