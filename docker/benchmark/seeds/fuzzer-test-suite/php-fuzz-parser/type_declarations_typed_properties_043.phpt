<?php

trait Test {
    public static self $selfProp;
    public static ?self $selfNullProp;
    public static parent $parentProp;
}

try {
    Test::$selfProp = new stdClass;
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}
try {
    Test::$selfNullProp = new stdClass;
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}
try {
    Test::$parentProp = new stdClass;
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}

Test::$selfNullProp = null;
var_dump(Test::$selfNullProp);

class Foo {}
class Bar extends Foo {
    use Test;
}

Bar::$selfProp = new Bar;
Bar::$selfNullProp = new Bar;
Bar::$parentProp = new Foo;

var_dump(Bar::$selfProp, Bar::$selfNullProp, Bar::$parentProp);

?>