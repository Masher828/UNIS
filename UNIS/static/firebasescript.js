// Your web app's Firebase configuration
  var firebaseConfig = {
    apiKey: "AIzaSyAHFF2PmthKh8FZ3HVfryK5RiBAz1xpZ_s",
    authDomain: "unistest-4f24c.firebaseapp.com",
    databaseURL: "https://unistest-4f24c.firebaseio.com",
    projectId: "unistest-4f24c",
    storageBucket: "unistest-4f24c.appspot.com",
    messagingSenderId: "970223467921",
    appId: "1:970223467921:web:ce1a4c134fd36ac4b06e30",
    measurementId: "G-33VFZHS024"
  };
  // Initialize Firebase
  firebase.initializeApp(firebaseConfig);

  console.log("all ri8");
   var database = firebase.database();
  console.log("all ri8-2");




  var adminid=document.getElementById("adminusername").value;
  var pathfornewmessage="contact_table/"+adminid+"/";




  function newchatnotifyfb(adminuserid, seconduserid) {
    var temp = "contact_table/"+seconduserid+"/"+adminuserid+"/";


    return firebase.database().ref(temp).once('value').then(function(snapshot) {
      var tt =snapshot.val().newmessage;
      var tt1=snapshot.val().istyping;

      if(tt=="yes"){
        database.ref(temp).set({
          newmessage: "yesss",
          istyping : tt1,

        });
      }

      else if(tt=="yesss"){

        database.ref(temp).set({
          newmessage: "yes",
          istyping : tt1,

        });
      }

      else if(tt=="no"){
        database.ref(temp).set({
          newmessage: "yes",
          istyping : tt1,

        });

      }
      // ...
    });







}




var starCountRef = firebase.database().ref(pathfornewmessage);
starCountRef.on('value', function(snapshot) {
  var list=[];
  var istypinglist=[];
  var istypingremovelist=[];
  var correctionlistformistyping =[];
  var check=0;
  var check2=0;
  var check3=0;
  snapshot.forEach((child) => {
  // console.log(child.key, child.val().newmessage);
   if(child.val().newmessage=="yes" || child.val().newmessage=="yesss" )
          { check=1;
            list.push(child.key);
            correctionlistformistyping.push(child.key);
          }

if(child.val().istyping=="yes")
{
  check2=1;
  istypinglist.push(child.key);
}

if(child.val().istyping=="no")
{
  check3=1;
  istypingremovelist.push(child.key);
}


 });
 if(check==1)
 {try{
   list.forEach(function(entry) {
      var tt="sn"+entry;
      var imgtt ="chatnmes"+entry;
      if(global_sendtouser==entry){
          showchatofthatuser(global_sendtouser);
        document.getElementById(tt).innerHTML="HI there i am using";
         document.getElementById(imgtt).style.visibility = "visible";
         changefbnewmessage(entry);



       }
       else{
//adding code so new msg doesnt show if already new messages are there
      if(istypinglist.includes(entry)  ||  document.getElementById(tt).innerHTML=='<span style="color : blue">new message.</span>'){}else{
      //  var trs=document.getElementById(tt).innerHTML;

        //alert(trs);

         document.getElementById(tt).innerHTML="<span style='color : blue'>new message.</span>";
       document.getElementById(imgtt).style.visibility = "visible";
       //Noty
    //   alert("new msg");
       new Noty({
         type: 'success',
         theme: 'nest',
         layout: 'topRight',
           text: 'New Message!',
             timeout: 2000,

       }).show();
       //noty

     }




     }
   });
 }catch(error){}

 }



 if(check2==1)
 {
   try{
     istypinglist.forEach(function(entry1) {
       var tttypingchats ="sn"+entry1;

        if(global_sendtouser==entry1){
          document.getElementById("chatheaderstatus").innerHTML="";
          $("#chatheaderstatus").append("<span style='color : green'><b>is typing...</b></span>")
         }
         //alert("typing changes");
// document.getElementById(tttypingchats).innerHTML="<span style='color : green'>is typing...</span>";
var ttrt="typingbyid"+entry1;
document.getElementById(ttrt).style.visibility="visible";

         //else{document.getElementById(tt).innerHTML="new message";}
     });

   }
   catch(error){}

 }

if(check3==1)
{
  try{
    istypingremovelist.forEach(function(entry2) {
       var tttypingchats1 ="sn"+entry2;
       if(global_sendtouser==entry2){
         document.getElementById("chatheaderstatus").innerHTML="";
         $("#chatheaderstatus").append("<span style=''><b></b></span>")
        }
      //  document.getElementById(tttypingchats1).innerHTML="";
      var ttrt="typingbyid"+entry2;
      document.getElementById(ttrt).style.visibility="hidden";
        //else{document.getElementById(tt).innerHTML="new message";}
    });

  }
  catch(error){}

}








});






function loadreadstatusonchatload(){
  var starCountRef = firebase.database().ref(pathfornewmessage);
  starCountRef.on('value', function(snapshot) {
    var list=[];
    //var ilist=[];
    var check=0;
    snapshot.forEach((child) => {
     console.log(child.key, child.val().newmessage);
     if(child.val().newmessage=="yes" || child.val().newmessage=="yesss")
            { check=1;
              list.push(child.key);}

   });
   if(check==1)
   {try{
     list.forEach(function(entry) {
        var tt="sn"+entry;
        var imgtt ="chatnmes"+entry;

        // alert(global_sendtouser);

          document.getElementById(tt).innerHTML="<span style='color : blue'>new message.</span>";
           document.getElementById(imgtt).style.visibility = "visible";

        //   alert("noe i m called");
     });
   }catch(error){}

   }



  });


}








