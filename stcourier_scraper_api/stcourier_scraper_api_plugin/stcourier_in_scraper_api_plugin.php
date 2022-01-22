<?php

/**
 * The plugin bootstrap file
 *
 * This file is read by WordPress to generate the plugin information in the plugin
 * admin area. This file also includes all of the dependencies used by the plugin,
 * registers the activation and deactivation functions, and defines a function
 * that starts the plugin.
 *
 * @link              http://huzaifairfan.com/
 * @since             1.0.0
 * @package           stcourier_scraper_api_plugin
 *
 * @wordpress-plugin
 * Plugin Name:       Stcourier Scraper API Plugin
 * Plugin URI:        http://huzaifairfan.com/
 * Description:       Display Stcourier Tracking Details on your Wordpress Website
 * Version:           1.0.0
 * Author:            Huzaifa Irfan
 * Author URI:        http://huzaifairfan.com/
 * License:           GPL-2.0+
 * License URI:       http://www.gnu.org/licenses/gpl-2.0.txt
 * Text Domain:       stcourier_scraper_api_plugin
 * Domain Path:       /languages
 */

// If this file is called directly, abort.
if ( ! defined( 'WPINC' ) ) {
    die("Hey, what are you doing here? You silly human!");
}


/**
 * Currently plugin version.
 * Start at version 1.0.0 and use SemVer - https://semver.org
 * Rename this for your plugin and update it as you release new versions.
 */
define( 'stcourier_SCRAPER_API_PLUGIN_VERSION', '1.0.0' );

/**
 * The code that runs during plugin activation.
 * This action is documented in includes/class-stcourier_scraper_api_plugin-activator.php
 */
function activate_stcourier_scraper_api_plugin() {
	require_once plugin_dir_path( __FILE__ ) . 'includes/class-stcourier_scraper_api_plugin-activator.php';
	stcourier_scraper_api_plugin_Activator::activate();


           $post = array(     
             'post_content'   => '
            [stcourier_track_form]
            [stcourier_track_details]

             ', //content of page
             'post_title'     =>'STCourier Shipment Details', //title of page
             'post_status'    =>  'publish' , //status of page - publish or draft
             'post_type'      =>  'page'  // type of post
   );
   wp_insert_post( $post ); // creates page

}

/**
 * The code that runs during plugin deactivation.
 * This action is documented in includes/class-stcourier_scraper_api_plugin-deactivator.php
 */
function deactivate_stcourier_scraper_api_plugin() {
	require_once plugin_dir_path( __FILE__ ) . 'includes/class-stcourier_scraper_api_plugin-deactivator.php';
	stcourier_scraper_api_plugin_Deactivator::deactivate();
}

register_activation_hook( __FILE__, 'activate_stcourier_scraper_api_plugin' );
register_deactivation_hook( __FILE__, 'deactivate_stcourier_scraper_api_plugin' );

/**
 * The core plugin class that is used to define internationalization,
 * admin-specific hooks, and public-facing site hooks.
 */
require plugin_dir_path( __FILE__ ) . 'includes/class-stcourier_scraper_api_plugin.php';

/**
 * Begins execution of the plugin.
 *
 * Since everything within the plugin is registered via hooks,
 * then kicking off the plugin from this point in the file does
 * not affect the page life cycle.
 *
 * @since    1.0.0
 */
function run_stcourier_scraper_api_plugin() {

	$plugin = new stcourier_scraper_api_plugin();
	$plugin->run();

}
run_stcourier_scraper_api_plugin();





// Plugin Code Start





function stcourier_track_submit_func(){


if (isset($_GET['tnum']))
{
    $tnum = $_GET['tnum'];
}else{

    $tnum = '';
}





    if($tnum ==''){
    
$content .="

<h3 align='center'>
Please Enter a Valid Tracking Number
</h3>



";


    }else{
        
        $content="
<h2 class='tracking-results-title'>
Tracking Result
</h2>
";



   
    $stcourier_tracking_api_url= get_option('stcourier_tracking_api_url','http://localhost/track/stcourier_scraper_api');

$stcourier_tracking_api_url .=  '?tnum='; 
$stcourier_tracking_api_url .= $tnum;


// $stcourier_tracking_api_url=str_replace(" ","%20",$stcourier_tracking_api_url);

// var_dump($stcourier_tracking_api_url);

$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, $stcourier_tracking_api_url); 
curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1); 
$output = curl_exec($ch);   

$res = json_decode($output, true);

  // var_dump($output);


$httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);

if ($httpCode == 422) {
    
    $content .="
<h2 align='center'>
Invalid Tracking Number
</h2>
";

    return $content;
}

curl_close($ch);

// $res = json_decode(file_get_contents($stcourier_tracking_api_url), true);
// print_r($res);

