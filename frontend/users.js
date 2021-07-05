stdout = null;
stderr = null;
setTimeout(function(){
  stdout = document.getElementById("stdout_send");
  stderr = document.getElementById("stderr_send");
}, 300);

function send_request(method, params, cb) {
  // Sends jRPC request, callbacks result
  const j = {"jsonrpc": "2.0",
             "method": method,
             "params": params,
             "id": 0}
  const options = {
    method: 'POST',
    body: JSON.stringify(j),
    headers: {
      'Content-Type': 'application/json'
    }
  }

  fetch('/v0.1', options)
    .then(res => res.json())
    .then(res => cb(JSON.stringify(res["result"], null, 2),
                    JSON.stringify(res["error"], null, 2)))
    .catch(err => cb(err));
}


function get_users(){
  // Lists all users in db
  send_request("manage.users.list", {}, function(res) {
    if (res == ""){
      res = "empty response result"
    }
    document.getElementById("stdout_users").value = res;
  });
}


function send_and_display_request(method, params){
  if (method.length == 0){
    stdout.value = "Method length should be > 0";
    return;
  }

  if (params.length == 0){
    params = "{}";
  }

  function callback_show(res, err){
    if (!res){
      stdout.value = "empty"
    }else{
      stdout.value = res
    }

    if (!err){
      stderr.value = "empty"
    }else{
      stderr.value = err
    }
  }
  send_request(method, params, callback_show);
}


function send_custom_request() {
  // Sends request with method and params in input fields
  method_name = document.getElementById("stdin_send_method").value;
  method_params = document.getElementById("stdin_send_params").value;
  send_and_display_request(method_name, method_params);
}
