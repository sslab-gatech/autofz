<?php

class Foo {
    public ?string $p;
    public ?iterable $i;
    public static ?string $s;
    public static ?array $a;
}

$a = new Foo;

$a->i[] = 1;
var_dump($a->i);

try {
    $a->p[] = "test";
} catch (TypeError $e) { var_dump($e->getMessage()); }
try { // must be uninit
    var_dump($a->p); // WRONG!
} catch (Error $e) { var_dump($e->getMessage()); }

$a->p = null;
try {
    $a->p[] = "test";
} catch (TypeError $e) { var_dump($e->getMessage()); }
var_dump($a->p);

Foo::$a["bar"] = 2;
var_dump(Foo::$a);

try {
    Foo::$s["baz"][] = "baz";
} catch (TypeError $e) { var_dump($e->getMessage()); }
try { // must be uninit
    var_dump(Foo::$s);
} catch (Error $e) { var_dump($e->getMessage()); }

Foo::$a = null;
$ref = &Foo::$a;
$ref[] = 3;
var_dump($ref);

$ref = &$a->p;
try {
    $ref[] = "bar";
} catch (TypeError $e) { var_dump($e->getMessage()); }
var_dump($ref);

try {
    $ref["baz"][] = "bar"; // indirect assign
} catch (TypeError $e) { var_dump($e->getMessage()); }
var_dump($ref);

?>