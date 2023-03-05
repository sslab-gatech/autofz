<?php
class Foo {
    public int $bar;
}

$foo = new Foo();

for ($i = 0; $i < 5; $i++) {
    $foo->bar = "5";
    var_dump($foo->bar);
}
?>