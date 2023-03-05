<?php
set_error_handler(function ($severity, $message, $file, $line) {
    throw new \Exception($message);
});

$x = "foo";
$y = &$x["bar"];
?>