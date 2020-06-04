$(window).on('load', function() {



autosize(document.getElementById("chat"));

document.getElementById("startimage").src= document.getElementById("chatinsideimagecoveruser2").src;
var tt="Hi, "+document.getElementById("notaname").innerHTML;
document.getElementById("notaname2").innerHTML= tt;
startcollapse();


checkfbuser();
});




//textarea div height

function resizeDivs() {
    var main = document.getElementById('chatcompose').offsetHeight;
    var sidebar = document.getElementById('chat').offsetHeight;
    if (sidebar > main) {
        main = sidebar;
        document.getElementById('chatcompose').style.height = document.getElementById('chat').style.height = main + 'px';
    }
}







//side menu
function expandside(profile,name,status,username,email,date){


var x=document.getElementById("sidemenuopen").value;
if(x==0){
 document.getElementById("chatinsideimagecover").src=profile;
 document.getElementById("clkonuserid").innerHTML=name;
  document.getElementById("clkonuserstatus").innerHTML=status;
  document.getElementById("clkonuserusername").innerHTML=username;
  document.getElementById("clkonuseremail").innerHTML=email;
  document.getElementById("clkonuserdate").innerHTML=date;
	$("#middiv").removeClass("col-sm-8");
   $("#middiv").addClass("col-sm-6");
	$("#sidediv").addClass("col-sm-2");
	document.getElementById("sidemenuopen").value=1;

}
else if(x==1)
{

$("#middiv").removeClass("col-sm-6");
   $("#middiv").addClass("col-sm-8");

	$("#sidediv").addClass("col-sm-0");
	document.getElementById("sidemenuopen").value=0;
}

}



//load chats
function collapprofile(){
	$('#multiCollapseExample2').collapse('show');
  		$('#multiCollapseExample1').collapse('hide');
  		$('#multiCollapseExample3').collapse('hide');
  		$('#multiCollapseExample4').collapse('hide');
      loadusersintovar();
}

function collapaccount(){
		$('#multiCollapseExample3').collapse('show');
  		$('#multiCollapseExample1').collapse('hide');
  		$('#multiCollapseExample2').collapse('hide');
  		$('#multiCollapseExample4').collapse('hide');
}

function collapchats(){
    loadchatintomultiCollapseExample1();
  		$('#multiCollapseExample1').collapse('show');
  		$('#multiCollapseExample2').collapse('hide');
  		$('#multiCollapseExample3').collapse('hide');
  		$('#multiCollapseExample4').collapse('hide');

}
function collapcontacts(){
  loadmyfrndsintocollapse4();
	$('#multiCollapseExample4').collapse('show');
	$('#multiCollapseExample1').collapse('hide');
	$('#multiCollapseExample2').collapse('hide');
	$('#multiCollapseExample3').collapse('hide');


}






//btntoaddfrnd










  var tags = [];
  var tagsid=[];
//ajax for fetching user deatilson add frnd

//wait for page load to initialize script
function loadusersintovar(){
      tags=[];
      tagsid=[];
      globallist=[];

      // AJAX
      $.ajax({

            cache: false,
            url: "get_user/",
            datatype: "html",
            data:'',
            success: function(data) {
            data = JSON.parse(data)
            var size=data['len'];

            for (var i = 0;i <size; i++)
            {
                var temp = data['username'][i];
                var tempid = data['id'][i]
                //alert(temp);

                tags.push(temp);
                tagsid.push(tempid);
            }

            $( "#texttoaddfrnd" ).autocomplete({
              source: tags

        /* #tthe ags is the id of the input element
        source: tags is the list of available tags*/


            });


    }

  });}



//ajax ends
var globallist=tags;


