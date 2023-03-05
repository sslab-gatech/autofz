<?php

spl_autoload_register(function($class) {
    var_dump($class);
    if ($class === 'X') {
        class X {}
    } else {
        class Y {}
    }
});

class A {
    public function method(X $param) : object {}
}

class B extends A {
    public function method(object $param) : Y {}
}

?>