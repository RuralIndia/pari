$(document).ready(function() {
	$('input[id*="is_cover"]').click(function(){
			if ($('input[id*="is_cover"]:checked').length > 1) {
				$('input[id*="is_cover"]:checked').each(function() {
					$(this)[0].checked = false;
				});
			}
			$(this)[0].checked = true;
	});	
});
