<?php

if($_POST['username'] == "string" && $_POST['password'] == "string"){
    $arr = array("username"=>"string",
              "name"=> "string",
              "biography"=> "string",
              "id"=> 1,
              "message"=>"OK",
              "stories"=> array("id"=> 1,
              "story_text"=> "Saya patah hati",
              "user_id"=> 1)); 
} 
else{
    $arr = array('message'=>"Wrong Username or Password");
}


  echo json_encode($arr);

?>