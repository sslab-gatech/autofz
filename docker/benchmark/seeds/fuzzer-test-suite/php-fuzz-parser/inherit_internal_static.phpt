<?php

class Test extends _ZendTestClass {
}

var_dump(Test::$_StaticProp);
_ZendTestClass::$_StaticProp = 42;
var_dump(Test::$_StaticProp);

?>