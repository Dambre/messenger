
$('.send-message-button').click(function(){
    window.location.href = $(this).attr('url');  
});

$('.message-wrapper').click(function(e) {
    if (e.target.className === 'button_100 orange send-message-button'){
        console.log('button');
    }
    else {
      window.location.href = $(this).attr('url');  
    }
});