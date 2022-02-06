<?php

/**
 * Provide a public-facing view for the plugin
 *
 * This file is used to markup the public-facing aspects of the plugin.
 *
 * @link       http://huzaifairfan.com/
 * @since      1.0.0
 *
 * @package    intelcom_ca_scraper_api_plugin
 * @subpackage intelcom_ca_scraper_api_plugin/public/partials
 */
?>

<!-- This file should primarily consist of HTML with a little bit of PHP. -->



<?php 

// function intelcom_ca_track_submit_func(){

  


if (isset($_GET['tnum']))
{
    $tnum = $_GET['tnum'];
}else{

    $tnum = '';
}





    if($tnum ==''){
    
      ?>


<h3 align='center'>
Please Enter a Valid Tracking Number
</h3>





<?php 
    }else{

?> 
        
<!-- 
<h4 class='tracking-results-title'>
Tracking Result
</h4> -->

<?php 


   
 $intelcom_ca_tracking_api_url= get_option('intelcom_ca_tracking_api_url','http://localhost/track/intelcom_ca_scraper_api');

$intelcom_ca_tracking_api_url .=  '?tnum='; 
$intelcom_ca_tracking_api_url .= $tnum;


// $intelcom_ca_tracking_api_url=str_replace(" ","%20",$intelcom_ca_tracking_api_url);

// var_dump($intelcom_ca_tracking_api_url);

$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, $intelcom_ca_tracking_api_url); 
curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1); 
$output = curl_exec($ch);   

$res = json_decode($output, true);

  // var_dump($output);


$httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);

if ($httpCode == 422) {
  ?>
  <br/>
<h2 align='center'>
Invalid Tracking Number
</h2>


<?php 
 return $content;
}



if ($httpCode == 404) {
    
  ?>
  <br/>
  <h2 align='center'>
  Tracking Details Not Found
  </h2>
  
  <?php 
  
      return $content;
  }



curl_close($ch);

// $res = json_decode(file_get_contents($intelcom_ca_tracking_api_url), true);
// print_r($res);

if($res == false){
?>

<h2 align='center'>
Please Enter a Valid Tracking Number
</h2>

<?php 
}else{




?>


<div class='jumbotron' style='display:flex; flex-direction:column;'>
<h3 class='intelcom_ca_red cls-trackno'>






</h3>



<?php 
$status=$res['track_histories'];

if($status){
	
	$deliveryStatus = 4; 

    ?>

<link rel="stylesheet" href="https://pro.fontawesome.com/releases/v5.10.0/css/all.css" integrity="sha384-AYmEC3Yw5cVb3ZcuHtOA93w35dYTsvhLPVnYs9eStHfGJvOvKxVfELGroGkvsg+p" crossorigin="anonymous"/>




 




<script>
   const progress = document.getElementById("progress");
const circles = document.querySelectorAll(".circle");


let currentActive = 4;

update();




function update() {
  circles.forEach((circle, idx) => {
    if (idx < currentActive) {
      circle.classList.add("active");
    } else {
      circle.classList.remove("active");
    }
  });
  const actives = document.querySelectorAll(".active");

  progress.style.width =
    ((actives.length - 1) / (circles.length - 1)) * 100 + "%";


}

</script>

<?php 


}








$track_histories=$res['track_histories'];


if($track_histories){

  ?>


<div class='track-history' style='overflow-x:auto;' >
<h4 style="font-weight:bold">
Track History for: <?php echo $tnum; ?>
</h4>


<div class="card card-stepProgress-Div  " style="margin:0% 2% 5% 2%;padding:2% 0%;">
      <div class="container" style="">

                  
               <ul class="StepProgress ">
                 <?php foreach($track_histories as $item) {
                   ?>

                  <li class="StepProgress-item is-done">
                   <span class="transaction-type"><strong> <?php echo strtolower($item['track_title']);?></strong> </span>
                     
                   <span class="status-type"><?php echo strtolower($item['track_text']);?> </span>  

                   <br> 
                   
                   <span class="date-type"> <i class="fas fa-clock fa-black-color" aria-hidden="true"></i> <?php echo strtolower($item['datetime']); ?>
                  </span>
                  
                  </li>        
                  
                  <?php }?>
                 
               </ul>
                        
      </div>
   </div>



</div>

<?php 


}else{

  ?>


<h2 align='center'>
Tracking Details Not Found!
</h2>










</div>


<?php 


   }


}






}


