$('#dia').change(function(){
    if($(this).val() == "05/11/2020") {
        $('#hora').show();
    } else {
        $('#hora').hide();
    }
}); 