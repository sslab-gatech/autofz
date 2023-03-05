<?php declare(strict_types=1);

class Test {
    public static int $intProp = 123;
    public static $prop;
}

Test::$prop =& Test::$intProp;
try {
    Test::$prop .= "foobar";
} catch (TypeError $e) {
    echo $e->getMessage(), "\n";
}
var_dump(Test::$prop, Test::$intProp);
?>