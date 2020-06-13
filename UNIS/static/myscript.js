$(window).on('load', function() {

$(".se-pre-con").fadeOut("slow");

autosize(document.getElementById("chat"));

document.getElementById("startimage").src= document.getElementById("chatinsideimagecoveruser2").src;
var tt="Hi, "+document.getElementById("notaname").innerHTML;
document.getElementById("notaname2").innerHTML= tt;
startcollapse();


checkfbuser();





//noty


// new Noty({
//   type: 'error',
//   theme: 'nest',
//   layout: 'topCenter',
//     text: 'switched to Dark Mode',
//       timeout: 2000,
//
// }).show();
//noty

updatecurrentuseronlinestatus("yes");




//local storage for audio Settings

if (localStorage.getItem("nmsgaudio") != null) {
  var audio1 = localStorage.getItem('nmsgaudio');
  var audio2 = localStorage.getItem('inchataudio');
  if(audio1=='no'){
    $('#chkToggle1').bootstrapToggle('off');
    globalaudiosettingsfornewmessage=0;
  }
  if(audio2=='no'){
    $('#chkToggle2').bootstrapToggle('off');
    globalaudiosettingsforinchat=0;
  }

}
else{
  localStorage.setItem('nmsgaudio', 'yes');
  localStorage.setItem('inchataudio', 'yes');
}
//local storage ends



});



var dataorderstlist=[];
var globalaudiosettingsfornewmessage=1;
var globalaudiosettingsforinchat=1;






window.onbeforeunload = function(){
   updatecurrentuseronlinestatus("no");
}





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
              //alert(result);

              if(tempres=="done"){
              addfrndsinfirebase(admin,touser);

              new Noty({
                type: 'success',
                theme: 'nest',
                layout: 'topCenter',
                  text: 'Friend added Successfully!',
                    timeout: 2000,

              }).show();


            }

            else{

              new Noty({
                type: 'error',
                theme: 'nest',
                layout: 'topCenter',
                  text: 'Already in friend list!',
                    timeout: 2000,

              }).show();


            }

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
//  if(document.getElementById(tt).innerHTML=="<span style='color : blue'>new message.</span>")
  //{
    changefbnewmessage(id);
    document.getElementById(tt).innerHTML="HI there i am using whatsapppppppppppppppppppppp";
//  }


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
var listoffriendsforfirebase=[];


//load chats into chat menu
function loadchatintomultiCollapseExample1(){


  var admin=document.getElementById("adminusername").value;
  listoffriendsforfirebase=[];
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
        for (var i = size-1;i >=0; i--)
        {
          var name = (data['fname'][i] + " "+ data['lname'][i]);
          var id1= (data['id'][i]);
          var status = (data['status'][i]);
          var email = (data['email'][i]);
          var uname = (data['uname'][i]);
          var date = (data['date'][i]);
          var profile = (data['profile_pic'][i]);
          var ar=[uname];
          var lmsg = (data['last_message'][i]);
          if(lmsg=='Photo'){lmsg="<span class='iconify' data-icon='ic:baseline-photo' data-inline='false'></span>"+'&nbsp;Photo';}
          var badge="badgeonline"+id1;
          var typingbyid ="typingbyid"+id1;
          var  mdivid="mdivid"+id1;
          listoffriendsforfirebase.push(id1);
          $("#multiCollapseExample1chat").append("<!-- Chat link --><a class='text-reset nav-link p-0 mb-6' id='"+mdivid+"' ><div class='card card-active-listener' style='background-color: #29242a; margin-top: 4%; border: none; cursor: pointer;' onclick='chatcollapse("+id1+")'><span class='badge badge-pill badge-primary' style='position: absolute; visibility:hidden; ' id='"+typingbyid+"'>Typing..</span><div class='card-body'><div class='numberCircle' id='chatnmes"+id1+"' style='visibility:hidden;'></div><div class='media'><img src="+profile+" alt='...' class=' ' id='contactimg' style='border: none; object-fit: cover; cursor: pointer;' onclick='expandside("+"`"+profile+"`"+","+"`"+name+"`"+","+"`"+status+"`"+","+"`"+uname+"`"+","+"`"+email+"`"+","+"`"+date+"`"+")'><span class='badge badge-pill badge-success text-success' id="+badge+" style='position: absolute; visibility: hidden;  left: 5%;'>.</span><div class='media-body overflow-hidden'><div class='d-flex align-items-center mb-1'><h6 class='text-truncate mb-0 mr-auto text-light'>"+name+"</h6><p class='small text-muted text-nowrap ml-4'>10:42 am<font class='onlinestaus'><B>.</B></font></p></div><div id='sn"+id1+"' class='text-truncate text-muted' style='text-overflow: ellipsis;'>"+lmsg+"</div></div></div></div></div></a><!-- Chat link -->");
        }
      }

        $('#textmsgcollapsebottom').collapse('show');
      loadreadstatusonchatload();
      callonlinecheckeronchatopen();

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
            data :{userid : admin,frienduserid : secondid,message : text,isimage : "no",image:"-" },
            // data: $('form').serialize(),
            success: function(result) {
                document.getElementById("chat").value="";

                showchatofthatuser(secondid);
                newchatnotifyfb(admin,secondid);


                //trial hree
              autosize.destroy(document.getElementById("chat"));
              autosize(document.getElementById("chat"));
              if(globalaudiosettingsforinchat==1){var x = document.getElementById("myAudio2");
              x.play();}

          //alert(OriginalHeight);
          //  $("#chat").height(OriginalHeight);
                //trial ends here

              //  document.getElementById('chat').style.height = hota+"px";
                //resizeDivs();
                //document.getElementById("chat").value="";
            // alert(result);
    }

        });
    });
  });







