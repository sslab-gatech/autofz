<?php

abstract class Test {
    abstract static function method();
}

try {
    Test::method(new stdClass);
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}

$ret = new stdClass;
try {
    $ret = Test::method(new stdClass);
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}

?>