function btntoaddfrnd(){

var temp=document.getElementById("texttoaddfrnd").value;

if(tags.includes(temp))
	{    var ind= tags.indexOf(temp);
      var ind1=tagsid[ind];
       document.getElementById("hiddenresid").value=ind1;
    //ajax call for getting desired search images

    $.ajax({
          type:"POST",
          cache: false,
          url: "get_user_details/",
          datatype: "html",
          data:{id : ind1},
          success: function(data) {
           data = JSON.parse(data)
            var temp = data['name'];
            var img= data['img'];
            var uname= data['uname'];
            var status=data['status'];
            //var id=data['id'];

            document.getElementById("chatinsideimagecoveruser").src=img;
            document.getElementById("searchresname").innerHTML=temp;
            document.getElementById("searchresuname").innerHTML=uname;
            document.getElementById("searchresstatus").innerHTML=status;
          //  document.getElementById("hiddenresid").value=id;
            document.getElementById("addfrndresult").style.visibility = "visible";


          }

      /* #tthe ags is the id of the input element
      source: tags is the list of available tags*/


          });



    //call ends




}
else{
document.getElementById("addfrndresult").style.visibility = "hidden";
	alert("Not a valid User");
}





}














//adding frnd from addfrnd button
function addfrndfromsearchres(){
  var admin=document.getElementById("adminusername").value;
  var touser=document.getElementById("hiddenresid").value;
  checkfbuser(touser);

  //alert(topass);

      $.ajax({
            type:"POST",
            cache: false,
            url: "adduser/",
            datatype: "html",
            data:{id1 : admin,id2: touser},
            success: function(result) {
            // data = JSON.parse(data)
              //var temp = data['name'];
              var tempres=result;
              alert(result);

              if(tempres=="done"){
              addfrndsinfirebase(admin,touser);}

            }

        /* #tthe ags is the id of the input element
        source: tags is the list of available tags*/


            });




}





//launch startcollapse
function startcollapse(){
  	$('#startcollapse').collapse('show');
    	$('#maincollapse').collapse('hide');


}
global_sendtouser = 0;

function chatcollapse(id){

    global_sendtouser = id;
    showchatofthatuser(id);
    $('#maincollapse').collapse('show');
  $('#startcollapse').collapse('hide');
  //alert("called");
  var tt="sn"+id;
  if(document.getElementById(tt).innerHTML=="new message")
  {
    changefbnewmessage(id);
    document.getElementById(tt).innerHTML="HI there i am using whatsapppppppppppppppppppppp";
  }


  //alert(global_sendtouser);

}


var dataofloadedfriends="";

function loadmyfrndsintocollapse4(){
  var admin=document.getElementById("adminusername").value;
  $.ajax({
        type:"POST",
        cache: false,
        url: "get_friends/",
        datatype: "html",
        data:{id1 : admin},
        success: function(data) {
          tempdata = data;
        data = JSON.parse(data)
        var size=data['len'];
        if(dataofloadedfriends!=tempdata)
        {dataofloadedfriends=tempdata;
        for (var i = 0;i <size; i++)
        {
          var name = (data['fname'][i] + " "+ data['lname'][i]);
          var id1= (data['id'][i]);
          var status = (data['status'][i]);
          var profile = (data['profile_pic'][i]);

          $("#multiCollapseExample4").append("<!-- Friend --><div class='card mb-6' style='margin-top: 5%; margin-bottom: 5% ;background-color :#29242a;'><div class='card-body' style='background-color :#29242a; '><div class='media' style='background-color :#29242a;text-align: left;'><div class='avatar ' style='background-color :#29242a;'><img class='avatar-img' src="+profile+" alt='Brian Dawson' id='contactimg' onclick=''></div><div class='media-body' style='background-color :#29242a; '><h6 class='mb-0 text-light'>"+name+"</h6><small class='text-muted'>"+status+"</small></div><div class='align-self-center ml-auto' style='background-color :#29242a;'><div class='custom-control custom-checkbox' style='background-color :#29242a;'><!-- Message: dropdown --><div class='dropdown' style='background-color :#29242a;'><a class='text-muted opacity-60 ml-3' href='#' data-toggle='dropdown' aria-haspopup='true' aria-expanded='false'><span class='iconify text-muted' data-icon='eva:more-vertical-fill' data-inline='false'></span></a><div class='dropdown-menu' style='background-color: #2f2a30;' ><a class='dropdown-item d-flex align-items-center' href='#' style='color :white; background-color: #2f2a30;'  onclick='deletefriend("+id1+")'> Delete<span class='ml-auto fe-trash-2'></span></a></div></div><!-- Message: dropdown --></div></div></div></div><!-- Label --><label class='stretched-label' for='id-user-2'></label></div><!-- Friend -->");
        }
      }




}

});

}



