<?php
function &ref($a = null) {
    static $f;
    if ($a !== null) $f = function &() use (&$a) { return $a; };
    return $f();
}

class Foo {
    public static int $i;
    public static string $s = "x";
}

Foo::$i = &ref(5);
var_dump(Foo::$i);

$i = &Foo::$i;
$i = 2;
var_dump($i, Foo::$i);

$i = "3";
var_dump($i, Foo::$i);

Foo::$i = "4";
var_dump($i, Foo::$i);

try {
    $i = null;
} catch (TypeError $e) { print $e->getMessage()."\n"; }
var_dump($i, Foo::$i);

try {
    Foo::$i = null;
} catch (TypeError $e) { print $e->getMessage()."\n"; }
var_dump($i, Foo::$i);

Foo::$s = &ref(5);
var_dump(Foo::$s, ref());

Foo::$i = &ref("0");
var_dump(Foo::$i, ref());

try {
    Foo::$i = &ref("x");
} catch (TypeError $e) { print $e->getMessage()."\n"; }
var_dump(Foo::$i, ref());

try {
    Foo::$i = &Foo::$s;
} catch (TypeError $e) { print $e->getMessage()."\n"; }
var_dump(Foo::$i, Foo::$s);

try {
    Foo::$s = &Foo::$i;
} catch (TypeError $e) { print $e->getMessage()."\n"; }
var_dump(Foo::$i, Foo::$s);

?>