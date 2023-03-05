<?php
class A {
    private function f() {
        return "A";
    }
}
class B extends A {
    protected function f() {
        return "B";
    }
}
$b = new B();
try {
    var_dump($b->f());
} catch (Throwable $e) {
    echo "Exception: ", $e->getMessage(), "\n";
}
?>