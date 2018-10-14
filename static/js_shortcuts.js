function client_ajax_post(passurl,postdata,success_fun=null,failure_fun=null) {
    // 客户端POST提交
    $.ajax({
        type: 'POST',
        url: passurl,
        cache: false,
        data:postdata,
        success: function (data) {
            if (data && data.success) {
                if(success_fun)
                {success_fun();}
            }
            else {
                $.toptip("操作失败，"+data.msg, 'error');
                if(failure_fun)
                {
                    failure_fun();
                }
            }
        },
        error: function (data) {
            $.toptip('操作失败' + data.responseText, 'error');
        }
    });
}



function common_ajax_post(post_url,post_data,success_msg=true,success_fun=null,failure_fun=null) {
// 常规POST提交
    $.ajax({
        type: 'POST',
        url: post_url,
        cache: false,
        data: post_data,
        success: function (data) {
            if (data && data.success) {
                if(success_msg){
                    $.messager.show({
                    title: '我的消息',
                    msg: data.msg,
                    timeout: 5000,
                    showType: 'slide'
                });
                }
                if(success_fun)
                {success_fun(data);}
            }
            else {
                $.messager.alert("提交失败",data.msg);
                if(failure_fun)
                {
                    failure_fun();
                }
            }
        },
        error: function (data) {
            $.messager.alert('错误', data.responseText);
        }
    });
}

function common_dialog(obj,init_title,d_width=650,d_height=300,open=true,save_fun=null,close_fun=null) {
    // 带有保存关闭的对话框
    $(obj).dialog({title:init_title,
            width:d_width,
            height:d_height,
            buttons:[{
                text:'保存',
                handler:function(){
                    if(save_fun)
                    {
                        save_fun();
                    }

                }
            },{
                text:'关闭',
                handler:function(){
                    $(obj).dialog('close');
                    if(close_fun)
                    {
                        close_fun();
                    }
                }
            }]
        });
        if (open)
        {$(obj).dialog('open');}
}

function common_dialog_only_close(obj,init_title,d_width=700,d_height=650) {
    $(obj).dialog({title:init_title,
            width:d_width,
            height:d_height,
            buttons:[{
				text:'关闭',
				handler:function(){
				    $(obj).dialog('close')
                }
			}]
        });
}