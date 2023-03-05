<?php

class foo {
    public function a() {
    }
}

$test = new foo;

$test->a()->a;
print "ok\n";

try {
    $test->a()->a = 1;
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}
print "ok\n";

?>