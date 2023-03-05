<?php
abstract class C {
    abstract static function foo();
}

function foo(callable $x) {
}

try {
    C::foo();
} catch (Error $e) {
    echo $e, "\n\n";
}

try {
    foo("C::foo");
} catch (Error $e) {
    echo $e, "\n\n";
}

C::foo();
?>