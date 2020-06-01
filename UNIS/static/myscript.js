$(window).on('load', function() {

//alert("hello");

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

var glist=[];
//autocomplete on adding frnds
$( function() {
    var tags = [
    "Delhi",
    "Ahemdabad",
    "Punjab",
    "Uttar Pradesh",
    "Himachal Pradesh",
    "Karnatka",
    "Kerela",
    "Maharashtra",
    "Gujrat",
    "Rajasthan",
    "Bihar",
    "Tamil Nadu",
    "Haryana"


      /* Making a list of available tags */


    ];
    glist=tags;
    $( "#texttoaddfrnd" ).autocomplete({
      source: tags

/* #tthe ags is the id of the input element
source: tags is the list of available tags*/


    });
  } );






//btntoaddfrnd
function btntoaddfrnd(){

var temp=document.getElementById("texttoaddfrnd").value;

if(glist.includes(temp))
	{document.getElementById("addfrndresult").style.visibility = "visible";}
else{
	document.getElementById("addfrndresult").style.visibility = "hidden";
	alert("Not a valid User");

}




}
