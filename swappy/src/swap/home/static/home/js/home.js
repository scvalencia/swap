var app = angular.module('home', []);

app.controller('MostActiveController', function(){
    
});

app.controller('NewsController', ['$http', function($http){
    var news = this;
    news.term = 'apple';
    news.url = '/news?q=' + news.term;
    news.results = [];
    $http.get(news.url).
        success(function(data, status, headers, config) {
            news.results = data;
            window.alert(news.url);
        }).
        error(function(data, status, headers, config) {
            news.results = [];
            window.alert('BAD');
        });
}]);