var chatloadedtiinow="";
var globalchatsdate ="";

//load chats of  that user
function showchatofthatuser(secondid){
  var admin=document.getElementById("adminusername").value;
  globalchatsdate="";

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
        var mynameforchat = document.getElementById("notaname").innerHTML;
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
            var image_url_id = (data['image_data'][i]);
            var is_image = (data['is_image'][i]);
            var timestamp = (data['timestamp'][i]);
            var date = timestamp.slice(0,10);
            var time = timestamp.slice(11,16)

            //date categorization
            if(date != globalchatsdate )
            {
             globalchatsdate=date;
              $("#chatwindow").append("<!--datecategorizer--><div style='width: 100%; height: 5vh; margin-top: 2%; align-items: center;text-align: center;'><div class='rounded-pill bg-success align-middle' style='display: inline-block; height: 5vh; text-align: center; margin: 0 auto; padding: 1%'><b><h6 class='text-light'>"+date+"</h6></b></div></div><!--datecategorizerends-->");
            }


            //categorizing messages
            if(sender_id==secondid && is_image=="no")
             {
               $("#chatwindow").append("<!--msgleft--><div class='mainouterdiv' style='overflow:auto;margin-top: 2%'><div class='imgdiv' style='width: 5%; float: left; '><img src="+friendprofilepic+" class='img-fluid rounded-circle'></div><div class='content-div' style=' width: 58%; float: left; margin-left: 2%;'><span class='text-light' style=''><b>"+friendname+"</b><span style='margin-left: 3%; '><small class='text-muted'>"+time+"</small></span></span><br><div class='bg-light .d-flex' style='border-radius: 0px 12px 12px 12px; min-width: 30%; max-width: 92%;padding: 3%; margin-top: 0.5%; word-wrap: break-word; white-space: pre-line; display: inline-block;'>"+message+"</div><!-- Message: dropdown --><div class='dropdown align-middle' style=' display: inline-block; ' ><a class='text-muted opacity-60 ' href='#' data-toggle='dropdown' aria-haspopup='true' aria-expanded='false'><span class='iconify text-muted' data-icon='eva:more-vertical-fill' data-inline='false'></span></a><div class='dropdown-menu' style='background-color: #2f2a30;' ><a class='dropdown-item d-flex align-items-center' onclick='deletechatmsgbyid("+messageid+")' style='color :white; cursor:pointer; background-color: #2f2a30;'> Delete<span class='ml-auto fe-trash-2'></span></a></div></div><!-- Message: dropdown --></div></div><!--msgleft ends-->");
             }


             else if(sender_id==admin && is_image=="no")
             {
               $("#chatwindow").append("<!--msgright--><div class='mainouterdiv' style='overflow:auto;margin-top: 2%;'><div class='imgdiv' style='width: 5%; float: right; '><img src="+mypic+" class='img-fluid rounded-circle'></div><div class='content-div' style=' width: 60%; float: left; margin-right: 2%; float: right; '><span class='text-light' style='float: right; margin-right: 1%; '><b>"+mynameforchat+"</b>&nbsp;&nbsp;&nbsp;<small class='text-muted'>"+time+"</small></span><br><div class='bg-primary text-light .d-flex' style='border-radius: 12px 0px 12px 12px; min-width: 30%; max-width: 90%;padding: 3%; margin-top: 0.5%; word-wrap: break-word;  white-space: pre-line;  display: inline-block; float: right;'>"+message+"</div><!-- Message: dropdown --><div class='dropdown ' style=' float: right;' ><a class='text-muted opacity-60 ' href='#' data-toggle='dropdown' aria-haspopup='true' aria-expanded='false'><span class='iconify text-muted' data-icon='eva:more-vertical-fill' data-inline='false'></span></a><div class='dropdown-menu' style='background-color: #2f2a30;' ><a class='dropdown-item d-flex align-items-center' onclick='deletechatmsgbyid("+messageid+")' style='color :white; cursor:pointer; background-color: #2f2a30;'> Delete<span class='ml-auto fe-trash-2'></span></a></div></div><!-- Message: dropdown --></div></div><!--msgright ends-->");
             }


             else if(sender_id==admin && is_image=="yes")
             {
               $("#chatwindow").append("<!--imgmsgright--><div class='mainouterdiv' style='overflow:auto;margin-top: 2%;'><div class='imgdiv' style='width: 5%; float: right; '><img src="+mypic+" class='img-fluid rounded-circle'></div><div class='content-div' style=' width: 50%; float: left; margin-right: 2%; float: right;'><span class='text-light' style='float: right; margin-right: 1%; '><b>"+mynameforchat+"</b>&nbsp;&nbsp;&nbsp;<small class='text-muted'>"+time+"</small></span><br><div class='bg-primary .d-flex' style='border-radius: 0px 12px 12px 12px; max-width: 70%; padding: 3%; margin-top: 0.5%; float: right;'><img src="+image_url_id+" class='img-fluid' ></div><!-- Message: dropdown --><div class='dropdown align-middle' style=' display: inline-block; float: right;' ><a class='text-muted opacity-60 ' href='#' data-toggle='dropdown' aria-haspopup='true' aria-expanded='false'><span class='iconify text-muted' data-icon='eva:more-vertical-fill' data-inline='false'></span></a><div class='dropdown-menu' style='background-color: #2f2a30;' ><a class='dropdown-item d-flex align-items-center' onclick='deletechatmsgbyid("+messageid+")' style='color :white; cursor:pointer; background-color: #2f2a30;'> Delete<span class='ml-auto fe-trash-2'></span></a></div></div><!-- Message: dropdown --></div></div><!--imgmsgrighendst-->");
             }

             else if(sender_id==secondid && is_image=="yes")
             {
               $("#chatwindow").append("<!--imagemsgleft--><div class='mainouterdiv' style='overflow:auto;margin-top: 2% ;'><div class='imgdiv' style='width: 5%; float: left; '><img src="+friendprofilepic+" class='img-fluid rounded-circle'></div><div class='content-div' style=' width: 40%; float: left; margin-left: 2%; '><span class='text-light' style=''><b>"+friendname+"</b><span style='margin-left: 3%; '><small class='text-muted'>"+time+"</small></span></span><br><div class='bg-light .d-flex' style='border-radius: 0px 12px 12px 12px; max-width: 85%; padding: 3%; margin-top: 0.5%; display: inline-block; '><img src="+image_url_id+" class='img-fluid' ></div><!-- Message: dropdown --><div class='dropdown align-middle' style=' display: inline-block; ' ><a class='text-muted opacity-60 ' href='#' data-toggle='dropdown' aria-haspopup='true' aria-expanded='false'><span class='iconify text-muted' data-icon='eva:more-vertical-fill' data-inline='false'></span></a><div class='dropdown-menu' style='background-color: #2f2a30;' ><a class='dropdown-item d-flex align-items-center' onclick='deletechatmsgbyid("+messageid+")' style='color :white; cursor:pointer; background-color: #2f2a30;'> Delete<span class='ml-auto fe-trash-2'></span></a></div></div><!-- Message: dropdown --></div></div><!--imagemsgleftends-->");
             }



        }
          $('#chatwindow').scrollTop($('#chatwindow')[0].scrollHeight);
      }




}

});




}





