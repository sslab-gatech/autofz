<?php
declare(strict_types=1);

class A {
    public string $foo;
}

$o = new A;
$o->foo = "1" . str_repeat("0", 2);
try {
    $o->foo += 5;
} catch (Throwable $e) {
    echo $e->getMessage() . "\n";
}
var_dump($o->foo);
unset($o);
?>