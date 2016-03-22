$(document).ready(function() {
  //Create handlers for buttons clicks
  $('#unprioritized').click(function() { unprioritized(); });
  $('#unchecked').click(function() { unchecked(); });

  // CSRF set-up copied from Django docs
  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
  }
  var csrftoken = getCookie('csrftoken');
  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
  });

});



function unprioritized() {
    $( ".content" ).remove()
    $.get("/priority")
      .done(function( data ) {
        for(index in data.patients) {
            $( "#main" ).append(data.patients[index].html);
            $( ".check" ).remove()
        }
        $('.prioritize').click(function() { prioritize(this); });
    })
}

function prioritize(t) {
    var patientce_id = t.value;
	var num = $("#" + patientce_id).val()
	$("#" + patientce_id).val("")
    $.post("/prioritize", {'id': patientce_id, 'priority': num})
      .done(function( data ) {
        if(data == 1) {
            $( "." + patientce_id ).remove()
        }
        else {
        }
    })
}

function unchecked() {
    $( ".content" ).remove()
    $.get("/check")
      .done(function( data ) {
        for(index in data.patients) {
            $( "#main" ).append(data.patients[index].html);
            $( ".priority" ).remove()
        }
        $('.checkin').click(function() { checkin(this); });
    })
}

function checkin(t) {
    var patientce_id = t.value;
    $.post("/checkin", {'id': patientce_id})
      .done(function( data ) {
        if(data == 1) {
            $( "." + patientce_id ).remove()
        }
        else {
        }
    })
}