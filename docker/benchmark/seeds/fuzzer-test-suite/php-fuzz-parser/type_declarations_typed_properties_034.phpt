<?php
$foo = new class {
    public ?int $bar = 42;
    public int $baz;

    public function &getIterator() {
        foreach (['1', &$this->bar] as &$item) {
            yield $item;
        }
    }
};

function foo(?int &$a) {
    var_dump($a);
    $a = null;
}

foo($foo->bar);

try {
    $foo->baz = &$foo->bar;
} catch (Error $e) { echo $e->getMessage(), "\n"; }
$foo->bar = 10;

foreach ($foo->getIterator() as &$item) {
    $foo->baz = &$item;
    var_dump($foo->baz);
}

try {
    foo($foo->bar);
} catch (Error $e) { echo $e->getMessage(), "\n"; }

var_dump($foo);
?>