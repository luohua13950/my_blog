$(function(){
	editormd.markdownToHTML("editormd-view", {
        htmlDecode      : "style,script,iframe",  // you can filter tags decode
        emoji           : true,
        taskList        : true,
        tex             : true,  // 默认不解析
        flowChart       : true,  // 默认不解析
        sequenceDiagram : true,  // 默认不解析
    });
});

function like_article(id,action){
    $.ajax({
        url: "{% url 'knowledge:like_article' %}",
        type: "POST",
        data: {"id":id},
        success: function(e){
            if(e=="1"){
                layer.msg("感谢点赞");
                window.location.reload();
            }else{
                layer.msg("我会继续努力");
                window.location.reload();
            }
        },
    });
}

function store(id) {
        $.ajax({
            url: store_post,
            type: 'post',
            data: {
                "id":id
            },
            success: function (cb) {
                if (cb.status=='ok'){
                    $('#tt').text(cb.msg)
                }else
                $('#tt').text(cb.msg)
            }
        })
    }