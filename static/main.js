


window.onload=function () {
    var objDiv = document.getElementById("bottom-up");
    objDiv.scrollTop = objDiv.scrollHeight;
}


document.addEventListener('DOMContentLoaded', () => {
   // Connect to websocket
   var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

   // When connected, configure buttons
   socket.on('connect', () => {

       // Each button should emit a "submit vote" event
       document.querySelectorAll('form').forEach(form => {
           form.onsubmit = () => {
                var today = new Date();
               const channel = form.dataset.channel;
               const info = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds()
                            + " # " + form.querySelector('#sendtext').value;
               socket.emit('submit text', {'channel': channel, 'info': info});
           };
       });
   });

   // When a new vote is announced, add to the unordered list
   socket.on('channel text', data => {
       document.querySelector('.list-group-mine').innerHTML += '<li class="list-group-item">' + data["info"] + 
                                                                 '</li>'
       var objDiv = document.getElementById("bottom-up");
       objDiv.scrollTop = objDiv.scrollHeight;
   });

});



