<?php

spl_autoload_register(function($class) {
    if ($class == 'A') {
        class A {
            public function method(): X {}
        }
        var_dump(new A);
    } else if ($class == 'B') {
        class B extends A {
            public function method(): Y {}
        }
        var_dump(new B);
    } else if ($class == 'X') {
        class X {
            public function method(Y $a) {}
        }
        var_dump(new X);
    } else if ($class == 'Y') {
        class Y extends X {
            public function method(Z $a) {}
        }
        var_dump(new Y);
    } else if ($class == 'Z') {
        class Z extends Y {
            public function method($a) {}
        }
        var_dump(new Z);
    }
});

var_dump(new B);

?>