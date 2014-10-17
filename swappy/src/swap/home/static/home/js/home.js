(function(){
    var app = angular.module('home', []);

    app.controller('MostActiveController', function(){
        
    });

    app.controller('NewsController', ['$http', function($http){
        var news = this;
        news.term = 'wall street';
        news.results = [];
        $http.get('/news/q=' + news.term).
            success(function(data, status, headers, config) {
                news.results = data;
                window.alert(data)
            }).
            error(function(data, status, headers, config) {
                news.results = [];
                window.alert('BAD');
            });
    }]);
})();