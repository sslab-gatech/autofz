<?php
class Foo {
    public int $bar = BAR::BAZ;
}

try {
    $foo = new Foo();
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}
?>