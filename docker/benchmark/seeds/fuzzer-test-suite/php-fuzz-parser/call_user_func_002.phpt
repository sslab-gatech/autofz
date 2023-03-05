<?php

spl_autoload_register(function ($class) {
    var_dump($class);
});

try {
    call_user_func(array('foo', 'bar'));
} catch (TypeError $e) {
    echo $e->getMessage(), "\n";
}
try {
    call_user_func(array('', 'bar'));
} catch (TypeError $e) {
    echo $e->getMessage(), "\n";
}
try {
    call_user_func(array($foo, 'bar'));
} catch (TypeError $e) {
    echo $e->getMessage(), "\n";
}
try {
    call_user_func(array($foo, ''));
} catch (TypeError $e) {
    echo $e->getMessage(), "\n";
}

?>