//chage read Status
function changefbnewmessage(id){
//  alert("fbcalled");
    var tempa = "contact_table/"+adminid+"/"+id+"/";
    var imgtt ="chatnmes"+id;

    return firebase.database().ref(tempa).once('value').then(function(snapshot) {
      var tt =snapshot.val().istyping;

      database.ref(tempa).set({
        istyping : tt,
        newmessage: "no",

      });
        document.getElementById(imgtt).style.visibility = "hidden";
    });






}




//isonline

$( "#chat" )
  .focusout(function() {
    console.log("focus lost");
  var localpath = "contact_table/"+global_sendtouser+"/"+adminid+"/";


  return firebase.database().ref(localpath).once('value').then(function(snapshot) {
  var tt =snapshot.val().newmessage;
  // ...
  database.ref(localpath).set({
    newmessage: tt,
    istyping: "no",

  });
});







  });


  $( "#chat" ).focus(function() {
  console.log("focus gained");
var localpath = "contact_table/"+global_sendtouser+"/"+adminid+"/";

  return firebase.database().ref(localpath).once('value').then(function(snapshot) {
  var tt =snapshot.val().newmessage;

  database.ref(localpath).set({
    newmessage: tt,
    istyping: "yes",

  });
  // ...
});




});



//check if user is there or not
// function checkfbuser(){
//   //alert(adminid);
//   var chk= "contact_table/";
//   try{
//   return firebase.database().ref(chk).once('value').then(function(snapshot) {
//       if(snapshot.hasChild(adminid)){alert("hai bhai");} else{
//         var localpath="contact_table/"+adminid+"/";
//        usersRef = firebase.database().ref(chk);
//         usersRef.push("name");
//
//         }
//
//
//       });}
//
//   catch(error){alert(error);}
//
// }


function checkfbuser(useridtocheck=adminid){

  var chk="global_users/"

  try{
   return firebase.database().ref(chk).once('value').then(function(snapshot) {
       if(snapshot.hasChild(useridtocheck)){ } else{




//code to add user in global accounts
              var t21 = "global_users/"+useridtocheck+"/";
                  database.ref(t21).set({
                  isonline:"no",
                  firsttime : "yes",

                  });
//code to add user in chat db
        var t22 = "contact_table/"+useridtocheck+"/"+"postgresfrnd/";

        database.ref(t22).set({
        newmessage: "no",
        istyping:"no",

        });



         }


       });}

   catch(error){alert(error);}

 }




function addfrndsinfirebase(firstid,secondid)
{
  var chk1 = "contact_table/"+firstid+"/"+secondid+"/";
  var chk2 = "contact_table/"+secondid+"/"+firstid+"/";
  database.ref(chk1).set({
  newmessage: "no",
  istyping:"no",

  });


  database.ref(chk2).set({
  newmessage: "no",
  istyping:"no",

  });


}





//setting online status in divs
var starCountRef2 = firebase.database().ref('global_users/');
starCountRef2.on('value', function(snapshot) {
for(var i=0;i<listoffriendsforfirebase.length;i++)
{
var pathr='global_users/'+listoffriendsforfirebase[i];
var ids='badgeonline'+listoffriendsforfirebase[i];
var sid =listoffriendsforfirebase[i];
updatedotstatus(pathr,ids,sid)

}
});


function callonlinecheckeronchatopen(){


  for(var i=0;i<listoffriendsforfirebase.length;i++)
  {
  var pathr='global_users/'+listoffriendsforfirebase[i];
  var ids='badgeonline'+listoffriendsforfirebase[i];
  var sid= listoffriendsforfirebase[i]

  updatedotstatus(pathr,ids,sid)

  }



}


function updatedotstatus(pathr,ids,sid){
  firebase.database().ref(pathr).once('value').then(function(snapshot) {
  var ttx =snapshot.val().isonline;
  console.log(ids);
//  var ids="badgeonline"+listoffriendsforfirebase[i];
  //alert(ids);

if(global_sendtouser==sid)
{
  if(ttx=="yes")
{document.getElementById("chatheaderonlinebubble").style.visibility = "visible";}
else if(ttx=="no")
{document.getElementById("chatheaderonlinebubble").style.visibility = "hidden";}

}


  if(ttx=="yes")
  {
    document.getElementById(ids).style.visibility = "visible";
  }
  else if(ttx=="no")
  {
   document.getElementById(ids).style.visibility = "hidden";
 }



  // database.ref(localpath).set({
  //   newmessage: tt,
  //   istyping: "yes",

  // });
  // ...
});
}

//setting online status in divs ends






//update current user online status
function updatecurrentuseronlinestatus(value)
{
  var pathhere = "global_users/"+adminid;
  firebase.database().ref(pathhere).once('value').then(function(snapshot) {
var tempdata1 = snapshot.val().firsttime;



database.ref(pathhere).set({
isonline:value,
firsttime : tempdata1,

});
  // ...
});
}

//update ends
