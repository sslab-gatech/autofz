<?php
$foo = new class {
    public int $foo = 1;
    public int $bar = 3;
    public int $baz = 5;
    public int $qux = PHP_INT_MAX;

    public function &fetch() {
        yield $this->foo;
        yield $this->bar;
        yield $this->baz;
        yield $this->qux;
    }
};

try {
    foreach ($foo->fetch() as &$prop) {
        $prop += 1;
    }
} catch (Error $e) { echo $e->getMessage(), "\n"; }

var_dump($foo);
?>