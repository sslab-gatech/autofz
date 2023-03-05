<?php
class Bomb {
    function foo() {
    }
    function __destruct() {
        throw new Exception("bomb!");
    }
}
try {
    $x = new ReflectionMethod(new Bomb(), "foo");
} catch (Throwable $e) {
    echo $e->getMessage() . "\n";
}
echo "ok\n";
?>