//show bottom image input
function showimageinputdiv(){
  $("#id_image").click();

}

function hideimagebottomdiv1()
{ $('#textmsgcollapsebottom').collapse('show');
  $('#imgmsgcollapsebottom').collapse('hide');

document.getElementById("sampleimageupload").src="";
document.getElementById("id_image").value = "";
}


var globalimageschoosed = ""
//setting images
function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
          globalimageschoosed = e.target.result;
            $('#sampleimageupload').attr('src', e.target.result);
        }

        reader.readAsDataURL(input.files[0]);
    }

    $('#imgmsgcollapsebottom').collapse('show');
  $('#textmsgcollapsebottom').collapse('hide');
}

$("#id_image").change(function(){
    readURL(this);

});
//setting image ends







//delete msg by id
function deletechatmsgbyid(msgid)
{   var admin=document.getElementById("adminusername").value;
  var seconduser = global_sendtouser;

  alert(admin+"-"+msgid+"-"+seconduser);

  $.ajax({
         type: "POST",

         cache: false,
         url: "delete_message/",
         datatype: "html",
         data :{user_id : admin,friend_id : seconduser,message_id : msgid},
         // data: $('form').serialize(),
         success: function(result) {

             document.getElementById("chat").value="";
             showchatofthatuser(seconduser);
             // newchatnotifyfb(admin,secondid);            don't know purpose added by manish

 }

     });


}