if($res == false){

$content .="
<h2 align='center'>
Please Enter a Valid Tracking Number
</h2>
";

}else{






$content .="
<br />
<br />
<div class='jumbotron' style='display:flex; flex-direction:column;'>
<h3 class='stcourier_red cls-trackno'>
Tracking Number : 
";

$content .=$tnum;

$content .="
</h3>
";



$status=$res['status'];

if($status){

$content .="
<div class='delivery-status'>
<h3>
Delivery Status:
</h3>
";






$content .="

<p>
Current Status :  
";

$content .=$status['Current_Status'];


$content .="
<br/>
Orgin SRC :  
";
$content .=$status['Orgin_SRC'];

$content .="
<br/>
Destination :  
";
$content .=$status['Destination'];

$content .="
<br/>
Consignment :  
";
$content .=$status['Consignment'];


$content .="
<br/>
Book Date/Time :  
";
$content .=$status['Book_DateTime'];

$content .="
<br/>
Delivery Date/Time :  
";
$content .=$status['Delivery_DateTime'];


$content .="
</p>
</div>
";

}








$track_histories=$res['track_histories'];


if($track_histories){

$content .="
<div class='track-history' style='overflow-x:scroll;' >
<h3>
Track History:
</h3>
";

$content .='
<table class="table table-hover">
<thead>
  <tr>
    <th>
        
        Date
       
    </th>

    <th>
        
       Time
        
    </th>

    <th>

    Status
   
</th>

    <th>

    Location
   
</th>
  </tr>
</thead>
<tbody>
';

foreach($track_histories as $item) 
{


$content .='
  <tr class="list-item" >
    <td >
    ';

$content .=$item['date'];

$content .='
    </td>
    <td >
   ';

$content .=$item['time'];


$content .='
    </td>   

     <td >
   ';

$content .=$item['tracking_title'];


$content .='
    </td>

    <td >
   ';

$content .=$item['span'];


// $content .='

//     </td>

//         <td >
//    ';

// $content .=$item['p'];


$content .='

    </td>

    </tr>

   ';



}


$content .='
</tbody>
</table>
</div>

   ';


}else{

    $content .="
<h2 align='center'>
Nothing Found!!
</h2>
";


}








$content .='


</div>



   ';

   }


}





    return $content;
}

add_shortcode('stcourier_track_details','stcourier_track_submit_func');














function stcourier_track_form_func(){

    if (isset($_GET['tnum']))
{
    $tnum = $_GET['tnum'];
}else{

    $tnum = '';
}


$stcourier_tracking_details_url= get_option('stcourier_tracking_details_url','/index.php/stcourier-shipment-details/');


 
    $content = "


<form method='get' action='
";

 $content .=$stcourier_tracking_details_url;

 $content .="
'>
<div style='display:flex; flex-direction:column; width:90%;'>

 <h3 for='tnum'>Tracking Number:</h3>
 <div style='display:flex; '>
<input name='tnum' type='text'  placeholder='Tracking Number'
value='
";

 $content .= $tnum;


 $content .="
'

/>
<input  type='submit' value='Track'/>

</div></div>
</form>



    ";




    return $content;
}

add_shortcode('stcourier_track_form','stcourier_track_form_func');



















function stcourier_scraper_admin(){
    add_menu_page('stcourier Scraper Admin','stcourier Scraper Admin','manage_options','stcourier-scraper-admin','stcourier_scraper_admin_page','',200);
}

add_action('admin_menu','stcourier_scraper_admin');


function stcourier_scraper_admin_page(){

if(array_key_exists('submit_api_url', $_POST)){
    update_option('stcourier_tracking_api_url',$_POST['api_url']);
    update_option('stcourier_tracking_details_url',$_POST['details_url']);

?>
<div id="setting-error-settings-updated" class="updated settings-error notice is-dismissible">
<strong>API URL Saved!!</strong>
</div>

<?php

}




    $stcourier_tracking_api_url= get_option('stcourier_tracking_api_url','http://localhost/track/stcourier_scraper_api');
    $stcourier_tracking_details_url= get_option('stcourier_tracking_details_url','/index.php/stcourier-shipment-details/');

    
?>


<h2>
Stcourier Scraper API Plugin Admin Page
</h2>



<form method="post" action="">

<label for="api_url">API URL:</label>
<input type="text" name="api_url" value="<?php print $stcourier_tracking_api_url; ?>"/>
<br/>
<label for="details_url">Tracking Details URL:</label>
<input type="text" name="details_url" value="<?php print $stcourier_tracking_details_url; ?>"/>
<br/>
<input type="submit" name="submit_api_url" class="button button-primary">
</form>

<?php


}


?>