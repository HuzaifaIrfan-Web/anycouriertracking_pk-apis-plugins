<?php

/**
 * Provide a public-facing view for the plugin
 *
 * This file is used to markup the public-facing aspects of the plugin.
 *
 * @link       http://huzaifairfan.com/
 * @since      1.0.0
 *
 * @package    madhurcouriers_in_scraper_api_plugin
 * @subpackage madhurcouriers_in_scraper_api_plugin/public/partials
 */
?>

<!-- This file should primarily consist of HTML with a little bit of PHP. -->



<?php 


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
<!-- <h2 class='tracking-results-title'>
Tracking Result
</h2> -->
<?php 



   
    $madhurcouriers_in_tracking_api_url= get_option('madhurcouriers_in_tracking_api_url','http://localhost/track/madhurcouriers_in_scraper_api');

$madhurcouriers_in_tracking_api_url .=  '?tnum='; 
$madhurcouriers_in_tracking_api_url .= $tnum;


// $madhurcouriers_in_tracking_api_url=str_replace(" ","%20",$madhurcouriers_in_tracking_api_url);

// var_dump($madhurcouriers_in_tracking_api_url);

$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, $madhurcouriers_in_tracking_api_url); 
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

// $res = json_decode(file_get_contents($madhurcouriers_in_tracking_api_url), true);
// print_r($res);

if($res == false){

?>

<h2 align='center'>
Please Enter a Valid Tracking Number
</h2>
<?php 

}else{






?>
<!-- <br />
<br /> -->
<div class='jumbotron' style='display:flex; flex-direction:column;'>
<h3 class='madhurcouriers_in_red cls-trackno'>


</h3>
<?php 









$track_histories=array_reverse($res['track_histories']);


if($track_histories){

	$deliveryStatus = 4; 

    ?>

<link rel="stylesheet" href="https://pro.fontawesome.com/releases/v5.10.0/css/all.css" integrity="sha384-AYmEC3Yw5cVb3ZcuHtOA93w35dYTsvhLPVnYs9eStHfGJvOvKxVfELGroGkvsg+p" crossorigin="anonymous"/>


<div class='track-history'  style='overflow-x:scroll;'>
<h4 style="font-weight:bold;">
Track History for: <?php echo $tnum; ?> 
</h4>



<div class="card" style="margin:5%;padding:2%;">
      <div class="container" style="">

                  
               <ul class="StepProgress ">
                 <?php foreach($track_histories as $item) {
                   ?>

                  <li class="StepProgress-item is-done"><strong><?php echo $item['Transaction_Type'];?></strong>
                     
                     <?php echo $item['Status'];?> 
                     <br>Remarks : <?php if($item['Remark'] ==''){echo "N/a";} else { echo $item['Remark'];}?>
                      <br> <i class="fas fa-clock fa-black-color" aria-hidden="true"></i> <?php echo $item['Date'];?> 
                  </li>        
                  
                  <?php }?>
                 
               </ul>
                        
      </div>
   </div>


</div>




</div>

<?php 


}else{

?>


<h2 align='center'>
Nothing Found!!
</h2>


<?php 


}








?>


</div>



<?php 

   }


}





  









