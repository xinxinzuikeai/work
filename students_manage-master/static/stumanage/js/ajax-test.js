/**
 * Created by python on 17-10-3.
 */
// 文档加载后激活函数
$(document).ready(function(){
    // 创建一个点击事件,去执行函数
    document.getElementById('btn').onclick = function(){
        // 函数是创建异步ajax请求
        $.ajax({
            type: 'get',  // 请求类型
            async: true,  // 请求是否异步处理
            url: '/stumanage/ajaxloadinfo/',  // 谁来处理请求
            dataType: 'json',  // 服务器相应的数据类型
            // 请求成功时运行的函数
            success: function(data, status){
                console.log(data);
                var info = data.data;  // 从data数组中取出data数据(全部学生)
                var div = document.getElementById('ajax');  // 获取页面中设定好的盛放学生信息的div
                for(var i=0; i<info.length; i++){  // 遍历输出
                    var p = document.createElement("p");  // 每循环一次创建一个p标签,一个p标签是一个学生的信息
                    p.innerHTML = info[i];  // 将数据添加到p标签内
                    div.appendChild(p);  // 将p标签添加到div中
                }
            }
        })
    }
});
