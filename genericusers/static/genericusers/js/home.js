(function(){
	var app = angular.module('home', []);

	app.controller('LoginController', function(){
		this.login = {};
	});

	app.controller('SignupController', function(){
		this.signup = {
			userType: '1',
		};
	});

	app.directive('productTitle', function(){
		return {
			restrict: 'E',
			templateUrl: 'product-title.html'
		};
	});
})();