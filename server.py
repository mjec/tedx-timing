from bottle import route, run, template, redirect, post
import time

start_time = time.time()

@route('/time')
def curtime():
    return template('{{time}}', time=int(time.time() - start_time))

@route('/')
def index():
    return template('''
<html>
  <head>
    <style type="text/css">
      #t { font-size: 30em; font-family: sans-serif; font-weight: bold; }
      .close { color: #f00; }
      .over { background-color: #ff0; color: #f00; }
    </style>
    <script type="text/javascript">
      time = {{time}};
      function tmr() {
        time++;
        document.getElementById("t").innerHTML =
          (Math.floor(time/60) < 10 ? "0" : "") + Math.floor(time/60).toString()
          + ":"
          + ((time % 60) < 10 ? "0" : "") + (time % 60).toString();
        if (time > 60 * 16) { document.getElementById("t").className = "close"; }
        if (time > 60 * 18) { document.getElementById("t").className = "over"; }
        if (time < 60 * 16) { document.getElementById("t").className = ""; }
      }
      function updatetime() {
        var xhr = new XMLHttpRequest();
        xhr.open("GET", "/time", true);
        xhr.send();
        xhr.onreadystatechange=function() {
          if (xhr.readyState==4 && xhr.status==200) {
            _t = parseInt(xhr.responseText);
            if (Math.abs(_t - time) > 2) { time = _t; }
          }
        }
      }
      var counter = setInterval(tmr, 1000);
      var updateTime = setInterval(updatetime, 2000);
    </script>
  </head>
  <body>
    <p class="" id="t">00:00</p>
    <form action="/reset" method="post">
    <p><input type="submit" value="Reset time"></p>
    </form>
  </body>
</html>''', time=int(time.time() - start_time))

@post('/reset')
def reset():
    global start_time
    start_time = int(time.time())
    redirect('/')

run(host='192.168.X.X')
