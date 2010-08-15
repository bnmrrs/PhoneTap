$(document).ready(function(){	
	
	$.fn.qtip.styles.errorstyle = {
	   width: 'auto',
	   background: '#ef2626',
	   color: 'white',
	   textAlign: 'center',
	   border: {
	      width: 7,
	      radius: 5,
	      color: '#ef2626'
	   },
	   tip: 'topMiddle',
	   name: 'dark'
	};
	
	$('#caller_num').qtip({
		content: {
			prerender: true,
			text: 'Error: Phone numbers must be 444-444-4444'
		},
		show: 'false',
		hide: 'fixed',
		style: 'errorstyle',
		position: {
		    corner: {
		       target: 'bottomMiddle',
		       tooltip: 'topMiddle'
			}
		}
	});
	
	$('#called_num').qtip({
		content: {
			prerender: true,
			text: 'Error: Phone numbers must be 444-444-4444'
		},
		show: 'false',
		hide: 'fixed',
		style: 'errorstyle',
		position: {
		    corner: {
		       target: 'bottomMiddle',
		       tooltip: 'topMiddle'
			}
		}
	});
	
	$('#caller_email').qtip({
		content: {
			prerender: true,
			text: 'Error: Email must be like you@example.org'
		},
		show: 'false',
		hide: 'fixed',
		style: 'errorstyle',
		position: {
		    corner: {
		       target: 'bottomMiddle',
		       tooltip: 'topMiddle'
			}
		}
	});
	
	// Hints
	$('input#caller_num').example('555-555-5555', { className: 'hint' });
	$('input#callee_num').example('555-555-5555', { className: 'hint' });
	$('input#caller_email').example('you@example.org', { className: 'hint' });
	
	$("#user-num-button").click(function () {
		if (is_valid_phone($('#caller_num').val())) {
			$('#caller_num').qtip("hide");
							
			$("#user-num-wrapper").hide("slide", { direction: "left" }, 1000);
			$("#called-num-wrapper").show("slide", { direction: "right" }, 1000);
		} else {
			$('#caller_num').qtip("show");
		}
	});
	
	$("#called-num-button").click(function () {
		if (is_valid_phone($('#caller_num').val())) {
			$('#called_num').qtip("hide");
			$("#called-num-wrapper").hide("slide", { direction: "left" }, 1000);
			$("#email-wrapper").show("slide", { direction: "right" }, 1000);
		} else{
			$('#called_num').qtip("show");
		}
	});
	
	$("#called-num-previous").click(function () {
		$('#called_num').qtip("hide");
		
		$("#called-num-wrapper").hide("slide", { direction: "right" }, 1000);
		$("#user-num-wrapper").show("slide", { direction: "left" }, 1000);
	});
	
	$("#email-previous").click(function () {
		$('#caller_email').qtip("hide");
		
		$("#email-wrapper").hide("slide", { direction: "right" }, 1000);
		$("#called-num-wrapper").show("slide", { direction: "left" }, 1000);
	});
	
	$("#email-button").click(function () {
		if (is_valid_email($('#caller_email').val())) {
			$('#caller_email').qtip("hide");
			
			$.blockUI({ message: 'We are processing your request.  You should receive a phone call soon.' });
			
			$('#call-form').submit();
		} else {
			$('#caller_email').qtip("show");
		}
	});
	
	var is_valid_phone = function(phone_number) {
		// nasty hack to get around the default			
		if (phone_number === '555-555-5555') {
			return false;
		}
		
		phone_number = phone_number.replace(/\s+/g, "");
		return phone_number.match(/^(1-?)?(\([2-9]\d{2}\)|[2-9]\d{2})-?[2-9]\d{2}-?\d{4}$/)
	}
	
	var is_valid_email = function(email) {
		// nasty hack to get around the default
		if (email === 'you@example.org') {
			return false;
		}
		
		return email.length > 1 && /^((([a-z]|\d|[!#\$%&'\*\+\-\/=\?\^_`{\|}~]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])+(\.([a-z]|\d|[!#\$%&'\*\+\-\/=\?\^_`{\|}~]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])+)*)|((\x22)((((\x20|\x09)*(\x0d\x0a))?(\x20|\x09)+)?(([\x01-\x08\x0b\x0c\x0e-\x1f\x7f]|\x21|[\x23-\x5b]|[\x5d-\x7e]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(\\([\x01-\x09\x0b\x0c\x0d-\x7f]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]))))*(((\x20|\x09)*(\x0d\x0a))?(\x20|\x09)+)?(\x22)))@((([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.)+(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.?$/i.test(email);
	}
	
	$('#call-form').ajaxForm({ 
		dataType: 'json',
		success: processResponse
	});
});

function processResponse(data) {
	if (data.success) {
		window.location = data.call_page_url;
	} else {
		alert('An error occurred.  Try again later.');
		console.log(data);
	}
}