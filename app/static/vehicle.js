function add_item()
{
	// console.log("Called");
    $.ajax({
	url:'http://127.0.0.1:8080/vehicle/add',
	method:'POST',
	data:{vehicle_no:$('#vno').val(),driver_name:$('#dnm').val(),capacity:$('#cp').val(),base_cost:$('#bc').val(),cost_per_km:$('#cpk').val()},
	success:function(response)
	{
		alert("Vehicle added Sucessfully");
		window.location="http://localhost:8080/vehicle"
	    ////console.log(response);
	},
	error:function(response)
	{
		alert("Try again");
	},
    });
}
var r_item="";
function get_items()
{
// console.log("Called");
    $.ajax({
	url:'http://127.0.0.1:8080/vehicle/get',
	method:'GET',
	success:function(response)
	{
		// alert("Item added Sucessfully");
		// window.location="http://localhost:8080/item"
	    // console.log(response);
	    var resp=response;
	    var arrayLength = resp.length;
	    str_html="<center><table class=\"table1\" margin=\"auto\"><tr class=\"tr1\"><th class=\"th1\">Vehicle No.</th><th class=\"th1\">Driver Name</th><th class=\"th1\">Capacity</th><th class=\"th1\">Base Cost</th><th class=\"th1\">Cost Per Km</th><th class=\"th1\">REMOVE</th></tr>";

	    for(var i=0;i<arrayLength;i++)
	    {
	    	str_html+="<tr class=\"tr1\">";
	    	for(var j=0;j<resp[i].length;j++)
	    	{
	    		str_html+="<td class=\"td1\">"+resp[i][j]+"&nbsp;&nbsp;</td>";
	    	}
	    	r_item=resp[i][0];
	    	str_html+="<td class=\"td1\"><button onclick=\"removeItem()\">Remove</button></td></tr>";
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
function removeItem()
{
	// console.log(id);
    $.ajax({
	url:'http://127.0.0.1:8080/vehicle/remove',
	method:'POST',
	data:{vid:r_item},
	success:function(response)
	{
		// alert("Item added Sucessfully");
		// window.location="http://localhost:8080/item"
	    // console.log(response);
	    alert("Vehicle Removed");
	    get_items();
	},
	error:function(response)
	{
		alert("Try again");
	},
    });	
}

get_items();