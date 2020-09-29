window.onload=function () {
    var objDiv = document.getElementById("bottom-up");
    objDiv.scrollTop = objDiv.scrollHeight;
}


document.addEventListener('DOMContentLoaded', () => {
   // Connect to websocket
   var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    document.querySelector("#sidebar").querySelectorAll('a').forEach(a => {
        a.onclick = () => {
            localStorage.setItem('channel', a.innerText.substring(1));
        }
    });

    //TODO: Remember channel after browser exit
    window.onload = function WindowLoad(event) {
        current_channel = localStorage.getItem('channel');
        if(current_channel == null){
            //localStorage.setItem('channel', 'General');
        }
        else{
            //window.location.href += current_channel;
        }
    }


   // When connected, configure form
   socket.on('connect', () => {
       // Form should emit a "submit vote" event
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

   // When a new message is sent, add to the unordered list
   socket.on('channel text', data => {
       document.querySelector('.list-group-mine').innerHTML += '<li class="list-group-item">' + data["info"] + 
                                                                 '</li>'
       var objDiv = document.getElementById("bottom-up");
       objDiv.scrollTop = objDiv.scrollHeight;
   });

});



