<?php

// Same as autoload3 test case, but with X, Y being interfaces.
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
        interface X {
            public function method(): A;
        }
        var_dump(interface_exists('X'));
    } else if ($class == 'Y') {
        interface Y extends X {
            public function method(): B;
        }
        var_dump(interface_exists('Y'));
    }
});

var_dump(new B);

?>