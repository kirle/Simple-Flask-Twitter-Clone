
function confirmRemove(){
  if(!confirm("Are you sure?")){
    return false;
  } else{
    return true;
  }
}

function validateUsername(){
  var text = document.getElementById("username");
  if(text.value == ""){ 
    text.style.borderColor = "red";
    //alert("Username not valid: "+ u);
    return false;
  }
  return true;
}

function validateTweet(){
  var text = document.getElementById("inputText");
  if (text.value == ""){
    text.style.borderColor = "red";
    //alert("Cant be empty");
    return false
  } 
  if (text.value.length > 150) {
    text.style.borderColor = "red";
    alert("Too long");
    return false
  }

  return true;

}

