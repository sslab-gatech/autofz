<?php

set_exception_handler(function($e) {
    var_dump($e);
});

exit("Exit\n");

?>