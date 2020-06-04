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
  var check=0;
  var check2=0;
  var check3=0;
  snapshot.forEach((child) => {
  // console.log(child.key, child.val().newmessage);
   if(child.val().newmessage=="yes" || child.val().newmessage=="yesss" )
          { check=1;
            list.push(child.key);}

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
         document.getElementById(imgtt).style.visibility = "hidden";
         changefbnewmessage(entry);



       }
       else{document.getElementById(tt).innerHTML="new message";
       document.getElementById(imgtt).style.visibility = "visible";

     }
   });
 }catch(error){}

 }



 if(check2==1)
 {
   try{
     istypinglist.forEach(function(entry1) {

        if(global_sendtouser==entry1){
          document.getElementById("chatheaderstatus").innerHTML="";
          $("#chatheaderstatus").append("<span style='color : green'><b>is typing...</b></span>")
         }
         //else{document.getElementById(tt).innerHTML="new message";}
     });

   }
   catch(error){}

 }

if(check3==1)
{
  try{
    istypingremovelist.forEach(function(entry2) {

       if(global_sendtouser==entry2){
         document.getElementById("chatheaderstatus").innerHTML="";
         $("#chatheaderstatus").append("<span style=''><b></b></span>")
        }
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

          document.getElementById(tt).innerHTML="new message";
           document.getElementById(imgtt).style.visibility = "visible";
     });
   }catch(error){}

   }



  });


}








//chage read Status
function changefbnewmessage(id){
    var temp = "contact_table/"+adminid+"/"+id+"/";
    var imgtt ="chatnmes"+id;

    return firebase.database().ref(temp).once('value').then(function(snapshot) {
      var tt =snapshot.val().istyping;

      database.ref(temp).set({
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