//delete whole Chats
function deletewholechatsbyids(){
var foo = prompt('To confirm enter DELETE below in all caps');
if(foo=="DELETE"){alert("ok");}
if(foo=="DELETE"){
    var admin=document.getElementById("adminusername").value;
    var seconduser = global_sendtouser;
  alert("ok");
  $.ajax({
        type: "POST",

        cache: false,
        url: "clear_chat/",
        datatype: "html",
        data :{user_id : admin,friend_id : seconduser},
        // data: $('form').serialize(),
        success: function(result) {

            document.getElementById("chat").value="";
            showchatofthatuser(seconduser);
            // newchatnotifyfb(admin,secondid);            don't know purpose added by manish


}

    });



}
else{alert("Operation cancelled by user.")}

}












//send image by idea
$(document).ready(function(){
    //listen for form submission
    $('#submitformforimage').on('click', function(e){
      document.getElementById("loaderforimg").style.visibility = "visible" ;

      e.preventDefault();
      var admin=document.getElementById("adminusername").value;

      var secondid = global_sendtouser;

      // AJAX
      $.ajax({
            type: "POST",

            cache: false,
            url: "send_message/",
            datatype: "html",
            data:{userid : admin,frienduserid : secondid,message : "null",isimage : "yes",image : globalimageschoosed},
            success: function(data) {
              showchatofthatuser(secondid);
              newchatnotifyfb(admin,secondid);
            //  document.getElementById("contactimgheader").src=data;
            document.getElementById("loaderforimg").style.visibility = "hidden" ;
            hideimagebottomdiv1();

    }

        });
    });
  });




  //enter button to sed chat
  $('#chat').keyup(function (event) {
         if (event.shiftKey  && event.keyCode == 13 ) {


              event.preventDefault();

              $('#sendchat').click();

            // alert("hi");
        }

  });


//trial


//detect offline connection_logged_in
window.addEventListener('offline', function(e) { console.log('offline');
$('#offlinemodal').modal('show');

window.addEventListener('online', function(e) { console.log('online');
$('#offlinemodal').modal('hide');
 });

 });
//ends




//toggle button change on startup
$(function() {
   $('#chkToggle1').change(function() {
     var x= $(this).prop('checked');
     if(x==true){
       localStorage.setItem('nmsgaudio', 'yes');
       globalaudiosettingsfornewmessage=1;
   }
     else{localStorage.setItem('nmsgaudio', 'no');
     globalaudiosettingsfornewmessage=0;
   }
   })
 })



 $(function() {
    $('#chkToggle2').change(function() {
      var x= $(this).prop('checked');
      if(x==true){
        localStorage.setItem('inchataudio', 'yes');
        globalaudiosettingsforinchat=1;
    }
      else{localStorage.setItem('inchataudio', 'no');
      globalaudiosettingsforinchat=0;
    }
    })
  })
//toggle button change ends









//send data order for chats
function storechatorder(){
  var adminidforstorage= document.getElementById("adminusername").value;
  var dts="";
for(var i=0;i<dataorderstlist.length;i++)
{
dts=dts+dataorderstlist[i]+'_';

}


$.ajax({
      type: "POST",

      cache: false,
      url: "store_chat_order/",
      datatype: "html",
      data:{user_id : adminidforstorage,order_list : dts },
      success: function(data) {


}

});}
//send data order ends
