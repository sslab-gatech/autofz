<?php
ini_set('memory_limit', '2M');
register_shutdown_function(function () {
    for ($n = 1000 * 1000; $n--;) {
        new stdClass;
    }
    echo "OK\n";
});
?>