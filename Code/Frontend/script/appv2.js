"use strict";

const lanIP = `${window.location.hostname}:5000`;
const socket = io(`${lanIP}`);

// Data page

const listenToSocketData = function () {
  socket.on("connected", function () {
    console.log("connected to socket webserver");
  });

  socket.on("B2F_MPU_read", function (data) {
    console.log("MPU values have been read");
    console.log(`Current acceleration is ${data.data}`);
    const acc = document.querySelector(".js-acc");
    acc.innerHTML = `${data.data} g`;
  });

  socket.on("B2F_MPU_read_e", function (data) {
    console.log("Possible MPU disconnect, check hardware");
    console.log(`Current acceleration is ${data.data}`);
    const acc = document.querySelector(".js-acc");
    acc.innerHTML = `${data.data} g`;
  });
  socket.on("B2F_temp_read", function (data) {
    console.log("Temperature has been read");
    console.log(`Current temperature is ${data.data}`);
    const temp = document.querySelector(".js-temp");
    temp.innerHTML = `${data.data} °C`;
  });
  socket.on("B2F_temp_read_e", function (data) {
    console.log("Possible temperature sensor disconnect, check hardware");
    console.log(`Current temperature is ${data.data}`);
    const temp = document.querySelector(".js-temp");
    temp.innerHTML = `${data.data} °C`;
  });
  socket.on("B2F_ldr_read", function (data) {
    console.log("LDR values have been read");
    console.log(`Current light intensity is ${data.data}`);
    const ldr = document.querySelector(".js-light");
    ldr.innerHTML = `${data.data} %`;
  });
  socket.on("B2F_ldr_read_e", function (data) {
    console.log("Possible LDR disconnect, check hardware");
    console.log(`Current light intensity is ${data.data}`);
    const ldr = document.querySelector(".js-light");
    ldr.innerHTML = `${data.data} %`;
  });
  socket.on("B2F_DATA_REQUEST", function(data){
    console.log("Request answered");
    console.log(data);
    const table = document.querySelector(".js-table-data");
    let result = ``;
    for(let i of data){
      result += `<div class="o-layout 
      o-layout--justify-center
      o-layout--align-center
      c-table-border">
        <div class="o-layout o-layout--column o-layout--align-center o-layout--justify-center o-layout__item u-1-of-4-bp2">
        <h3 class="o-layout__item u-1-of-2-bp2 c-label">Time</h3>
        <p class=" o-layout__item u-1-of-2-bp2">${i.date}</p>
        </div>
        <div class="o-layout o-layout--column o-layout--align-center o-layout--justify-center o-layout__item u-1-of-4-bp2">
        <h3 class="o-layout__item u-1-of-2-bp2 c-label">Acceleration</h3>
        <p class="o-layout__item u-1-of-2-bp2">${i.acc} g</p>
        </div>
        <div class="o-layout o-layout--column o-layout--align-center o-layout--justify-center o-layout__item u-1-of-4-bp2">
        <h3 class="o-layout__item u-1-of-2-bp2 c-label">Temperature</h3>
        <p class="o-layout__item u-1-of-2-bp2">${i.temp} °C</p>
        </div>
        <div class="o-layout o-layout--column o-layout--align-center o-layout--justify-center o-layout__item u-1-of-4-bp2">
          <h3 class="o-layout__item u-1-of-2-bp2 c-label">Light</h3>
          <p class="o-layout__item u-1-of-2-bp2">${i.ldr} %</p>
        </div>
      </div>`
    }
    table.innerHTML = result;
  });
};

const submitFilters = function(){
  let jsonobject = {
    amount: document.querySelector(".js-amount").value,
    startdate: document.querySelector(".js-start").value,
    enddate: document.querySelector(".js-end").value
  };
  console.log(jsonobject);
  socket.emit('F2B_data', jsonobject);
  console.log("Data request complete")
};

const dataEvent = function() {
  let item = document.querySelector(".js-btn-data");
  item.addEventListener("click", function(){
    submitFilters();
  });
  console.log("Events loaded")
};

// Controls page

const submitLights = function () {
  let jsonobject = {
    red: document.querySelector(".js-red").value,
    green: document.querySelector(".js-green").value,
    blue: document.querySelector(".js-blue").value
  };
  console.log(jsonobject);
  socket.emit('F2B_lights', jsonobject);
};

const submitIntensity = function () {
  let jsonobject = {
    intensity: document.querySelector(".js-intensity").value
  };
  console.log(jsonobject);
  socket.emit('F2B_intensity', jsonobject);
};

const submitAlarm = function () {
  let jsonobject = {
    alarm: (document.querySelector(".js-alarm").value * 10)
  };
  console.log(jsonobject);
  socket.emit('F2B_alarm', jsonobject);
};

const submitOverride = function (manual) {
  let jsonobject = {
    override: manual
  };
  console.log(jsonobject);
  socket.emit('F2B_override', jsonobject);
};

const submitPower = function(){
  socket.emit('F2B_shutdown');
}


const controlEvent = function() {
  let lightbtn = document.querySelector(".js-btn-light");
  lightbtn.addEventListener("click", function(){
    submitLights();
  });
  let intbtn = document.querySelector(".js-btn-percent");
  intbtn.addEventListener("click", function(){
    submitIntensity();
  });
  let manualbtn = document.querySelector(".js-btn-manual");
  manualbtn.addEventListener("click", function(){
    submitOverride(1);
  });
  let autobtn = document.querySelector(".js-btn-auto");
  autobtn.addEventListener("click", function(){
    submitOverride(0);
  });
  let alarmbtn = document.querySelector(".js-btn-alarm");
  alarmbtn.addEventListener("click", function(){
    submitAlarm();
  });
  let powerbtn = document.querySelector(".js-btn-power");
  powerbtn.addEventListener("click", function(){
    submitPower();
  });
  console.log("Events loaded");
};

const listenToSocketControl = function () {
  socket.on("connected", function () {
    console.log("connected to socket webserver");
  });
  socket.on('B2F_light_status', function(data){
    let red = document.querySelector(".js-red-val");
    let green = document.querySelector(".js-green-val");
    let blue = document.querySelector(".js-blue-val");
    let percent = document.querySelector(".js-auto-val");
    red.innerHTML = data.red;
    green.innerHTML = data.green;
    blue.innerHTML = data.blue;
    percent.innerHTML = data.percent;
  });
}

// Init

document.addEventListener("DOMContentLoaded", function () {
  console.info("DOM loaded");
  if(document.querySelector(".js-controls")){
    controlEvent();
    listenToSocketControl();
  }
  else if(document.querySelector(".js-data")){
    dataEvent();
    listenToSocketData();
  }
});

