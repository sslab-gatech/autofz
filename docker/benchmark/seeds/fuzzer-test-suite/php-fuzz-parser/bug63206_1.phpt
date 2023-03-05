<?php

set_error_handler(function() {
    echo 'First handler' . PHP_EOL;
});

set_error_handler(function() {
    echo 'Second handler' . PHP_EOL;
});

set_error_handler(null);

set_error_handler(function() {
    echo 'Fourth handler' . PHP_EOL;
});

restore_error_handler();
restore_error_handler();

$triggerNotice++;
?>