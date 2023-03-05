<?php

set_error_handler(function() {
    echo 'First handler' . PHP_EOL;
});

set_error_handler(function() {
    echo 'Second handler' . PHP_EOL;

    set_error_handler(function() {
        echo 'Internal handler' . PHP_EOL;
    });

    $triggerInternalNotice++; // warnings while handling the error should go into internal handler

    restore_error_handler();
});

$triggerNotice1++;
$triggerNotice2++;
?>