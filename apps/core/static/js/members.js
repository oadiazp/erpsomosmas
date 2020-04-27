$(function () {
    var map = L.map('continents-container', {
        zoomAnimation: false
    });

    L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1Ijoib2FkaWF6IiwiYSI6ImNrOWg5bGdxdjA5cDMzZW54azgxZTRicWcifQ.cs5abjLhdy4UHCgw1yCNQA', {
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
        maxZoom: 18,
        id: 'mapbox/streets-v11',
        tileSize: 512,
        zoomOffset: -1,
        accessToken: 'your.mapbox.access.token'
    }).addTo(map);

    map.fitWorld().zoomIn();

    map.on('resize', function (e) {
        map.fitWorld({reset: true}).zoomIn();
    });
});