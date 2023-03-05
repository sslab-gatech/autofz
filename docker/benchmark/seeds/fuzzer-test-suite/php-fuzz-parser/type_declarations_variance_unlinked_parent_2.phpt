<?php

spl_autoload_register(function($class) {
    class X implements B {}
});

try {
    interface B extends A {
    }
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}

?>