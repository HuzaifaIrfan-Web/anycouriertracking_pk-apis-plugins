<?php

/**
 * Provide a admin area view for the plugin
 *
 * This file is used to markup the admin-facing aspects of the plugin.
 *
 * @link       http://huzaifairfan.com/
 * @since      1.0.0
 *
 * @package    intelcom_ca_scraper_api_plugin
 * @subpackage intelcom_ca_scraper_api_plugin/admin/partials
 */
?>

<!-- This file should primarily consist of HTML with a little bit of PHP. -->


<?php 





if(array_key_exists('submit_api_url', $_POST)){
    update_option('intelcom_ca_tracking_api_url',$_POST['api_url']);
    update_option('intelcom_ca_tracking_details_url',$_POST['details_url']);

?>
<div id="setting-error-settings-updated" class="updated settings-error notice is-dismissible">
<strong>API URL Saved!!</strong>
</div>

<?php

}




    $intelcom_ca_tracking_api_url= get_option('intelcom_ca_tracking_api_url','http://localhost/track/intelcom_ca_scraper_api');
    $intelcom_ca_tracking_details_url= get_option('intelcom_ca_tracking_details_url','/intelcom-ca-shipment-details');

    
?>


<h2>
intelcom_ca Scraper API Plugin Admin Page
</h2>



<form method="post" action="">

<label for="api_url">API URL:</label>
<input type="text" name="api_url" value="<?php echo $intelcom_ca_tracking_api_url; ?>"/>
<br/>
<label for="details_url">Form Action URL:</label>
<input type="text" name="details_url" value="<?php echo $intelcom_ca_tracking_details_url; ?>"/>
<br/>
<input type="submit" name="submit_api_url" class="button button-primary">
</form>