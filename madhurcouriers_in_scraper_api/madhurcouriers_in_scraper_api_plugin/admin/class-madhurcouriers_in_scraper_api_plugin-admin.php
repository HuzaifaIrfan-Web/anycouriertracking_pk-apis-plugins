<?php

/**
 * The admin-specific functionality of the plugin.
 *
 * @link       http://huzaifairfan.com/
 * @since      1.0.0
 *
 * @package    madhurcouriers_in_scraper_api_plugin
 * @subpackage madhurcouriers_in_scraper_api_plugin/admin
 */

/**
 * The admin-specific functionality of the plugin.
 *
 * Defines the plugin name, version, and two examples hooks for how to
 * enqueue the admin-specific stylesheet and JavaScript.
 *
 * @package    madhurcouriers_in_scraper_api_plugin
 * @subpackage madhurcouriers_in_scraper_api_plugin/admin
 * @author     Huzaifa Irfan <huzaifairfan2001@gmail.com>
 */
class madhurcouriers_in_scraper_api_plugin_Admin {

	/**
	 * The ID of this plugin.
	 *
	 * @since    1.0.0
	 * @access   private
	 * @var      string    $plugin_name    The ID of this plugin.
	 */
	private $plugin_name;

	/**
	 * The version of this plugin.
	 *
	 * @since    1.0.0
	 * @access   private
	 * @var      string    $version    The current version of this plugin.
	 */
	private $version;

	/**
	 * Initialize the class and set its properties.
	 *
	 * @since    1.0.0
	 * @param      string    $plugin_name       The name of this plugin.
	 * @param      string    $version    The version of this plugin.
	 */
	public function __construct( $plugin_name, $version ) {

		$this->plugin_name = $plugin_name;
		$this->version = $version;


	function	madhurcouriers_in_scraper_admin_page()
		{
			require_once 'partials/madhurcouriers_in_scraper_api_plugin-admin-display.php';
		}

				
		function madhurcouriers_in_scraper_admin(){
			add_menu_page('Madhurcouriers.in Scraper Admin','Madhurcouriers.in Scraper Admin','manage_options','madhurcouriers_in-scraper-admin','madhurcouriers_in_scraper_admin_page','',200);
		}

		add_action('admin_menu','madhurcouriers_in_scraper_admin');

	}

	/**
	 * Register the stylesheets for the admin area.
	 *
	 * @since    1.0.0
	 */
	public function enqueue_styles() {

		/**
		 * This function is provided for demonstration purposes only.
		 *
		 * An instance of this class should be passed to the run() function
		 * defined in madhurcouriers_in_scraper_api_plugin_Loader as all of the hooks are defined
		 * in that particular class.
		 *
		 * The madhurcouriers_in_scraper_api_plugin_Loader will then create the relationship
		 * between the defined hooks and the functions defined in this
		 * class.
		 */

		wp_enqueue_style( $this->plugin_name, plugin_dir_url( __FILE__ ) . 'css/madhurcouriers_in_scraper_api_plugin-admin.css', array(), $this->version, 'all' );

	}

	/**
	 * Register the JavaScript for the admin area.
	 *
	 * @since    1.0.0
	 */
	public function enqueue_scripts() {

		/**
		 * This function is provided for demonstration purposes only.
		 *
		 * An instance of this class should be passed to the run() function
		 * defined in madhurcouriers_in_scraper_api_plugin_Loader as all of the hooks are defined
		 * in that particular class.
		 *
		 * The madhurcouriers_in_scraper_api_plugin_Loader will then create the relationship
		 * between the defined hooks and the functions defined in this
		 * class.
		 */

		wp_enqueue_script( $this->plugin_name, plugin_dir_url( __FILE__ ) . 'js/madhurcouriers_in_scraper_api_plugin-admin.js', array( 'jquery' ), $this->version, false );

	}

}
