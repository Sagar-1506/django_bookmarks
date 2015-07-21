function bookmark_edit() {
    var item=$(this).parent();
    var url =item.find(".title").attr("href");
    print(url) ;
    item.load("/save/?ajax&url="+escape(url),null,function (){
       $("#save-form").submit(bookmark_save) ;
    });
    return false ;
}
$(document).ready(function (){
    $(".edit" ).click(bookmark_new);
    
    
    });

function bookmark_new(){
    alert("Ok") ;
}

function bookmark_save()
{
    var item=$(this).parent();
    
    var data = {
        url:item.find("#id_url").val(),
        title:item.find("#id_title").val(),
        tags:item.find("#id_tags").val()
    };
    $.post("save/?ajax",data,function(result){
        if (result!=failure) {
            item.before($("td",result).get(0));
            item.remove();
            $("td.bookmark .edit").click(bookmark_edit);
        }
        else
        {
            alert("Failed to validate")
        }
        
        
    });
    return false ;
    
}

