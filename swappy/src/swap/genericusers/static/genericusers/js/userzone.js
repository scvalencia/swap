var app = angular.module('userzone', []);

app.controller('LoginController', function(){
	this.login = {};

	this.submit = function() {
		$http.post('/userzone', this.login).
        success(function(data, status, headers, config) {
            window.alert('YES');
        }).
        error(function(data, status, headers, config) {
            window.alert('BAD');
        });
	}
});

app.controller('SignupController', function(){
	this.signup = {
		userType: '1',
	};
});