<?php

set_error_handler(function($_, $msg) {
    throw new Exception($msg);
}, E_NOTICE);

try {
    wordwrap("foo", "123foo", "");
} catch (Exception $e) {
    echo $e, "\n";
}

?>