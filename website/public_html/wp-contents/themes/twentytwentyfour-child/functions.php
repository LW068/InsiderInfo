<?php
add_action( 'wp_enqueue_scripts', 'my_child_theme_enqueue_styles' );
function my_child_theme_enqueue_styles() {
    wp_enqueue_style( 'parent-style', get_template_directory_uri() . '/style.css' );
    wp_enqueue_style( 'child-style', get_stylesheet_uri(), array( 'parent-style' ) );
}
## # on staging branch - test #6