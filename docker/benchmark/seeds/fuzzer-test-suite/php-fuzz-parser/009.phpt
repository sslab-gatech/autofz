<?php

class foo {
    function bar () {
        var_dump(get_class());
    }
    function testNull ()
    {
        try {
            var_dump(get_class(null));
        } catch (TypeError $e) {
            echo $e->getMessage(), "\n";
        }
    }
}

class foo2 extends foo {
}

$f1 = new foo;
$f2 = new foo2;

$f1->bar();
$f2->bar();

var_dump(get_class());
try {
    var_dump(get_class("qwerty"));
} catch (TypeError $e) {
    echo $e->getMessage(), "\n";
}

var_dump(get_class($f1));
var_dump(get_class($f2));

$f1->testNull();

echo "Done\n";
?>