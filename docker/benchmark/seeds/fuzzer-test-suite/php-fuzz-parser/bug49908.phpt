<?php

spl_autoload_register(function ($className) {
    var_dump($className);

    if ($className == 'Foo') {
        class Foo implements Bar {};
    } else {
        throw new Exception($className);
    }
});

try {
    new Foo();
} catch (Exception $e) { }

// We never reach here.
var_dump(new Foo());

?>