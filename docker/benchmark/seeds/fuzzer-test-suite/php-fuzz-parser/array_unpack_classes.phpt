<?php

class C {
    public const FOO = [0, ...self::ARR, 4];
    public const ARR = [1, 2, 3];
    public static $bar = [...self::ARR];
}

class D {
    public const A = [...self::B];
    public const B = [...self::A];
}

var_dump(C::FOO);
var_dump(C::$bar);

try {
    var_dump(D::A);
} catch (Error $ex) {
    echo "Exception: " . $ex->getMessage() . "\n";
}