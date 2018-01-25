
$(document).ready(
//matching password with confirm-password
$('#pass2').blur(()=>{
  if( $('#pass1').val()!== $('#pass2').val() ){
    $('#unmatch-pass').show();
    $('button').attr('disabled','true');
  }
  else{
    $('button').removeAttr('disabled');
    $('#unmatch-pass').hide();
  }
  }
));








// (function() {
//   'use strict';


 
// })();
