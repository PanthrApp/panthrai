function populate(text) {
  document.getElementById('message').value = text;
  document.getElementById('messagesender').click();
}

document.getElementById('message').onkeydown = function(e){
  if(e.keyCode == 13 && !e.shiftKey){
    onsend();
  }
};

function onsend() {
  document.getElementById("messagesender").disabled = true;
  document.getElementById("message").disabled = true;
  document.getElementById('explore').classList.add('inactive');
  document.getElementById('loading').classList.remove('inactive');
  var message = document.getElementById('message').value;
  document.getElementById('message').value = "";
  var newelement = document.createElement('div');
  newelement.classList.add("message");
  newelement.classList.add("usermessage");
  var paragraph = document.createElement('p');
  paragraph.innerHTML = message;
  newelement.appendChild(paragraph);
  document.getElementsByClassName('messagesentarea')[0].appendChild(newelement);
  if (message.length > 0) {
    var http = new XMLHttpRequest();
    var url = '/api/message';
    var params = `threadid=${window.location.pathname.split('/')[2]}&message=${message}`;
    http.open('POST', url, true);
    http.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    var newelement = document.createElement('div');
    newelement.classList.add("message");
    newelement.classList.add("assistantmessage");
    http.onreadystatechange = function() {
      if(http.readyState == 4 && http.status == 200) {
        var converter = new showdown.Converter(),
        text = http.responseText,
        html = converter.makeHtml(text);
        var paragraph = document.createElement('p');
        paragraph.innerHTML = html;
        newelement.appendChild(paragraph);
        document.getElementsByClassName('messagesentarea')[0].appendChild(newelement);
        document.getElementById("messagesender").disabled = false;
        document.getElementById("message").disabled = false;
        document.getElementById('message').select();
        document.getElementById('loading').classList.add('inactive');
        document.getElementById('explore').classList.remove('inactive');
      } else if (http.readyState == 4 && http.status == 500) {
        newelement.class = "message";
        var paragraph = document.createElement('p');
        paragraph.innerHTML = "There was a problem sending your message. Please <a href='/thread'>create a new thread</a> and try again. If the problem persists, <a href='/contact'>contact us</a>.";
        newelement.appendChild(paragraph);
        document.getElementsByClassName('messagesentarea')[0].appendChild(newelement);
        document.getElementById("messagesender").disabled = false;
        document.getElementById("message").disabled = false;
        document.getElementById('message').select();
        document.getElementById('loading').classList.add('inactive');
        document.getElementById('explore').classList.remove('inactive');
      } else if (http.readyState == 4) {
        newelement.class = "message";
        var paragraph = document.createElement('p');
        paragraph.innerHTML = "The request timed out. Please refresh the page. If the problem persists, contact us.";
        newelement.appendChild(paragraph);
        document.getElementsByClassName('messagesentarea')[0].appendChild(newelement);
        document.getElementById("messagesender").disabled = false;
        document.getElementById("message").disabled = false;
        document.getElementById('message').select();
        document.getElementById('loading').classList.add('inactive');
        document.getElementById('explore').classList.remove('inactive');
      }
    }
    http.send(params);
  }
}

  function loadmessages() {
    var http = new XMLHttpRequest();
    var url = '/api/getmessages';
    var params = `threadid=${window.location.pathname.split('/')[2]}`;
    http.open('POST', url, true);
    http.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    http.onreadystatechange = function() {
        if(http.readyState == 4 && http.status == 200) {
          var messages = JSON.parse(http.responseText)['messages'];
          for (var i = 0; i < messages.length; i++) {
            if (messages[i].role == "assistant") {
              var converter = new showdown.Converter(),
              text = messages[i].content,
              html = converter.makeHtml(text);
              var newelement = document.createElement('div');
              newelement.classList.add("message");
              newelement.classList.add("assistantmessage");
              var paragraph = document.createElement('p');
              paragraph.innerHTML = html;
              newelement.appendChild(paragraph);
              document.getElementsByClassName('messagesentarea')[0].appendChild(newelement);
            } else {
              var newelement = document.createElement('div');
              newelement.classList.add("message");
              newelement.classList.add("usermessage");
              var paragraph = document.createElement('p');
              paragraph.innerHTML = messages[i].content;
              newelement.appendChild(paragraph);
              document.getElementsByClassName('messagesentarea')[0].appendChild(newelement);
            }
          }
        }
    }
    http.send(params);
  }
  