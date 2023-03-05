<?php

spl_autoload_register(function ($a) {
    class foo { }
});

class_alias('foo', 'bar', 1);

var_dump(new foo, new bar);

?>