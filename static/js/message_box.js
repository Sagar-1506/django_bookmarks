function msg_fun(){
  var item1 =$(this);
  var user=$(item1).attr("id");
  
  $(item1).hide();
  
  var item3=$(item1).parent();
  var item4=$(item3).get(0);
  var msg_box=$(item4).find(".message_box");
  $(msg_box).show();
  var form=$(msg_box).find(".form");
  $(form).attr("action","/message/?username="+user);
  
}

$(document).ready(function (){
    $(".message_box").hide();
    $(".msg-btn").click(msg_fun);
});
