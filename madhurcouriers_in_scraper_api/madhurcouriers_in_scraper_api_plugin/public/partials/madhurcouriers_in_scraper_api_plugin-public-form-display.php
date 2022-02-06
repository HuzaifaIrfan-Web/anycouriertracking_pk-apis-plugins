<?php

/**
 * Provide a public-facing view for the plugin
 *
 * This file is used to markup the public-facing aspects of the plugin.
 *
 * @link       http://huzaifairfan.com/
 * @since      1.0.0
 *
 * @package    stcourier_scraper_api_plugin
 * @subpackage stcourier_scraper_api_plugin/public/partials
 */
?>

<!-- This file should primarily consist of HTML with a little bit of PHP. -->
<?php 

// function madhurcouriers_in_track_form_func(){

if (isset($_GET['tnum']))
{
$tnum = $_GET['tnum'];
}else{

$tnum = '';
}


$madhurcouriers_in_tracking_details_url= get_option('madhurcouriers_in_tracking_details_url','/madhurcouriers-in-shipment-details');



?>


<form method='get' action='<?php echo $madhurcouriers_in_tracking_details_url;?>'>
<div  style='display:flex; flex-direction:column; width:100%;'>
<h4 for='tnum' style="font-weight:bold;">Tracking Number:</h4>
<div style='display:flex; width:100%;' >
<input  style='display:flex; width:100%;' name='tnum' type='text'  placeholder='Tracking Number'
value='<?php echo $tnum;?>'/>
<input type='submit' value='Track'/>

</div></div>
</form>



<?php 






add_shortcode('madhurcouriers_in_track_form','madhurcouriers_in_track_form_func');