//deleting friend
function deletefriend(id){



alert(id);


}






var chatofloadedfrnds="";

//load chats into chat menu
function loadchatintomultiCollapseExample1(){


  var admin=document.getElementById("adminusername").value;
  $.ajax({
        type:"POST",
        cache: false,
        url: "get_chat_list/",
        datatype: "html",
        data:{id : admin},
        success: function(data) {
          var tempdata = data;
        data = JSON.parse(data)
        var size=data['len'];
       if(chatofloadedfrnds!=tempdata)
      {  chatofloadedfrnds=tempdata;
        for (var i = 0;i <size; i++)
        {
          var name = (data['fname'][i] + " "+ data['lname'][i]);
          var id1= (data['id'][i]);
          var status = (data['status'][i]);
          var email = (data['email'][i]);
          var uname = (data['uname'][i]);
          var date = (data['date'][i]);
          var profile = (data['profile_pic'][i]);
          var ar=[uname];
          $("#multiCollapseExample1").append("<!-- Chat link --><a class='text-reset nav-link p-0 mb-6' ><div class='card card-active-listener' style='background-color: #29242a; margin-top: 4%; border: none; cursor: pointer;' onclick='chatcollapse("+id1+")'><div class='card-body'><div class='numberCircle' id='chatnmes"+id1+"' style='visibility:hidden;'></div><div class='media'><img src="+profile+" alt='...' class=' ' id='contactimg' style='border: none; object-fit: cover; cursor: pointer;' onclick='expandside("+"`"+profile+"`"+","+"`"+name+"`"+","+"`"+status+"`"+","+"`"+uname+"`"+","+"`"+email+"`"+","+"`"+date+"`"+")'><div class='media-body overflow-hidden'><div class='d-flex align-items-center mb-1'><h6 class='text-truncate mb-0 mr-auto text-light'>"+name+"</h6><p class='small text-muted text-nowrap ml-4'>10:42 am<font class='onlinestaus'><B>.</B></font></p></div><div id='sn"+id1+"' class='text-truncate text-muted' style='text-overflow: ellipsis;'>HI there i am using whatsapppppppppppppppppppppp</div></div></div></div></div></a><!-- Chat link -->");
        }
      }


      loadreadstatusonchatload();

}

});

}









//send message


$(document).ready(function(){
    //listen for form submission
    $('#sendchat').on('click', function(e){
      var admin=document.getElementById("adminusername").value;
      var text=document.getElementById("chat").value;
      var secondid = global_sendtouser;
      e.preventDefault();
    //  alert(secondid);

      // AJAX
      $.ajax({
            type: "POST",

            cache: false,
            url: "send_message/",
            datatype: "html",
            data :{userid : admin,frienduserid : secondid,message : text},
            // data: $('form').serialize(),
            success: function(result) {
                document.getElementById("chat").value="";
                showchatofthatuser(secondid);
                newchatnotifyfb(admin,secondid);
            // alert(result);
    }

        });
    });
  });







var chatloadedtiinow="";

