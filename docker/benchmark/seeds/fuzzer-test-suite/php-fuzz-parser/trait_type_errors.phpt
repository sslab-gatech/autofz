<?php

trait T {
    public function test1($arg): int {
        return $arg;
    }
    public function test2(int $arg) {
    }
    public function test3(int $arg = 42) {
    }
}

class C {
    use T;
}
class P extends C {
}

$c = new C;
try {
    $c->test1("foo");
} catch (TypeError $e) {
    echo $e->getMessage(), "\n";
}
try {
    $c->test2("foo");
} catch (TypeError $e) {
    echo $e->getMessage(), "\n";
}
try {
    $c->test3("foo");
} catch (TypeError $e) {
    echo $e->getMessage(), "\n";
}

?>