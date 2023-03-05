<?php

register_shutdown_function(function() {
    new stdClass;
});

$ary = [];
while (true) {
    $ary[] = new stdClass;
}

?>