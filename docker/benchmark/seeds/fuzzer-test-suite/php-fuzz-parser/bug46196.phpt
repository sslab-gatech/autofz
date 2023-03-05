<?php
echo "*** Testing restore_error_handler() : error bug #46196 ***\n";

var_dump( set_error_handler( 'myErrorHandler' ) );
var_dump( restore_error_handler() );
var_dump( set_error_handler( 'myErrorHandler' ) );

function myErrorHandler($errno, $errstr, $errfile, $errline)
{
    return true;
}

?>