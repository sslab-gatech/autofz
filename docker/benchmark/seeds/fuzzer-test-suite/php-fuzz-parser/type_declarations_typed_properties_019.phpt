<?php
class Foo {
    public int $bar = PHP_INT_MAX;

    public function inc() {
        return ++$this->bar;
    }
}

$foo = new Foo();

try {
    $foo->inc();
} catch (TypeError $e) {
    echo $e->getMessage(), "\n";
}
?>