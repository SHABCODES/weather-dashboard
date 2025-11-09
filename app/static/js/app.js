// SIMPLE WORKING WEATHER APP
console.log('Weather app loading...');

document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded - setting up events');
    
    // Main search form
    document.getElementById('weatherForm').addEventListener('submit', function(e) {
        e.preventDefault();
        const city = document.getElementById('cityInput').value;
        console.log('Searching for:', city);
        getWeather(city);
    });
    
    // Quick city buttons
    document.querySelectorAll('.quick-city').forEach(button => {
        button.addEventListener('click', function() {
            const city = this.getAttribute('data-city');
            document.getElementById('cityInput').value = city;
            getWeather(city);
        });
    });
    
    console.log('All event listeners setup complete');
});

function getWeather(city) {
    console.log('Fetching weather for:', city);
    
    // Show loading
    document.getElementById('weatherResults').innerHTML = `
        <div class="text-center py-4">
            <div class="spinner-border text-primary"></div>
            <p class="mt-2">Loading weather for ${city}...</p>
        </div>
    `;
    
    // Simple fetch request
    fetch(`/api/v1/weather/current?city=${encodeURIComponent(city)}`)
        .then(response => {
            if (!response.ok) throw new Error('API error');
            return response.json();
        })
        .then(data => {
            console.log('Weather data:', data);
            displayWeather(data);
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('weatherResults').innerHTML = `
                <div class="alert alert-danger mt-4">
                    Error: ${error.message}
                </div>
            `;
        });
}

function displayWeather(weather) {
    const html = `
        <div class="card mt-4">
            <div class="card-body">
                <h3>${weather.city}, ${weather.country}</h3>
                <div style="font-size: 2rem; color: blue;">${Math.round(weather.temperature)}°C</div>
                <p>${weather.description}</p>
                <div class="row text-center">
                    <div class="col-3"><strong>${weather.humidity}%</strong><br><small>Humidity</small></div>
                    <div class="col-3"><strong>${weather.wind_speed} m/s</strong><br><small>Wind</small></div>
                    <div class="col-3"><strong>${weather.pressure} hPa</strong><br><small>Pressure</small></div>
                    <div class="col-3"><strong>${Math.round(weather.feels_like)}°C</strong><br><small>Feels Like</small></div>
                </div>
            </div>
        </div>
    `;
    document.getElementById('weatherResults').innerHTML = html;
}

// Global function for summary button
window.getWeatherSummary = function() {
    const cities = document.getElementById('citiesInput').value;
    alert('Summary would search for: ' + cities);
}