<?php

function handleError($errno, $errstr, $errfile, $errline) {
    $exception = new exception("blah");
    throw $exception;
}
set_error_handler('handleError', E_ALL);
$c = $b[$a];
?>