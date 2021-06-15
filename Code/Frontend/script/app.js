"use strict";

const lanIP = `${window.location.hostname}:5000`;
const socket = io(`${lanIP}`);




const listenToSocket = function () {
  socket.on("connected", function () {
    console.log("verbonden met socket webserver");
  });

    socket.on("B2F_MPU_read", function (data){
      console.log("MPU values have been read");
      console.log(`Current acceleration is ${data.data}`);
      const acc = document.querySelector(".js-acc");
      acc.innerHTML = data.data;
  });

};

document.addEventListener("DOMContentLoaded", function () {
  console.info("DOM geladen");
  listenToSocket();
  
});
