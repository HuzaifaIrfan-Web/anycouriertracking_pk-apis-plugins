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
 * @package           madhurcouriers_in_scraper_api_plugin
 *
 * @wordpress-plugin
 * Plugin Name:       Madhurcouriers in Scraper API Plugin
 * Plugin URI:        http://huzaifairfan.com/
 * Description:       Display Madhurcouriers in Tracking Details on your Wordpress Website
 * Version:           1.0.0
 * Author:            Huzaifa Irfan
 * Author URI:        http://huzaifairfan.com/
 * License:           GPL-2.0+
 * License URI:       http://www.gnu.org/licenses/gpl-2.0.txt
 * Text Domain:       madhurcouriers_in_scraper_api_plugin
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
define( 'madhurcouriers_in_SCRAPER_API_PLUGIN_VERSION', '1.0.0' );

/**
 * The code that runs during plugin activation.
 * This action is documented in includes/class-madhurcouriers_in_scraper_api_plugin-activator.php
 */
function activate_madhurcouriers_in_scraper_api_plugin() {
	require_once plugin_dir_path( __FILE__ ) . 'includes/class-madhurcouriers_in_scraper_api_plugin-activator.php';
	madhurcouriers_in_scraper_api_plugin_Activator::activate();


           $post = array(     
             'post_content'   => '
            [madhurcouriers_in_track_form]
            [madhurcouriers_in_track_details]

             ', //content of page
             'post_title'     =>'MadhurCouriers IN Shipment Details', //title of page
             'post_status'    =>  'publish' , //status of page - publish or draft
             'post_type'      =>  'page'  // type of post
   );
   wp_insert_post( $post ); // creates page

}

/**
 * The code that runs during plugin deactivation.
 * This action is documented in includes/class-madhurcouriers_in_scraper_api_plugin-deactivator.php
 */
function deactivate_madhurcouriers_in_scraper_api_plugin() {
	require_once plugin_dir_path( __FILE__ ) . 'includes/class-madhurcouriers_in_scraper_api_plugin-deactivator.php';
	madhurcouriers_in_scraper_api_plugin_Deactivator::deactivate();
}

register_activation_hook( __FILE__, 'activate_madhurcouriers_in_scraper_api_plugin' );
register_deactivation_hook( __FILE__, 'deactivate_madhurcouriers_in_scraper_api_plugin' );

/**
 * The core plugin class that is used to define internationalization,
 * admin-specific hooks, and public-facing site hooks.
 */
require plugin_dir_path( __FILE__ ) . 'includes/class-madhurcouriers_in_scraper_api_plugin.php';

/**
 * Begins execution of the plugin.
 *
 * Since everything within the plugin is registered via hooks,
 * then kicking off the plugin from this point in the file does
 * not affect the page life cycle.
 *
 * @since    1.0.0
 */
function run_madhurcouriers_in_scraper_api_plugin() {

	$plugin = new madhurcouriers_in_scraper_api_plugin();
	$plugin->run();

}
run_madhurcouriers_in_scraper_api_plugin();





// Plugin Code Start





function madhurcouriers_in_track_submit_func(){


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
    
    $content .="
<h2 align='center'>
Invalid Tracking Number
</h2>
";

    return $content;
}

if ($httpCode == 404) {
    
    $content .="
<h2 align='center'>
Tracking Details Not Found
</h2>
";

    return $content;
}

curl_close($ch);

// $res = json_decode(file_get_contents($madhurcouriers_in_tracking_api_url), true);
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
<h3 class='madhurcouriers_in_red cls-trackno'>
Tracking Number : 
";

$content .=$tnum;

$content .="
</h3>
";










$track_histories=array_reverse($res['track_histories']);


if($track_histories){

$content .="
<div class='track-history'  style='overflow-x:scroll;'>
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
        
        Transaction Type
        
    </th>

    <th>

    Status
   
</th>

    <th>

    Remarks
   
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

$content .=$item['Date'];

$content .='
    </td>
    <td >
   ';

$content .=$item['Transaction_Type'];


$content .='
    </td>   

     <td >
   ';

$content .=$item['Status'];


$content .='
    </td>

    <td >
   ';

$content .=$item['Remark'];


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

add_shortcode('madhurcouriers_in_track_details','madhurcouriers_in_track_submit_func');














function madhurcouriers_in_track_form_func(){

    if (isset($_GET['tnum']))
{
    $tnum = $_GET['tnum'];
}else{

    $tnum = '';
}


$madhurcouriers_in_tracking_details_url= get_option('madhurcouriers_in_tracking_details_url','/index.php/madhurcouriers-in-shipment-details/');


 
    $content = "


<form method='get' action='
";

 $content .=$madhurcouriers_in_tracking_details_url;

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

add_shortcode('madhurcouriers_in_track_form','madhurcouriers_in_track_form_func');



















function madhurcouriers_in_scraper_admin(){
    add_menu_page('madhurcouriers_in Scraper Admin','madhurcouriers_in Scraper Admin','manage_options','madhurcouriers_in-scraper-admin','madhurcouriers_in_scraper_admin_page','',200);
}

add_action('admin_menu','madhurcouriers_in_scraper_admin');


function madhurcouriers_in_scraper_admin_page(){

if(array_key_exists('submit_api_url', $_POST)){
    update_option('madhurcouriers_in_tracking_api_url',$_POST['api_url']);
    update_option('madhurcouriers_in_tracking_details_url',$_POST['details_url']);

?>
<div id="setting-error-settings-updated" class="updated settings-error notice is-dismissible">
<strong>API URL Saved!!</strong>
</div>

<?php

}




    $madhurcouriers_in_tracking_api_url= get_option('madhurcouriers_in_tracking_api_url','http://localhost/track/madhurcouriers_in_scraper_api');
    $madhurcouriers_in_tracking_details_url= get_option('madhurcouriers_in_tracking_details_url','/index.php/madhurcouriers-in-shipment-details/');

    
?>


<h2>
madhurcouriers_in Scraper API Plugin Admin Page
</h2>



<form method="post" action="">

<label for="api_url">API URL:</label>
<input type="text" name="api_url" value="<?php print $madhurcouriers_in_tracking_api_url; ?>"/>
<br/>
<label for="details_url">Tracking Details URL:</label>
<input type="text" name="details_url" value="<?php print $madhurcouriers_in_tracking_details_url; ?>"/>
<br/>
<input type="submit" name="submit_api_url" class="button button-primary">
</form>

<?php


}


?>