//load chats of  that user
function showchatofthatuser(secondid){
  var admin=document.getElementById("adminusername").value;


  $.ajax({
        type:"POST",
        cache: false,
        url: "get_friends_chat/",
        datatype: "html",
        data:{userid : admin,friendid:secondid},
        success: function(data) {
          var check= data;
        data = JSON.parse(data)

        var size=data['len'];
        var friendname = (data['friend_name']);
        var friendprofilepic = (data['friend_profile_pic']);
        var mypic =document.getElementById("chatinsideimagecoveruser2").src;
        document.getElementById("contactimgheader").src=friendprofilepic;
        document.getElementById("chatheadername").innerHTML=friendname;
        if(chatloadedtiinow!=check)
        {document.getElementById("chatwindow").innerHTML="";
          chatloadedtiinow=check;
               for (var i = 0;i <size; i++)
        {
        //  var name = (data['fname'][i] + " "+ data['lname'][i]);
            var messageid = (data['message_id'][i]);
            var sender_id = (data['friend_id'][i]);
            var message = (data['message'][i]);
            var image_url_id = (data['image_url_id'][i]);
            var is_image = (data['is_image'][i]);
            var timestamp = (data['timestamp'][i]);



            //categorizing messages
            if(sender_id==secondid && is_image=="false")
             {
               $("#chatwindow").append("<!-- Message left --><div style='width: 100%;'><div class='message' id='msgleft' style='width: 55%; margin-top: 1.5% ;margin-bottom: 1.5%;'><!-- Avatar --><img class='avatar-img' src="+friendprofilepic+" alt='' id='contactimgleft'><!-- Message: body --><div class='message-body'><!-- Message: row --><div class='message-row'><div class='d-flex align-items-center'><!-- Message: content --><div class='message-content bg-light' style='border-radius: 12px 12px 12px 0px; min-width: 50%; '><h6 class='mb-2'>"+friendname+"</h6><div>"+message+"</div><div class='mt-1'><small class='opacity-65'>"+timestamp+"</small></div></div><!-- Message: content --><!-- Message: dropdown --><div class='dropdown' ><a class='text-muted opacity-60 ml-3' href='#' data-toggle='dropdown' aria-haspopup='true' aria-expanded='false'><span class='iconify text-muted' data-icon='eva:more-vertical-fill' data-inline='false'></span></a><div class='dropdown-menu' style='background-color: #2f2a30;' ><a class='dropdown-item d-flex align-items-center' href='#' style='color :white; background-color: #2f2a30;'> Delete<span class='ml-auto fe-trash-2'></span></a></div></div><!-- Message: dropdown --></div></div><!-- Message: row --></div><!-- Message: body --></div><!-- Message --></div><!-- Message left ends-->");
             }


             else if(sender_id==admin && is_image=="false")
             {
               $("#chatwindow").append("<!-- Message right --><div style='width: 100%;'><div class='message message-right' style='width: 60%; margin-top: 1.5% ;margin-bottom: 1.5%; '><!-- Avatar --><img class='avatar-img' src="+mypic+" alt='' id='contactimgright'><!-- Message: body --><div class='message-body'><!-- Message: row --><div class='message-row'><div class='d-flex align-items-center justify-content-end'><!-- Message: dropdown --><div class='dropdown' ><a class='text-muted opacity-60 ml-3' href='#' data-toggle='dropdown' aria-haspopup='true' aria-expanded='false'><span class='iconify text-muted' data-icon='eva:more-vertical-fill' data-inline='false'></span></a><div class='dropdown-menu' style='background-color: #2f2a30;' ><a class='dropdown-item d-flex align-items-center' href='#' style='color :white; background-color: #2f2a30;'> Delete<span class='ml-auto fe-trash-2'></span></a></div></div><!-- Message: dropdown --><!-- Message: content --><div class='message-content bg-primary text-white' style='min-width: 50%; '><div>"+message+"</div><div class='mt-1'><small class='opacity-65'>"+timestamp+"</small></div></div><!-- Message: content --></div></div><!-- Message: row --></div><!-- Message: body --></div></div><!-- Message right end-->")
             }


        }
          $('#chatwindow').scrollTop($('#chatwindow')[0].scrollHeight);
      }




}

});




}
