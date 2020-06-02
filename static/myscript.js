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

if(globallist.includes(temp))
	{    var ind= globallist.indexof(temp);

    //ajax call for getting desired search images

    $.ajax({

          cache: false,
          url: "{% url 'chats:get_user_details' %}",
          datatype: "html",
          data:'{id : ind}',
          success: function(data) {
          // data = JSON.parse(data)
          // var size=data['len'];
          //
          // for (var i = 0;i <size; i++)
          // {
          //
          // }



      /* #tthe ags is the id of the input element
      source: tags is the list of available tags*/


          });


  }

});
    //call ends


  //
  //   $("#multiCollapseExample2").append("<div class='container-fluid' style='width: 100%; height: auto; align-items: center;text-align: center;' id='addfrndresult'><!--middle--><!--cards--><div class='card mb-6 ' style='background-color: #29242a;'><div class='card-body ' style='background-color: #29242a; padding: 0px;'><img src='https://assets.materialup.com/uploads/13ce0637-32b0-4ed0-96fe-5214075a4e2c/preview.png' id='chatinsideimagecoveruser'><br><br><h3 style='color: white;'>Tacaz</h3><h6 class='text text-muted' style=''>I am gonna save the world!</h6></div></div><!--cards--><!--cards--><div class='card mb-6 ' style='background-color: #29242a;'><div class='card-body ' style='background-color: #29242a; padding: 0px;'><ul class='list-group list-group-flush ' style='background-color: #29242a;'><li class='list-group-item px-0 py-6' style='background-color: #29242a;'><div class='media align-items-center' style='background-color: #29242a;'><div class='media-body shadow p-3' style=' text-align: left;'><p class='small text-muted mb-0'>User Name</p><p class='text text-muted'>Iron667</p></div><span class='iconify text-muted' data-icon='bx:bxs-user-circle' data-inline='false' style='margin-right: 3%;'></span></div></li></ul></div></div><!--cards--><br><button type='button' class='btn btn-success align-self-center'>Add Friend</button></div>");
  //
  //
  //
  //
  //
	// document.getElementById("addfrndresult").style.visibility = "visible";
  //












}
else{
	document.getElementById("addfrndresult").style.visibility = "hidden";
	alert("Not a valid User");
}





}
