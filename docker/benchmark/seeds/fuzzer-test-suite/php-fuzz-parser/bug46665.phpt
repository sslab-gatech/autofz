<?php

spl_autoload_register(function ($class) {
    var_dump($class);
    require __DIR__ .'/bug46665_autoload.inc';
});

$baz = '\\Foo\\Bar\\Baz';
new $baz();

?>