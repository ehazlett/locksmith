function flash(text, status){
  var msg = $("<div class='alert'></div>");
  msg.addClass('alert-'+status);
  msg.append("<a class='close' href='#' data-dismiss='alert'>x</a>");
  msg.append('<p>'+text+'</p>');
  $("#messages").append(msg);
  $("#messages").removeClass('hide');
  $(".alert").alert();
  $(".alert").delay(5000).fadeOut();
}

function redirect(url) {
    window.location.href = url;
    return false;
}

jQuery.fn.serializeObject = function() {
  var arrayData, objectData;
  arrayData = this.serializeArray();
  objectData = {};
  $.each(arrayData, function() {
    var value;
    if (this.value != null) {
      value = this.value;
    } else {
      value = '';
    }
    if (objectData[this.name] != null) {
      if (!objectData[this.name].push) {
        objectData[this.name] = [objectData[this.name]];
      }
      objectData[this.name].push(value);
    } else {
      objectData[this.name] = value;
    }
  });
  return objectData;
};

// TODO: redesign this
// api
var API_URL = '/api/v1/';
function createCredentialGroup(options, callback) {
    var opt = options || {};
    var data = {
        name: opt.name
    }
    var cb = callback || function(){};
    $.ajax({
        url: API_URL + 'credentialgroups/',
        data: JSON.stringify(data),
        type: "POST",
        dataType: "application/json",
        contentType: "application/json",
        complete: function(xhr) {
            cb(xhr);
        }
    });
}
function deleteCredentialGroup(uuid, callback) {
    var cb = callback || function(){};
    $.ajax({
        url: API_URL + 'credentialgroups/' + uuid + '/',
        type: "DELETE",
        complete: function(xhr) {
            cb(xhr);
        }
    });
}
function createCredential(options, callback) {
    var opt = options || {};
    var data = {
        name: opt.name,
        description: opt.description,
        url: opt.url,
        username: opt.username,
        password: opt.password,
        groups: [API_URL + "credentialgroups/" + opt.groupUUID + "/"]
    }
    var cb = callback || function(){};
    $.ajax({
        url: API_URL + 'credentials/',
        data: JSON.stringify(data),
        type: "POST",
        dataType: "application/json",
        contentType: "application/json",
        complete: function(xhr) {
            cb(xhr);
        }
    });
}
function getCredential(uuid, callback) {
    var cb = callback || function(){};
    $.ajax({
        url: API_URL + 'credentials/' + uuid + '/',
        type: "GET",
        complete: function(xhr) {
            var data = JSON.parse(xhr.responseText);
            cb(data, xhr);
        }
    });
}
