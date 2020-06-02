$(window).on('load', function() {



autosize(document.getElementById("chat"));
$('#chatwindow').scrollTop($('#chatwindow')[0].scrollHeight);

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



//ajax test


  $(document).ready(function(){

     $("#runcode").click(function(){

          // $("#output").html("Loading ......");
   });

  });
//wait for page load to initialize script
$(document).ready(function(){
    //listen for form submission
    $('#runcode').on('click', function(e){

      e.preventDefault();

      // AJAX
      $.ajax({
            type: "POST",

            cache: false,
            url: "submission/",
            datatype: "html",
            data: $('form').serialize(),
            success: function(result) {

            alert(result);
    }

        });
    });
  });





//ajax for send data


  $(document).ready(function(){

     $("#sendchat").click(function(){

          // $("#output").html("Loading ......");
   });

  });
//wait for page load to initialize script
$(document).ready(function(){
    //listen for form submission
    $('#sendchat').on('click', function(e){

      e.preventDefault();

      // AJAX
      $.ajax({
            type: "POST",

            cache: false,
            url: "submission/",
            datatype: "html",
            data: $('form').serialize(),
            success: function(result) {

            alert(result);
    }

        });
    });
  });



//side menu
function expandside(){


var x=document.getElementById("sidemenuopen").value;
if(x==0){
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
  		$('#multiCollapseExample1').collapse('show');
  		$('#multiCollapseExample2').collapse('hide');
  		$('#multiCollapseExample3').collapse('hide');
  		$('#multiCollapseExample4').collapse('hide');
}
function collapcontacts(){
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

            document.getElementById("chatinsideimagecoveruser").src=img;
            document.getElementById("searchresname").innerHTML=temp;
            document.getElementById("searchresuname").innerHTML=uname;
            document.getElementById("searchresstatus").innerHTML=status;
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
