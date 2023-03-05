<?php
set_error_handler(function($no, $msg) { throw new Exception; });

try {
    $a = [];
    $str = "$a${"y$a$a"}y";
} catch (Exception $e) {
}
?>
DONE