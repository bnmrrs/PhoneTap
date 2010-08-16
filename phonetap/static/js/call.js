$(document).ready(function(){
	if (call_status != 'Completed') {
		$.blockUI({ message: 'This call is in progress.  This page will update as soon as it has been completed' });
		
		function updater() {
			$.ajax({
				method: 'get',
				url : '/check_call_status/'+call_id,
				dataType : 'json',
				success: function (data) {
					if (data.call_status == 'Completed') {
						location.reload();
					}
				}
			});
		}

		var interval = setInterval(updater, 3000);
	}
});