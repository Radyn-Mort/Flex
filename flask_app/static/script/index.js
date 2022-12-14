let KEY =
let lat = 47.7511
let lon = -120.7401
const weather = document.querySelector('#weather')
fetch(`https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${lon}&appid=${KEY}`)
    .then(response => response.json() )
    .then(coderData => {
        // console.log(coderData)
        weather.innerHTML=`
        <h4 class="olive-pale align-text">Temp</h4>
        <p class="align-text text-white">${Math.round((coderData.main.temp-273.15)*1.8+32)} F</p>
        <h4 class="olive-pale align-text" >Humidity</h4>
        <p class="align-text text-white">${coderData.main.humidity}</p>
        <h4 class="olive-pale align-text" >Min</h4>
        <p class="align-text text-blue">${Math.round((coderData.main.temp_min-273.15)*1.8+32)} F</p>
        <h4 class="olive-pale align-text" >Max</h4>
        <p class="align-text text-red">${Math.round((coderData.main.temp_max-273.15)*1.8+32)} F</p>
        `
    } )
    .catch(err => console.log(err) )
