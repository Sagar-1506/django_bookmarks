function get_messages(start)
{
    var received_message=$(document).find(".received_messages");
    received_message.load("/received/?start="+start);
    
}

function prev_message(start)
{
    get_messages(start+5);
}
function next_message(start)
{
    get_messages(start-5);
}
$(document).ready(get_messages(0));