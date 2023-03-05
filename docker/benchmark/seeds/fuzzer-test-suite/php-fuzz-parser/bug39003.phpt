<?php

class ClassName
{
    public $var = 'bla';
}

function test (OtherClassName $object) { }

spl_autoload_register(function ($class) {
    var_dump("__autload($class)");
});

$obj = new ClassName;
test($obj);

echo "Done\n";
?>