<?php


   if($_POST['user_id'] == 1 || $_POST['user_id'] == '1'){
    $arr = array("message"=>"OK",
    "stories"=> array(["id"=> 1,
    "story_text"=> "I feel broken heart, and lonely.",
    "quotes"=> "A vase need to be thrown to the fire to be a stronger Vase.",
    "datetime"=>"8 June 2022"],["id"=> 2,
    "story_text"=> "I'm fired from my job, got no money.",
    "quotes"=> "The way I see it, if you want the rainbow, you gotta put up with the rain.",
    "datetime"=>"5 June 2022"],["id"=> 3,
    "story_text"=> "I'm fired from my job, got no money.",
    "quotes"=> "Sometimes what we feared is nothing than hallucination.",
    "datetime"=>"5 June 2022"]));
             
   }
   else{
    $arr = array("message"=>"No history list was found");

   }



  echo json_encode($arr);

?>