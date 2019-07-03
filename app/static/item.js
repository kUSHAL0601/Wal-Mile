function add_item()
{
	// console.log("Called");
    $.ajax({
	url:'http://127.0.0.1:8080/item/add',
	method:'POST',
	data:{height:$('#ht').val(),width:$('#wt').val(),fragile:$('input[name=fragile]:checked').val(),weight:$('#weight').val(),status:'NOT_DEPARTED',client_id:'NA',vehicle_no:'NA'},
	success:function(response)
	{
		alert("Item added Sucessfully");
		window.location="http://localhost:8080/item"
	    ////console.log(response);
	},
	error:function(response)
	{
		alert("Try again");
	},
    });

}
function get_items()
{
// console.log("Called");
    $.ajax({
	url:'http://127.0.0.1:8080/item/get',
	method:'GET',
	success:function(response)
	{
		// alert("Item added Sucessfully");
		// window.location="http://localhost:8080/item"
	    // console.log(response);
	    var resp=response;
	    var arrayLength = resp.length;
	    str_html="<center><table class=\"table1\" margin=\"auto\"><tr class=\"tr1\"><th class=\"th1\">ID</th><th class=\"th1\">HEIGHT</th><th class=\"th1\">WIDTH</th><th class=\"th1\">WEIGHT</th><th class=\"th1\">FRAGILE</th><th class=\"th1\">REMOVE</th></tr>";

	    for(var i=0;i<arrayLength;i++)
	    {
	    	str_html+="<tr class=\"tr1\">";
	    	for(var j=0;j<resp[i].length;j++)
	    	{
	    		str_html+="<td class=\"td1\">"+resp[i][j]+"&nbsp;&nbsp;</td>";
	    	}
	    	str_html+="<td class=\"td1\"><button onclick=\"removeItem("+resp[i][0]+")\">REMOVE</button></td></tr>";
	    }
	    str_html+="</table></center>";
	    // console.log(str_html);
	    document.getElementById('main_data').innerHTML=str_html;
	},
	error:function(response)
	{
		// alert("Try again");
	},
    });	
}
function removeItem(id)
{
	// console.log(id);
    $.ajax({
	url:'http://127.0.0.1:8080/item/remove',
	method:'POST',
	data:{itd:id},
	success:function(response)
	{
		// alert("Item added Sucessfully");
		// window.location="http://localhost:8080/item"
	    console.log(response);
	    alert("Item Removed");
	    get_items();
	},
	error:function(response)
	{
		alert("Try again");
	},
    });	
}

get_items();