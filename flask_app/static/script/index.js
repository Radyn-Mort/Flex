let KEY = '888e1c1817c4948d34d37f0ffd3e29ea'
let lat = 47.7511
let lon = -120.7401
const weather = document.querySelector('#weather')
fetch(`https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${lon}&appid=${KEY}`)
    .then(response => response.json() )
    .then(coderData => {
        // console.log(coderData)
        weather.innerHTML=`
        <h4 class="olive-pale">Temp</h4>
        <p>${Math.round((coderData.main.temp-273.15)*1.8+32)} F</p>
        <h4 class="olive-pale" >Humidity</h4>
        <p>${coderData.main.humidity}</p>
        <h4 class="olive-pale" >Min</h4>
        <p>${Math.round((coderData.main.temp_min-273.15)*1.8+32)} F</p>
        <h4 class="olive-pale" >Max</h4>
        <p>${Math.round((coderData.main.temp_max-273.15)*1.8+32)} F</p>
        `
    } )
    .catch(err => console.log(err) )