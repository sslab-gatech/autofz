<?php
set_error_handler('func_get_args');
function test($a) {
    echo $undef;
}
try {
    test(1);
} catch (\Error $e) {
    echo $e->getMessage();
}
?>