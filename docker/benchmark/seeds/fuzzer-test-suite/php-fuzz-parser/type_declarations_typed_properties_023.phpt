<?php
function &ref() {
    static $a = 5;
    return $a;
}

class Foo {
    public static int $i;
    public static string $s = "x";
}

var_dump(Foo::$i = 1);
var_dump(Foo::$i);
var_dump(Foo::$i = "1");
var_dump(Foo::$i);

var_dump(Foo::$s);
var_dump(Foo::$s = Foo::$i++);
var_dump(Foo::$s, Foo::$i);
$a = 3;
var_dump(Foo::$s = $a);
var_dump(Foo::$s);
var_dump(Foo::$i = "4");
var_dump(Foo::$i);

var_dump(Foo::$i = ref());
var_dump(Foo::$i);
var_dump(Foo::$s = ref());
var_dump(Foo::$s);
var_dump(ref());
?>